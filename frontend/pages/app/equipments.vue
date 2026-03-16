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
                <v-avatar class="my-2 cursor-pointer" size="60" rounded="circle" color="grey-lighten-2" v-bind="props"
                  @click="async () => { form.id = item.id; await getMedia(); mediaDialog = true; }">
                  <v-img v-if="item.mainPicture" alt="Machine photo" cover :src="`/api/files?path=${item.mainPicture}`">
                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <v-progress-circular indeterminate color="grey-lighten-5" size="20" />
                      </v-row>
                    </template>
                    <v-overlay :model-value="isHovering" contained scrim="black" class="align-center justify-center">
                      <v-icon icon="mdi-eye" color="white" size="28" />
                    </v-overlay>
                  </v-img>
                  <v-icon v-else icon="mdi-car-wrench" color="grey-darken-1" />
                </v-avatar>
              </v-hover>
            </template>
            <template v-slot:item.option="{ item }">
              <div class="d-flex align-center justify-center ga-2">
                <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getEquipment(item.id)" />
                <v-btn class="my-2 bg-secondary" size="small" icon="mdi-image-area"
                  @click="async () => { form.id = item.id; await getMedia(); editMediaDialog = true; }" />
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

            <!-- Media -->
            <v-col class="mt-2" cols="12">
              <p class="text-subtitle-1 text-primary">Media</p>
              <p class="text-caption text-primary">
                {{ $t('equipments.media.description') }}
              </p>
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="mainPicture" :label="$t('equipments.media.main')" :prepend-icon="null"
                prepend-inner-icon="mdi-paperclip" hide-details="auto" chips />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="secondaryPictures" :label="$t('equipments.media.secondary')" :prepend-icon="null"
                prepend-inner-icon="mdi-paperclip" hide-details="auto" multiple chips />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="videos" :label="$t('equipments.media.videos')" :prepend-icon="null"
                prepend-inner-icon="mdi-paperclip" hide-details="auto" multiple chips />
            </v-col>

            <v-col class="text-end mt-2">
              <v-btn variant="outlined" @click="createDialog = false" @mousedown.prevent :disabled="loading">{{
                $t('cancel') }}</v-btn>
              <span class="mx-1" />
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

            <!-- Media -->
            <v-col class="mt-2" cols="12">
              <p class="text-subtitle-1 text-primary">Media</p>
              <p class="text-caption text-primary">
                {{ $t('equipments.media.description') }}
              </p>
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="mainPicture" :label="$t('equipments.media.main')" :prepend-icon="null"
                prepend-inner-icon="mdi-paperclip" hide-details="auto" chips />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="secondaryPictures" :label="$t('equipments.media.secondary')" :prepend-icon="null"
                prepend-inner-icon="mdi-paperclip" hide-details="auto" multiple chips />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="videos" :label="$t('equipments.media.videos')" :prepend-icon="null"
                prepend-inner-icon="mdi-paperclip" hide-details="auto" multiple chips />
            </v-col>

            <v-col class="text-end">
              <v-btn variant="outlined" @click="updateDialog = false" @mousedown.prevent :disabled="loading">{{
                $t('cancel') }}</v-btn>
              <span class="mx-1" />
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

  <!-- View Media -->
  <v-dialog v-model="mediaDialog" max-width="800" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card class="bg-grey-darken-4">
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          <p>Media</p>
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="mediaDialog = false" />
        </v-row>
      </v-card-title>

      <v-card-text class="pa-0 d-flex justify-center align-center">
        <v-carousel>
          <v-carousel-item v-for="file of files">
            <v-img v-if="file.extension !== '.mp4'" width="100%" height="100%" contain
              :src="`/api/files?path=${file.path}`">
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="white" size="40" />
                </v-row>
              </template>
            </v-img>
            <video controls preload="metadata" style="width: 100%; height: calc(100% - 50px); object-fit: contain;">
              <source :src="`/api/files?path=${file.path}`" type="video/mp4" />
              Tu navegador no soporta el elemento de video.
            </video>
          </v-carousel-item>
        </v-carousel>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- View Edit Media -->
  <v-dialog v-model="editMediaDialog" max-width="900" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          <p>Media</p>
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="editMediaDialog = false" />
        </v-row>
      </v-card-title>

      <v-card-text>
        <v-data-table :items="files" :headers="headersMedia" :page="pageMedia" :items-per-page="perPageMedia"
          :items-length="totalMedia" :items-per-page-options="itemsPerPageOptions" @update:page="v => pageMedia = v"
          @update:itemsPerPage="v => perPageMedia = v" :disable-sort="true" density="compact">
          <template v-slot:item.picture="{ item }">
            <v-avatar size="30" rounded="circle" color="grey-lighten-2">
              <v-img v-if="item.extension !== '.mp4'" alt="Machine photo" cover :src="`/api/files?path=${item.path}`">
                <template v-slot:placeholder>
                  <v-row class="fill-height ma-0" align="center" justify="center">
                    <v-progress-circular indeterminate color="grey-lighten-5" size="20" />
                  </v-row>
                </template>
              </v-img>
              <v-icon v-else icon="mdi-video" color="grey-darken-1" />
            </v-avatar>
          </template>

          <template v-slot:item.originalName="{ item }">
            <span class="d-inline-block text-truncate" style="max-width: 100px;" :title="item.originalName">
              {{ item.originalName }}
            </span>
          </template>

          <template v-slot:item.size="{ item }">
            {{ formatFileSize(item.size) }}
          </template>

          <template v-slot:item.isMain="{ item }">
            <v-icon v-if="item.isMain === 'True'" icon="mdi-check-circle" color="success" size="small" />
            <span v-else class="text-grey-lighten-1">-</span>
          </template>

          <template v-slot:item.option="{ item }">
            <div class="d-flex align-center justify-center ga-2">
              <v-btn class="my-2 bg-secondary" size="x-small" icon="mdi-open-in-new"
                :href="`/api/files?path=${item.path}`" target="_blank" />
              <v-btn class="my-2 bg-primary" size="x-small" icon="mdi-download"
                :href="`/api/files?path=${item.path}&download=true&filename=${item.originalName}`" />
              <v-btn class="my-2 bg-red" size="x-small" icon="mdi-trash-can"
                @click="fileId = item.id; deleteMediaDialog = true" />
            </div>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Delete Dialog -->
  <v-dialog v-model="deleteMediaDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('equipments.media.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteMediaDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('equipments.media.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined" :disabled="loading">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteEquipmentFile" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>
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

