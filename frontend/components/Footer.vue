<template>
  <v-container fluid class="bg-primary pa-0">
    <v-row no-gutters justify="space-between" :class="`py-4 ${$vuetify.display.mdAndUp && 'px-4'}`">
      <v-col :class="`d-flex align-center ${$vuetify.display.smAndDown && 'justify-center'}`">
        <NuxtLink class="text-white text-decoration-none" :to="$localePath('/')">
          <v-img width="200" height="30" src="/public/snapon_navbar.svg"></v-img>
        </NuxtLink>
      </v-col>

      <v-col v-if="$vuetify.display.mdAndUp" class="d-flex ga-4 align-center justify-end">
        <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/services')">
          {{ $t('services.title') }}
        </NuxtLink>
        <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/roi')">
          {{ $t('menu.roi') }}
        </NuxtLink>
        <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/about')">
          {{ $t('menu.about') }}
        </NuxtLink>
        <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/blog')">
          {{ $t('menu.blog') }}
        </NuxtLink>
        <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/forum')">
          {{ $t('menu.forum') }}
        </NuxtLink>
        <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/login')">
          {{ $t('menu.logIn') }}
        </NuxtLink>
        <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/contact')">
          {{ $t('contact.title') }}
        </NuxtLink>
      </v-col>

      <!-- Responsive -->
      <v-col v-else>
        <v-row no-gutters class="align-center">
          <v-col class="d-flex flex-column text-center justify-end ga-2" cols="6">
            <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/services')">
              {{ $t('services.title') }}
            </NuxtLink>
            <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/roi')">
              {{ $t('menu.roi') }}
            </NuxtLink>
            <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/about')">
              {{ $t('menu.about') }}
            </NuxtLink>
          </v-col>
          <v-col class="d-flex flex-column text-center ga-2" cols="6">
            <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/blog')">
              {{ $t('menu.blog') }}
            </NuxtLink>
            <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/forum')">
              {{ $t('menu.forum') }}
            </NuxtLink>
            <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/login')">
              {{ $t('menu.logIn') }}
            </NuxtLink>
            <NuxtLink class="text-white text-decoration-none text-caption" :to="$localePath('/contact')">
              {{ $t('contact.title') }}
            </NuxtLink>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <div :class="`py-4 border-surface-light border-t-md d-flex ${$vuetify.display.mdAndUp ? 'flex-row align-center justify-space-between px-4' : 'flex-column ga-1'}`">
      <p
        :class="`text-center text-subtitle-2 d-flex justify-center items-center ${$vuetify.display.mdAndUp ? 'ga-2' : 'flex-column ga-1 text-caption'}`">
        <span>© Snapon SOE Latam 2025.</span>
        <span>{{ $t('menu.rights') }}</span>
      </p>
      <div class="d-flex justify-center align-center">
        <v-btn class="text-caption" variant="plain" :to="$localePath('/terms')">{{ $t('menu.terms') }}</v-btn>
        <v-btn class="text-caption" variant="plain" :to="$localePath('/privacy')">{{ $t('menu.privacy') }}</v-btn>
      </div>
    </div>

    <p class="text-caption text-center font-weight-thin pb-2">
      With
      <v-icon>mdi-heart</v-icon>
      from jdcabal.com
    </p>
  </v-container>
</template>

<script setup>

</script>
