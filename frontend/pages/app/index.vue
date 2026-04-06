<template>
  <v-container min-height="100%" fluid>
    <v-row class="gc-2">
      <v-col cols="12">
        <p class="text-h6">Home</p>
      </v-col>

      <v-col style="min-width: 180px; max-width: 250px;" v-for="route in routes">
        <NuxtLink class="d-flex align-center justify-space-between w-100 pa-2 text-white rounded-lg text-decoration-none"
          :style="{ background: route.background, cursor: 'pointer' }" :to="route.path">
          <span class="text-h6">{{ $t(`${route.subject}.title`, 2) }}</span>
          <v-icon :icon="route.icon" />
        </NuxtLink>
      </v-col>

      <!-- <v-card class="me-8" href="http://localhost:1337" width="200" height="200">
        <v-img src="/public/bg_about.png" />
        <v-card-title>Strapi</v-card-title>
      </v-card>

      <v-card class="me-8" href="http://192.168.0.104:4200" width="200" height="200">
        <v-img src="/public/bg_about.png" />
        <v-card-title>Forum</v-card-title>
      </v-card> -->
    </v-row>
  </v-container>
</template>

<script setup>
const { $ability } = useNuxtApp();

definePageMeta({
  layout: 'app',
  middleware: 'private'
})

useHead({
  title: 'SOE Latam | App'
})

const routes = ref([])
const menu = ref([
  {
    title: 'Distributors',
    subject: 'distributors',
    path: '/app/distributors',
    icon: 'mdi-domain',
    background: '#1976D2' // Blue
  },
  {
    title: 'Clients',
    subject: 'clients',
    path: '/app/clients',
    icon: 'mdi-account-tie',
    background: '#009688' // Teal
  },
  {
    title: 'Sites',
    subject: 'sites',
    path: '/app/sites',
    icon: 'mdi-fireplace-off',
    background: '#FF9800' // Orange
  },
  {
    title: 'Users',
    subject: 'users',
    path: '/app/users',
    icon: 'mdi-account',
    background: '#3F51B5' // Indigo
  },
  {
    title: 'Groups',
    subject: 'groups',
    path: '/app/groups',
    icon: 'mdi-account-group',
    background: '#9C27B0' // Purple
  },
  {
    title: 'Brands',
    subject: 'brands',
    path: '/app/brands',
    icon: 'mdi-shield-car',
    background: '#E91E63' // Pink
  },
  {
    title: 'Categories',
    subject: 'categories',
    path: '/app/categories',
    icon: 'mdi-shape-outline',
    background: '#4CAF50' // Green
  },
  {
    title: 'Equipments',
    subject: 'equipments',
    path: '/app/equipments',
    icon: 'mdi-car-cog',
    background: '#607D8B' // Blue Grey
  },
  // {
  //   title: 'Parts',
  //   subject: 'parts',
  //   path: '/app/parts',
  //   icon: 'mdi-nut',
  //   background: '#795548' // Brown
  // },
  {
    title: 'Installations',
    subject: 'installations',
    path: '/app/installations',
    icon: 'mdi-train-car-flatbed-car',
    background: '#00BCD4' // Cyan
  },
  // {
  //   title: 'Reasons',
  //   subject: 'reasons',
  //   path: '/app/reasons',
  //   icon: 'mdi-file-cancel',
  //   background: '#F44336' // Red
  // },
  // {
  //   title: 'Warranties',
  //   subject: 'warranties',
  //   path: '/app/warranties',
  //   icon: 'mdi-certificate',
  //   background: '#FFC107' // Amber
  // },
  // {
  //   title: 'Manuals',
  //   subject: 'manuals',
  //   path: '/app/manuals',
  //   icon: 'mdi-book-cog',
  //   background: '#8BC34A' // Light Green
  // },
  {
    title: 'Lists',
    subject: 'lists',
    path: '/app/lists',
    icon: 'mdi-office-building-cog-outline',
    background: '#673AB7' // Deep Purple
  },
  // {
  //   title: 'Configuration',
  //   subject: 'configuration',
  //   path: '/app/configuration',
  //   icon: 'mdi-cog',
  //   background: '#9E9E9E' // Grey
  // },
  // {
  //   title: 'Forums',
  //   subject: 'forums',
  //   path: 'http://192.168.0.104:4200',
  //   icon: 'mdi-open-in-new',
  //   background: '#03A9F4' // Light Blue
  // },
  // {
  //   title: 'Strapi',
  //   subject: 'strapi',
  //   path: 'http://localhost:1337',
  //   icon: 'mdi-open-in-new',
  //   background: '#2F2E8B' // Strapi Blue
  // }
])

onMounted(() => {
  try {
    routes.value = menu.value.filter(item => $ability.can('read', item.subject));
  } catch (err) {
    console.error(err);
  }
})
</script>