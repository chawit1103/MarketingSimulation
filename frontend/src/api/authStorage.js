const AUTH_TOKEN_KEY = '3c-auth-token'
const API_KEY_KEY = '3c-api-key'

function storageAvailable(storage) {
  try {
    const testKey = '__3c_storage_test__'
    storage.setItem(testKey, '1')
    storage.removeItem(testKey)
    return true
  } catch {
    return false
  }
}

const hasSessionStorage = typeof sessionStorage !== 'undefined' && storageAvailable(sessionStorage)
const hasLocalStorage = typeof localStorage !== 'undefined' && storageAvailable(localStorage)

function safeGet(storage, key) {
  if (!storage) return ''
  try {
    return storage.getItem(key) || ''
  } catch {
    return ''
  }
}

function safeSet(storage, key, value) {
  if (!storage) return
  try {
    storage.setItem(key, value)
  } catch {
    // Ignore unavailable browser storage. Requests will continue unauthenticated.
  }
}

function safeRemove(storage, key) {
  if (!storage) return
  try {
    storage.removeItem(key)
  } catch {
    // Ignore unavailable browser storage.
  }
}

const session = hasSessionStorage ? sessionStorage : null
const local = hasLocalStorage ? localStorage : null

export function migrateLegacyAuthStorage() {
  const legacyToken = safeGet(local, AUTH_TOKEN_KEY)
  if (legacyToken && !safeGet(session, AUTH_TOKEN_KEY)) {
    safeSet(session, AUTH_TOKEN_KEY, legacyToken)
  }
  safeRemove(local, AUTH_TOKEN_KEY)

  // API keys are administrative credentials; do not keep them in persistent
  // browser storage for normal UI sessions.
  safeRemove(local, API_KEY_KEY)
}

export function getAuthToken() {
  migrateLegacyAuthStorage()
  return safeGet(session, AUTH_TOKEN_KEY)
}

export function setAuthToken(token) {
  safeRemove(local, AUTH_TOKEN_KEY)
  if (token) {
    safeSet(session, AUTH_TOKEN_KEY, token)
  } else {
    safeRemove(session, AUTH_TOKEN_KEY)
  }
}

export function clearAuthToken() {
  safeRemove(session, AUTH_TOKEN_KEY)
  safeRemove(local, AUTH_TOKEN_KEY)
}

export function getEphemeralApiKey() {
  migrateLegacyAuthStorage()
  return safeGet(session, API_KEY_KEY)
}

export function setEphemeralApiKey(apiKey) {
  safeRemove(local, API_KEY_KEY)
  if (apiKey) {
    safeSet(session, API_KEY_KEY, apiKey)
  } else {
    safeRemove(session, API_KEY_KEY)
  }
}

export function clearEphemeralApiKey() {
  safeRemove(session, API_KEY_KEY)
  safeRemove(local, API_KEY_KEY)
}

export function hasBrowserAuth() {
  return Boolean(getAuthToken() || getEphemeralApiKey())
}
