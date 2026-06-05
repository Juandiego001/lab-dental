<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('warranties.title', 2) }}</p>
        <div>
          <client-only>
            <v-btn v-if="$ability.can('create', 'warranties')" class="me-2" icon="mdi-plus" size="small" variant="text"
              @click="createDialog = !createDialog" />
            <v-btn v-if="$ability.can('read', 'warranties')" class="me-2" icon="mdi-magnify" size="small" variant="text"
              @click="searchDialog = !searchDialog" />
          </client-only>
        </div>
      </v-card-title>
      <v-card-text>
        <v-data-table :items="items" :headers="headers" :page="page" :items-per-page="perPage" :items-length="total"
          :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <div class="d-flex align-center justify-center ga-2">
              <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getWarranty(item.id)" />
              <v-btn class="my-2 bg-red" size="small" icon="mdi-trash-can"
                @click="form.id = item.id; deleteDialog = true" />
            </div>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('warranties.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createWarranty">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.invoice" hide-details="auto" :label="$t('warranties.invoice')"
                :rules="[invoiceRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.problemDescription" hide-details="auto"
                :label="$t('warranties.problemDescription')" :rules="[problemDescriptionRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.solutionDescription" hide-details="auto"
                :label="$t('warranties.solutionDescription')" :rules="[solutionDescriptionRequired]"></v-text-field>
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
  <v-dialog v-model="updateDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('warranties.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateWarranty">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.invoice" hide-details="auto" label="Full name"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.problemDescription" hide-details="auto" label="Email"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.solutionDescription" hide-details="auto" label="Password"></v-text-field>
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
  <v-dialog v-model="deleteDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('warranties.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('warranties.delete.message') }}</p>

        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteWarranty" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('warranties.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="doSearch">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('warranties.search.fields')" hide-details="auto"
                prepend-inner-icon="mdi-magnify" clearable></v-text-field>
            </v-col>

            <v-col class="text-end" cols="12">
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
import { useI18n } from 'vue-i18n'

const { back } = useBack()
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { t } = useI18n();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('warranties.title', 2)}`
})

const searchDialog = ref(false);
const createDialog = ref(false);
const items = ref([]);
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
  id: '',
  invoice: '',
  problemDescription: '',
  solutionDescription: '',
  status: '',
  created_at: '',
  updated_at: ''
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: t('warranties.invoice'), key: 'invoice', align: 'start', sortable: false },
  { title: t('warranties.problemDescription'), key: 'problemDescription', align: 'center', sortable: false },
  { title: t('warranties.solutionDescription'), key: 'solutionDescription', align: 'center', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (val) { }
  else {
    createForm.value.reset();
    resetForm();
  }
})

watch(updateDialog, async (val) => {
  if (val) { }
  else {
    updateForm.value.reset();
    resetForm();
  }
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await getEquipments();
})

watch(perPage, async () => {
  await getEquipments();
})

onBeforeMount(async () => {
  if ($ability.can('read', 'warranties')) {
    await getWarranties();
    return;
  }

  back();
})

const resetForm = () => {
  form.value = {
    id: '',
    invoice: '',
    problemDescription: '',
    solutionDescription: '',
    status: '',
    created_at: '',
    updated_at: ''
  }
}

const getWarranties = async () => {
  try {
    const data = await $api('/api/warranties/', {
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
    notify(err, 'error');
  }
}

const getWarranty = async (id) => {
  try {
    const user = await $api(`/api/warranties/${id}`, {
      method: 'GET'
    })
    form.value = user
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  }
}

const createWarranty = async () => {
  try {
    if (!createModel.value) return;
    const { message } = await $api('/api/warranties/', {
      method: 'POST',
      body: form.value
    })
    notify(message, 'success');
    await getWarranties()
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

const updateWarranty = async () => {
  try {
    if (!updateModel.value) return;
    const { message } = await $api(`/api/warranties/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await getWarranties()
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

const deleteWarranty = async () => {
  try {
    const { message } = await $api(`/api/warranties/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getWarranties()
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getWarranties()
    searchDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

// Rules
const invoiceRequired = (v) => !!v || t('warranties.rules.invoiceRequired');
const problemDescriptionRequired = (v) => !!v || t('warranties.rules.problemDescriptionRequired');
const solutionDescriptionRequired = (v) => !!v || t('warranties.rules.solutionDescriptionRequired');

</script>
