<template>
<v-container min-height="100vh" class="justify-center">

    <NuxtLink :href="`${discourseUrl}/latest`" target="_blank" class="text-center py-6 text-primary d-flex align-center justify-center text-decoration-none">
        <span class="text-h4 me-2">{{ $t('forum.title') }}</span>
        <v-icon class="text-h5">mdi-forum</v-icon>
    </NuxtLink>
    <p class="text-h6 mt-8 text-primary">
        {{ $t('forum.latestPost') }}
        <v-icon class="text-h5">mdi-forum-outline</v-icon>
    </p>

    <v-row no-gutters>
        <v-card width="300" v-for="post in posts" :key="`post_${post.id}`" class="mt-6 me-6"
        :href="`${discourseUrl}${post.post_url}`">
            <v-card-title>
                <v-row class="py-4 px-2">
                    <p class="text-caption pa-1 rounded-lg text-white" :style="{ background: post.category_color }">{{ post.category_slug }}</p>
                    <v-spacer></v-spacer>
                    <p class="text-caption">{{ $t('forum.replies') }} {{ post.reply_count }}</p>
                </v-row>
            </v-card-title>
            <v-card-text>
                <p class="text-h6">{{ post.topic_title }}</p>
            </v-card-text>
            <v-card-actions>
                <v-row no-gutters>
                    <p class="text-caption">{{ post.username }}</p>
                    <v-spacer></v-spacer>
                    <p class="text-caption">{{ $dateFormat(new Date(post.created_at)) }}</p>
                </v-row>
            </v-card-actions>
        </v-card>
    </v-row>
</v-container>
</template>

<script setup>
import { onBeforeMount } from 'vue';

const config = useRuntimeConfig();
const { $dateFormat } = useNuxtApp();

const discourseUrl = config.public.discourseUrl;
const posts = ref([]);

onBeforeMount(async () => {
    try {
        let { latest_posts } = await $api('/discourse/posts.json');
        const { categories } = (await $api('/discourse/categories.json')).category_list;
        latest_posts = latest_posts.map(a => {
            let { slug, color } = categories.find(b => b.id === a.category_id);
            a['category_color'] = `#${color}`;
            a['category_slug'] = slug;
            return a;
        })
        posts.value = latest_posts
    } catch (err) {
        console.error(err);
    }
})

</script>
