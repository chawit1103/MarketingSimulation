"""Manual actual-results import and deterministic calibration comparison."""

from __future__ import annotations

import csv
import io
import json
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from ..config import Config


class CalibrationValidationError(ValueError):
    """Raised when imported actual results are unsafe or invalid."""


FORBIDDEN_FIELDS = {
    "email",
    "phone",
    "phone_number",
    "customer_name",
    "customer_id",
    "customer_ids",
    "contact",
    "contacts",
    "customer_list",
    "crm_records",
    "raw_posts",
    "social_posts",
    "comments",
    "raw_comments",
    "usernames",
    "handles",
}

NUMERIC_METRICS = (
    "impressions",
    "clicks",
    "ctr",
    "conversion_count",
    "conversion_rate",
    "sales_lift",
    "sentiment_score",
)

ESTIMATE_ALIASES = {
    "estimated_impressions": "impressions",
    "estimated_clicks": "clicks",
    "estimated_ctr": "ctr",
    "estimated_conversion_count": "conversion_count",
    "estimated_conversion_rate": "conversion_rate",
    "estimated_sales_lift": "sales_lift",
    "estimated_sentiment_score": "sentiment_score",
    "estimated_crisis_risk": "crisis_risk",
}

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
PHONE_RE = re.compile(r"(?:\+?\d[\s().-]?){8,}")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _to_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    try:
        return float(str(value).replace("%", "").replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _to_bool(value: Any) -> Optional[bool]:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "incident", "crisis"}:
        return True
    if normalized in {"0", "false", "no", "n", "none", "no_incident"}:
        return False
    return None


