<template>
    <v-container fluid class="bg-primary py-0 border">
        <v-row class="ma-0 py-2 justify-center align-center no-gutters">
            <div>
                <NuxtLink class="text-decoration-none text-white text-h5" to="/">
                    <v-img width="200" height="30" src="/public/snapon_navbar.svg"></v-img>
                </NuxtLink>
            </div>

            <v-spacer></v-spacer>

            <div>
                <v-btn class="text-none me-2" :to="$localePath('/')" variant="text">{{ $t('menu.home') }}</v-btn>
                <v-btn class="text-none me-2" :to="$localePath('/services')" variant="text">{{ $t('services.title') }}</v-btn>
                <v-btn class="text-none me-2" :to="$localePath('/roi')" variant="text">{{ $t('menu.roi') }}</v-btn>
                <v-btn class="text-none me-2" :to="$localePath('/about')" variant="text">{{ $t('menu.about') }}</v-btn>
                <v-btn class="text-none me-2" :to="$localePath('/blog')" variant="text">{{ $t('menu.blog') }}</v-btn>
                <v-btn class="text-none me-2" :to="$localePath('/forum')" variant="text">{{ $t('menu.forum') }}</v-btn>
                <v-btn class="text-none font-weight-bold me-2" variant="text" :to="$localePath('/login')">{{ $t('menu.logIn') }}</v-btn>
                <v-btn class="text-none text-primary font-weight-bold" :to="$localePath('/contact')">{{ $t('contact.title') }}</v-btn>
            </div>

            <v-spacer></v-spacer>

            <v-menu>
                <template v-slot:activator="{ props }">
                    <v-btn color="primary" class="text-white" variant="text" elevation="0" v-bind="props">
                        <span class="me-2">{{ locale }}</span>
                        <v-icon>mdi-chevron-down</v-icon>

                    </v-btn>
                </template>
                <v-list class="bg-primary text-white">
                    <v-list-item v-for="(eachLocale, index) in locales" :key="`${eachLocale.code}_${index}`" :value="eachLocale.code" @click="setLocale(eachLocale.code)">
                        <v-list-item-title class="text-subtitle-2">{{ eachLocale.name }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-row>
    </v-container>
</template>

<script setup>
import { computed, onBeforeMount } from 'vue'

const { locale, locales, setLocale } = useI18n();
</script>