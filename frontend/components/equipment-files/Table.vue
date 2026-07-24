<template>
  <v-dialog v-model="tableDialog" max-width="900" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('equipments.files.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="tableDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-row class="ma-0 mb-2">
          <v-spacer />
          <v-btn v-if="isAdmin" class="me-2" icon="mdi-plus" size="x-small" @click="createDialog = !createDialog" />
          <v-btn icon="mdi-magnify" size="x-small" @click="searchDialog = !searchDialog" />
        </v-row>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" density="compact" :disable-sort="true" :loading="loading">
          <template v-slot:item.picture="{ item }">
            <v-avatar class="my-2" size="50" rounded="circle" color="grey-lighten-2">
              <v-img v-if="item.extension !== '.mp4'" alt="Machine photo" cover :src="`/api/files?path=${item.path}`">
                <template v-slot:placeholder>
                  <v-row class="fill-height ma-0" align="center" justify="center">
                    <v-progress-circular indeterminate color="grey-lighten-5" size="20" />
                  </v-row>
                </template>
              </v-img>
              <v-icon v-else icon="mdi-video" color="grey-darken-2" />
            </v-avatar>
          </template>

          <template v-slot:item.originalName="{ item }">
            <div class="d-inline-flex" style="max-width: 190px;">
              <span class="text-truncate" :title="item.originalName">
                {{ item.originalName }}
              </span>
            </div>
          </template>

          <template v-slot:item.option="{ item }">
            <div class="d-flex align-center justify-center ga-2">
              <v-btn class="my-1 bg-secondary" size="x-small" icon="mdi-open-in-new"
                :href="`/api/files?path=${item.path}`" target="_blank" />
              <template v-if="isAdmin">
                <v-btn class="my-1 bg-primary" size="x-small" icon="mdi-pencil" @click="getEquipmentFile(item.id)" />
                <v-btn class="my-1 bg-red" size="x-small" icon="mdi-trash-can"
                  @click="form.id = item.id; deleteDialog = true" />
                <div class="d-flex ga-1 my-1 flex-column">
                  <v-btn v-if="item.sortOrder > 1" class="bg-secondary" size="x-small" icon="mdi-arrow-up-bold"
                    @click="updateEquipmentFileOrder(item.id, item.sortOrder - 1)" />
                  <v-btn v-if="item.sortOrder < total" class="bg-secondary" size="x-small" icon="mdi-arrow-down-bold"
                    @click="updateEquipmentFileOrder(item.id, item.sortOrder + 1)" />
                </div>
              </template>
            </div>
          </template>
        </v-data-table-server>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('equipments.files.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createEquipmentFile">
          <v-row dense>
            <v-col cols="12">
              <v-file-input v-model="files" :prepend-icon="null" prepend-inner-icon="mdi-paperclip" hide-details="auto"
                :label="$t('equipments.files.files')" multiple chips accept=".mp4, .jpg, .jpeg, .png, .webp, .svg"
                :rules="fileRules">
                <template v-slot:selection="{ fileNames }">
                  <v-chip v-for="fileName in fileNames" :key="fileName" size="small" label>
                    {{ fileName }}
                  </v-chip>
                </template>
              </v-file-input>
            </v-col>
            <v-col class="mt-3 text-end">
              <v-btn variant="outlined" size="small" @click="createDialog = false" @mousedown.prevent
                :disabled="loading">
                {{ $t('cancel') }}
              </v-btn>
              <span class="mx-1" />
              <v-btn class="bg-primary" size="small" type="submit" @mousedown.prevent :loading="loading">
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
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('equipments.files.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateEquipmentFile">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.title" hide-details="auto" :label="$t('equipments.files.labelTitle')"
                counter="50" maxlength="50" autocomplete="off" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.description" hide-details="auto" :label="$t('equipments.files.description')"
                counter="100" maxlength="100" autocomplete="off" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.originalName" hide-details="auto" :label="$t('equipments.files.filename')"
                readonly />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.size" hide-details="auto" :label="$t('equipments.files.size')" readonly />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.extension" hide-details="auto" :label="$t('equipments.files.extension')"
                readonly />
            </v-col>
            <v-col class="mt-3 text-end">
              <v-btn variant="outlined" size="small" @click="updateDialog = false" @mousedown.prevent
                :disabled="loading">
                {{ $t('cancel') }}
              </v-btn>
              <span class="mx-1" />
              <v-btn class="bg-primary" size="small" type="submit" @mousedown.prevent :loading="loading">
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
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('equipments.files.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-4">
        <p class="text-subtitle-1 mb-2
         text-center">{{ $t('equipments.files.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" size="small" variant="outlined" :disabled="loading">
          {{ $t('cancel') }}
        </v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteEquipmentFile" class="bg-red" size="small" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="700" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('equipments.files.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchEquipmentsFiles(1, 15);
          searchDialog = false
        }">
          <v-row dense>
            <v-col cols="6">
              <v-text-field v-model="searchForm.originalName" hide-details="auto"
                :label="$t('equipments.files.filename')" counter="50" maxlength="50" clearable autocomplete="off" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.title" hide-details="auto" :label="$t('equipments.files.labelTitle')"
                counter="100" maxlength="100" clearable autocomplete="off" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="searchForm.description" hide-details="auto"
                :label="$t('equipments.files.description')" counter="100" maxlength="100" clearable autocomplete="off" />
            </v-col>
            <v-col cols="12">
              <v-select v-model="searchForm.extension" item-title="title" item-value="value" hide-details="auto"
                :label="$t('equipments.files.extension')" :items="extensions" clearable autocomplete="off" />
            </v-col>
            <v-col class="mt-3 text-end" cols="12">
              <v-btn class="bg-primary" size="small" type="submit" @mousedown.prevent :loading="loading">
                {{ $t('search') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n();
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { isAdmin } = useProfile();
const { equipmentId, getEquipmentFiles, tableDialog, items, total } = useEquipmentFiles();

const loading = ref(false);
const page = ref(1);
const perPage = ref(15);

const searchDialog = ref(false);
const createDialog = ref(false);
const updateDialog = ref(false);
const deleteDialog = ref(false);

const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref();
const updateForm = ref();

const files = ref(null);
const form = ref({
  title: '',
  description: '',
  originalName: '',
  size: '',
  extension: ''
})
const searchForm = ref({
  title: null,
  description: null,
  originalName: null,
  extension: null
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  const defaultHeaders = [
    { key: 'picture', align: 'center', sortable: false },
    { title: t('equipments.files.filename'), key: 'originalName', sortable: false },
    { title: t('equipments.files.size'), key: 'size', align: 'center', sortable: false },
    { title: t('equipments.files.extension'), key: 'extension', align: 'center', sortable: false },
    { title: t('options'), key: 'option', align: 'center', sortable: false }
  ]
  return defaultHeaders;
})

const extensions = computed(() => [
  { title: 'MP4', value: '.mp4' },
  { title: 'JPG', value: '.jpg' },
  { title: 'JPEG', value: '.jpeg' },
  { title: 'PNG', value: '.png' },
  { title: 'PDF', value: '.pdf' },
  { title: 'WEBP', value: '.webp' },
  { title: 'SVG', value: '.svg' },
])

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
})

watch(updateDialog, async (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
    return;
  }
})

watch(page, async () => {
  await searchEquipmentsFiles();
})

watch(perPage, async () => {
  await searchEquipmentsFiles();
})

const resetForm = () => {
  files.value = null;
  form.value = {
    title: '',
    description: '',
    originalName: '',
    size: '',
    extension: ''
  }
}

const searchEquipmentsFiles = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getEquipmentFiles({
      title: searchForm.value.title,
      description: searchForm.value.description,
      originalName: searchForm.value.originalName,
      extension: searchForm.value.extension,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value
    })
  } catch (err) { }
  finally {
    loading.value = false;
  }
}

