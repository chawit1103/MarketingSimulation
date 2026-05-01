import service from './index'

export const compareCampaigns = (campaignIds) => {
  return service.post('/api/comparator/compare', { campaign_ids: campaignIds })
}

export const getComparisonMetrics = () => {
  return service.get('/api/comparator/metrics')
}