def _safe_filename_part(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", value)[:120] or "unknown"


class CalibrationService:
    """Import manual actuals and compare them with prior deterministic estimates.

    This service intentionally does not mutate simulation outputs or call live
    providers. It records user-supplied actual campaign summaries and computes a
    transparent estimate-vs-actual comparison.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir or os.path.join(Config.UPLOAD_FOLDER, "calibration")

    def import_actual_results(self, org_id: str, payload: Mapping[str, Any]) -> Dict[str, Any]:
        self._validate_payload(payload)
        campaign_id = str(payload.get("campaign_id") or "").strip()
        if not campaign_id:
            raise CalibrationValidationError("campaign_id is required")

        actual = self._extract_actual_metrics(payload)
        if not actual and _to_bool(payload.get("crisis_incident_flag")) is None:
            raise CalibrationValidationError("At least one actual result metric is required")

        estimate = self._extract_estimates(payload)
        comparison = self._compare_metrics(estimate, actual)
        risk_classification = self._classify_risk(estimate, payload)
        segment_gaps = self._compare_segments(payload)

        record = {
            "record_id": f"cal_{uuid.uuid4().hex[:12]}",
            "org_id": org_id,
            "campaign_id": campaign_id,
            "imported_at": _now_iso(),
            "date_range": payload.get("date_range") or {
                "start": payload.get("start_date"),
                "end": payload.get("end_date"),
            },
            "actual": actual,
            "estimate": estimate,
            "crisis_incident_flag": _to_bool(payload.get("crisis_incident_flag")),
            "qualitative_notes": self._sanitize_notes(payload.get("qualitative_notes")),
            "comparison": comparison,
            "risk_classification": risk_classification,
            "segment_assumption_gaps": segment_gaps,
            "source": {
                "source_mode": "live_backend",
                "data_basis": "manual_actual_import",
                "warning": (
                    "Manual actual results supplied by the user; this is not live CRM "
                    "or social listening ingestion."
                ),
            },
            "privacy_review": {
                "pii_detected": False,
                "notes_stored": bool(payload.get("qualitative_notes")),
                "rejected_fields": [],
            },
            "limitations": [
                "Calibration uses user-supplied aggregate actuals only.",
                "No raw customer lists, CRM contacts, or social posts are ingested.",
                "This comparison does not retrain or overwrite the original simulation.",
            ],
            "recommended_validation_step": (
                "Add actual results from at least three comparable campaigns before treating "
                "calibration as directional evidence."
            ),
        }

        records = self._load_records(org_id)
        records.append(record)
        record["calibration_status"] = self._status_for_records(records, record)
        self._save_records(org_id, records)
        return self._public_record(record)

    def get_status(self, org_id: str, campaign_id: str) -> Dict[str, Any]:
        records = [
            record for record in self._load_records(org_id)
            if str(record.get("campaign_id")) == str(campaign_id)
        ]
        if not records:
            return {
                "campaign_id": campaign_id,
                "calibration_status": "not_calibrated",
                "records": [],
                "source": {
                    "source_mode": "unknown",
                    "data_basis": "unknown",
                },
                "limitations": ["No actual campaign results have been imported for this campaign."],
            }
        latest = records[-1]
        latest["calibration_status"] = self._status_for_records(self._load_records(org_id), latest)
        return {
            "campaign_id": campaign_id,
            "calibration_status": latest["calibration_status"],
            "record_count": len(records),
            "latest": self._public_record(latest),
        }

    def parse_json_text(self, text: str) -> Dict[str, Any]:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise CalibrationValidationError("Invalid JSON actual-results file") from exc
        if isinstance(data, list):
            if len(data) != 1:
                raise CalibrationValidationError("JSON upload must contain exactly one campaign summary")
            data = data[0]
        if not isinstance(data, dict):
            raise CalibrationValidationError("JSON upload must be an object")
        return data

    def parse_csv_text(self, text: str) -> Dict[str, Any]:
        reader = csv.DictReader(io.StringIO(text))
        rows = [row for row in reader if any((value or "").strip() for value in row.values())]
        if not rows:
            raise CalibrationValidationError("CSV upload must contain one campaign summary row")
        if len(rows) > 1:
            raise CalibrationValidationError("CSV upload currently supports one aggregate campaign row")
        return {key: value for key, value in rows[0].items() if key}

    def _validate_payload(self, payload: Mapping[str, Any]) -> None:
        if not isinstance(payload, Mapping):
            raise CalibrationValidationError("Actual-results payload must be an object")
        found = self._find_forbidden_fields(payload)
        if found:
            raise CalibrationValidationError(
                "Actual-results import accepts aggregate summaries only; remove PII/raw data fields: "
                + ", ".join(sorted(found))
            )
        notes = payload.get("qualitative_notes")
        if notes and self._contains_pii(str(notes)):
            raise CalibrationValidationError("qualitative_notes appears to contain PII; import an anonymized summary")
        if notes and len(str(notes)) > 2000:
            raise CalibrationValidationError("qualitative_notes is too long for an aggregate summary")

    def _find_forbidden_fields(self, value: Any, prefix: str = "") -> set[str]:
        found: set[str] = set()
        if isinstance(value, Mapping):
            for key, nested in value.items():
                normalized = str(key).strip().lower()
                path = f"{prefix}.{normalized}" if prefix else normalized
                if normalized in FORBIDDEN_FIELDS or any(term in normalized for term in ("password", "secret", "token")):
                    found.add(path)
                found.update(self._find_forbidden_fields(nested, path))
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                found.update(self._find_forbidden_fields(item, f"{prefix}[{idx}]"))
        return found

    def _contains_pii(self, text: str) -> bool:
        return bool(EMAIL_RE.search(text) or PHONE_RE.search(text))

    def _sanitize_notes(self, value: Any) -> str:
        if not value:
            return ""
        text = re.sub(r"\s+", " ", str(value)).strip()
        return text[:500]

    def _extract_actual_metrics(self, payload: Mapping[str, Any]) -> Dict[str, float]:
        metrics: Dict[str, float] = {}
        actuals = payload.get("actual") if isinstance(payload.get("actual"), Mapping) else payload
        for metric in NUMERIC_METRICS:
            parsed = _to_float(actuals.get(metric))
            if parsed is not None:
                metrics[metric] = parsed
        return metrics

    def _extract_estimates(self, payload: Mapping[str, Any]) -> Dict[str, float]:
        estimates: Dict[str, float] = {}
        nested = payload.get("estimate") or payload.get("estimates")
        if isinstance(nested, Mapping):
            for metric in (*NUMERIC_METRICS, "crisis_risk"):
                parsed = _to_float(nested.get(metric))
                if parsed is not None:
                    estimates[metric] = parsed
        for alias, metric in ESTIMATE_ALIASES.items():
            parsed = _to_float(payload.get(alias))
            if parsed is not None:
                estimates[metric] = parsed
        return estimates

    def _compare_metrics(self, estimate: Mapping[str, float], actual: Mapping[str, float]) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for metric in NUMERIC_METRICS:
            if metric not in estimate or metric not in actual:
                continue
            estimated = estimate[metric]
            actual_value = actual[metric]
            delta = actual_value - estimated
            error_pct = None
            if estimated != 0:
                error_pct = abs(delta) / abs(estimated) * 100
            rows.append({
                "metric": metric,
                "estimate": round(estimated, 4),
                "actual": round(actual_value, 4),
                "delta": round(delta, 4),
                "absolute_error_pct": round(error_pct, 2) if error_pct is not None else None,
            })
        return rows

    def _classify_risk(self, estimate: Mapping[str, float], payload: Mapping[str, Any]) -> str:
        actual_crisis = _to_bool(payload.get("crisis_incident_flag"))
        if actual_crisis is None:
            return "not_available"
        estimated_crisis = None
        if "crisis_risk" in estimate:
            estimated_crisis = estimate["crisis_risk"] >= 50
        elif "crisis_incident_flag" in estimate:
            estimated_crisis = bool(estimate["crisis_incident_flag"])
        if estimated_crisis is None:
            return "not_available"
        if estimated_crisis and actual_crisis:
            return "matched_crisis"
        if not estimated_crisis and not actual_crisis:
            return "matched_no_crisis"
        if not estimated_crisis and actual_crisis:
            return "missed_crisis"
        return "false_alarm"

    def _compare_segments(self, payload: Mapping[str, Any]) -> List[Dict[str, Any]]:
        actuals = self._index_segments(payload.get("segment_actuals") or [])
        estimates = self._index_segments(payload.get("segment_estimates") or [])
        gaps: List[Dict[str, Any]] = []
        for segment, actual in actuals.items():
            estimate = estimates.get(segment)
            if not estimate:
                gaps.append({
                    "segment": segment,
                    "gap": "actual_segment_missing_from_estimate",
                })
                continue
            metric_rows = self._compare_metrics(estimate, actual)
            if metric_rows:
                gaps.append({"segment": segment, "metrics": metric_rows})
        return gaps

    def _index_segments(self, rows: Iterable[Any]) -> Dict[str, Dict[str, float]]:
        indexed: Dict[str, Dict[str, float]] = {}
        if not isinstance(rows, list):
            return indexed
        for row in rows:
            if not isinstance(row, Mapping):
                continue
            segment = str(row.get("segment") or row.get("name") or "").strip()
            if not segment:
                continue
            indexed[segment] = {
                metric: value
                for metric, value in (
                    (metric, _to_float(row.get(metric))) for metric in NUMERIC_METRICS
                )
                if value is not None
            }
        return indexed

    def _status_for_records(self, records: List[Mapping[str, Any]], record: Mapping[str, Any]) -> str:
        if not record.get("comparison") and record.get("risk_classification") == "not_available":
            return "not_calibrated"
        campaign_count = len({str(item.get("campaign_id")) for item in records if item.get("campaign_id")})
        if campaign_count >= 3:
            return f"calibrated_with_{campaign_count}_campaigns"
        return "partially_calibrated"

    def _records_path(self, org_id: str) -> str:
        return os.path.join(self.storage_dir, f"{_safe_filename_part(org_id)}.json")

    def _load_records(self, org_id: str) -> List[Dict[str, Any]]:
        path = self._records_path(org_id)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []

    def _save_records(self, org_id: str, records: List[Mapping[str, Any]]) -> None:
        os.makedirs(self.storage_dir, exist_ok=True)
        try:
            os.chmod(self.storage_dir, 0o700)
        except OSError:
            pass
        path = self._records_path(org_id)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(records, fh, ensure_ascii=False, indent=2)
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass

    def _public_record(self, record: Mapping[str, Any]) -> Dict[str, Any]:
        public = dict(record)
        public.pop("org_id", None)
        return public
