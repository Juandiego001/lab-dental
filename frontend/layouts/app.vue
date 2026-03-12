<template>
  <v-app>
    <v-layout style="max-height: 100vh;">
      <AppNavigation />
      <v-main>
        <v-container fluid class="fill-height pa-0" style="overflow-y: auto;">
          <NuxtPage />
        </v-container>
      </v-main>
    </v-layout>
  </v-app>
</template>

<script setup>

</script>
