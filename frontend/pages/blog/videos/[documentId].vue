<template>
  <div class="px-4 my-4 text-secondary d-flex align-center">
    <NuxtLink class="text-secondary text-caption" :to="$localePath('/blog')">{{ $t('blog.title') }}</NuxtLink>
    <v-icon class="mx-2">mdi-chevron-right</v-icon>
    <NuxtLink class="text-secondary text-caption" :to="$localePath('/blog/videos')">{{ $t('blog.videos.title') }}</NuxtLink>
    <v-icon class="mx-2">mdi-chevron-right</v-icon>
    <span class="text-caption">{{ video.slug }}</span>
  </div>

  <v-container min-height="100vh">
    <v-row class="py-12">
      <v-col class="d-flex align-center">
        <p class="text-h4 font-weight-bold">{{ video.title }}</p>
      </v-col>
      <v-col>
        <p class="text-caption text-grey">{{ $t('blog.date') }}</p>
        <p class="text-caption mb-2">{{ $dateFormat(new Date(video.createdAt)) }}</p>
      </v-col>
    </v-row>

    <video :src="`http://localhost:1337${video.file.url}`" width="100%" :poster="`http://localhost:1337${video.poster.url}`" controls autoplay>
    </video>
    <a class="text-subtitle-1 mt-2 d-block text-grey text-caption" :href="video.url" target="_blank">{{ video.url }}</a>
    <p class="text-subtitle-1 mt-2">{{ video.description }}</p>
  </v-container>
</template>

<script setup>
import { onBeforeMount } from 'vue';

const config = useRuntimeConfig();
const { $dateFormat } = useNuxtApp();
const route = useRoute()

const strapiUrl = config.public.strapiUrl;
const video = ref({
  slug: '',
  title: '',
  createdAt: '',
  file: {
    url: ''
  },
  poster: {
    url: ''
  },
})

onBeforeMount(async () => {
  const { data } = await $fetch(`/strapi/videos/${route.params.documentId}?populate=*`)
  video.value = data;
})
</script>