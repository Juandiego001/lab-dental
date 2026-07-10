<template>
  <v-dialog v-model="reasonsDialog" max-width="900" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('reasons.title', 2) }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="reasonsDialog = false" />
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
              <template v-if="isAdmin">
                <v-btn class="bg-primary" size="x-small" icon="mdi-pencil" @click="getReason(item.id)" />
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
          {{ $t('reasons.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createReason">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('reasons.name')"
                :rules="[nameRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.slug" hide-details="auto" :label="$t('reasons.slug')"
                :rules="[slugRequired]" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.description" hide-details="auto" :label="$t('reasons.description')" />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="createDialog = false">{{ $t('cancel') }}</v-btn>
              <span class="mx-1" />
              <v-btn type="submit" class="bg-primary">{{ $t('confirm') }}</v-btn>
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
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateReason">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('reasons.name')"
                :rules="[nameRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.slug" hide-details="auto" :label="$t('reasons.slug')"
                :rules="[slugRequired]" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.description" hide-details="auto" :label="$t('reasons.description')" />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="updateDialog = false">{{ $t('cancel') }}</v-btn>
              <span class="mx-1" />
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
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('reasons.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-4">
        <p class="text-subtitle-1 mb-2 text-center">
          {{ $t('reasons.delete.message') }}
        </p>
        <v-btn @click="deleteDialog = false" size="small" variant="outlined" :disabled="loading">
          {{ $t('cancel') }}
        </v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteReason" class="bg-red" size="small" :loading="loading">
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
          {{ $t('reasons.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchReasons(1, 15);
          searchDialog = false
        }">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('reasons.search.fields')" hide-details="auto"
                prepend-inner-icon="mdi-magnify" clearable />
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
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n();
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { isAdmin } = useProfile();
const { items, total, categoryId, reasonsDialog, getReasons, get, create, update, remove } = useReasons();

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
  name: '',
  slug: '',
  description: ''
})
const searchForm = ref({
  name: null,
  slug: null,
  description: null
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  return [
    { title: t('reasons.name'), key: 'name' },
    { title: t('reasons.slug'), key: 'slug' },
    { title: t('options'), key: 'option', align: 'center', sortable: false }
  ]
})

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

watch(searchDialog, async (val) => {
  if (!val) return;
})

watch(page, async () => {
  await searchReasons();
})

watch(perPage, async () => {
  await searchReasons();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchReasons();
  }
})

const resetForm = () => {
  form.value = {
    name: '',
    slug: '',
    description: ''
  }
}

const searchReasons = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getReasons({
      categoryId: categoryId.value,
      name: searchForm.value.name,
      slug: searchForm.value.slug,
      description: searchForm.value.description,
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

const createReason = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await create({ categoryId: categoryId.value, ...form.value });
    notify(message, 'success');
    await getReasons({ categoryId: categoryId.value });
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getReason = async (id) => {
  try {
    const data = await get(id);
    form.value = data
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  }
}

const updateReason = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await update(
      form.value.id,
      {
        categoryId: categoryId.value,
        ...form.value
      }
    );
    notify(message, 'success');
    await getReasons({ categoryId: categoryId.value });
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteReason = async () => {
  try {
    loading.value = true;
    const { message } = await remove(form.value.id)
    notify(message, 'success');
    await getReasons({ categoryId: categoryId.value });
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const nameRequired = (v) => !!v || t('reasons.rules.nameRequired');
const slugRequired = (v) => !!v || t('reasons.rules.slugRequired');
</script>