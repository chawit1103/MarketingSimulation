import service from './index'

export const calculateImpact = (campaignId, businessParams) => {
  return service.post('/api/impact/calculate', {
    campaign_id: campaignId,
    business: businessParams,
  })
}

export const quickScenario = (sentiment, params = {}) => {
  const qs = new URLSearchParams({
    price: params.unit_price || 100,
    market: params.market_size || 100000,
    share: params.current_market_share || 10,
    conversion: params.base_conversion_rate || 5,
    cost: params.campaign_cost || 500000,
    months: params.time_horizon_months || 6,
    product: params.product_name || 'Product',
  }).toString()
  return service.get(`/api/impact/scenarios/${sentiment}?${qs}`)
}
