import service from './index'

export const getKPIs = (campaignId) => {
  return service.get(`/api/dashboard/campaign/${campaignId}/kpi`)
}

export const getReport = (campaignId) => {
  return service.get(`/api/dashboard/campaign/${campaignId}/report`)
}

export const getTimeline = (campaignId) => {
  return service.get(`/api/dashboard/campaign/${campaignId}/timeline`)
}

export const getSegments = (campaignId) => {
  return service.get(`/api/dashboard/campaign/${campaignId}/segments`)
}

export const getInfluencers = (campaignId) => {
  return service.get(`/api/dashboard/campaign/${campaignId}/timeline`)
}
