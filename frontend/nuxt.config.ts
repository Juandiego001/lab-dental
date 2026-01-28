// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from "vite-plugin-vuetify";

export default defineNuxtConfig({
  app: {
    head: {
      title: "SOE Latam",
      link: [{ rel: "icon", type: "image/x-icon", href: "/logo2.png" }],
    },
  },
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      appUrl: process.env.NUXT_APP_URL,
      strapiUrl: process.env.NUXT_STRAPI_URL,
      discourseUrl: process.env.NUXT_DISCOURSE_URL,
    },
  },
  build: {
    transpile: ["vuetify"],
  },
  routeRules: {
    "/api/**": { proxy: `${process.env.NUXT_APP_URL}/api/**` },
    "/strapi/**": { proxy: `${process.env.NUXT_STRAPI_URL}/strapi/**` },
    "/discourse/**": { proxy: `${process.env.NUXT_DISCOURSE_URL}/**` },
  },
  modules: [
    (_options, nuxt) => {
      nuxt.hooks.hook("vite:extendConfig", (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }));
      });
    },
    "@nuxtjs/i18n",
  ],
  i18n: {
    bundle: {
      optimizeTranslationDirective: false,
    },
    compilation: {
      strictMessage: false,
    },
    defaultLocale: "en",
    locales: [
      { code: "en", name: "EN", file: "en.json" },
      { code: "es", name: "ES", file: "es.json" },
    ],
  },
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
});