const createEquipmentFile = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const formData = new FormData();

    for (let file of files.value) {
      formData.append('files', file)
    }

    const { message } = await $api(`/api/equipments/${equipmentId.value}/files`, {
      method: 'POST',
      body: formData
    })
    notify(message, 'success');
    await getEquipmentFiles({});
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getEquipmentFile = async (id) => {
  try {
    const data = await $api(`/api/equipments/files/${id}`, {
      method: 'GET'
    })
    form.value = data
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  }
}

const updateEquipmentFile = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/equipments/files/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await getEquipmentFiles({});
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateEquipmentFileOrder = async (id, newSortOrder) => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/equipments/${equipmentId.value}/files/${id}/order`, {
      method: 'PUT',
      body: {
        newSortOrder
      }
    })
    notify(message, 'success');
    await searchEquipmentsFiles();
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteEquipmentFile = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/equipments/files/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getEquipmentFiles({});
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const allowedMimeTypes = [
  'video/mp4',
  'image/jpeg',
  'image/png',
  'image/webp',
  'image/svg+xml'
];

const fileRules = [
  (value) => {
    if (!value || !value.length) {
      return t('equipments.files.rules.filesRequired')
    }

    for (let i = 0; i < value.length; i++) {
      const file = value[i]

      if (!allowedMimeTypes.includes(file.type)) {
        return t('equipments.files.rules.invalidFileType')
      }
    }

    return true
  }
]
</script>