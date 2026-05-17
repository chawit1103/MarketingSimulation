import service from './index'

export const runBudgetScenario = (inputs) => {
  return service.post('/api/decision/budget-scenario', { inputs })
}
