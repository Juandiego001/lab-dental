<template>
  <v-container class="d-flex justify-center align-center" min-height="100%">
    <v-row no-gutters class="align-center justify-center">
      <v-card class="me-8" to="/app/users" width="200" height="200">
        <v-img src="/public/bg_about.png" />
        <v-card-title>Users</v-card-title>
      </v-card>

      <v-card class="me-8" to="/app/groups" width="200" height="200">
        <v-img src="/public/bg_about.png" />
        <v-card-title>Groups</v-card-title>
      </v-card>

      <v-card class="me-8" href="http://localhost:1337" width="200" height="200">
        <v-img src="/public/bg_about.png" />
        <v-card-title>Strapi</v-card-title>
      </v-card>

      <v-card class="me-8" href="http://192.168.0.104:4200" width="200" height="200">
        <v-img src="/public/bg_about.png" />
        <v-card-title>Forum</v-card-title>
      </v-card>
    </v-row>
  </v-container>
</template>

<script setup>

definePageMeta({
  layout: 'app',
  middleware: 'private'
})

useHead({
  title: 'SOE Latam | App'
})

</script>