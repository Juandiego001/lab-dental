<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('reasons.title', 2) }}</p>
        <div>
          <client-only>
            <v-tooltip :text="$t('tooltip.create')" :disabled="loading" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('create', 'reasons')" class="me-2" icon="mdi-plus" size="small"
                  variant="text" @click="createDialog = !createDialog" :disabled="loading" />
              </template>
            </v-tooltip>

            <v-tooltip :text="$t('tooltip.search')" :disabled="loading" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('read', 'reasons')" class="me-2" icon="mdi-magnify"
                  size="small" variant="text" @click="searchDialog = !searchDialog" :disabled="loading" />
              </template>
            </v-tooltip>
          </client-only>
        </div>
      </v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :loading="loading" :disable-sort="loading"
          :hide-default-footer="loading">
          <template v-slot:item.option="{ item }">
            <div class="d-flex align-center justify-center ga-2">
              <v-tooltip :text="$t('tooltip.viewUpdate')" :disabled="loading" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" class="my-2 bg-primary" size="small" icon="mdi-pencil"
                    @click="getReason(item.id)" :loading="loading && reasonId === item.id" :disabled="loading" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('tooltip.delete')" :disabled="loading" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" class="my-2 bg-red" size="small" icon="mdi-trash-can"
                    @click="form.id = item.id; deleteDialog = true" :disabled="loading" />
                </template>
              </v-tooltip>
            </div>
          </template>
        </v-data-table-server>
      </v-card-text>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('reasons.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createReason">
          <v-row dense>
            <v-col cols="12">
              <v-autocomplete v-model="form.categoryId" :label="$t('categories.title', 1)" :items="categories"
                item-title="name" item-value="id" hide-details="auto" :rules="[categoryRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getCategories({ name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('reasons.name')"
                :rules="[nameRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.slug" hide-details="auto" :label="$t('reasons.slug')" :rules="[slugRequired]"
                @input="(v) => form.slug = $generateSlug(v)" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.description" hide-details="auto" :label="$t('reasons.description')" />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="createDialog = false" :disabled="loading">{{ $t('cancel') }}</v-btn>
              <span class="mx-1" />
              <v-btn type="submit" class="bg-primary" :loading="loading" :disabled="loading">{{ $t('confirm') }}</v-btn>
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
          {{ $t('reasons.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateReason">
          <v-row dense>
            <v-col cols="12">
              <v-autocomplete v-model="form.categoryId" :label="$t('categories.title', 1)" :items="categories"
                item-title="name" item-value="id" hide-details="auto" :rules="[categoryRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getCategories({ name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('reasons.name')"
                :rules="[nameRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.slug" hide-details="auto" :label="$t('reasons.slug')" :rules="[slugRequired]"
                @input="() => form.slug = $generateSlug(form.slug)" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.description" hide-details="auto" :label="$t('reasons.description')" />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="updateDialog = false" :disabled="loading">{{ $t('cancel') }}</v-btn>
              <span class="mx-1" />
              <v-btn type="submit" class="bg-primary" :loading="loading" :disabled="loading">{{ $t('confirm') }}</v-btn>
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
          {{ $t('reasons.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('reasons.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteReason" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('reasons.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
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
import { ref, computed, watch, onBeforeMount } from 'vue'
import { useI18n } from 'vue-i18n'

const { back } = useBack()
const { notify } = useSnackbar();
const { $ability, $generateSlug } = useNuxtApp();
const { t } = useI18n();
const { items, total, getReasons, create, update, remove } = useReasons();
const { items: categories, getCategories } = useCategories();

const loading = ref(false);
const reasonId = ref(null);
const page = ref(1);
const perPage = ref(15);
const sortBy = ref(null);

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('reasons.title', 2)}`
})


const search = ref('');
const createDialog = ref(false);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const searchDialog = ref(false);
const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref(false);
const updateForm = ref(false);
const form = ref({
  id: '',
  name: '',
  slug: ''
})
const searchForm = ref({
  categoryId: null,
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

const headers = computed(() => [
  { title: t('reasons.name'), key: 'name', align: 'start', sortable: false },
  { title: t('reasons.slug'), key: 'slug', align: 'center', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
  await getCategories({});
})

watch(updateDialog, async (val) => {
  if (!val) {
    reasonId.value = null;
    updateForm.value.reset();
    resetForm();
    return;
  }
  await getCategories({ categoryId: form.value.categoryId });
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
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

watch(() => form.value.name, (v) => {
  form.value.slug = $generateSlug(v);
})

onBeforeMount(async () => {
  if ($ability.can('read', 'reasons')) {
    await searchReasons();
    return;
  }
  back();
})

const resetForm = () => {
  form.value = {
    id: '',
    name: '',
    slug: ''
  }
}

const formatManualSlug = () => {
  form.value.slug = $generateSlug(form.value.slug);
}

const searchReasons = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getReasons({
      categoryId: searchForm.value.categoryId,
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

const getReason = async (id) => {
  try {
    loading.value = true;
    reasonId.value = id;
    const user = await $api(`/api/reasons/${id}`, {
      method: 'GET'
    })
    form.value = user
    updateDialog.value = true
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
    const { message } = await create(form.value);
    notify(message, 'success');
    await getReasons({})
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateReason = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await update(form.value.id, form.value);
    notify(message, 'success');
    await getReasons({})
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
    const { message } = await remove(form.value);
    notify(message, 'success');
    await getReasons({})
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

// Rules
const nameRequired = (v) => !!v || t('reasons.rules.nameRequired');
const slugRequired = (v) => !!v || t('reasons.rules.slugRequired');
const categoryRequired = (v) => !!v || t('equipments.rules.categoryRequired');

</script>
