<template>
  <v-navigation-drawer v-model="drawer" class="bg-primary" location="left">
    <v-list-item>
      <v-list-item-title class="py-3">
        <NuxtLink to="/app" class="text-white text-decoration-none">
          <v-img width="100" height="25" class="mx-auto" src="/public/soe_navbar.png"></v-img>
        </NuxtLink>
      </v-list-item-title>
    </v-list-item>
    <v-divider></v-divider>

    <template v-for="route in routes">
      <v-list-item v-if="!['forums', 'strapi'].includes(route.subject)" link :to="route.path" :title="route.title"
        :append-icon="route.icon"></v-list-item>
      <v-list-item v-if="['forums', 'strapi'].includes(route.subject)" link :href="route.path" :title="route.title"
        :append-icon="route.icon"></v-list-item>
    </template>

    <template v-slot:append>
      <div class="pa-2">
        <v-btn class="bg-primary" block variant="text" @click="navigateTo('/')">
          <v-icon icon="mdi-logout" class="me-2"></v-icon>
          Logout
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>

  <v-app-bar color="primary">
    <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    <v-toolbar-title>SOE Latam</v-toolbar-title>
    <v-spacer />
  </v-app-bar>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const module = ref('');
const { $ability } = useNuxtApp();
const routes = ref([])
const drawer = ref(true);
const menu = ref([

  {
    title: 'Distributors',
    subject: 'distributors',
    path: '/app/distributors',
    icon: 'mdi-domain'
  },
  {
    title: 'Clients',
    subject: 'clients',
    path: '/app/clients',
    icon: 'mdi-account-tie'
  },
  {
    title: 'Sites',
    subject: 'sites',
    path: '/app/sites',
    icon: 'mdi-fireplace-off'
  },
  {
    title: 'Users',
    subject: 'users',
    path: '/app/users',
    icon: 'mdi-account'

  },
  {
    title: 'Groups',
    subject: 'groups',
    path: '/app/groups',
    icon: 'mdi-account-group'

  },
  {
    title: 'Brands',
    subject: 'brands',
    path: '/app/brands',
    icon: 'mdi-shield-car'
  },
  {
    title: 'Categories',
    subject: 'categories',
    path: '/app/categories',
    icon: 'mdi-shape-outline'
  },
  {
    title: 'Equipments',
    subject: 'equipments',
    path: '/app/equipments',
    icon: 'mdi-car-cog'
  },
  // {
  //   title: 'Parts',
  //   subject: 'parts',
  //   path: '/app/parts',
  //   icon: 'mdi-nut'
  // },
  {
    title: 'Installations',
    subject: 'installations',
    path: '/app/installations',
    icon: 'mdi-train-car-flatbed-car'
  },
  // {
  //   title: 'Reasons',
  //   subject: 'reasons',
  //   path: '/app/reasons',
  //   icon: 'mdi-file-cancel'
  // },
  // {
  //   title: 'Warranties',
  //   subject: 'warranties',
  //   path: '/app/warranties',
  //   icon: 'mdi-certificate'
  // },
  // {
  //   title: 'Manuals',
  //   subject: 'manuals',
  //   path: '/app/manuals',
  //   icon: 'mdi-book-cog'

  // },
  {
    title: 'Lists',
    subject: 'lists',
    path: '/app/lists',
    icon: 'mdi-office-building-cog-outline'
  },
  // {
  //   title: 'Configuration',
  //   subject: 'configuration',
  //   path: '/app/configuration',
  //   icon: 'mdi-cog'

  // },
  // {
  //   title: 'Forums',
  //   subject: 'forums',
  //   path: 'http://192.168.0.104:4200',
  //   icon: 'mdi-open-in-new'
  // },
  // {
  //   title: 'Strapi',
  //   subject: 'strapi',
  //   path: 'http://localhost:1337',
  //   icon: 'mdi-open-in-new'
  // }
])

watch(() => route.path, (newPath) => {
  if (newPath.includes('/app/')) {
    module.value = newPath.split('/app/')[1];
  }
},
  { immediate: true }
);

onMounted(() => {
  try {
    routes.value = menu.value.filter(item => $ability.can('read', item.subject));
  } catch (err) {
    console.error(err);
  }
})
</script>