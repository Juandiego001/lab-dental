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

.v-input:not(:has(input:focus, textarea:focus)) .v-input__details {
  display: none;
}

.v-input__control:not(:has(textarea:focus)) .v-input__details {
  display: none;
}

.v-input.v-input--error .v-input__details {
  display: flex !important;
}
</style>