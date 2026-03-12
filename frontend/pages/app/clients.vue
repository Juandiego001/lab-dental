<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('clients.title', 2) }}</p>
        <div>
          <client-only>
            <v-btn v-if="$ability.can('create', 'clients')" class="me-2" icon="mdi-plus" size="small" variant="text"
              @click="createDialog = !createDialog" />
            <v-btn v-if="$ability.can('read', 'clients')" class="me-2" icon="mdi-magnify" size="small" variant="text"
              @click="searchDialog = !searchDialog" />
          </client-only>
        </div>
      </v-card-title>
      <v-card-text>
        <client-only>
          <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
            :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" :loading="loading">
            <template v-slot:item.option="{ item }">
              <div class="d-flex align-center justify-center ga-2">
                <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getClient(item.id);" />
                <v-btn class="my-2 bg-red" size="small" icon="mdi-trash-can"
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
          {{ $t('clients.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createClient">
          <v-row dense>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" hide-details="auto" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" :rules="[distributorRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getDistributors({ distributorsIds: [form.distributorId], name });
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('clients.name')" :rules="[nameRequired]"
                counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.phone" hide-details="auto" :label="$t('clients.phone')"
                :rules="[phoneRequired]" counter="20" maxlength="20" />
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
          {{ $t('clients.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateClient">
          <v-row dense>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" hide-details="auto" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" :rules="[distributorRequired]" @update:search="(name) => {
                  if (!updateDialog || !name) return;
                  getDistributors({ distributorsIds: [form.distributorId], name });
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('clients.name')" :rules="[nameRequired]"
                counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.phone" hide-details="auto" :label="$t('clients.phone')"
                :rules="[phoneRequired]" counter="20" maxlength="20" />
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
          {{ $t('clients.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('clients.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined" :disabled="loading">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteClient" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="700" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('clients.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchClients(1, 15);
          searchDialog = false;
        }">
          <v-row dense>
            <!-- Distributors -->
            <v-col v-if="isAdmin" cols="12">
              <p class="text-body-2 text-primary">{{ $t('distributors.title', 2) }}</p>
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="searchForm.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" clearable
                @update:search="(name) => getDistributors({ distributorsIds: [searchForm.distributorId], name })" />
            </v-col>

            <!-- Clients -->
            <v-col v-if="isAdmin" class="pt-4" cols="12">
              <p class="text-body-2 text-primary">{{ $t('clients.title', 2) }}</p>
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.name" :label="$t('clients.name')" hide-details="auto" counter="50"
                maxlength="50" clearable />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.phone" :label="$t('clients.phone')" hide-details="auto" counter="20"
                maxlength="20" clearable />
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
const { items, total, getClients } = useClients();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('clients.title', 2)}`
})

const loading = ref(false);
const searchDialog = ref(false);
const createDialog = ref(false);
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
  distributorName: '',
  name: '',
  phone: ''
})
const searchForm = ref({
  distributorName: '',
  name: '',
  phone: ''
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  if (isAdmin.value) {
    return [
      { title: t('clients.name'), key: 'name' },
      { title: t('clients.phone'), key: 'phone', align: 'center' },
      { title: t('clients.distributor'), key: 'distributorName', align: 'center' },
      { title: t('options'), key: 'option', align: 'center', sortable: false }
    ]
  }

  return [
    { title: t('clients.name'), key: 'name' },
    { title: t('clients.phone'), key: 'phone', align: 'center' },
    { title: t('options'), key: 'option', align: 'center', sortable: false }
  ]
})

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
  if (isAdmin.value) await getDistributors({});
})

watch(updateDialog, async (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
    return;
  }
  if (isAdmin.value) await getDistributors({ name: form.value.distributorName });
})

watch(searchDialog, async (val) => {
  if (!val) return;
  if (isAdmin.value) await getDistributors({ distributorsIds: [searchForm.value.distributorId] });
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await searchClients();
})

watch(perPage, async () => {
  await searchClients();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchClients();
  }
})

onBeforeMount(async () => {
  if ($ability.can('read', 'clients')) {
    await getClients({});
    return;
  }
  back();
})

const resetForm = () => {
  form.value = {
    distributorId: null,
    name: '',
    phone: ''
  }
}

const searchClients = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getClients({
      distributorId: searchForm.value.distributorId,
      name: searchForm.value.name,
      phone: searchForm.value.phone,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value,
      sortBy: sortBy.value?.length ? sortBy.value[0] : null
    })
  } catch (err) { }
  finally {
    loading.value = false;
  }
}

const getClient = async (id) => {
  try {
    const client = await $api(`/api/clients/${id}`, {
      method: 'GET'
    })
    form.value = client
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  }
}

const createClient = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/clients/', {
      method: 'POST',
      body: form.value
    })
    notify(message, 'success');
    await getClients({})
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateClient = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await $api(`/api/clients/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await searchClients();
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteClient = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/clients/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await searchClients();
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

// Rules
const distributorRequired = (v) => !!v || t('clients.rules.distributorRequired');
const nameRequired = (v) => !!v || t('clients.rules.nameRequired');
const phoneRequired = (v) => !!v || t('clients.rules.phoneRequired');

</script>
