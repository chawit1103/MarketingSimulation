import service from './index'

export const scoreBriefQuality = (brief) => {
  return service.post('/api/brief/quality', { brief })
}
