<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('sites.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage" :items-length="total"
          :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getSite(item.id)"></v-btn>
            <span class="mx-2"></span>
            <v-btn class="my-2 bg-red" size="small" icon="mdi-trash-can"
              @click="form.id = item.id; deleteDialog = true"></v-btn>
          </template>
        </v-data-table-server>
      </v-card-text>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('sites.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="createSite">
          <v-row>
            <v-col cols="12">
              <v-radio-group v-model="companyType" :label="$t('sites.create.companyType')" hide-details="auto" inline>
                <v-radio :label="$t('distributors.title', 2)" value="distributors"></v-radio>
                <v-radio :label="$t('clients.title', 2)" value="clients"></v-radio>
              </v-radio-group>
            </v-col>
            <v-col cols="12">
              <v-select v-model="companyId"
                :label="companyType === 'distributors' ? $t('distributors.title') : $t('clients.title')"
                :items="companies" item-title="name" item-value="id" hide-details="auto" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="countryId" :label="$t('countries')" :items="countries" item-title="name"
                item-value="id" hide-details="auto" @update:search="getCountries" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="stateId" :label="$t('states')" :items="states" item-title="name" item-value="id"
                hide-details="auto" @update:search="getStates" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="cityId" :label="$t('cities')" :items="cities" item-title="name" item-value="id"
                hide-details="auto" @update:search="getCities" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.description" hide-details="auto" :label="$t('sites.address')"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('sites.name')"></v-text-field>
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
          {{ $t('sites.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateSite">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('sites.name')"></v-text-field>
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
  <v-dialog v-model="searchDialog" max-width="500">
    <v-card>
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
const companyType = ref('distributors');
const companyId = ref('');
const companies = ref([]);
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
const form = ref({
  cityId: '',
  description: '',
  name: ''
})

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
    await getCompanies();
    await getCountries();
  }
})

watch(companyType, async (val) => {
  if (val) await getCompanies();
})

watch(companyId, async (val) => {
  if (val) {
    if (companyType.value === 'distributors') {
      form.value.distributorId = val;
    } else {
      form.value.clientId = val;
    }
  }
})

watch(countryId, async (val) => {
  if (val) await getStates();
})

watch(stateId, async (val) => {
  if (val) await getCities();
})

watch(cityId, async (val) => {
  if (val) form.value.cityId = val;
})

watch(page, async () => {
  await getSites();
})

watch(perPage, async () => {
  await getSites();
})

onBeforeMount(async () => {
  await getSites();
})

const getCompanies = async () => {
  try {
    const data = await $fetch(`/api/${companyType.value}/`, {
      query: {
        search: '',
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    companies.value = data.items
  } catch (err) {
    console.log(err);
  }
}

const getCountries = async (search) => {
  try {
    const data = await $fetch(`/api/locations/countries`, {
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
    const data = await $fetch(`/api/locations/states/${countryId.value}`, {
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
    const data = await $fetch(`/api/locations/cities/${stateId.value}`, {
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
    const data = await $fetch('/api/sites/', {
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
    const site = await $fetch(`/api/sites/${id}`, {
      method: 'GET'
    })
    form.value = site
    updateDialog.value = true
  } catch (err) {
    console.log(err)
  }
}

const createSite = async () => {
  try {
    const response = await $fetch('/api/sites/', {
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
    const response = await $fetch(`/api/sites/${form.value.id}`, {
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
  const response = await $fetch(`/api/sites/${form.value.id}`, {
    method: 'DELETE'
  })
  await getSites()
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

</script>
