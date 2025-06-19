<template>
    <v-navigation-drawer v-model="drawer" class="bg-primary" location="left">
        <v-list-item>
            <v-list-item-title>
                <NuxtLink to="/app" class="text-white text-decoration-none">
                    <v-img width="100" height="30" class="mx-auto" src="/public/snapon_navbar.svg"></v-img>
                </NuxtLink>
            </v-list-item-title>
        </v-list-item>
        <v-divider></v-divider>

        <template v-for="route in routes">
            <v-list-item v-if="!['forums', 'strapi'].includes(route.subject)" link :to="route.path" :title="route.title" :append-icon="route.icon"></v-list-item>
            <v-list-item v-if="['forums', 'strapi'].includes(route.subject)" link :href="route.path" :title="route.title" :append-icon="route.icon"></v-list-item>
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
        <v-spacer></v-spacer>
        <template v-if="$vuetify.display.mdAndUp">
            <v-btn class="me-2" icon="mdi-plus" size="small" variant="text" @click="createDialog = !createDialog"></v-btn>
            <v-btn class="me-2" icon="mdi-magnify" size="small" variant="text" @click="searchDialog = !searchDialog"></v-btn>
        </template>
        <v-btn icon="mdi-dots-vertical" size="small" variant="text"></v-btn>
    </v-app-bar>
</template>

<script setup>
import { toRefs } from 'vue'
import { searchMixin } from '~/mixins/searchMixin'
import { createMixin } from '~/mixins/createMixin'

const { $ability } = useNuxtApp();
const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)

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
        subject: 'distributors',
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
    {
        title: 'Parts',
        subject: 'equipments',
        path: '/app/parts',
        icon: 'mdi-nut'
    },
    {
        title: 'Installations',
        subject: 'installations',
        path: '/app/installations',
        icon: 'mdi-train-car-flatbed-car'
    },
    {
        title: 'Reasons',
        subject: 'warranties',
        path: '/app/reasons',
        icon: 'mdi-file-cancel'
    },
    {
        title: 'Warranties',
        subject: 'warranties',
        path: '/app/warranties',
        icon: 'mdi-certificate'
    },
    {
        title: 'Manuals',
        subject: 'manuals',
        path: '/app/manuals',
        icon: 'mdi-book-cog'
        
    },
    {
        title: 'Lists',
        subject: 'zones',
        path: '/app/lists',
        icon: 'mdi-office-building-cog-outline'
    },
    {
        title: 'Configuration',
        subject: 'configuration',
        path: '/app/configuration',
        icon: 'mdi-cog'

    },
    {
        title: 'Forums',
        subject: 'forums',
        path: 'http://192.168.0.104:4200',
        icon: 'mdi-open-in-new'
    },
    {
        title: 'Strapi',
        subject: 'strapi',
        path: 'http://localhost:1337',
        icon: 'mdi-open-in-new'
    }
])


onMounted(() => {
    try {
        routes.value = menu.value.filter(item => $ability.can('read', item.subject));
    } catch (err) {
        console.error(err);
    }
})
</script>