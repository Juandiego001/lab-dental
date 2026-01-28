<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  <TheSnackbar />
</template>

<script setup>
import TheSnackbar from '~/components/TheSnackbar.vue'
</script>

<style>
html {
  overflow-y: auto;
}
</style>