import service from './index'

export const analyzeDecision = (payload) => {
  return service.post('/api/decision/analyze', payload)
}

export const runWhatIf = (payload) => {
  return service.post('/api/decision/what-if', payload)
}

