import service from './index'

export function getSettings() {
  return service.get('/api/settings')
}

export function updateSettings(data) {
  return service.put('/api/settings', data)
}

export function getProviders() {
  return service.get('/api/settings/providers')
}

export function testLLMConnection(config) {
  return service.post('/api/settings/test-llm', config)
}

export function checkSettingsReadiness(config) {
  return service.post('/api/settings/readiness', config)
}
