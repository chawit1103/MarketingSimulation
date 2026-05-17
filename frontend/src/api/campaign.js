import service from './index'
import { hasBrowserAuth } from './authStorage'

export const createCampaign = (data) => {
  return service.post('/api/campaign', data)
}

export const listCampaigns = () => {
  return service.get('/api/campaign')
}

export const getCampaign = (id) => {
  return service.get(`/api/campaign/${id}`)
}

export const updateCampaign = (id, data) => {
  return service.put(`/api/campaign/${id}`, data)
}

export const deleteCampaign = (id) => {
  return service.delete(`/api/campaign/${id}`)
}

export const startPipeline = (id) => {
  return service.post(`/api/campaign/${id}/pipeline/start`)
}

export const getPipelineStatus = (id) => {
  return service.get(`/api/campaign/${id}/pipeline/status`)
}

export const hasCampaignAuth = () => {
  return hasBrowserAuth()
}
