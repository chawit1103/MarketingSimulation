import request from './index'

export const importActualResults = (payload) => {
  if (payload instanceof FormData) {
    return request.post('/api/calibration/actual-results', payload, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  }
  return request.post('/api/calibration/actual-results', payload)
}

export const getCalibrationStatus = (campaignId) => {
  return request.get(`/api/calibration/status/${encodeURIComponent(campaignId)}`)
}
