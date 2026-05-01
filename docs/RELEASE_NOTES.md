# Release Notes

Updated: 2026-05-01

## PR T: Public Pilot Go/No-Go Verification

This verification pass adds no product features. It records the current release posture after PR P, PR Q, PR R, and PR S.

### Verification Summary

- Backend tests passed.
- Focused security tests passed.
- Frontend production build passed.
- Mocked Playwright e2e smoke tests passed.
- CI-equivalent secret hygiene scan passed.
- `git diff --check` passed.

### Go/No-Go Decision

| Release path | Current decision | Reason |
| --- | --- | --- |
| Local demo | Go | Demo mode works without real provider keys when synthetic data is used. |
| Controlled private pilot | Conditional go | Acceptable only for trusted users after manual credential rotation is confirmed, deployment secrets come from environment variables, and pilot data is non-confidential or explicitly approved. |
| Public pilot / public internet exposure | No-go | Manual credential rotation is not evidenced, production rate limiting still requires edge/shared enforcement, and browser auth storage is mitigated but not fully hardened. |
| Production customer deployment | No-go | Requires manual credential rotation, shared/edge rate limiting, hardened browser auth, formal data-retention/deletion policy, production storage decisions, and deployment operations controls. |

### Remaining Blockers

- Repository owners must rotate any provider/API/graph credentials that may have been committed before SEC-001 remediation.
- Public deployments need edge/API-gateway or shared-store rate limiting.
- Public/customer deployments need HttpOnly cookie auth, refresh-token auth, or an equivalent hardened browser-auth strategy.
- Pilot data-retention and deletion procedures must be approved before external users enter real scenarios.
- Legacy local JSON records without `org_id` must be reviewed, backfilled, or re-created before production use.

### Screenshot Note

No UI/security label text changed in PR T itself. Existing screenshots should still be re-reviewed before any public demo to confirm visible Demo Mode, Local Estimate, Live Backend, or Backend Verified labels and to ensure no secrets, tokens, private URLs, or customer data are visible.
