<template>
  <v-dialog v-model="manualsDialog" max-width="900" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('manuals.title', 2) }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="manualsDialog = false" />
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
          @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" density="compact" :loading="loading"
          show-expand>
          <template v-slot:expanded-row="{ columns, item }">
            <tr>
              <td :colspan="columns.length" class="bg-grey-lighten-4 pa-3">
                <div class="d-flex flex-column ga-3">
                  <p class="text-caption text-decoration-underline">{{ $t('manuals.description') }}</p>
                  <pre class="text-body-2" style="white-space: pre-wrap;">{{ item.description }}</pre>
                </div>
              </td>
            </tr>
          </template>

          <template v-slot:item.title="{ item }">
            <div class="d-inline-flex" style="max-width: 190px;">
              <span class="text-truncate" :title="item.title">
                {{ item.title }}
              </span>
            </div>
          </template>

          <template v-slot:item.option="{ item }">
            <div class="d-flex align-center justify-center ga-2 my-2">
              <v-btn class="bg-secondary" size="x-small" icon="mdi-open-in-new"
                :href="`/api/files?path=${item.manualFile.path}`" target="_blank" />
              <template v-if="isAdmin">
                <v-btn class="bg-primary" size="x-small" icon="mdi-pencil" @click="getManual(item.id)" />
                <v-btn class="bg-red" size="x-small" icon="mdi-trash-can"
                  @click="form.id = item.id; deleteDialog = true" />
              </template>
            </div>
          </template>
        </v-data-table-server>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="650" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('manuals.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createManual">
          <v-row dense>
            <v-col cols="12">
              <v-select v-model="form.manualTypeId" item-title="name" item-value="id" :items="itemsTypes"
                hide-details="auto" :label="$t('manuals.manualType')" clearable :rules="[manualTypeRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.title" hide-details="auto" :label="$t('manuals.labelTitle')" counter="50"
                maxlength="50" :rules="[titleRequired]" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.description" hide-details="auto" :label="$t('manuals.description')"
                counter="800" maxlength="800" />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="file" :prepend-icon="null" prepend-inner-icon="mdi-paperclip" hide-details="auto"
                :label="$t('manuals.file.title')" chips accept=".jpg, .jpeg, .png, .webp, .svg, .pdf, .docx"
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
  <v-dialog v-model="updateDialog" max-width="650" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('manuals.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateManual">
          <v-row dense>
            <v-col cols="12">
              <v-select v-model="form.manualTypeId" item-title="name" item-value="id" :items="itemsTypes"
                hide-details="auto" :label="$t('manuals.manualType')" clearable :rules="[manualTypeRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.title" hide-details="auto" :label="$t('manuals.labelTitle')" counter="50"
                maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.description" hide-details="auto" :label="$t('manuals.description')"
                counter="800" maxlength="800" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.manualFile.originalName" hide-details="auto" :label="$t('manuals.file.title')"
                readonly />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.manualFile.size" hide-details="auto" :label="$t('manuals.file.size')"
                readonly />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.manualFile.extension" hide-details="auto"
                :label="$t('manuals.file.extension')" readonly />
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
          {{ $t('manuals.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-4">
        <p class="text-subtitle-1 mb-2 text-center">
          {{ $t('manuals.delete.message') }}
        </p>
        <v-btn @click="deleteDialog = false" size="small" variant="outlined" :disabled="loading">
          {{ $t('cancel') }}
        </v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteManual" class="bg-red" size="small" :loading="loading">
          {{ $t('confirm') }}
        </v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="600" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('manuals.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchManuals(1, 15);
          searchDialog = false
        }">
          <v-row dense>
            <v-col cols="6">
              <v-text-field v-model="searchForm.title" hide-details="auto" :label="$t('manuals.labelTitle')"
                counter="100" maxlength="100" clearable />
            </v-col>
            <v-col cols="6">
              <v-select v-model="searchForm.manualTypeId" item-title="name" item-value="id" :items="itemsTypes"
                hide-details="auto" :label="$t('manuals.manualType')" clearable />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.description" hide-details="auto" :label="$t('manuals.description')"
                counter="100" maxlength="100" clearable />
            </v-col>
            <v-col cols="6">
              <v-select v-model="searchForm.extension" item-title="title" item-value="value" hide-details="auto"
                :label="$t('manuals.file.extension')" :items="extensions" clearable />
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
const { equipmentId, getManuals, get, create, update, remove, manualsDialog, items, total, getManualTypes, itemsTypes, totalTypes } = useManuals();

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

const file = ref(null);
const form = ref({
  title: '',
  description: '',
  manualTypeId: '',
  manualFile: {
    originalName: '',
    extension: '',
    size: ''
  }
})
const searchForm = ref({
  title: null,
  description: null,
  manualTypeId: null,
  extension: null
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  return [
    { title: t('manuals.labelTitle'), key: 'title' },
    { title: t('manuals.manualType'), key: 'manualType.name', align: 'center' },
    { title: t('manuals.file.size'), key: 'manualFile.size', align: 'center' },
    { title: t('manuals.file.extension'), key: 'manualFile.extension', align: 'center' },
    { title: t('options'), key: 'option', align: 'center', sortable: false }
  ]
})

const extensions = computed(() => [
  { title: 'PDF', value: '.pdf' },
  { title: 'DOCX', value: '.docx' },
  { title: 'JPG', value: '.jpg' },
  { title: 'JPEG', value: '.jpeg' },
  { title: 'PNG', value: '.png' },
  { title: 'WEBP', value: '.webp' },
  { title: 'SVG', value: '.svg' },
])

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
  await getManualTypes({});
})

watch(updateDialog, async (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
    return;
  }
  await getManualTypes({});
})

watch(searchDialog, async (val) => {
  if (!val) return;
  await getManualTypes({});
})

watch(page, async () => {
  await searchManuals();
})

watch(perPage, async () => {
  await searchManuals();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchManuals();
  }
})

const resetForm = () => {
  file.value = null;
  form.value = {
    title: '',
    description: '',
    manualFile: {
      originalName: '',
      extension: '',
      size: ''
    }
  }
}

const searchManuals = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getManuals({
      equipmentId: equipmentId.value,
      title: searchForm.value.title,
      description: searchForm.value.description,
      manualTypeId: searchForm.value.manualTypeId,
      originalName: searchForm.value.originalName,
      extension: searchForm.value.extension,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value,
      sortBy: sortBy.value?.length ? sortBy.value[0] : null
    })
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const createManual = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;

    const formData = new FormData();
    formData.append('file', file.value);
    for (const [key, value] of Object.entries(form.value)) {
      formData.append(key, value);
    }
    formData.append('equipmentId', equipmentId.value);

    const { message } = await create(formData);
    notify(message, 'success');
    await getManuals({ equipmentId: equipmentId.value });
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getManual = async (id) => {
  try {
    const data = await get(id);
    form.value = data
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  }
}

const updateManual = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await update(
      form.value.id,
      {
        equipmentId: equipmentId.value,
        ...form.value
      }
    );
    notify(message, 'success');
    await getManuals({ equipmentId: equipmentId.value });
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteManual = async () => {
  try {
    loading.value = true;
    const { message } = await remove(form.value.id)
    notify(message, 'success');
    await getManuals({ equipmentId: equipmentId.value });
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const allowedMimeTypes = [
  'image/jpeg',
  'image/png',
  'image/webp',
  'image/svg+xml',
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
];

const fileRules = [
  (value) => {
    if (!value) return t('manuals.rules.fileRequired')
    if (!allowedMimeTypes.includes(value.type)) return t('manuals.rules.invalidFileType')
    return true
  }
]

const manualTypeRequired = (v) => !!v || t('manuals.rules.typeRequired');
const titleRequired = (v) => !!v || t('manuals.rules.titleRequired');
</script>