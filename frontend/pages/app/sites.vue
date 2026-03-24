<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('sites.title', 2) }}</p>
        <div>
          <client-only>
            <v-btn v-if="$ability.can('create', 'sites')" class="me-2" icon="mdi-plus" size="small" variant="text"
              @click="createDialog = !createDialog" />
            <v-btn v-if="$ability.can('read', 'sites')" class="me-2" icon="mdi-magnify" size="small" variant="text"
              @click="searchDialog = !searchDialog" />
          </client-only>
        </div>
      </v-card-title>
      <v-card-text>
        <client-only>
          <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
            :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" :loading="loading">
            <template v-slot:item.siteType="{ item }">
              <p class="d-inline-block py-1 px-2 rounded-lg text-caption"
                :class="item.distributorId ? 'bg-primary' : 'bg-secondary'">
                {{ item.distributorId ? $t('distributors.title') : $t('clients.title') }}
              </p>
            </template>
            <template v-slot:item.option="{ item }">
              <div class="d-flex align-center justify-center ga-2">
                <v-btn v-if="$ability.can('update', 'sites')" class="my-2 bg-primary" size="small" icon="mdi-pencil"
                  @click="getSite(item.id)" />
                <v-btn v-if="$ability.can('delete', 'sites')" class="my-2 bg-red" size="small" icon="mdi-trash-can"
                  @click="form.id = item.id; deleteDialog = true" />
              </div>
            </template>
          </v-data-table-server>
        </client-only>
      </v-card-text>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('sites.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createSite">
          <v-row dense>
            <v-col cols="12">
              <v-radio-group v-model="form.companyType" :label="$t('sites.create.companyType')" hide-details="auto"
                inline>
                <v-radio :label="$t('distributors.title', 2)" value="distributors" />
                <v-radio :label="$t('clients.title', 2)" value="clients" />
              </v-radio-group>
            </v-col>
            <template v-if="isAdmin && form.companyType === 'distributors'">
              <v-col cols="12">
                <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                  item-title="name" item-value="id" hide-details="auto" clearable :rules="[distributorRequired]"
                  @update:search="(name) => {
                    if (!createDialog) return;
                    getDistributors({ distributorsIds: [form.distributorId], name })
                  }" />
              </v-col>
            </template>
            <template v-else-if="form.companyType === 'clients'">
              <v-col cols="12">
                <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                  item-value="id" hide-details="auto" clearable :rules="[clientRequired]" @update:search="(name) => {
                    if (!createDialog) return;
                    getClients({ clientId: form.clientId, name })
                  }" />
              </v-col>
            </template>
            <v-col cols="12">
              <v-autocomplete v-model="form.countryId" :label="$t('countries')" :items="countries" item-title="name"
                item-value="id" hide-details="auto" clearable :rules="[countryRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getCountries(name);
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.stateId" :label="$t('states')" :items="states" item-title="name"
                item-value="id" hide-details="auto" clearable :readonly="!form.countryId" :rules="[stateRequired]"
                @update:search="(name) => {
                  if (!createDialog) return;
                  getStates(name);
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.cityId" :label="$t('cities')" :items="cities" item-title="name"
                item-value="id" hide-details="auto" :readonly="!form.stateId" @update:search="(name) => {
                  if (!createDialog) return;
                  getCities(name);
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.description" hide-details="auto" :label="$t('sites.address')"
                :rules="[addressRequired]" counter="255" maxlength="255" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('sites.name')" :rules="[nameRequired]"
                counter="50" maxlength="50" />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="createDialog = false" @mousedown.prevent :disabled="loading">{{
                $t('cancel') }}</v-btn>
              <span class="mx-1"></span>
              <v-btn type="submit" class="bg-primary" @mousedown.prevent :loading="loading">{{ $t('confirm') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Update Dialog -->
  <v-dialog v-model="updateDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('sites.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateSite">
          <v-row dense>
            <v-col cols="12">
              <p class="text-body-2 font-bold text-primary text-decoration-underline">
                {{ form.companyType === 'distributors' ? $t('sites.distributorsSite') : $t('sites.clientsSite') }}
              </p>
            </v-col>
            <template v-if="isAdmin && form.companyType === 'distributors'">
              <v-col cols="12">
                <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                  item-title="name" item-value="id" hide-details="auto" clearable :rules="[distributorRequired]"
                  @update:search="(name) => {
                    if (!updateDialog) return;
                    getDistributors({ distributorsIds: [form.distributorId], name })
                  }" />
              </v-col>
            </template>
            <template v-else-if="form.companyType === 'clients'">
              <v-col cols="12">
                <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                  item-value="id" hide-details="auto" clearable :rules="[clientRequired]" @update:search="(name) => {
                    if (!updateDialog) return;
                    getClients({ clientId: form.clientId, name })
                  }" />
              </v-col>
            </template>
            <v-col cols="12">
              <v-autocomplete v-model="form.countryId" :label="$t('countries')" :items="countries" item-title="name"
                item-value="id" hide-details="auto" clearable :rules="[countryRequired]" @update:search="(name) => {
                  if (!updateDialog) return;
                  getCountries(name);
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.stateId" :label="$t('states')" :items="states" item-title="name"
                item-value="id" hide-details="auto" clearable :readonly="!form.countryId" :rules="[stateRequired]"
                @update:search="(name) => {
                  if (!updateDialog) return;
                  getStates(name);
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.cityId" :label="$t('cities')" :items="cities" item-title="name"
                item-value="id" hide-details="auto" :readonly="!form.stateId" @update:search="(name) => {
                  if (!updateDialog) return;
                  getCities(name);
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.description" hide-details="auto" :label="$t('sites.address')"
                :rules="[addressRequired]" counter="255" maxlength="255" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('sites.name')" :rules="[nameRequired]"
                counter="50" maxlength="50" />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="updateDialog = false" @mousedown.prevent :disabled="loading">{{
                $t('cancel') }}</v-btn>
              <span class="mx-1"></span>
              <v-btn type="submit" class="bg-primary" @mousedown.prevent :loading="loading">{{ $t('confirm') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Delete Dialog -->
  <v-dialog v-model="deleteDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('sites.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('sites.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined" :disabled="loading">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteSite" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="700" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('sites.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchSites(1, 15);
          searchDialog = false;
        }">
          <v-row dense>
            <v-col cols="6">
              <p class="text-body-2 text-primary">{{ $t('distributors.title') }}</p>
            </v-col>
            <v-col cols="6">
              <p class="text-body-2 text-primary">{{ $t('clients.title') }}</p>
            </v-col>

            <!-- Distributors -->
            <v-col cols="6">
              <v-autocomplete v-model="searchForm.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" clearable
                @update:search="(name) => getDistributors({ distributorsIds: [searchForm.distributorId], name })" />
            </v-col>

            <!-- Clients -->
            <v-col cols="6">
              <v-autocomplete v-model="searchForm.clientId" :label="$t('clients.title')" :items="clients"
                item-title="name" item-value="id" hide-details="auto" clearable
                @update:search="(name) => getClients({ clientId: searchForm.clientId, name })" />
            </v-col>

            <!-- Sites -->
            <v-col class="pt-4" cols="12">
              <p class="text-body-2 text-primary">{{ $t('sites.title', 2) }}</p>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="searchForm.name" :label="$t('sites.name')" hide-details="auto" clearable />
            </v-col>

            <!-- Search Button -->
            <v-col class="text-end" cols="12">
              <v-btn class="bg-primary" type="submit" @mousedown.prevent :loading="loading">{{ $t('search') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onBeforeMount, } from 'vue'
import { useI18n } from 'vue-i18n'

const { back } = useBack()
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { isAdmin } = useProfile();
const { t } = useI18n();
const { items: distributors, getDistributors } = useDistributors();
const { items: clients, getClients } = useClients();
const { items, total, getSites } = useSites();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('sites.title', 2)}`
})

const loading = ref(false);
const searchDialog = ref(false);
const createDialog = ref(false);
const countries = ref([]);
const states = ref([]);
const cities = ref([]);
const page = ref(1);
const perPage = ref(15);
const sortBy = ref(null);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref();
const updateForm = ref();
const form = ref({
  companyType: 'distributors',
  distributorName: '',
  clientName: '',
  countryId: null,
  countryName: '',
  addressId: null,
  description: '',
  name: ''
})
const searchForm = ref({
  distributorId: null,
  clientId: null,
  name: '',
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: t('sites.name'), key: 'name' },
  { title: t('sites.distributorClient'), key: 'distributorClient', align: 'center' },
  { key: 'siteType', align: 'center', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
  if (isAdmin.value) await getDistributors({});
  await getClients({});
  await getCountries();
})

watch(updateDialog, async (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
    return;
  }
  if (isAdmin.value) await getDistributors({ distributorsIds: [form.value.distributorId], name: form.value.distributorName });
  await getClients({ clientId: form.value.clientId, name: form.value.clientName });
  await getCountries(form.value.countryName);
})

watch(searchDialog, async (val) => {
  if (!val) return;
  await getDistributors({ distributorsIds: [searchForm.value.distributorId] });
  await getClients({ clientId: searchForm.value.clientId });
})

watch(() => form.value.companyType, (val) => {
  if (val === 'clients') {
    delete form.value.distributorName;
    delete form.value.distributorId;
  }

  if (val === 'distributors') {
    delete form.value.clientName;
    delete form.value.clientId;
  }
})

watch(() => form.value.countryId, async (val) => {
  if (!val) {
    form.value.stateId = null;
    form.value.stateName = null
    return;
  }

  if (updateDialog.value || createDialog.value) await getStates();
  else await getStates(form.value.stateName);

  nextTick(() => {
    if (form.value.stateId && !(states.value.map(e => e.id)).includes(form.value.stateId)) {
      form.value.stateId = null;
      form.value.stateName = null;
    }
  })
})

watch(() => form.value.stateId, async (val) => {
  if (!val) {
    form.value.cityId = null;
    form.value.cityName = null;
    return;
  }

  if (updateDialog.value || createDialog.value) await getCities();
  else await getCities(form.value.cityName);

  nextTick(() => {
    if (form.value.cityId && !(cities.value.map(e => e.id)).includes(form.value.cityId)) {
      form.value.cityId = null;
      form.value.cityName = null;
    }
  })
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await searchSites();
})

watch(perPage, async () => {
  await searchSites();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchSites();
  }
})

onBeforeMount(async () => {
  if ($ability.can('read', 'sites')) {
    await getSites({});
    return;
  }
  back();
})

const resetForm = () => {
  form.value = {
    companyType: 'distributors',
    countryId: null,
    countryName: '',
    addressId: null,
    description: '',
    name: ''
  }
}

const searchSites = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getSites({
      distributorId: searchForm.value.distributorId,
      clientId: searchForm.value.clientId,
      name: searchForm.value.name,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value,
      sortBy: sortBy.value?.length ? sortBy.value[0] : null
    })
  } catch (err) { }
  finally {
    loading.value = false;
  }
}

const getCountries = async (name) => {
  try {
    const data = await $api(`/api/locations/countries/search`, {
      body: {
        id: form.value.countryId,
        name,
        page: 1,
        perPage: 15
      },
      method: 'POST'
    })
    countries.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getStates = async (name) => {
  try {
    if (!form.value.countryId) return;
    const data = await $api(`/api/locations/states/${form.value.countryId}/search`, {
      body: {
        id: form.value.stateId,
        name,
        page: 1,
        perPage: 15
      },
      method: 'POST'
    })
    states.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getCities = async (name) => {
  try {
    if (!form.value.stateId) return;
    const data = await $api(`/api/locations/cities/${form.value.stateId}/search`, {
      body: {
        id: form.value.cityId,
        name,
        page: 1,
        perPage: 15
      },
      method: 'POST'
    })
    cities.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getSite = async (id) => {
  try {
    const site = await $api(`/api/sites/${id}`, {
      method: 'GET'
    })
    form.value = site
    updateDialog.value = true;
  } catch (err) {
    notify(err, 'error');
  }
}

const createSite = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/sites/', {
      method: 'POST',
      body: form.value
    })
    notify(message, 'success');
    await getSites({})
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateSite = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await $api(`/api/sites/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await searchSites();
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteSite = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/sites/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await searchSites();
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

// Rules
const distributorRequired = (v) => !!v || t('sites.rules.distributorRequired');
const clientRequired = (v) => !!v || t('sites.rules.clientRequired');
const countryRequired = (v) => !!v || t('sites.rules.countryRequired');
const stateRequired = (v) => !!v || t('sites.rules.stateRequired');
const addressRequired = (v) => !!v || t('sites.rules.addressRequired');
const nameRequired = (v) => !!v || t('sites.rules.nameRequired');

</script>
