import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zhCN from './locales/zh-CN.json'
import th from './locales/th.json'
import es from './locales/es.json'
import fr from './locales/fr.json'
import ar from './locales/ar.json'
import pt from './locales/pt.json'
import ru from './locales/ru.json'
import hi from './locales/hi.json'
import bn from './locales/bn.json'
import ur from './locales/ur.json'

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: { en, 'zh-CN': zhCN, th, es, fr, ar, pt, ru, hi, bn, ur }
})

export default i18n
