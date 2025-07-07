<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('clients.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getClient(item.id)"></v-btn>
            <span class="mx-2"></span>
            <v-btn class="my-2 bg-red" size="small" icon="mdi-trash-can"
              @click="form.id = item.id; deleteDialog = true"></v-btn>
          </template>
        </v-data-table-server>
      </v-card-text>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('clients.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="createClient">
          <v-row>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" hide-details="auto" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" @update:search="getDistributors" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('clients.name')"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.phone" hide-details="auto" :label="$t('clients.phone')"></v-text-field>
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="createDialog = false">{{ $t('cancel') }}</v-btn>
              <span class="mx-1"></span>
              <v-btn type="submit" class="bg-primary">{{ $t('confirm') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Update Dialog -->
  <v-dialog v-model="updateDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('clients.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateClient">
          <v-row>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" hide-details="auto" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" @update:search="getDistributors" />
            </v-col>
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
  <v-dialog v-model="deleteDialog" max-width="500" persistent>
    <v-card tile>
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
  <v-dialog v-model="searchDialog" max-width="500" persistent>
    <v-card tile>
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
const { profile } = useProfile();
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
const distributors = ref([]);
const search = ref('');
const page = ref(1);
const perPage = ref(15);
const total = ref(15);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const form = ref({
  distributorId: '',
  distributorName: '',
  name: '',
  phone: ''
})

const isAdmin = computed(() => profile.value.role === 'ADMIN');

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  if (isAdmin.value) {
    return [
      { title: 'Id', key: 'id', sortable: false },
      { title: t('clients.name'), key: 'name', sortable: false },
      { title: t('clients.phone'), key: 'phone', sortable: false },
      { title: t('clients.distributor'), key: 'distributorName', sortable: false },
      { title: t('options'), key: 'option', align: 'center', sortable: false }
    ]
  }

  return [
    { title: 'Id', key: 'id', sortable: false },
      { title: t('clients.name'), key: 'name', sortable: false },
      { title: t('clients.phone'), key: 'phone', sortable: false },
      { title: t('options'), key: 'option', align: 'center', sortable: false }
  ]
})

watch(createDialog, async (val) => {
  if (val) { if (isAdmin.value) await getDistributors(); }
  else resetForm();
})

watch(updateDialog, async (val) => {
  if (val) { if (isAdmin.value) await getDistributors(form.value.distributorName); }
  else resetForm();
})

watch(page, async () => {
  await getClients();
})

watch(perPage, async () => {
  await getClients();
})

onBeforeMount(async () => {
  await getClients();
})

const resetForm = () => {
  form.value = {
    distributorId: null,
    name: '',
    phone: ''
  }
}

const getDistributors = async (search) => {
  try {
    const data = await $api('/api/distributors/', {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    distributors.value = data.items;
  } catch (err) {
    console.log(err);
  }
}

const getClients = async () => {
  try {
    const data = await $api('/api/clients/', {
      query: {
        search: search.value,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    items.value = data.items;
    total.value = data.total
  } catch (err) {
    console.log(err)
  }
}

const getClient = async (id) => {
  try {
    const client = await $api(`/api/clients/${id}`, {
      method: 'GET'
    })
    form.value = client
    nextTick(() => updateDialog.value = true);
  } catch (err) {
    console.log(err)
  }
}

const createClient = async () => {
  try {
    const response = await $api('/api/clients/', {
      method: 'POST',
      body: form.value
    })
    await getClients()
    createDialog.value = false
    resetForm()
  } catch (err) {
    console.log(err)
  }
}

const updateClient = async () => {
  try {
    const response = await $api(`/api/clients/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    await getClients()
    updateDialog.value = false
    resetForm()
  } catch (err) {
    console.log(err)
  }
}

const deleteClient = async () => {
  try {
    const response = await $api(`/api/clients/${form.value.id}`, {
      method: 'DELETE'
    })
    await getClients()
    deleteDialog.value = false
    resetForm()
  } catch (err) {
    console.log(err);
  }
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