const totalMedia = ref(null);
const pageMedia = ref(null);
const perPageMedia = ref(null);

const searchDialog = ref(false);
const createDialog = ref(false);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const mediaDialog = ref(false);
const editMediaDialog = ref(false);
const deleteMediaDialog = ref(false);

const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref();
const updateForm = ref();

const mainPicture = ref(null);
const secondaryPictures = ref(null);
const videos = ref(null);
const files = ref([]);
const fileId = ref(null);

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
    { title: t('equipments.reference'), key: 'reference', align: 'center' }
  ]

  if ($ability.can('update', 'equipments') || $ability.can('delete', 'equipments')) {
    defaultHeaders.push({ title: t('options'), key: 'option', align: 'center', sortable: false })
  }

  return defaultHeaders;
})

const headersMedia = computed(() => {
  const defaultHeaders = [
    { key: 'picture', sortable: false },
    { title: t('equipments.media.filename'), key: 'originalName' },
    { title: t('equipments.media.size'), key: 'size', align: 'center' },
    { title: t('equipments.media.extension'), key: 'extension', align: 'center' },
    { title: t('equipments.media.main'), key: 'isMain', align: 'center' }
  ]

  if ($ability.can('update', 'equipments') || $ability.can('delete', 'equipments')) {
    defaultHeaders.push({ title: t('options'), key: 'option', align: 'center', sortable: false })
  }

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
    await getEquipments({ withPicture: true })
    return;
  }
  back();
})

const resetForm = () => {
  mainPicture.value = null;
  secondaryPictures.value = null;
  videos.value = null;
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

    const formData = new FormData();

    if (mainPicture.value) {
      formData.append('mainPicture', mainPicture.value);
    }

    if (secondaryPictures.value && secondaryPictures.value.length) {
      for (const picture of secondaryPictures.value) {
        formData.append('secondaryPictures', picture);
      }
    }

    if (videos.value && videos.value.length) {
      for (const video of videos.value) {
        formData.append('videos', video);
      }
    }

    for (const [key, value] of Object.entries(form.value)) {
      formData.append(key, value);
    }

    const { message } = await $api('/api/equipments/', {
      method: 'POST',
      body: formData
    })
    notify(message, 'success');
    await getEquipments({ withPicture: true, })
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

    const formData = new FormData();

    if (mainPicture.value) {
      formData.append('mainPicture', mainPicture.value);
    }

    if (secondaryPictures.value && secondaryPictures.value.length) {
      for (const picture of secondaryPictures.value) {
        formData.append('secondaryPictures', picture);
      }
    }

    if (videos.value && videos.value.length) {
      for (const video of videos.value) {
        formData.append('videos', video);
      }
    }

    for (const [key, value] of Object.entries(form.value)) {
      formData.append(key, value);
    }

    const { message } = await $api(`/api/equipments/${form.value.id}`, {
      method: 'PUT',
      body: formData
    })
    notify(message, 'success');
    await getEquipments({ withPicture: true, })
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
    await getEquipments({ withPicture: true, })
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getMedia = async () => {
  try {
    loading.value = true;
    const data = await $api(`/api/equipments/${form.value.id}/files`, {
      method: 'GET'
    })
    files.value = data.equipmentFiles;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
};

const formatFileSize = (bytes) => {
  if (bytes === 0 || !bytes) return '0 Bytes';

  const k = 1024;
  const decimals = 2;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
};

const deleteEquipmentFile = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/equipments/files/${fileId.value}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getMedia();
    deleteMediaDialog.value = false
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
