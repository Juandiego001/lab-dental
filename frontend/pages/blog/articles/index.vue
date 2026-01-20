<template>
  <div class="px-4 my-4 text-primary d-flex align-center">
    <NuxtLink class="text-primary text-caption" :to="$localePath('/blog')">{{ $t('blog.title') }}</NuxtLink>
    <v-icon class="mx-2">mdi-chevron-right</v-icon>
    <span class="text-caption">{{ $t('blog.articles.title') }}</span>
  </div>

  <v-container min-height="100%">

    <div class="my-4 text-primary d-flex align-center">
      <span class="text-h5 me-2">{{ $t('blog.articles.title') }}</span>
      <v-icon>mdi-file-document-multiple</v-icon>
    </div>

    <v-row class="my-6">
      <v-card v-for="article in articles" :key="article.documentId"
      width="300" height="300" :to="$localePath(`/blog/articles/${article.documentId}`)" class="me-6">
        <v-img max-height="100" cover :src="`${strapiUrl}${article.cover.url}`" />
        <v-card-title>{{ article.title }}</v-card-title>
        <v-card-text>{{ article.description }}</v-card-text>
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
const articles = ref([]);

onBeforeMount(async () => {
  const { data } = await $api('/strapi/articles?populate=*');
  articles.value = data;
})
</script>