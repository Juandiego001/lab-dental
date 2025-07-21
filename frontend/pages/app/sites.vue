<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('sites.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <v-btn v-if="$ability.can('update', 'sites')" class="my-2 bg-primary" size="small" icon="mdi-pencil"
              @click="getSite(item.id)"></v-btn>
            <span class="mx-2"></span>
            <v-btn v-if="$ability.can('delete', 'sites')" class="my-2 bg-red" size="small" icon="mdi-trash-can"
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
          {{ $t('sites.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createSite">
          <v-row>
            <v-col cols="12">
              <v-radio-group v-model="form.companyType" :label="$t('sites.create.companyType')" hide-details="auto"
                inline>
                <v-radio :label="$t('distributors.title', 2)" value="distributors"></v-radio>
                <v-radio :label="$t('clients.title', 2)" value="clients"></v-radio>
              </v-radio-group>
            </v-col>
            <template v-if="isAdmin && form.companyType === 'distributors'">
              <v-col cols="12">
                <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                  item-title="name" item-value="id" hide-details="auto" clearable @update:search="getDistributors"
                  :rules="[distributorRequired]" />
              </v-col>
            </template>
            <template v-else-if="form.companyType === 'clients'">
              <v-col cols="12">
                <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                  item-value="id" hide-details="auto" clearable @update:search="getClients" :rules="[clientRequired]" />
              </v-col>
            </template>
            <v-col cols="12">
              <v-autocomplete v-model="form.countryId" :label="$t('countries')" :items="countries" item-title="name"
                item-value="id" hide-details="auto" @update:search="getCountries" clearable
                :rules="[countryRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.stateId" :label="$t('states')" :items="states" item-title="name"
                item-value="id" hide-details="auto" @update:search="getStates" clearable :readonly="!form.countryId"
                :rules="[stateRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.cityId" :label="$t('cities')" :items="cities" item-title="name"
                item-value="id" hide-details="auto" @update:search="getCities" :readonly="!form.stateId"
                :rules="[cityRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.description" hide-details="auto" :label="$t('sites.address')"
                :rules="[addressRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('sites.name')"
                :rules="[nameRequired]"></v-text-field>
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
          {{ $t('sites.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateSite">
          <v-row>
            <v-col cols="12">
              <v-radio-group v-model="form.companyType" :label="$t('sites.create.companyType')" hide-details="auto"
                inline>
                <v-radio :label="$t('distributors.title', 2)" value="distributors"></v-radio>
                <v-radio :label="$t('clients.title', 2)" value="clients"></v-radio>
              </v-radio-group>
            </v-col>
            <template v-if="isAdmin && form.companyType === 'distributors'">
              <v-col cols="12">
                <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                  item-title="name" item-value="id" hide-details="auto" clearable @update:search="getDistributors"
                  :rules="[distributorRequired]" />
              </v-col>
            </template>
            <template v-else-if="form.companyType === 'clients'">
              <v-col cols="12">
                <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                  item-value="id" hide-details="auto" clearable @update:search="getClients" :rules="[clientRequired]" />
              </v-col>
            </template>
            <v-col cols="12">
              <v-autocomplete v-model="form.countryId" :label="$t('countries')" :items="countries" item-title="name"
                item-value="id" hide-details="auto" @update:search="getCountries" clearable
                :rules="[countryRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.stateId" :label="$t('states')" :items="states" item-title="name"
                item-value="id" hide-details="auto" @update:search="getStates" clearable :readonly="!form.countryId"
                :rules="[stateRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.cityId" :label="$t('cities')" :items="cities" item-title="name"
                item-value="id" hide-details="auto" @update:search="getCities" :readonly="!form.stateId"
                :rules="[cityRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.description" hide-details="auto" :label="$t('sites.address')"
                :rules="[addressRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('sites.name')"
                :rules="[nameRequired]"></v-text-field>
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
          {{ $t('sites.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('sites.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2"></span>
        <v-btn @click="deleteSite" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('sites.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <p class="text-subtitle-2 pb-2">{{ $t('sites.search.message') }}</p>
        <v-form @submit.prevent="doSearch">
          <v-row no-gutters="">
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('sites.search.fields')" hide-details="auto"
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
const { $ability } = useNuxtApp();
const { profile } = useProfile();
const { t } = useI18n();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('sites.title', 2)}`
})

const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)
const items = ref([]);
const distributors = ref([]);
const clients = ref([]);
const countries = ref([]);
const states = ref([]);
const cities = ref([]);
const countryId = ref('');
const stateId = ref('');
const cityId = ref('');
const search = ref('');
const page = ref(1);
const perPage = ref(15);
const total = ref(15);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref();
const updateForm = ref();
const form = ref({
  companyType: 'distributors',
  distributorId: null,
  clientId: null,
  distributorName: '',
  clientName: '',
  cityId: '',
  cityName: '',
  stateId: '',
  stateName: '',
  countryId: '',
  countryName: '',
  addressId: '',
  description: '',
  name: ''
})

const isAdmin = computed(() => profile.value.role === 'ADMIN');

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: 'Id', key: 'id', sortable: false },
  { title: t('sites.name'), key: 'name', sortable: false },
  { title: t('sites.distributorClient'), key: 'distributorClient', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (val) {
    if (isAdmin.value) await getDistributors();
    await getClients();
    await getCountries();
  } else {
    createForm.value.reset();
    resetForm();
  }
})

watch(updateDialog, async (val) => {
  if (val) {
    if (isAdmin.value) await getDistributors(form.value.distributorName);
    await getClients(form.value.clientName);
    await getCountries(form.value.countryName);
  } else {
    updateForm.value.reset();
    resetForm();
  }
})

watch(() => form.value.countryId, async (val) => {
  if (val) {
    if (updateDialog.value || createDialog.value) await getStates();
    else await getStates(form.value.stateName);
    nextTick(() => {
      if (form.value.stateId && !(states.value.map(e => e.id)).includes(form.value.stateId)) {
        form.value.stateId = '';
        form.value.stateName = '';
      }
    })
  }
  else { form.value.stateId = ''; form.value.stateName = '' }
})

watch(() => form.value.stateId, async (val) => {
  if (val) {
    if (updateDialog.value || createDialog.value) await getCities();
    else await getCities(form.value.cityName);
    nextTick(() => {
      if (form.value.cityId && !(cities.value.map(e => e.id)).includes(form.value.cityId)) {
        form.value.cityId = '';
        form.value.cityName = '';
      }
    })
  }
  else { form.value.cityId = ''; form.value.cityName = ''; }
})

watch(page, async () => {
  await getSites();
})

watch(perPage, async () => {
  await getSites();
})

onBeforeMount(async () => {
  if (!$ability.can('read', 'sites')) {
    navigateTo(history.state?.back || '/login');
    return;
  }
  await getSites();
})

const resetForm = () => {
  countryId.value = ''
  stateId.value = ''
  cityId.value = ''
  form.value = {
    companyType: 'distributors',
    distributorId: null,
    clientId: null,
    cityId: '',
    cityName: '',
    stateId: '',
    stateName: '',
    countryId: '',
    countryName: '',
    addressId: '',
    description: '',
    name: ''
  }
}

const getDistributors = async (search) => {
  try {
    const data = await $api(`/api/distributors/`, {
      query: {
        search,
        page: 1,
        perPage: 15
      },
      method: 'GET'
    })
    distributors.value = data.items
  } catch (err) {
    console.log(err);
  }
}

const getClients = async (search) => {
  try {
    const data = await $api(`/api/clients/`, {
      query: {
        search,
        page: 1,
        perPage: 15
      },
      method: 'GET'
    })
    clients.value = data.items
  } catch (err) {
    console.log(err);
  }
}

const getCountries = async (search) => {
  try {
    const data = await $api(`/api/locations/countries`, {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    countries.value = data.items
  } catch (err) {
    console.log(err);
  }
}

const getStates = async (search) => {
  try {
    if (!form.value.countryId) return;
    const data = await $api(`/api/locations/states/${form.value.countryId}`, {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    states.value = data.items
  } catch (err) {
    console.log(err);
  }
}

const getCities = async (search) => {
  try {
    if (!form.value.stateId) return;
    const data = await $api(`/api/locations/cities/${form.value.stateId}`, {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    cities.value = data.items
  } catch (err) {
    console.log(err);
  }
}

const getSites = async () => {
  try {
    const data = await $api('/api/sites/', {
      query: {
        search: search.value,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    items.value = data.items
    total.value = data.total
  } catch (err) {
    console.log(err)
  }
}

const getSite = async (id) => {
  try {
    const site = await $api(`/api/sites/${id}`, {
      method: 'GET'
    })
    form.value = site
    nextTick(() => updateDialog.value = true);
  } catch (err) {
    console.log(err)
  }
}

const createSite = async () => {
  try {
    if (!createModel.value) return;
    const response = await $api('/api/sites/', {
      method: 'POST',
      body: form.value
    })
    await getSites()
    createDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

const updateSite = async () => {
  try {
    if (!updateModel.value) return;
    const response = await $api(`/api/sites/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    await getSites()
    updateDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

const deleteSite = async () => {
  const response = await $api(`/api/sites/${form.value.id}`, {
    method: 'DELETE'
  })
  await getSites()
  resetForm()
  deleteDialog.value = false
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getSites()
    searchDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

// Rules
const distributorRequired = (v) => !!v || t('sites.rules.distributorRequired');
const clientRequired = (v) => !!v || t('sites.rules.clientRequired');
const countryRequired = (v) => !!v || t('sites.rules.countryRequired');
const stateRequired = (v) => !!v || t('sites.rules.stateRequired');
const cityRequired = (v) => !!v || t('sites.rules.cityRequired');
const addressRequired = (v) => !!v || t('sites.rules.addressRequired');
const nameRequired = (v) => !!v || t('sites.rules.nameRequired');

</script>
