<template>
  <!-- Banner -->
  <v-container class="position-relative pa-0 ma-0 d-flex justify-center align-center" fluid>
    <v-img class="w-100" :max-height="$vuetify.display.mdAndUp && 400 || $vuetify.display.sm && 350 || 200" cover
      src="/public/index_banner_img.jpg" style="filter:brightness(40%);" />
    <v-sheet class="bg-transparent position-absolute text-center">
      <v-img class="mx-auto" :width="$vuetify.display.mdAndUp && 400 ||
        $vuetify.display.smAndDown && 200
        " src="/snapon_navbar.svg" />
      <h1 v-html="$t('index.banner')" :class="`text-white my-6
          ${$vuetify.display.mdAndUp && 'text-h4'}
          ${$vuetify.display.smAndUp && 'text-h5'}
          ${$vuetify.display.xs && 'text-body-2'}
        `" />
      <NuxtLink :to="$localePath('/contact')" :class="`d-inline-block text-primary bg-white font-weight-bold text-decoration-none  rounded-lg
          ${$vuetify.display.mdAndUp && 'text-h6 pa-4'}
          ${$vuetify.display.smAndDown && 'text-body-2 pa-2'}
        `">
        <span class="text-primary">{{ $t('contact.title') }}</span>
      </NuxtLink>
    </v-sheet>
  </v-container>

  <!-- Our brands -->
  <v-container class="py-16 px-0" fluid>
    <v-row no-gutters>
      <v-col class="d-flex justify-center align-center text-center mb-8" cols="12">
        <h1 class="text-h4 text-primary font-weight-bold">{{ $t('index.ourBrands.title') }}</h1>
      </v-col>

      <v-col sm="12" md="12" lg="6" cols="12">
        <NuxtLink to="https://www.johnbean.com/la-en/about-us/"
          class="d-flex align-center justify-center position-relative h-100 w-100 text-decoration-none pa-8"
          target="_blank">
          <v-img width="100%" height="100%" cover class="position-absolute"
            src="/public/Jhon_Bean/bg_wheel_aligners.jpg"></v-img>

          <div class="bg-transparent rounded-xl" style="backdrop-filter: blur(24px);">
            <v-img max-width="80%" width="300" class="mx-auto my-4" src="/public/Jhon_Bean/logo_white.png"></v-img>
            <p class="text-subtitle-2 text-center text-white pa-4">{{ $t('index.ourBrands.johnBean') }}</p>
          </div>
        </NuxtLink>
      </v-col>

      <v-col sm="12" md="12" lg="6" cols="12">
        <NuxtLink to="https://hofmann-equipment.com/la-en/wheel-alignment-machines"
          class="d-flex align-center justify-center position-relative h-100 w-100 text-decoration-none pa-8"
          target="_blank">
          <v-img width="100%" height="100%" cover class="position-absolute"
            src="/public/Hofmann/bg_wheel_aligners.png"></v-img>

          <div class="bg-transparent rounded-xl" style="backdrop-filter: blur(24px);">
            <v-img max-width="80%" width="300" class="mx-auto my-4" src="/public/Hofmann/logo_white.png"></v-img>
            <p class="text-subtitle-2 text-center text-white pa-4">{{ $t('index.ourBrands.hoffman') }}</p>
          </div>
        </NuxtLink>
      </v-col>
    </v-row>
  </v-container>

  <!-- Services -->
  <v-container :class="`bg-primary text-center py-16  mb-8 ${$vuetify.display.mdAndUp && 'rounded-lg'}`">
    <v-sheet class="bg-white d-inline-block mx-auto text-center mb-12 w-auto rounded-xl pa-4">
      <h2 class="text-primary text-h4 font-weight-bold">{{ $t('services.title') }}</h2>
    </v-sheet>

    <v-row class="justify-center">
      <v-col class="d-flex justify-center align-center" sm="6" md="4" lg="3" cols="12">
        <NuxtLink :to="('/app/installations')" class="d-block bg-white rounded-xl pa-8 text-decoration-none">
          <v-icon class="text-primary text-h2" size="x-large">mdi-train-car-flatbed-car</v-icon>
          <p class="text-primary text-h5">{{ $t('services.installations.title') }}</p>
        </NuxtLink>
      </v-col>
      <v-col class="d-flex justify-center align-center" sm="6" md="4" lg="3" cols="12">
        <NuxtLink :to="$localePath('/app/equipments')" class="d-block bg-white rounded-xl pa-8 text-decoration-none">
          <v-icon class="text-primary text-h2" size="x-large">mdi-car-cog</v-icon>
          <p class="text-primary text-h5">{{ $t('services.equipments.title') }}</p>
        </NuxtLink>
      </v-col>
      <v-col class="d-flex justify-center align-center" sm="6" md="4" lg="3" cols="12">
        <NuxtLink :to="$localePath('/app/warranties')" class="d-block bg-white rounded-xl pa-8 text-decoration-none">
          <v-icon class="text-primary text-h2" size="x-large">mdi-certificate</v-icon>
          <p class="text-primary text-h5">{{ $t('services.warranties.title') }}</p>
        </NuxtLink>
      </v-col>
      <v-col class="d-flex justify-center align-center" sm="6" md="4" lg="3" cols="12">
        <NuxtLink :to="$localePath('/app/manuals')" class="d-block bg-white rounded-xl pa-8 text-decoration-none">
          <v-icon class="text-primary text-h2" size="x-large">mdi-book-cog</v-icon>
          <p class="text-primary text-h5">{{ $t('services.manuals.title') }}</p>
        </NuxtLink>
      </v-col>
    </v-row>
  </v-container>

  <!-- Manuals -->
  <v-container class="text-center py-12">
    <h2 class="text-primary mb-4 text-h4 font-weight-bold">{{ $t('manuals.title') }}</h2>
  </v-container>

  <!-- Blog -->
  <v-container class="text-center py-12">
    <h2 class="text-primary mb-6 text-h4 font-weight-bold">{{ $t('index.ourBlog') }}</h2>

    <v-row no-gutters class="justify-center">
      <v-card v-for="article in articles" :key="article.documentId" width="300" height="300"
        :to="$localePath(`/blog/articles/${article.documentId}`)" class="my-6 me-6">
        <v-img max-height="100" cover :src="`${strapiUrl}${article.cover.url}`" />
        <v-card-title>{{ article.title }}</v-card-title>
        <v-card-text class="text-start">{{ article.description }}</v-card-text>
      </v-card>
    </v-row>
  </v-container>


  <!-- Contact Us -->
  <v-container max-width="900" :class="`bg-primary text-center pa-8 mb-12 ${$vuetify.display.mdAndUp && 'rounded-lg'}`">
    <h2 class="text-white mb-8 text-h4 font-weight-bold">{{ $t('contact.us') }}</h2>

    <v-form>
      <v-row class="justify-center align-center">
        <v-col sm="12" md="6" lg="6" cols="12">
          <v-text-field :label="$t('email')" hide-details="auto"></v-text-field>
        </v-col>

        <v-col sm="12" md="6" lg="6" cols="12">
          <v-text-field :label="$t('phone')" hide-details="auto"></v-text-field>
        </v-col>

        <v-col sm="12" md="12" lg="12" cols="12">
          <v-text-field :label="$t('name')" hide-details="auto"></v-text-field>
        </v-col>

        <v-col sm="12" md="12" lg="12" cols="12">
          <v-textarea :label="$t('message')" hide-details="auto"></v-textarea>
        </v-col>

        <v-col class="text-end" cols="12">
          <v-btn type="submit" variant="outlined">{{ $t('contact.send') }}</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script setup>
import { onBeforeMount } from 'vue'

const { locales, setLocale } = useI18n();
const config = useRuntimeConfig();

const strapiUrl = config.public.strapiUrl;
const articles = ref([]);
const videos = ref([]);

onBeforeMount(async () => {
  try {
    const { data } = await $api('/strapi/articles?populate=*');
    articles.value = data;
  } catch (err) {
    console.log('Ocurrió un error al intentar obtener las entradas de blog');
  }
})

</script>
