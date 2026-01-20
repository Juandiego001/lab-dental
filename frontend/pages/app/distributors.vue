<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('distributors.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <div class="d-flex align-center justify-center ga-2">
              <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getDistributor(item.id)"></v-btn>
              <v-btn class="my-2 bg-red" size="small" icon="mdi-trash-can"
                @click="form.id = item.id; deleteDialog = true"></v-btn>
            </div>
          </template>
        </v-data-table-server>
      </v-card-text>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('distributors.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createDistributor">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('distributors.name')"
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
  <v-dialog v-model="updateDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('distributors.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateDistributor">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('distributors.name')"
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
  <v-dialog v-model="deleteDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('distributors.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('distributors.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2"></span>
        <v-btn @click="deleteDistributor" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('distributors.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <p class="text-subtitle-2 pb-2">{{ $t('distributors.search.message') }}</p>
        <v-form @submit.prevent="doSearch">
          <v-row no-gutters="">
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('distributors.search.fields')" hide-details="auto"
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
const { show } = useSnackbar();
const { $ability } = useNuxtApp();
const { t } = useI18n();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('distributors.title', 2)}`
})

const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)
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
  name: ''
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: 'Id', key: 'id', align: 'center', sortable: false },
  { title: t('distributors.name'), key: 'name', align: 'center', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
  }
})

watch(updateDialog, (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
  }
})

watch(deleteDialog, (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await getDistributors();
})

watch(perPage, async () => {
  await getDistributors();
})

onBeforeMount(async () => {
  if (!$ability.can('read', 'distributors')) {
    navigateTo(history.state?.back || '/login');
    return;
  }
  await getDistributors();
})

const resetForm = () => {
  form.value = {
    name: ''
  }
}

const getDistributors = async () => {
  try {
    const data = await $api('/api/distributors/', {
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
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getDistributor = async (id) => {
  try {
    const user = await $api(`/api/distributors/${id}`, {
      method: 'GET'
    })
    form.value = user
    updateDialog.value = true
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const createDistributor = async () => {
  try {
    if (!createModel.value) return;
    const { message } = await $api('/api/distributors/', {
      method: 'POST',
      body: form.value
    })

    show(message, 'success');
    await getDistributors()
    createDialog.value = false;
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const updateDistributor = async () => {
  try {
    if (!updateModel.value) return;
    const { message } = await $api(`/api/distributors/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    show(message, 'success');
    await getDistributors()
    updateDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const deleteDistributor = async () => {
  try {
    const { message } = await $api(`/api/distributors/${form.value.id}`, {
      method: 'DELETE'
    })
    show(message, 'success');
    await getDistributors();
    deleteDialog.value = false;
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getDistributors()
    searchDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

// Rules
const nameRequired = (v) => !!v || t('distributors.rules.nameRequired');

</script>
