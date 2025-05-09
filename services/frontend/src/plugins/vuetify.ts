/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'
import DateFnsAdapter from '@date-io/date-fns'
import { ru } from 'date-fns/locale'
import { ru as messages_ru, en } from 'vuetify/locale'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  locale: {
    locale: 'ru',
    messages: {ru: messages_ru, en},
  },
  date: {
    adapter: DateFnsAdapter,
    locale: {
      ru: ru
    }
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          'app-primary': '#00b559',
          'background': '#eaeaea'
        },
      },
      dark: {
        colors: {
          'app-primary': '#17793b',
        }
      }
    },
  },
})
