<template>
    <v-row no-gutters class="bg-primary border border-t-lg">
        <v-col cols="6 pa-4">
            <NuxtLink class="text-white text-decoration-none" :to="$localePath('/')">
                <v-img width="200" height="30" src="/public/snapon_navbar.svg"></v-img>
            </NuxtLink>
        </v-col>

        <v-col class="text-end" cols="6 pa-4">
            <NuxtLink class="text-white text-decoration-none me-4 text-caption" :to="$localePath('/services')">{{ $t('services.title') }}</NuxtLink>
            <NuxtLink class="text-white text-decoration-none me-4 text-caption" :to="$localePath('/roi')">{{ $t('menu.roi') }}</NuxtLink>
            <NuxtLink class="text-white text-decoration-none me-4 text-caption" :to="$localePath('/about')">{{ $t('menu.about') }}</NuxtLink>
            <NuxtLink class="text-white text-decoration-none me-4 text-caption" :to="$localePath('/blog')">{{ $t('menu.blog') }}</NuxtLink>
            <NuxtLink class="text-white text-decoration-none me-4 text-caption" :to="$localePath('/forum')">{{ $t('menu.forum') }}</NuxtLink>
            <NuxtLink class="text-white text-decoration-none me-4 text-caption" :to="$localePath('/login')">{{ $t('menu.logIn') }}</NuxtLink>
            <NuxtLink class="text-white text-decoration-none me-4 text-caption" :to="$localePath('/contact')">{{ $t('contact.title') }}</NuxtLink>
        </v-col>

        <v-col cols="12" class="text-center d-flex align-center pa-4 border-surface-light border-t-md">
            <p class="text-subtitle-2 d-flex align-center">© Snapon SOE Latam 2025. {{ $t('menu.rights') }}</p>
            <v-spacer></v-spacer>
            <v-btn class="text-caption" variant="plain" :to="$localePath('/terms')">{{ $t('menu.terms') }}</v-btn>
            <v-btn class="text-caption" variant="plain" :to="$localePath('/privacy')">{{ $t('menu.privacy') }}</v-btn>
        </v-col>

        <v-col cols="12" class="text-caption text-center pb-4 font-weight-thin">
            With
            <v-icon>mdi-heart</v-icon>
            from jdcabal.com
        </v-col>
    </v-row>
</template>

<script setup>

</script>
