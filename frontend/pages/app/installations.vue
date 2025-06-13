<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('installations.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getInstallation(item.id)"></v-btn>
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
          {{ $t('installations.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="createInstallation">
          <v-row>
            <v-col cols="12">
              <v-autocomplete v-model="form.equipmentId" :label="$t('equipments.title')" :items="equipments"
                item-title="serial" item-value="id" hide-details="auto" @update:search="getEquipments" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                item-value="id" hide-details="auto" @update:search="getClients" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.clientSiteId" :label="`${$t('sites.title')} ${$t('clients.title')}`"
                :items="clientsSites" item-title="name" item-value="id" hide-details="auto"
                @update:search="getClientsSites" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.distributorSiteId"
                :label="`${$t('sites.title')} ${$t('distributors.title')}`" :items="distributorsSites" item-title="name"
                item-value="id" hide-details="auto" @update:search="getDistributorsSites" />
            </v-col>
            <v-col cols="12">
              <v-menu v-model="showPicker" :close-on-content-click="false" transition="scale-transition" offset-y
                full-width max-width="290px" min-width="290px">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="selectedDateText" :label="$t('installations.installedDate')" readonly hide-details="auto" v-bind="props"></v-text-field>
                </template>
                <v-date-picker v-model="selectedDate" title="" hide-header @update:model-value="showPicker=false"></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="format" hide-details="auto" :label="$t('installations.format')" />
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
          {{ $t('installations.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateUser">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.installedAt" hide-details="auto"
                :label="$t('installations.installedAt')"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.installedDate" hide-details="auto"
                :label="$t('installations.installedDate')"></v-text-field>
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
          {{ $t('installations.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('installations.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2"></span>
        <v-btn @click="deleteInstallation" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <p class="text-subtitle-2 pb-2">{{ $t('installations.search.message') }}</p>
        <v-form @submit.prevent="doSearch">
          <v-row no-gutters="">
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('installations.search.fields')" hide-details="auto"
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
import { useDate } from 'vuetify'

const { t } = useI18n();
const date = useDate();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('installations.title', 2)}`
})

const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)
const equipments = ref([]);
const clients = ref([]);
const clientsSites = ref([]);
const distributors = ref([]);
const distributorsSites = ref([]);
const items = ref([]);
const search = ref('');
const page = ref(1);
const perPage = ref(15);
const total = ref(15);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const format = ref(null);
const showPicker = ref(false);
const selectedDate = ref(null);
const selectedDateText = ref(null);
const form = ref({
  equipmentId: '',
  clientId: '',
  clientSiteId: '',
  distributorId: '',
  distributorSiteId: '',
  installedDate: null,
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: 'Id', key: 'id', sortable: false },
  { title: t('installations.installedAt'), key: 'installedAt', sortable: false },
  { title: t('installations.installedDate'), key: 'installedDate', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (val) {
    await getEquipments();
    await getClients();
    await getDistributors();
  }
})

watch(page, async () => {
  await getInstallations();
})

watch(perPage, async () => {
  await getInstallations();
})

watch(() => form.value.clientId, async (val) => {
  if (val) await getClientsSites();
})

watch(() => form.value.distributorId, async (val) => {
  if (val) await getDistributorsSites();
})

watch(selectedDate, async (val) => {
  if (val) selectedDateText.value = date.format(val, 'fullDate');
})

onBeforeMount(async () => {
  await getInstallations();
})

const getEquipments = async (search) => {
  try {
    const data = await $fetch('/api/equipments/', {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    equipments.value = data.items
  } catch (err) {
    console.log(err)
  }
}

const getClients = async (search) => {
  try {
    const data = await $fetch('/api/clients/', {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    clients.value = data.items
  } catch (err) {
    console.log(err)
  }
}

const getDistributors = async (search) => {
  try {
    const data = await $fetch('/api/distributors/', {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    distributors.value = data.items
  } catch (err) {
    console.log(err)
  }
}

const getClientsSites = async (search) => {
  try {
    const data = await $fetch(`/api/sites/clients/${form.value.clientId}`, {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    clientsSites.value = data.items
  } catch (err) {
    console.log(err)
  }
}

const getDistributorsSites = async (search) => {
  try {
    const data = await $fetch(`/api/sites/distributors/${form.value.distributorId}`, {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    distributorsSites.value = data.items
  } catch (err) {
    console.log(err)
  }
}

const getInstallations = async () => {
  try {
    const data = await $fetch('/api/installations/', {
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

const getInstallation = async (id) => {
  try {
    const user = await $fetch(`/api/installations/${id}`, {
      method: 'GET'
    })
    form.value = user
    updateDialog.value = true
  } catch (err) {
    console.log(err)
  }
}

const createInstallation = async () => {
  try {
    const response = await $fetch('/api/installations/', {
      method: 'POST',
      body: form.value
    })
    await getInstallations()
    createDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

const updateUser = async () => {
  try {
    const response = await $fetch(`/api/installations/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    await getInstallations()
    updateDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

const deleteInstallation = async () => {
  const response = await $fetch(`/api/installations/${form.value.id}`, {
    method: 'DELETE'
  })
  await getInstallations()
  deleteDialog.value = false
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getInstallations()
    searchDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

</script>
