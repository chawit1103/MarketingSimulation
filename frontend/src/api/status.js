import service from './index'

export const getSystemStatus = () => {
  return service.get('/api/status')
}

