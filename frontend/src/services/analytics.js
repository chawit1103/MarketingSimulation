const ALLOWED_EVENTS = new Set([
  'demo_dashboard_opened',
  'brief_quality_scored',
  'simulation_started',
  'simulation_completed',
  'dashboard_viewed',
  'war_room_scenario_run',
  'action_plan_viewed',
  'revised_brief_created',
  'comparator_used',
  'budget_scenario_run',
  'export_clicked',
  'settings_provider_test_failed',
  'feedback_submitted',
])

const BLOCKED_KEYS = [
  'api_key',
  'apikey',
  'auth',
  'brief',
  'campaign_name',
  'content',
  'description',
  'email',
  'key',
  'name',
  'password',
  'phone',
  'prompt',
  'raw',
  'secret',
  'text',
  'token',
]

const SECRET_PATTERNS = [
  /sk-[A-Za-z0-9_-]{8,}/g,
  /sk-ant-[A-Za-z0-9_-]{8,}/g,
  /gsk_[A-Za-z0-9_-]{8,}/g,
  /sk-or-[A-Za-z0-9_-]{8,}/g,
]

export function analyticsEnabled() {
  const envValue = String(import.meta.env?.VITE_ANALYTICS_ENABLED ?? 'true').toLowerCase()
  return !['0', 'false', 'off', 'no'].includes(envValue)
}

export function trackEvent(eventName, payload = {}) {
  if (!analyticsEnabled() || !ALLOWED_EVENTS.has(eventName)) return false

  const event = {
    event: eventName,
    occurred_at: new Date().toISOString(),
    source: 'frontend',
    session_scope: 'browser_session',
    properties: sanitizePayload(payload),
  }

  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('3c:analytics', { detail: event }))
  }

  if (String(import.meta.env?.VITE_ANALYTICS_DEBUG || '').toLowerCase() === 'true') {
    console.info('[analytics]', event)
  }

  return true
}

export function isAllowedAnalyticsEvent(eventName) {
  return ALLOWED_EVENTS.has(eventName)
}

export function routeBucket(route) {
  const name = String(route?.name || '').toLowerCase()
  if (name) return name
  const path = String(route?.path || route?.fullPath || '')
  if (path.startsWith('/dashboard/')) return 'dashboard'
  if (path.startsWith('/simulation/')) return 'simulation'
  if (path.startsWith('/war-room')) return 'war_room'
  if (path.startsWith('/settings')) return 'settings'
  if (path.startsWith('/campaigns')) return 'campaigns'
  return path === '/' ? 'home' : 'unknown'
}

export function sourceModeFromValue(value) {
  const normalized = String(value || '').toLowerCase()
  const allowed = ['demo_mode', 'local_estimate', 'live_backend', 'backend_verified', 'unknown']
  return allowed.includes(normalized) ? normalized : 'unknown'
}

export function sanitizeAnalyticsPayload(payload) {
  const clean = {}
  const input = payload && typeof payload === 'object' ? payload : {}

  Object.entries(input).forEach(([key, value]) => {
    const normalizedKey = String(key || '').toLowerCase()
    if (BLOCKED_KEYS.some(blocked => normalizedKey.includes(blocked))) return

    const sanitized = sanitizeValue(value)
    if (sanitized !== undefined) {
      clean[key] = sanitized
    }
  })

  return clean
}

const sanitizePayload = sanitizeAnalyticsPayload

function sanitizeValue(value) {
  if (value == null) return undefined
  if (typeof value === 'boolean') return value
  if (typeof value === 'number') return Number.isFinite(value) ? value : undefined
  if (typeof value === 'string') {
    let output = value.slice(0, 80)
    SECRET_PATTERNS.forEach((pattern) => {
      output = output.replace(pattern, '[redacted]')
    })
    return output
  }
  if (Array.isArray(value)) {
    const items = value
      .map(item => sanitizeValue(item))
      .filter(item => item !== undefined)
      .slice(0, 12)
    return items.length ? items : undefined
  }
  return undefined
}
