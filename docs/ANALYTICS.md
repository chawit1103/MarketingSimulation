# Analytics And Feedback

Updated: 2026-05-01

This release adds a lightweight, provider-neutral frontend analytics abstraction and a small feedback widget. It is designed for product-learning during demos and pilots without sending data to third-party analytics services by default.

## Default Behavior

- Events are emitted as browser `CustomEvent` messages named `3c:analytics`.
- No third-party analytics SDK is installed.
- No network request is made by the analytics service.
- No raw campaign brief, prompt, customer data, API key, auth token, password, or secret should be included in event properties.
- Free-form feedback text is intentionally not collected. The feedback widget only sends a 1-5 usefulness rating and a fixed confusion category.

## Disable Analytics

Set this frontend environment variable before building or running Vite:

```bash
VITE_ANALYTICS_ENABLED=false
```

Optional local debugging:

```bash
VITE_ANALYTICS_DEBUG=true
```

Debug mode logs sanitized events to the browser console. Do not enable debug logs in shared demo recordings if they could reveal internal testing behavior.

## Tracked Events

| Event | Purpose | Sensitive fields intentionally excluded |
|---|---|---|
| `demo_dashboard_opened` | Demo onboarding usage | campaign name, raw route path |
| `brief_quality_scored` | Brief readiness engagement | raw brief, description, recommendations text |
| `simulation_started` | Simulation flow start | campaign name, brief content, user identity |
| `simulation_completed` | Simulation flow completion | raw logs, generated actions text |
| `dashboard_viewed` | Dashboard usage | campaign name, full route path |
| `war_room_scenario_run` | War Room scenario engagement | campaign content, competitor free text |
| `action_plan_viewed` | Action Plan visibility | recommendation text, raw action plan |
| `export_clicked` | Export intent | report title, campaign name, file content |
| `provider_test_failed` | Setup friction | API keys, provider error dumps, passwords |
| `feedback_submitted` | Usefulness/confusion feedback | free-form text, PII |

## Sanitization

The frontend analytics service drops fields whose keys look sensitive, including keys containing:

- `api_key`
- `auth`
- `brief`
- `campaign_name`
- `content`
- `description`
- `email`
- `key`
- `name`
- `password`
- `phone`
- `prompt`
- `raw`
- `secret`
- `text`
- `token`

String values are truncated and common provider-key patterns are redacted as a second guardrail.

## Future Provider Integration

If a team later connects PostHog, Segment, Snowplow, OpenTelemetry, or an internal endpoint:

1. Keep the event names stable.
2. Keep the same denylist and payload minimization rules.
3. Document the destination, retention, opt-out behavior, and data owner.
4. Do not enable third-party analytics for customer pilots without privacy review.
5. Keep Demo Mode, Local Estimate, Live Backend, and Backend Verified source labels visible in analytics-relevant UI.
