<template>
  <v-dialog v-model="dialog" max-width="900" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('distributors.aligners.title', 2) }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="dialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="pb-2">
        <v-row class="ma-0 mb-2">
          <v-spacer />
          <v-btn class="me-2" icon="mdi-reload" size="x-small" @click="refreshAligners" :disabled="loading" />
          <v-btn class="me-2" icon="mdi-plus" size="x-small" @click="createDialog = !createDialog"
            :disabled="loading" />
          <v-btn class="me-2" icon="mdi-file-document-plus" size="x-small" @click="fileDialog = !fileDialog"
            :disabled="loading" />
          <v-btn icon="mdi-magnify" size="x-small" @click="searchDialog = !searchDialog" :disabled="loading" />
        </v-row>
        <client-only>
          <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
            :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" :loading="loading"
            density="compact">
            <template v-slot:item.vCreatedAt="{ item }">
              <v-chip class="text-caption my-2">
                {{ $dateFormat(new Date(item.vCreatedAt)) }}
              </v-chip>
            </template>
            <template v-slot:item.option="{ item }">
              <div class="d-flex align-center justify-center ga-2">
                <v-btn class="my-1 bg-secondary" size="x-small" icon="mdi-eye"
                  @click="async () => { serialNumber = item.serial; await getAligner() }"
                  :loading="serialNumber == item.serial && loading" />
                <v-btn class="my-1 bg-red" size="x-small" icon="mdi-trash-can"
                  @click="form.id = item.id; deleteDialog = true" />
              </div>
            </template>

          </v-data-table-server>
        </client-only>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="600" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('distributors.aligners.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createAligner">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.serial" hide-details="auto" :label="$t('distributors.aligners.serial')"
                :rules="[serialRequired]" counter="50" maxlength="50" autocomplete="off" />
            </v-col>
            <v-col class="mt-3 text-end" cols="12">
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

  <!-- File Dialog -->
  <v-dialog v-model="fileDialog" max-width="700" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('distributors.aligners.file.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="fileDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="fileForm" v-model="fileModel" @submit.prevent="validateAlignersFile">
          <v-row dense>
            <v-col cols="12">
              <v-file-input v-model="file" :prepend-icon="null" prepend-inner-icon="mdi-paperclip" hide-details="auto"
                :label="$t('distributors.aligners.file.label')" chips :rules="fileRequired" accept=".txt" />
            </v-col>
            <v-col cols="12">
              <v-data-table :items="validationItems" :headers="validationHeaders" :loading="validationLoading"
                density="compact">
                <template v-slot:item.serial="{ item }">
                  <v-chip class="text-caption my-2">
                    {{ item.serial }}
                  </v-chip>
                </template>
                <template v-slot:item.message="{ item }">
                  <v-chip class="text-caption" :class="`bg-${item.messageType}`">
                    {{ item.message }}
                  </v-chip>
                </template>
                <template v-slot:item.option="{ item, index }">
                  <div class="d-flex align-center justify-center ga-2">
                    <v-btn class="my-1 bg-red" size="x-small" icon="mdi-trash-can"
                      @click="validationItems.splice(index, 1)" />
                  </div>
                </template>
              </v-data-table>
            </v-col>
            <v-col class="mt-3 text-end d-flex ga-2 justify-end" cols="12">
              <v-btn variant="outlined" size="small" @click="fileDialog = false" @mousedown.prevent
                :disabled="validationLoading">
                {{ $t('cancel') }}
              </v-btn>
              <v-btn class="bg-secondary" size="small" type="submit" @mousedown.prevent :disabled="validationLoading">
                {{ $t('distributors.aligners.validate') }}
              </v-btn>
              <v-btn v-if="validationItems.length" class="bg-primary" size="small" @mousedown.prevent
                :disabled="validationLoading || canConfirm" @click="uploadMultipleAligners">
                {{ $t('confirm') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('distributors.aligners.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchAligners(1, 15);
          searchDialog = false;
        }">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="searchForm.serial" :label="$t('distributors.aligners.serial')" hide-details="auto"
                counter="50" maxlength="50" clearable autocomplete="off" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="searchForm.software" :label="$t('distributors.aligners.software')"
                hide-details="auto" counter="50" maxlength="50" clearable autocomplete="off" />
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

  <!-- Delete Dialog -->
  <v-dialog v-model="deleteDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('distributors.aligners.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center">
        <p class="text-subtitle-1 mb-3 text-center">{{ $t('distributors.aligners.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" size="small" variant="outlined" :disabled="loading">
          {{ $t('cancel') }}
        </v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteAligner" class="bg-red" size="small" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <AlignersModal />
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { notify } = useSnackbar();
const { t } = useI18n();

const { serialNumber, getAligner: getAlignerData, getLastVersion, viewAligner } = useAligners();
const {
  items,
  total,
  getAligners,
  dialog,
  distributorId
} = useDistributorsAligners();

const loading = ref(false)
const searchDialog = ref(false)
const createDialog = ref(false)
const fileDialog = ref(false)

const validationItems = ref([]);
const validationLoading = ref(false);

const page = ref(1)
const perPage = ref(15)
const sortBy = ref(null)

const deleteDialog = ref(false)

const createModel = ref(false)
const fileModel = ref(false)
const createForm = ref()
const fileForm = ref()
const file = ref(null);
const form = ref({
  serial: ''
})
const searchForm = ref({
  serial: '',
  software: '',
})

const resetForm = () => {
  form.value = {
    serial: '',
  }
  file.value = null;
  validationItems.value = [];
}

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: t('distributors.aligners.serial'), key: 'serial' },
  { title: t('distributors.aligners.software'), align: 'center', key: 'software' },
  { title: t('distributors.aligners.specs'), align: 'center', key: 'specs', sortable: false },
  { title: t('distributors.aligners.createdAt'), align: 'center', key: 'vCreatedAt' },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

const validationHeaders = computed(() => [
  { title: t('distributors.aligners.serial'), key: 'serial', sortable: false },
  { title: t('distributors.aligners.message'), align: 'center', key: 'message', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

const canConfirm = computed(() => {
  return validationItems.value.findIndex((e) => e.messageType !== 'success') !== -1;
})

watch(createDialog, (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
})

watch(fileDialog, (val) => {
  if (!val) {
    fileForm.value.reset();
    resetForm();
    return;
  }
})

watch(deleteDialog, (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await searchAligners();
})

watch(perPage, async () => {
  await searchAligners();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchAligners();
  }
})

watch(viewAligner, (v) => {
  if (!v) serialNumber.value = false;
})

const searchAligners = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getAligners({
      serial: searchForm.value.serial,
      software: searchForm.value.software,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value,
      sortBy: sortBy.value?.length ? sortBy.value[0] : null
    });
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const createAligner = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/distributors/aligners', {
      method: 'POST',
      body: {
        distributorId: distributorId.value,
        ...form.value
      }
    })
    notify(message, 'success');
    await getAligners({});
    createDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const validateAlignersFile = async () => {
  try {
    validationLoading.value = true;
    if (!fileModel.value) return;

    const formData = new FormData();
    formData.append('file', file.value);
    const { validations } = await $api(`/api/distributors/aligners/file/${distributorId.value}`, {
      method: 'PUT',
      body: formData
    })
    validationItems.value = validations
  } catch (err) {
    notify(err, 'error');
  } finally {
    validationLoading.value = false;
  }
}

const deleteAligner = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/distributors/aligners/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getAligners({});
    deleteDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const refreshAligners = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/distributors/aligners/refresh/${distributorId.value}`, { method: 'POST', })
    notify(message, 'success');
    await getAligners({});
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}


const uploadMultipleAligners = async () => {
  try {
    validationLoading.value = true;
    const { message } = await $api(`/api/distributors/aligners/file/${distributorId.value}`, {
      method: 'POST',
      body: {
        serials: validationItems.value
      }
    })
    notify(message, 'success');
    await getAligners({});
    fileDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    validationLoading.value = false;
  }
}


const getAligner = async () => {
  try {
    loading.value = true;
    await getLastVersion();
    await getAlignerData();
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}


const serialRequired = (v) => !!v || t('distributors.aligners.rules.serialRequired');
const fileRequired = [
  (v) => !!v || t('distributors.aligners.rules.fileRequired'),
  (v) => v.size !== 0 || t('distributors.aligners.rules.fileSize0')
];

</script>