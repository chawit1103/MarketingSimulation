import service from './index'

export const compareCampaigns = (campaignIds) => {
  return service.post('/api/comparator/compare', { campaign_ids: campaignIds })
}

export const listDemoComparatorCampaigns = () => {
  return service.get('/api/comparator/demo/campaigns')
}

export const compareDemoCampaigns = (campaignIds) => {
  return service.post('/api/comparator/demo/compare', { campaign_ids: campaignIds })
}

export const getComparisonMetrics = () => {
  return service.get('/api/comparator/metrics')
}
