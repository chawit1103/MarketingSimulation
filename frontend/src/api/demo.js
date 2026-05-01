import service from './index'

export const listDemoCampaigns = () => {
  return service.get('/api/demo/campaigns')
}

export const getDemoDashboard = (demoId) => {
  return service.get(`/api/demo/campaigns/${demoId}/dashboard`)
}

