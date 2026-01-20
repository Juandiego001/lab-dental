// import this after install `@mdi/font` package
import '@mdi/font/css/materialdesignicons.css'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    theme: {
      themes: {
        light: {
          dark: false,
          colors: {
            primary: '#003049',
            secondary: '#669BBC',
            beige: '#C4A484',
            brown: '#8B4513',
            black: '#1A1A1A'
          }
        },
      },
    },
    ssr: true
  })
  app.vueApp.use(vuetify)
})