<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('equipments.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getEquipment(item.id)"></v-btn>
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
          {{ $t('equipments.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createEquipment">
          <v-row>
            <v-col cols="12">
              <v-autocomplete v-model="form.brandId" :label="$t('brands.title', 1)" :items="brands" item-title="name"
                item-value="id" hide-details="auto" @update:search="getBrands" :rules="[brandRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.categoryId" :label="$t('categories.title', 1)" :items="categories"
                item-title="name" item-value="id" hide-details="auto" @update:search="getCategories" :rules="[categoryRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" hide-details="auto" :label="$t('equipments.serial')" :rules="[serialRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.model" hide-details="auto" :label="$t('equipments.model')" :rules="[modelRequired]"></v-text-field>
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
          {{ $t('equipments.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateEquipment">
          <v-row>
            <v-col cols="12">
              <v-autocomplete v-model="form.brandId" :label="$t('brands.title', 1)" :items="brands" item-title="name"
                item-value="id" hide-details="auto" @update:search="getBrands" clearable :rules="[brandRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.categoryId" :label="$t('categories.title', 1)" :items="categories"
                item-title="name" item-value="id" hide-details="auto" @update:search="getCategories" clearable :rules="[categoryRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" hide-details="auto" :label="$t('equipments.serial')" :rules="[serialRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.model" hide-details="auto" :label="$t('equipments.model')" :rules="[modelRequired]"></v-text-field>
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
          {{ $t('equipments.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('equipments.delete.message') }}</p>

        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2"></span>
        <v-btn @click="deleteEquipment" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('equipments.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <p class="text-subtitle-2 pb-2">{{ $t('equipments.search.message') }}</p>
        <v-form @submit.prevent="doSearch">
          <v-row no-gutters="">
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('equipments.search.fields')" hide-details="auto"
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
import { ref, computed, watch, onBeforeMount } from 'vue'
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
  title: `SOE Latam | ${t('equipments.title', 2)}`
})

const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)
const items = ref([]);
const brands = ref([]);
const categories = ref([]);
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
  brandId: '',
  brandName: '',
  categoryId: '',
  categoryName: '',
  serial: '',
  model: ''
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  const defaultHeaders = [
    { title: 'Id', key: 'id', sortable: false },
    { title: t('brands.title', 1), key: 'brandName', sortable: false },
    { title: t('categories.title', 1), key: 'categoryName', sortable: false },
    { title: t('equipments.serial'), key: 'serial', sortable: false },
    { title: t('equipments.model'), key: 'model', sortable: false }
  ]

  if ($ability.can('update', 'equipments') || $ability.can('delete', 'equipments')) {
    defaultHeaders.push({ title: t('options'), key: 'option', align: 'center', sortable: false })
  }

  return defaultHeaders;
})

watch(createDialog, async (val) => {
  if (val) {
    await getBrands();
    await getCategories();
  } else {
    createForm.value.reset();
    resetForm();
  }
})

watch(updateDialog, async (val) => {
  if (val) {
    await getBrands(form.value.brandName);
    await getCategories(form.value.categoryName);
  } else {
    updateForm.value.reset();
    resetForm();
  }
})

watch(page, async () => {
  await getEquipments();
})

watch(perPage, async () => {
  await getEquipments();
})

onBeforeMount(async () => {
  if (!$ability.can('read', 'equipments')) {
    navigateTo(history.state?.back || '/login');
    return;
  }
  await getEquipments();
})

const resetForm = () => {
  form.value = {
    brandId: '',
    brandName: '',
    categoryId: '',
    categoryName: '',
    serial: '',
    model: ''
  }
}

const getBrands = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value) return;
    const data = await $api('/api/brands/', {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    brands.value = data.items
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');;
  }
}

const getCategories = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value) return;
    const data = await $api('/api/categories/', {
      query: {
        search: search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    categories.value = data.items
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');;
  }
}

const getEquipments = async () => {
  try {
    const data = await $api('/api/equipments/', {
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

const getEquipment = async (id) => {
  try {
    const data = await $api(`/api/equipments/${id}`, {
      method: 'GET'
    })
    form.value = data
    updateDialog.value = true
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const createEquipment = async () => {
  if (!createModel.value) return;
  try {
    const response = await $api('/api/equipments/', {
      method: 'POST',
      body: form.value
    })
    await getEquipments()
    createDialog.value = false
    resetForm()
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const updateEquipment = async () => {
  try {
    if (!updateModel.value) return;
    const response = await $api(`/api/equipments/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    await getEquipments()
    updateDialog.value = false
    resetForm()
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const deleteEquipment = async () => {
  try {
    const response = await $api(`/api/equipments/${form.value.id}`, {
      method: 'DELETE'
    })
    await getEquipments()
    deleteDialog.value = false
    resetForm()
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');;
  }
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getEquipments()
    searchDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

// Rules
const brandRequired = (v) => !!v || t('equipments.rules.brandRequired');
const categoryRequired = (v) => !!v || t('equipments.rules.categoryRequired');
const serialRequired = (v) => !!v || t('equipments.rules.serialRequired');
const modelRequired = (v) => !!v || t('equipments.rules.modelRequired');

</script>
