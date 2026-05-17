import { afterEach, vi } from 'vitest'
import { config } from '@vue/test-utils'

function createMemoryStorage() {
  const store = new Map()
  return {
    get length() {
      return store.size
    },
    clear() {
      store.clear()
    },
    getItem(key) {
      return store.has(key) ? store.get(key) : null
    },
    key(index) {
      return Array.from(store.keys())[index] || null
    },
    removeItem(key) {
      store.delete(key)
    },
    setItem(key, value) {
      store.set(key, String(value))
    },
  }
}

const testLocalStorage = window.localStorage || createMemoryStorage()
const testSessionStorage = window.sessionStorage || createMemoryStorage()

Object.defineProperty(window, 'localStorage', {
  configurable: true,
  value: testLocalStorage,
})

Object.defineProperty(window, 'sessionStorage', {
  configurable: true,
  value: testSessionStorage,
})

Object.defineProperty(globalThis, 'localStorage', {
  configurable: true,
  value: testLocalStorage,
})

Object.defineProperty(globalThis, 'sessionStorage', {
  configurable: true,
  value: testSessionStorage,
})

config.global.stubs = {
  RouterLink: {
    props: ['to'],
    template: '<a :href="typeof to === \'string\' ? to : \'#\'"><slot /></a>',
  },
}

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

afterEach(() => {
  window.localStorage.clear()
  window.sessionStorage.clear()
  vi.restoreAllMocks()
})
