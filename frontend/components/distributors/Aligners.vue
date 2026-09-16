<template>
  <v-dialog v-model="dialog" max-width="900" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('distributors.aligners.title', 2) }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="closeDialog" />
        </v-row>
      </v-card-title>
      <v-card-text class="pb-2">
        <v-row class="ma-0 mb-2">
          <v-spacer />
          <v-tooltip :text="$t('tooltip.refresh')" :disabled="loading" location="bottom">
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" class="me-2" icon="mdi-reload" size="x-small" @click="getAllAligners"
                :disabled="loading" />
            </template>
          </v-tooltip>

          <v-tooltip :text="$t('aligners.tooltip.add')" :disabled="loading" location="bottom">
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" class="me-2" icon="mdi-plus" size="x-small" @click="createDialog = !createDialog"
                :disabled="loading" />
            </template>
          </v-tooltip>

          <v-tooltip :text="$t('aligners.tooltip.addMultiple')" :disabled="loading" location="bottom">
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" class="me-2" icon="mdi-file-document-plus" size="x-small"
                @click="fileDialog = !fileDialog" :disabled="loading" />
            </template>
          </v-tooltip>
        </v-row>
        <v-data-table :items="items" :headers="headers" :loading="loading" density="compact">
          <template v-slot:item.alias="{ item }">
            <div v-if="item.alias" class="d-flex align-center justify-center">
              <span class="w-100 d-inline-block bg-grey-darken-1 py-1 px-2 rounded-pill text-caption text-center"
                style="max-width: 150px; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; background-color: rgb(228, 228, 228) !important; color: black !important;"
                :title="item.alias">
                {{ item.alias }}
              </span>
            </div>
            <span v-else>-</span>
          </template>
          <template v-slot:item.createdAt="{ item }">
            <v-chip class="text-caption my-2">
              {{ $dateFormat(new Date(item.createdAt)) }}
            </v-chip>
          </template>
          <template v-slot:item.option="{ item }">
            <div class="d-flex align-center justify-center ga-2">
              <v-tooltip :text="$t('aligners.tooltip.setAlias')" :disabled="loading" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" class="my-1 bg-secondary" size="x-small" icon="mdi-pencil"
                    @click="alignerId = item.id; aliasDialog = true" :disabled="loading" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('aligners.tooltip.viewAligner')" :disabled="loading" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" class="my-1 bg-secondary" size="x-small" icon="mdi-eye"
                    @click="async () => { serialNumber = item.serialNumber; await getAligner() }" :disabled="loading"
                    :loading="serialNumber == item.serialNumber && loading" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('aligners.tooltip.unlink')" :disabled="loading" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" class="my-1 bg-red" size="x-small" icon="mdi-trash-can" :disabled="loading"
                    @click="form.id = item.id; deleteDialog = true" />
                </template>
              </v-tooltip>
            </div>
          </template>

        </v-data-table>
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
                density="compact" v-model:page="validationPage" v-model:items-per-page="validationPerPage">
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
                <template v-slot:item.option="{ item, index, }">
                  <div class="d-flex align-center justify-center ga-2">
                    <v-tooltip :text="$t('tooltip.remove')" location="bottom">
                      <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" class="my-1 bg-red" size="x-small" icon="mdi-trash-can" @click="removeSerial(index)" />
                      </template>
                    </v-tooltip>
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

  <!-- Set Alias for Aligner Dialog -->
  <v-dialog v-model="aliasDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('aligners.alias.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="aliasDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center">
        <v-row no-gutters>
          <v-col cols="12" class="mb-4">
            <v-text-field v-model="alias" :label="$t('aligners.alias.label')" hide-details="auto" counter="30"
              maxlength="30" />
          </v-col>
          <v-col cols="12" class="d-flex justify-end align-center ga-2">
            <v-btn @click="aliasDialog = false" size="small" variant="outlined" :disabled="loading">
              {{ $t('cancel') }}
            </v-btn>
            <v-btn @click="setAlignerAlias" class="bg-primary" size="small" :loading="loading">
              {{ $t('confirm') }}
            </v-btn>
          </v-col>
        </v-row>
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
const { dialog, distributorId } = useDistributorsAligners();

const loading = ref(false)
const createDialog = ref(false)
const fileDialog = ref(false)
const deleteDialog = ref(false)
const aliasDialog = ref(false);

const validationItems = ref([]);
const validationLoading = ref(false);

const validationPage = ref(1);
const validationPerPage = ref(10);

const alignerId = ref('');
const alias = ref('');
const abortController = ref(null);
const items = ref([]);
const createModel = ref(false)
const fileModel = ref(false)
const createForm = ref()
const fileForm = ref()
const file = ref(null);
const form = ref({
  serial: ''
})

const headers = computed(() => [
  { title: t('distributors.aligners.serial'), key: 'serialNumber' },
  { title: t('aligners.alias.label'), align: 'center', key: 'alias', sortable: false },
  { title: t('distributors.aligners.software'), align: 'center', key: 'software' },
  { title: t('distributors.aligners.specs'), align: 'center', key: 'specs', sortable: false },
  { title: t('distributors.aligners.createdAt'), align: 'center', key: 'createdAt' },
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

watch(viewAligner, (v) => {
  if (!v) serialNumber.value = false;
})

watch(dialog, async (v) => {
  if (!v) return;
  await getAllAligners();
})

const resetForm = () => {
  form.value = {
    serial: '',
  }
  file.value = null;
  validationItems.value = [];
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
    await getAllAligners();
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
    await getAllAligners();
    deleteDialog.value = false;
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
    await getAllAligners();
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

const removeSerial = (index) => {
  validationItems.value.splice((index + (validationPerPage.value * (validationPage.value - 1))), 1)
}

const getAllAligners = async () => {
  try {
    loading.value = true;
    items.value = [];
    abortController.value = new AbortController();

    const response = await $api(`/api/distributors/aligners/${distributorId.value}`, {
      method: 'GET',
      responseType: 'stream',
      signal: abortController.value.signal
    });

    const reader = response.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split('\n\n');
      buffer = events.pop();

      for (const event of events) {
        if (event.trim().startsWith('data:')) {
          const dataStr = event.replace(/^data:/, '').trim();
          if (dataStr) {
            const aligner = JSON.parse(dataStr);
            let specs = null;
            if (aligner.specs) {
              specs = `${aligner?.specs?.name} ${aligner?.specs?.month}/${aligner?.specs?.year}`
            }
            const formattedAligner = {
              ...aligner,
              specs,
              software: aligner.version.semantic,
            };
            items.value.push(formattedAligner);
          };
        }
      }
    }

  } catch (err) {
    if (err.name === 'AbortError' || err.cause?.name === 'AbortError') {
      return;
    }
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const setAlignerAlias = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/distributors/aligners/alias/${alignerId.value}`, {
      method: 'POST',
      body: {
        alias: alias.value
      }
    })
    notify(message, 'success');
    aliasDialog.value = false;
    await getAllAligners();
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const closeDialog = () => {
  dialog.value = false;
  if (abortController.value) abortController.value.abort();
}

const serialRequired = (v) => !!v || t('distributors.aligners.rules.serialRequired');
const fileRequired = [
  (v) => !!v || t('distributors.aligners.rules.fileRequired'),
  (v) => v.size !== 0 || t('distributors.aligners.rules.fileSize0')
];

</script>