<template>
  <v-navigation-drawer v-model="drawer" class="bg-primary" location="left">
    <v-list-item>
      <v-list-item-title class="py-3">
        <NuxtLink to="/app" class="text-white text-decoration-none">
          <v-img width="100" height="25" class="mx-auto" src="/public/soe_navbar.png" />
        </NuxtLink>
      </v-list-item-title>
    </v-list-item>

    <v-divider />

    <v-list-item link to="/app" title="Home" append-icon="mdi-home" />

    <template v-for="route in routes">
      <v-list-item v-if="!['forums', 'strapi'].includes(route.subject)" link @click="goTo(route.path)"
        :title="$t(`${route.subject}.title`, 2)" :append-icon="route.icon" />
      <v-list-item v-if="['forums', 'strapi'].includes(route.subject)" link :href="route.path"
        :title="$t(`${route.subject}.title`, 2)" :append-icon="route.icon" />
    </template>

    <template v-slot:append>
      <div class="pa-2">
        <v-btn class="bg-primary" block variant="text" @click="logout">
          <v-icon icon="mdi-logout" class="me-2" />
          {{ $t('logout') }}
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>

  <v-app-bar color="primary">
    <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer" />
    <v-toolbar-title>SOE Latam</v-toolbar-title>
    <v-spacer />

    <v-menu open-on-hover>
      <template v-slot:activator="{ props }">
        <v-btn icon v-bind="props">
          <v-avatar v-bind="props" color="primary" size="32" class="position-relative cursor-pointer">
            <v-img style v-if="profile.photo" :src="`/api/files/users/${profile.photo}`" cover>
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="grey-lighten-5" size="20" />
                </v-row>
              </template>
            </v-img>
            <v-icon v-else icon="mdi-account-circle" />
          </v-avatar>
        </v-btn>
      </template>

      <v-list density="compact" nav>
        <v-list-item density="compact" variant="flat" append-icon="mdi-account" :title="$t('profile.title')"
          @click="goTo('/app/profile')" />
        <v-list-item :title="$t('logout')" append-icon="mdi-logout" class="text-error" @click="logout" />
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script setup>
import { ref } from 'vue';

const { notify } = useSnackbar();
const { t } = useI18n();
const { $ability } = useNuxtApp();
const routes = ref([])
const drawer = ref(true);
const { profile } = useProfile();
const { abortController } = useAligners();

const menu = ref([
  {

    subject: 'distributors',
    path: '/app/distributors',
    icon: 'mdi-domain'
  },
  {

    subject: 'clients',
    path: '/app/clients',
    icon: 'mdi-account-tie'
  },
  {

    subject: 'sites',
    path: '/app/sites',
    icon: 'mdi-fireplace-off'
  },
  {

    subject: 'users',
    path: '/app/users',
    icon: 'mdi-account'

  },
  {

    subject: 'groups',
    path: '/app/groups',
    icon: 'mdi-account-group'

  },
  {

    subject: 'brands',
    path: '/app/brands',
    icon: 'mdi-shield-car'
  },
  {

    subject: 'categories',
    path: '/app/categories',
    icon: 'mdi-shape-outline'
  },
  {

    subject: 'equipments',
    path: '/app/equipments',
    icon: 'mdi-car-cog'
  },
  // {
  //   subject: 'parts',
  //   path: '/app/parts',
  //   icon: 'mdi-nut'
  // },
  {

    subject: 'installations',
    path: '/app/installations',
    icon: 'mdi-train-car-flatbed-car'
  },
  {
    subject: 'reasons',
    path: '/app/reasons',
    icon: 'mdi-file-cancel'
  },
  {
    subject: 'warranties',
    path: '/app/warranties',
    icon: 'mdi-certificate'
  },
  // {
  //   subject: 'manuals',
  //   path: '/app/manuals',
  //   icon: 'mdi-book-cog'

  // },
  {
    subject: 'lists',
    path: '/app/lists',
    icon: 'mdi-office-building-cog-outline'
  },
  {
    subject: 'aligners',
    path: '/app/aligners',
    icon: 'mdi-car-wrench'
  },
  {
    subject: 'notifications',
    path: '/app/notifications',
    icon: 'mdi-bell'
  },
  // {
  //   subject: 'configuration',
  //   path: '/app/configuration',
  //   icon: 'mdi-cog'

  // },
  // {
  //   subject: 'forums',
  //   path: 'http://192.168.0.104:4200',
  //   icon: 'mdi-open-in-new'
  // },
  // {
  //   subject: 'strapi',
  //   path: 'http://localhost:1337',
  //   icon: 'mdi-open-in-new'
  // }
])

onMounted(() => {
  try {
    routes.value = menu.value.filter(item => $ability.can('read', item.subject));
  } catch (err) { }
})

const logout = async () => {
  try {

    if (abortController.value) {
      abortController.value.abort();
    }
    const { message } = await $api('/api/users/logout', { method: 'GET' });
    await navigateTo('/');
    notify(message, 'success');
  } catch (err) {
    notify(err, 'error');
  }
}

const goTo = async (path) => {
  if (path !== '/app' && abortController.value) {
    abortController.value.abort();
  }
  await navigateTo(path);
}
</script>