<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('equipments.title', 2) }}</p>
        <div>
          <client-only>
            <v-btn v-if="$ability.can('create', 'equipments')" class="me-2" icon="mdi-plus" size="small" variant="text"
              @click="createDialog = !createDialog" />
            <v-btn v-if="$ability.can('read', 'equipments')" class="me-2" icon="mdi-magnify" size="small" variant="text"
              @click="searchDialog = !searchDialog" />
          </client-only>
        </div>
      </v-card-title>
      <v-card-text>
        <client-only>
          <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
            :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" :loading="loading">
            <template v-slot:item.picture="{ item }">
              <v-hover v-slot="{ isHovering, props }">
                <v-avatar class="my-2 cursor-pointer" size="50" rounded="circle" color="grey-lighten-2" v-bind="props"
                  @click="async () => { filesEquipmentId = item.id; await getEquipmentFiles({}); sliderDialog = true; }">
                  <v-img v-if="item.mainPicture && item.extension !== '.mp4'" alt="Machine photo" cover
                    :src="`/api/files?path=${item.mainPicture}`">
                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <v-progress-circular indeterminate color="grey-lighten-5" size="20" />
                      </v-row>
                    </template>
                    <v-overlay :model-value="isHovering" contained scrim="black" class="align-center justify-center">
                      <v-icon icon="mdi-eye" color="white" size="28" />
                    </v-overlay>
                  </v-img>
                  <v-icon v-else icon="mdi-car-wrench" color="grey-darken-2" />
                </v-avatar>
              </v-hover>
            </template>
            <template v-slot:item.option="{ item }">
              <div class="d-flex align-center justify-center ga-2">
                <v-btn v-if="isAdmin" class="my-2 bg-primary" size="small" icon="mdi-pencil"
                  @click="getEquipment(item.id)" />
                <v-btn class="my-2 bg-secondary" size="small" icon="mdi-image-area"
                  @click="async () => { filesEquipmentId = item.id; await getEquipmentFiles({}); tableDialog = true; }" />
                <v-btn class="my-2 bg-secondary" size="small" icon="mdi-file-multiple"
                  @click="async () => { manualsEquipmentId = item.id; await getManuals({ equipmentId: item.id }); manualsDialog = true; }" />
                <v-btn v-if="isAdmin" class="my-2 bg-red" size="small" icon="mdi-trash-can"
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
          {{ $t('equipments.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createEquipment">
          <v-row dense>
            <v-col cols="12">
              <v-autocomplete v-model="form.brandId" :label="$t('brands.title', 1)" :items="brands" item-title="name"
                item-value="id" hide-details="auto" :rules="[brandRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getBrands({ name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.categoryId" :label="$t('categories.title', 1)" :items="categories"
                item-title="name" item-value="id" hide-details="auto" :rules="[categoryRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getCategories({ name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.model" hide-details="auto" :label="$t('equipments.model')"
                :rules="[modelRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.reference" hide-details="auto" :label="$t('equipments.reference')"
                :rules="[referenceRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="updateDialog = false" @mousedown.prevent :disabled="loading">
                {{ $t('cancel') }}
              </v-btn>
              <span class="mx-1" />
              <v-btn type="submit" class="bg-primary" @mousedown.prevent :loading="loading">
                {{ $t('confirm') }}
              </v-btn>
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
          {{ $t('equipments.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateEquipment">
          <v-row dense>
            <v-col cols="12">
              <v-autocomplete v-model="form.brandId" :label="$t('brands.title', 1)" :items="brands" item-title="name"
                item-value="id" hide-details="auto" clearable :rules="[brandRequired]" @update:search="(name) => {
                  if (!updateDialog) return;
                  getBrands({ name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.categoryId" :label="$t('categories.title', 1)" :items="categories"
                item-title="name" item-value="id" hide-details="auto" clearable :rules="[categoryRequired]"
                @update:search="(name) => {
                  if (!updateDialog) return;
                  getCategories({ name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.model" hide-details="auto" :label="$t('equipments.model')"
                :rules="[modelRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.reference" hide-details="auto" :label="$t('equipments.reference')"
                :rules="[referenceRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="updateDialog = false" @mousedown.prevent :disabled="loading">
                {{ $t('cancel') }}
              </v-btn>
              <span class="mx-1" />
              <v-btn type="submit" class="bg-primary" @mousedown.prevent :loading="loading">
                {{ $t('confirm') }}
              </v-btn>
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
          {{ $t('equipments.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('equipments.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined" :disabled="loading">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteEquipment" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="700" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('equipments.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchEquipments(1, 15);
          searchDialog = false
        }">
          <v-row dense>
            <v-col cols="6">
              <v-autocomplete v-model="searchForm.brandId" :label="$t('brands.title', 1)" :items="brands"
                item-title="name" item-value="id" hide-details="auto" clearable
                @update:search="(name) => getBrands({ brandId: searchForm.brandId, name })" />
            </v-col>
            <v-col cols="6">
              <v-autocomplete v-model="searchForm.categoryId" :label="$t('categories.title', 1)" :items="categories"
                item-title="name" item-value="id" hide-details="auto" clearable
                @update:search="(name) => getCategories({ categoryId: searchForm.categoryId, name })" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.model" hide-details="auto" :label="$t('equipments.model')" counter="50"
                maxlength="50" clearable />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.reference" hide-details="auto" :label="$t('equipments.reference')"
                counter="50" maxlength="50" clearable />
            </v-col>
            <v-col class="text-end" cols="12">
              <v-btn class="bg-primary" type="submit" @mousedown.prevent :loading="loading">{{ $t('search') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <EquipmentFilesSlider />
  <EquipmentFilesTable />
  <EquipmentFilesManuals />
</template>

<script setup>
import { ref, computed, watch, onBeforeMount } from 'vue'
import { useI18n } from 'vue-i18n'

const { back } = useBack()
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { t } = useI18n();
const { items: brands, getBrands } = useBrands();
const { items: categories, getCategories } = useCategories();
const { items, total, getEquipments } = useEquipments();
const { isAdmin } = useProfile();
const { equipmentId: filesEquipmentId, getEquipmentFiles, sliderDialog, tableDialog } = useEquipmentFiles();
const { equipmentId: manualsEquipmentId, getManuals, manualsDialog } = useManuals();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('equipments.title', 2)}`
})

const loading = ref(false);
const page = ref(1);
const perPage = ref(15);
const sortBy = ref(null);

const searchDialog = ref(false);
const createDialog = ref(false);
const updateDialog = ref(false);
const deleteDialog = ref(false);

const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref();
const updateForm = ref();

const form = ref({
  brandId: null,
  brandName: '',
  categoryId: null,
  categoryName: '',
  reference: '',
  model: ''
})
const searchForm = ref({
  brandId: null,
  categoryId: null,
  model: null,
  reference: null
})


const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  const defaultHeaders = [
    { key: 'picture', sortable: false },
    { title: t('brands.title', 1), key: 'brandName' },
    { title: t('categories.title', 1), key: 'categoryName', align: 'center' },
    { title: t('equipments.model'), key: 'model', align: 'center' },
    { title: t('equipments.reference'), key: 'reference', align: 'center' },
    { title: t('options'), key: 'option', align: 'center', sortable: false }
  ]
  return defaultHeaders;
})

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
  await getBrands({});
  await getCategories({});
})

watch(updateDialog, async (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
    return;
  }
  await getBrands({ name: form.value.brandName });
  await getCategories({ name: form.value.categoryName });
})

watch(searchDialog, async (val) => {
  if (!val) return;
  await getBrands({
    brandId: searchForm.value.brandId
  });
  await getCategories({
    categoryId: searchForm.value.categoryId
  });
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await searchEquipments();
})

watch(perPage, async () => {
  await searchEquipments();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchEquipments();
  }
})

onBeforeMount(async () => {
  if ($ability.can('read', 'equipments')) {
    await getEquipments({})
    return;
  }
  back();
})

const resetForm = () => {
  form.value = {
    brandId: null,
    brandName: '',
    categoryId: null,
    categoryName: '',
    reference: null,
    model: null
  }
}

const searchEquipments = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getEquipments({
      brandId: searchForm.value.brandId,
      categoryId: searchForm.value.categoryId,
      model: searchForm.value.model,
      reference: searchForm.value.reference,
      withPicture: true,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value,
      sortBy: sortBy.value?.length ? sortBy.value[0] : null
    })
  } catch (err) { }
  finally {
    loading.value = false;
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
    notify(err, 'error');
  }
}

const createEquipment = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/equipments/', {
      method: 'POST',
      body: form.value
    })
    notify(message, 'success');
    await getEquipments({})
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateEquipment = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await $api(`/api/equipments/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await getEquipments({})
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteEquipment = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/equipments/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getEquipments({})
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

// Rules
const brandRequired = (v) => !!v || t('equipments.rules.brandRequired');
const categoryRequired = (v) => !!v || t('equipments.rules.categoryRequired');
const referenceRequired = (v) => !!v || t('equipments.rules.referenceRequired');
const modelRequired = (v) => !!v || t('equipments.rules.modelRequired');

</script>
