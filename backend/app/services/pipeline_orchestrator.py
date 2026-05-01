"""PipelineOrchestrator — orchestrates the full campaign simulation pipeline.

Flow:
  Step 1: Campaign creation              → status=draft
  Step 2: Persona generation             → status=persona_building
  Step 3: Graph building                 → status=graph_building
  Step 4: Simulation execution           → status=simulating
  Step 5: KPI report generation          → status=completed

Each step updates the campaign status and persists progress.
"""

import os
import json
import logging
import threading
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime, timezone

from ..config import Config
from ..models.campaign import (
    Campaign, CampaignStatus, CampaignObjective,
    CampaignTarget, SimulationConfig,
)
from ..models.persona import ThaiPersona
from ..models.report import ExecutiveReport
from ..utils.logger import get_logger
from .oasis_platform_presets import resolve_preset

logger = get_logger('mirofish.pipeline_orchestrator')


class PipelineStep(str, Enum):
    """Named pipeline steps for status reporting."""
    CREATING = "creating"
    GENERATING_PERSONAS = "generating_personas"
    BUILDING_GRAPH = "building_graph"
    RUNNING_SIMULATION = "running_simulation"
    GENERATING_REPORT = "generating_report"
    COMPLETED = "completed"
    FAILED = "failed"


class PipelineProgress:
    """Mutable progress tracker stored alongside a campaign during pipeline runs."""

    def __init__(self, campaign_id: str, total_steps: int = 5):
        self.campaign_id = campaign_id
        self.current_step: PipelineStep = PipelineStep.CREATING
        self.current_step_number: int = 0
        self.total_steps: int = total_steps
        self.step_status: str = "pending"   # pending, running, done, error
        self.step_message: str = ""
        self.step_percent: int = 0
        self.started_at: Optional[str] = None
        self.error: Optional[str] = None

        # Per-step detail
        self.persona_count: int = 0
        self.graph_task_id: Optional[str] = None
        self.simulation_id: Optional[str] = None
        self.report_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "current_step": self.current_step.value,
            "current_step_number": self.current_step_number,
            "total_steps": self.total_steps,
            "step_status": self.step_status,
            "step_message": self.step_message,
            "step_percent": self.step_percent,
            "started_at": self.started_at,
            "error": self.error,
            "persona_count": self.persona_count,
            "graph_task_id": self.graph_task_id,
            "simulation_id": self.simulation_id,
            "report_id": self.report_id,
        }


