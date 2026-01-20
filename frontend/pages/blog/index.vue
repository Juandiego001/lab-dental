<template>
  <v-container min-height="100vh">
    <div class="py-8 text-center d-flex justify-center align-center">
      <span class="text-primary text-h4 me-2">{{ $t('blog.title') }}</span>
      <v-icon color="primary" class="text-h5">mdi-file-document-multiple</v-icon>
    </div>

    <NuxtLink :to="$localePath('/blog/articles')" class="my-4 text-primary text-decoration-none d-flex align-center">
      <span class="text-h5 me-2">{{ $t('blog.articles.title') }}</span>
      <v-icon>mdi-file-document-multiple</v-icon>
    </NuxtLink>

    <v-row no-gutters>
      <v-card v-for="article in articles" :key="article.documentId"
      width="300" height="300" :to="$localePath(`/blog/articles/${article.documentId}`)" class="me-6">
        <v-img max-height="100" cover :src="`${strapiUrl}${article.cover.url}`" />
        <v-card-title>{{ article.title }}</v-card-title>
        <v-card-text>{{ article.description }}</v-card-text>
      </v-card>
    </v-row>

    <div class="py-4">
      <v-btn class="text-primary" :to="$localePath('/blog/articles')" variant="text" append-icon="mdi-chevron-double-right">{{ $t('blog.viewMore') }}</v-btn>
    </div>

    <NuxtLink :to="$localePath('/blog/videos')" class="my-4 text-primary text-decoration-none d-flex align-center">
      <span class="text-h5 me-2">{{ $t('blog.videos.title') }}</span>
      <v-icon>mdi-video</v-icon>
    </NuxtLink>

    <v-row no-gutters>
      <v-card v-for="video in videos" :key="video.documentId" width="300" height="300"
        :to="$localePath(`/blog/videos/${video.documentId}`)" class="me-6">
        <v-img max-height="100" cover :src="`${strapiUrl}${video.poster.url}`" />
        <v-card-title>{{ video.title }}</v-card-title>
        <v-card-text>{{ video.description }}</v-card-text>
      </v-card>
    </v-row>

    <div class="py-4">
      <v-btn class="text-primary" :to="$localePath('/blog/videos')" variant="text" append-icon="mdi-chevron-double-right">{{ $t('blog.viewMore') }}</v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { onBeforeMount } from 'vue'

const config = useRuntimeConfig();

const strapiUrl = config.public.strapiUrl;
const articles = ref([]);
const videos = ref([]);

onBeforeMount(async () => {
  let data;
  ({ data } = await $api('/strapi/articles?populate=*'));
  articles.value = data;
  ({ data } = await $api('/strapi/videos?populate=*'));
  videos.value = data;
})

</script>
