<template>
  <div class="px-4 my-4 text-primary d-flex align-center">
    <NuxtLink class="text-primary text-caption" :to="$localePath('/blog')">{{ $t('blog.title') }}</NuxtLink>
    <v-icon class="mx-2">mdi-chevron-right</v-icon>
    <span class="text-caption">{{ $t('blog.videos.title') }}</span>
  </div>

  <v-container min-height="100%">

    <div class="my-4 text-primary d-flex align-center">
      <span class="text-h5 me-2">{{ $t('blog.videos.title') }}</span>
      <v-icon>mdi-video</v-icon>
    </div>

    <v-row class="my-6">
        <v-card v-for="video in videos" :key="video.documentId"
          width="300" height="300" :to="$localePath(`/blog/videos/${video.documentId}`)" class="me-6">
          <v-img max-height="100" cover :src="`${strapiUrl}${video.poster.url}`" />
          <v-card-title>{{ video.title }}</v-card-title>
          <v-card-text>{{ video.description }}</v-card-text>
        </v-card>
    </v-row>

    <div class="py-4 text-center">
      <v-btn class="text-primary" variant="text" append-icon="mdi-chevron-double-down">{{ $t('blog.loadMore') }}</v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { onBeforeMount } from 'vue'

const config = useRuntimeConfig();

const strapiUrl = config.public.strapiUrl;
const videos = ref([]);

onBeforeMount(async () => {
  const { data } = await $fetch('/strapi/videos?populate=*');
  videos.value = data;
})
</script>