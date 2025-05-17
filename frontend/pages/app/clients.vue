<template>
    <v-container fluid class="fill-height align-start">
        <v-card width="100%" flat>
            <v-card-title>{{ $t('clients.title', 2) }}</v-card-title>
            <v-card-text>
                <v-data-table :items="items" :headers="headers" :items-per-page="perPage"
                    @update:itemsPerPage="v => perPage = v">

                    <template v-slot:item.option="{ item }">
                        <v-btn class="my-2 bg-primary" icon="mdi-pencil" @click="getClient(item.id)"></v-btn>
                        <span class="mx-2"></span>
                        <v-btn class="my-2 bg-red" icon="mdi-trash-can"
                            @click="form.id = item.id; deleteDialog = true"></v-btn>
                    </template>
                </v-data-table>
            </v-card-text>
        </v-card>
    </v-container>

    <!-- Create Dialog -->
    <v-dialog v-model="createDialog" max-width="500">
        <v-card>
            <v-card-title class="bg-primary">
                <v-row no-gutters align="center">
                    {{ $t('clients.create.title') }}
                    <v-spacer></v-spacer>
                    <v-btn class="bg-primary" icon="mdi-close" @click="createDialog = false"></v-btn>
                </v-row>
            </v-card-title>
            <v-card-text>
                <v-form @submit.prevent="createClient">
                    <v-row>
                        <v-col cols="12">
                            <v-text-field v-model="form.name" hide-details="auto" :label="$t('clients.name')"></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field v-model="form.phone" hide-details="auto" :label="$t('clients.phone')"></v-text-field>
                        </v-col>
                        <v-col class="text-end">
                            <v-btn variant="outlined" @click="updateDialog = false">{{ $t('cancel') }}</v-btn>
                            <span class="mx-1"></span>
                            <v-btn type="submit" class="bg-primary">{{ $t('confirm') }}</v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>

    <!-- Update Dialog -->
    <v-dialog v-model="updateDialog" max-width="500">
        <v-card>
            <v-card-title class="bg-primary">
                <v-row no-gutters align="center">
                    {{ $t('clients.update.title') }}
                    <v-spacer></v-spacer>
                    <v-btn class="bg-primary" icon="mdi-close" @click="updateDialog = false"></v-btn>
                </v-row>
            </v-card-title>
            <v-card-text>
                <v-form @submit.prevent="updateClient">
                    <v-row>
                        <v-col cols="12">
                            <v-text-field v-model="form.name" hide-details="auto" :label="$t('clients.name')"></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field v-model="form.phone" hide-details="auto" :label="$t('clients.phone')"></v-text-field>
                        </v-col>
                        <v-col class="text-end">
                            <v-btn variant="outlined" @click="updateDialog = false">{{ $t('cancel') }}</v-btn>
                            <span class="mx-1"></span>
                            <v-btn type="submit" class="bg-primary">{{ $t('confirm') }}</v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>

    <!-- Delete Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500">
        <v-card>
            <v-card-title class="bg-primary">
                <v-row no-gutters align="center">
                    {{ $t('clients.delete.title') }}
                    <v-spacer></v-spacer>
                    <v-btn class="bg-primary" icon="mdi-close" @click="deleteDialog = false"></v-btn>
                </v-row>
            </v-card-title>
            <v-card-text class="text-center py-6">
                <p class="text-subtitle-1 mb-6 text-center">{{ $t('clients.delete.message') }}</p>
                <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
                <span class="mx-2"></span>
                <v-btn @click="deleteClient" class="bg-red">{{ $t('confirm') }}</v-btn>
            </v-card-text>
        </v-card>
    </v-dialog>

    <!-- Search Dialog -->
    <v-dialog v-model="searchDialog" max-width="500">
        <v-card>
            <v-card-title class="bg-primary">
                <v-row no-gutters align="center">
                    {{ $t('clients.search.title') }}
                    <v-spacer></v-spacer>
                    <v-btn class="bg-primary" icon="mdi-close" @click="searchDialog = false"></v-btn>
                </v-row>
            </v-card-title>
            <v-card-text>
                <p class="text-subtitle-2 pb-2">{{ $t('clients.search.message') }}</p>
                <v-form @submit.prevent="doSearch">
                    <v-row no-gutters="">
                        <v-col cols="12">
                            <v-text-field v-model="search" :label="$t('clients.search.fields')" hide-details="auto"
                                prepend-inner-icon="mdi-magnify" clearable></v-text-field>
                        </v-col>
                        <v-col class="text-end mt-4" cols="12">
                            <v-btn class="bg-primary" type="submit">{{ $t('search') }}</v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onBeforeMount, } from 'vue'
import { toRefs } from 'vue'
import { searchMixin } from '~/mixins/searchMixin'
import { createMixin } from '~/mixins/createMixin'
import { useI18n } from 'vue-i18n'
const { t } = useI18n();

definePageMeta({
    layout: 'app',
    middleware: ['private']
})

useHead({
    title: `SOE Latam | ${t('clients.title', 2)}`
})

const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)
const items = ref([]);
const search = ref('');
const page = ref(1);
const perPage = ref(15);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const form = ref({
    id: '',
    name: '',
    phone: '',
    status: '',
    created_at: '',
    updated_at: ''
})


const headers = computed(() => [
    { title: 'Id', key: 'id' },
    { title: t('clients.name'), key: 'name' },
    { title: t('clients.phone'), key: 'phone' },
    { title: t('options'), key: 'option', align: 'center' }
])

// watch(perPage, async (val) => {
//     await getClients();
// })

onBeforeMount(async () => {
    await getClients();
})

const getClients = async () => {
    try {
        const data = await $fetch('/api/clients/', {
            query: {
                search: search.value,
                page: page.value,
                perPage: perPage.value
            },
            method: 'GET'
        })
        console.log('ITEMS: ', data.items);
        items.value = data.items
    } catch (err) {
        console.log(err)
    }
}

const getClient = async (id) => {
    try {
        const user = await $fetch(`/api/clients/${id}`, {
            method: 'GET'
        })
        form.value = user
        updateDialog.value = true
    } catch (err) {
        console.log(err)
    }
}

const createClient = async () => {
    try {
        const response = await $fetch('/api/clients/', {
            method: 'POST',
            body: form.value
        })
        await getClients()
        createDialog.value = false
    } catch (err) {
        console.log(err)
    }
}

const updateClient = async () => {
    try {
        const response = await $fetch(`/api/clients/${form.value.id}`, {
            method: 'PUT',
            body: form.value
        })
        await getClients()
        updateDialog.value = false
    } catch (err) {
        console.log(err)
    }
}

const deleteClient = async () => {
    const response = await $fetch(`/api/clients/${form.value.id}`, {
        method: 'DELETE'
    })
    await getClients()
    deleteDialog.value = false
}

const doSearch = async () => {
    try {
        page.value = 1
        perPage.value = 15
        await getClients()
        searchDialog.value = false
    } catch (err) {
        console.log(err)
    }
}

</script>