class PipelineOrchestrator:
    """Orchestrate the full campaign pipeline from creation to report."""

    def __init__(
        self,
        campaign_service=None,
        persona_factory=None,
        graph_builder=None,
        simulation_manager=None,
        kpi_calculator=None,
    ):
        # Deferred imports for loose coupling
        from .campaign_service import CampaignService
        from .persona_factory import PersonaFactory
        from .kpi_calculator import KPICalculator

        self.campaign_service = campaign_service or CampaignService()
        self.persona_factory = persona_factory or PersonaFactory()
        self.graph_builder = graph_builder  # GraphBuilderService or None
        self.simulation_manager = simulation_manager  # SimulationManager or None
        self.kpi_calculator = kpi_calculator or KPICalculator()

        # Active pipeline runs: campaign_id -> PipelineProgress
        self._active: Dict[str, PipelineProgress] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_pipeline(self, campaign_id: str, org_id: str) -> PipelineProgress:
        """Run full pipeline for a campaign. Returns progress tracker.

        Can be called synchronously (blocks until done or fails) or used
        for polling via get_pipeline_status().
        """
        progress = PipelineProgress(campaign_id)
        progress.started_at = datetime.now(timezone.utc).isoformat()

        with self._lock:
            self._active[campaign_id] = progress

        try:
            self._execute_pipeline(campaign_id, org_id, progress)
        except Exception as e:
            logger.error(f"Pipeline failed for campaign '{campaign_id}': {e}")
            import traceback
            logger.error(traceback.format_exc())
            progress.error = str(e)
            progress.step_status = "error"
            progress.step_message = str(e)

            # Mark campaign as failed
            self._update_campaign_status(campaign_id, org_id, CampaignStatus.FAILED)

        return progress

    def get_pipeline_status(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get current pipeline progress for a campaign."""
        with self._lock:
            progress = self._active.get(campaign_id)
        if progress:
            return progress.to_dict()

        # Check if campaign exists and return its status
        campaign = self.campaign_service.get_campaign(campaign_id)
        if campaign is None:
            return None

        return {
            "campaign_id": campaign.campaign_id,
            "campaign_status": campaign.status.value,
            "current_step": None,
            "current_step_number": 0,
            "total_steps": 5,
            "step_status": "done" if campaign.status == CampaignStatus.COMPLETED else "pending",
            "step_message": "",
            "step_percent": 100 if campaign.status == CampaignStatus.COMPLETED else 0,
            "error": None,
            "persona_count": 0,
            "simulation_id": campaign.simulation_id,
            "report_id": campaign.report_id,
        }

    # ------------------------------------------------------------------
    # Pipeline steps
    # ------------------------------------------------------------------

    def _execute_pipeline(
        self, campaign_id: str, org_id: str, progress: PipelineProgress
    ) -> None:
        """Execute all pipeline steps in sequence."""
        campaign = self.campaign_service.get_campaign(campaign_id, org_id=org_id)
        if campaign is None:
            raise ValueError(f"Campaign '{campaign_id}' not found in org '{org_id}'")

        if campaign.status not in (CampaignStatus.DRAFT, CampaignStatus.FAILED):
            raise ValueError(
                f"Campaign '{campaign_id}' is in status '{campaign.status.value}', "
                f"cannot start pipeline (must be draft or failed)"
            )

        # ── Step 1: Confirm status is draft ──
        self._step_create(campaign, progress)

        # ── Step 2: Generate personas ──
        self._step_generate_personas(campaign, progress)

        # ── Step 3: Build graph ──
        self._step_build_graph(campaign, progress)

        # ── Step 4: Run simulation ──
        self._step_run_simulation(campaign, progress)

        # ── Step 5: Generate report ──
        self._step_generate_report(campaign, progress)

        # ── Done ──
        progress.current_step = PipelineStep.COMPLETED
        progress.step_status = "done"
        progress.step_percent = 100
        progress.step_message = "Campaign pipeline completed successfully"
        self._update_campaign_status(campaign_id, org_id, CampaignStatus.COMPLETED)
        logger.info(f"Pipeline completed for campaign '{campaign_id}'")

    def _step_create(self, campaign: Campaign, progress: PipelineProgress) -> None:
        """Step 1: Validate campaign is ready to start."""
        progress.current_step = PipelineStep.CREATING
        progress.current_step_number = 1
        progress.step_status = "done"
        progress.step_percent = 100
        progress.step_message = "Campaign ready"
        logger.info(f"Pipeline step 1/5: Campaign '{campaign.campaign_id}' confirmed draft")

    def _step_generate_personas(
        self, campaign: Campaign, progress: PipelineProgress
    ) -> None:
        """Step 2: Generate Thai synthetic consumer personas via PersonaFactory."""
        progress.current_step = PipelineStep.GENERATING_PERSONAS
        progress.current_step_number = 2
        progress.step_status = "running"
        progress.step_percent = 0
        progress.step_message = "Generating personas..."

        self._update_campaign_status(
            campaign.campaign_id, campaign.org_id, CampaignStatus.PERSONA_BUILDING
        )

        try:
            # Build CampaignTarget from campaign data
            target = campaign.target
            if isinstance(target, dict):
                target = CampaignTarget(**target)

            # Determine language from sim_config
            language = "th"
            if hasattr(campaign.sim_config, 'language'):
                language = campaign.sim_config.language
            elif isinstance(campaign.sim_config, dict):
                language = campaign.sim_config.get('language', 'th')

            count = target.persona_count if hasattr(target, 'persona_count') else 100

            personas = self.persona_factory.generate_batch(
                org_id=campaign.org_id,
                campaign_id=campaign.campaign_id,
                target=target,
                count=count,
                language=language,
            )

            progress.persona_count = len(personas)
            progress.step_status = "done"
            progress.step_percent = 100
            progress.step_message = f"Generated {len(personas)} personas"

            logger.info(
                f"Pipeline step 2/5: Generated {len(personas)} personas "
                f"for campaign '{campaign.campaign_id}'"
            )

        except Exception as e:
            progress.step_status = "error"
            progress.step_message = f"Persona generation failed: {e}"
            raise

    def _step_build_graph(
        self, campaign: Campaign, progress: PipelineProgress
    ) -> None:
        """Step 3: Build Neo4j knowledge graph via GraphBuilderService."""
        progress.current_step = PipelineStep.BUILDING_GRAPH
        progress.current_step_number = 3
        progress.step_status = "running"
        progress.step_percent = 10
        progress.step_message = "Building knowledge graph..."

        # Build graph text from campaign context
        graph_text = self._build_graph_text(campaign)

        ontology = self._build_ontology(campaign)

        if self.graph_builder is not None:
            try:
                task_id = self.graph_builder.build_graph_async(
                    text=graph_text,
                    ontology=ontology,
                    graph_name=f"Campaign: {campaign.name}",
                )
                progress.graph_task_id = task_id
                progress.step_status = "done"
                progress.step_percent = 100
                progress.step_message = f"Graph build task started: {task_id}"
                logger.info(
                    f"Pipeline step 3/5: Graph build task '{task_id}' "
                    f"for campaign '{campaign.campaign_id}'"
                )
            except Exception as e:
                progress.step_status = "error"
                progress.step_message = f"Graph building failed: {e}"
                raise
        else:
            # No graph builder available — log and skip
            progress.step_status = "done"
            progress.step_percent = 100
            progress.step_message = "Graph building skipped (no builder available)"
            logger.warning(
                f"Pipeline step 3/5: Graph builder not available, "
                f"skipping for campaign '{campaign.campaign_id}'"
            )

    def _step_run_simulation(
        self, campaign: Campaign, progress: PipelineProgress
    ) -> None:
        """Step 4: Run OASIS simulation via SimulationManager."""
        progress.current_step = PipelineStep.RUNNING_SIMULATION
        progress.current_step_number = 4
        progress.step_status = "running"
        progress.step_percent = 0
        progress.step_message = "Starting simulation..."

        self._update_campaign_status(
            campaign.campaign_id, campaign.org_id, CampaignStatus.SIMULATING
        )

        if self.simulation_manager is not None:
            try:
                # Determine platform preferences from sim_config
                platform = "twitter"
                enable_twitter = True
                enable_reddit = False
                if hasattr(campaign.sim_config, 'platform'):
                    platform = campaign.sim_config.platform
                elif isinstance(campaign.sim_config, dict):
                    platform = campaign.sim_config.get('platform', 'twitter')

                if platform == "reddit":
                    enable_twitter = False
                    enable_reddit = True
                elif platform == "both":
                    enable_twitter = True
                    enable_reddit = True

                language = "th"
                if hasattr(campaign.sim_config, 'language'):
                    language = campaign.sim_config.language
                elif isinstance(campaign.sim_config, dict):
                    language = campaign.sim_config.get('language', 'th')

                platform_mode = "auto"
                audience_channels = []
                oasis_preset = {}
                if hasattr(campaign.sim_config, 'platform_mode'):
                    platform_mode = campaign.sim_config.platform_mode
                    audience_channels = getattr(campaign.sim_config, 'audience_channels', []) or []
                    oasis_preset = getattr(campaign.sim_config, 'oasis_preset', {}) or {}
                elif isinstance(campaign.sim_config, dict):
                    platform_mode = campaign.sim_config.get('platform_mode', 'auto')
                    audience_channels = campaign.sim_config.get('audience_channels', []) or []
                    oasis_preset = campaign.sim_config.get('oasis_preset', {}) or {}

                if not audience_channels:
                    target = campaign.target
                    if isinstance(target, dict):
                        audience_channels = target.get('channels', []) or []
                    elif getattr(target, 'channels', None):
                        audience_channels = target.channels

                if not oasis_preset:
                    oasis_preset = resolve_preset(
                        mode=platform_mode,
                        channels=audience_channels,
                        engine_platform=platform,
                    )

                # Create simulation in SimulationManager
                sim_state = self.simulation_manager.create_simulation(
                    project_id=campaign.project_id or campaign.campaign_id,
                    graph_id=campaign.graph_id or campaign.campaign_id,
                    enable_twitter=enable_twitter,
                    enable_reddit=enable_reddit,
                    language=language,
                    platform_mode=platform_mode,
                    audience_channels=audience_channels,
                    oasis_preset=oasis_preset,
                )

                progress.simulation_id = sim_state.simulation_id

                # Link simulation to campaign
                self.campaign_service.update_links(
                    campaign,
                    simulation_id=sim_state.simulation_id,
                )

                progress.step_status = "done"
                progress.step_percent = 100
                progress.step_message = (
                    f"Simulation created: {sim_state.simulation_id}"
                )
                logger.info(
                    f"Pipeline step 4/5: Simulation '{sim_state.simulation_id}' "
                    f"created for campaign '{campaign.campaign_id}'"
                )

            except Exception as e:
                progress.step_status = "error"
                progress.step_message = f"Simulation failed: {e}"
                raise
        else:
            progress.step_status = "done"
            progress.step_percent = 100
            progress.step_message = "Simulation skipped (no simulation manager)"
            logger.warning(
                f"Pipeline step 4/5: Simulation manager not available, "
                f"skipping for campaign '{campaign.campaign_id}'"
            )

    def _step_generate_report(
        self, campaign: Campaign, progress: PipelineProgress
    ) -> None:
        """Step 5: Generate KPI executive report via KPICalculator."""
        progress.current_step = PipelineStep.GENERATING_REPORT
        progress.current_step_number = 5
        progress.step_status = "running"
        progress.step_percent = 0
        progress.step_message = "Generating KPI report..."

        try:
            report = self.kpi_calculator.calculate(
                campaign_id=campaign.campaign_id,
                org_id=campaign.org_id,
            )

            progress.report_id = report.report_id
            progress.step_status = "done"
            progress.step_percent = 100
            progress.step_message = f"Report generated: {report.report_id}"

            # Save report results to campaign
            self.campaign_service.update_campaign(
                campaign.campaign_id,
                campaign.org_id,
                {
                    "results_summary": report.to_dict() if hasattr(report, 'to_dict') else {},
                    "status": CampaignStatus.COMPLETED.value,
                },
            )

            self.campaign_service.update_links(
                campaign,
                report_id=report.report_id,
            )

            logger.info(
                f"Pipeline step 5/5: Report '{report.report_id}' "
                f"for campaign '{campaign.campaign_id}'"
            )

        except Exception as e:
            progress.step_status = "error"
            progress.step_message = f"Report generation failed: {e}"
            raise

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _update_campaign_status(
        self, campaign_id: str, org_id: str, status: CampaignStatus
    ) -> None:
        """Update campaign status and persist."""
        try:
            self.campaign_service.update_campaign(
                campaign_id, org_id, {"status": status.value}
            )
        except Exception as e:
            logger.warning(f"Failed to update campaign status: {e}")

    def _build_graph_text(self, campaign: Campaign) -> str:
        """Build text for graph construction from campaign data."""
        parts = [
            f"Campaign: {campaign.name}",
            f"Objective: {campaign.objective.value}",
        ]
        if campaign.description:
            parts.append(f"Description: {campaign.description}")

        target = campaign.target
        if isinstance(target, dict):
            parts.append(f"Target Segment: {target.get('segment_name', 'General')}")
            parts.append(f"Target Regions: {', '.join(target.get('regions', []))}")
            if target.get('channels'):
                parts.append(f"Audience Channels: {', '.join(target.get('channels', []))}")
        elif hasattr(target, 'segment_name'):
            parts.append(f"Target Segment: {target.segment_name}")
            parts.append(f"Target Regions: {', '.join(target.regions)}")
            if getattr(target, 'channels', None):
                parts.append(f"Audience Channels: {', '.join(target.channels)}")

        sim = campaign.sim_config
        if isinstance(sim, dict):
            parts.append(f"Simulation Engine: {sim.get('platform', 'twitter')}")
            parts.append(f"Platform Mode: {sim.get('platform_mode', 'auto')}")
            preset = sim.get("oasis_preset") or {}
            if preset.get("modeled_behavior"):
                parts.append(f"OASIS Behavior Model: {preset.get('modeled_behavior')}")
            parts.append(f"Language: {sim.get('language', 'th')}")
        elif hasattr(sim, 'platform'):
            parts.append(f"Simulation Engine: {sim.platform}")
            parts.append(f"Platform Mode: {getattr(sim, 'platform_mode', 'auto')}")
            preset = getattr(sim, 'oasis_preset', {}) or {}
            if preset.get("modeled_behavior"):
                parts.append(f"OASIS Behavior Model: {preset.get('modeled_behavior')}")
            parts.append(f"Language: {sim.language}")

        return "\n".join(parts)

    def _build_ontology(self, campaign: Campaign) -> Dict[str, Any]:
        """Build a simple ontology for the campaign graph."""
        target = campaign.target
        regions = []
        if isinstance(target, dict):
            regions = target.get('regions', [])
        elif hasattr(target, 'regions'):
            regions = target.regions

        return {
            "entity_types": [
                {
                    "type": "Campaign",
                    "description": "Marketing simulation campaign",
                },
                {
                    "type": "Segment",
                    "description": "Target audience segment",
                },
                {
                    "type": "Persona",
                    "description": "Synthetic consumer persona",
                },
                {
                    "type": "Region",
                    "description": "Geographic region in Thailand",
                },
            ],
            "relation_types": [
                {"type": "TARGETS", "description": "Campaign targets a segment"},
                {"type": "LOCATED_IN", "description": "Segment located in region"},
                {"type": "GENERATED_FOR", "description": "Persona generated for campaign"},
            ],
            "context": {
                "campaign_name": campaign.name,
                "objective": campaign.objective.value,
                "target_regions": regions,
            },
        }
