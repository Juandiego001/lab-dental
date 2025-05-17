<template>
  <div class="px-4 my-4 text-primary d-flex align-center">
    <NuxtLink class="text-primary text-caption" :to="$localePath('/blog')">{{ $t('blog.title') }}</NuxtLink>
    <v-icon class="mx-2">mdi-chevron-right</v-icon>
    <NuxtLink class="text-primary text-caption" :to="$localePath('/blog/articles')">{{ $t('blog.articles.title') }}</NuxtLink>
    <v-icon class="mx-2">mdi-chevron-right</v-icon>
    <span class="text-caption">{{ article.slug }}</span>
  </div>

  <v-container min-height="100vh">
    <v-row class="py-12">
      <v-col class="d-flex align-center">
        <p class="text-h4 font-weight-bold">{{ article.title }}</p>
      </v-col>
      <v-col>
        <p class="text-caption text-grey">{{ $t('blog.date') }}</p>
        <p class="text-caption mb-2">{{ $dateFormat(new Date(article.createdAt)) }}</p>
        <p class="text-caption text-grey">{{ $t('blog.articles.category') }}</p>
        <p class="text-caption py-1 px-2 bg-grey-lighten-2 d-inline-block rounded-xl">{{ article.category.name }}</p>
      </v-col>
    </v-row>

    <v-img max-height="400" cover :src="`${strapiUrl}${article.cover.url}`"></v-img>
    <p class="text-subtitle-1 mt-2">{{ article.description }}</p>

    <v-container>
      <template v-for="block in article.blocks" :key="`${article.documentId}_${block.id}`">
        <template v-if="block.__component === 'shared.media'">
          <v-img contain class="mx-auto my-4" max-height="250" :src="`${strapiUrl}${block.file.url}`"></v-img>
        </template>
        <template v-if="block.__component === 'shared.quote'">
          <v-sheet class="border-s-md pa-4 my-4 font-italic">
            <p class="text-subtitle-1">{{ block.title }}</p>
            <p class="text-subtitle-2">{{ block.body }}</p>
          </v-sheet>
        </template>
        <template v-if="block.__component === 'shared.slider'">
            <v-carousel class="my-4">
              <v-carousel-item v-for="file in block.files" :src="`${strapiUrl}${file.url}`" cover></v-carousel-item>
            </v-carousel>
        </template>
        <template v-if="block.__component === 'rich-json.rich-json'">
          <template v-for="node in block.richtext">
            <p v-if="node.type === 'heading'" class="text-h6">{{ node.children[0].text }}</p>
            <p v-if="node.type === 'paragraph'">{{ node.children[0].text }}</p>
          </template>
        </template>
      </template>
    </v-container>
  </v-container>
</template>

<script setup>
import { onBeforeMount } from 'vue';

const config = useRuntimeConfig();
const { $dateFormat } = useNuxtApp();
const route = useRoute()

const strapiUrl = config.public.strapiUrl;
const article = ref({
  cover: {
    url: ''
  },
  title: '',
  createdAt: '',
  category: {
    name: ''
  },
  blocks: []
})

onBeforeMount(async () => {
  const { data } = await $fetch(`/strapi/articles/${route.params.documentId}?populate[cover][fields][0]=url&populate[category][fields][0]=name&populate[author][fields][0]=name&populate[blocks][on][shared.media][populate][file][fields][0]=url&populate[blocks][on][rich-json.rich-json][populate]=*&populate[blocks][on][shared.quote][populate]=*&populate[blocks][on][shared.slider][populate][files][fields][0]=url`)
  article.value = data;
})
</script>