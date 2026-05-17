import service from './index'

export const listCompetitorScenarios = () => {
  return service.get('/api/competitor/scenarios')
}

export const runCompetitorSimulation = (payload) => {
  return service.post('/api/competitor/simulate', payload)
}
