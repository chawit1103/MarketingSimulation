import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'

export function testI18n() {
  return createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages: { en },
  })
}

export function flushPromises() {
  return new Promise((resolve) => setTimeout(resolve, 0))
}
