<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('categories.title', 2) }}</p>
        <div>
          <client-only>
            <v-btn v-if="$ability.can('create', 'categories')" class="me-2" icon="mdi-plus" size="small" variant="text"
              @click="createDialog = !createDialog" />
            <v-btn v-if="$ability.can('read', 'categories')" class="me-2" icon="mdi-magnify" size="small" variant="text"
              @click="searchDialog = !searchDialog" />
          </client-only>
        </div>
      </v-card-title>
      <v-card-text>
        <client-only>
          <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
            :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" :loading="loading">
            <template v-slot:item.option="{ item }">
              <div class="d-flex align-center justify-center ga-2">
                <v-btn v-if="$ability.can('update', 'categories')" class="my-2 bg-primary" size="small"
                  icon="mdi-pencil" @click="getCategory(item.id)" />
                <v-btn v-if="isAdmin" class="bg-info" size="small" icon="mdi-file-cancel"
                  @click="async () => { categoryId = item.id; await getReasons({ categoryId: item.id }); reasonsDialog = true }" />
                <v-btn v-if="$ability.can('delete', 'categories')" class="my-2 bg-red" size="small" icon="mdi-trash-can"
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
          {{ $t('categories.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createCategory">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('categories.name')"
                :rules="[nameRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.slug" hide-details="auto" :label="$t('categories.slug')"
                :rules="[slugRequired]" counter="50" maxlength="50"
                @input="() => form.slug = $generateSlug(form.slug)" />
            </v-col>
            <v-col class="text-end">
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
          {{ $t('categories.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateCategory">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('categories.name')"
                :rules="[nameRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.slug" hide-details="auto" :label="$t('categories.slug')"
                :rules="[slugRequired]" counter="50" maxlength="50"
                @input="() => form.slug = $generateSlug(form.slug)" />
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
          {{ $t('categories.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('categories.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined" :disabled="loading">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteCategory" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="700" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('categories.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchCategories(1, 15);
          searchDialog = false;
        }">
          <v-row dense>
            <v-col cols="6">
              <v-text-field v-model="searchForm.name" :label="$t('categories.name')" hide-details="auto" clearable
                counter="50" maxlength="50" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.slug" :label="$t('categories.slug')" hide-details="auto" clearable
                counter="50" maxlength="50" />
            </v-col>
            <v-col class="text-end" cols="12">
              <v-btn class="bg-primary" type="submit" @mousedown.prevent :loading="loading">{{ $t('search') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <CategoriesReasons />
</template>

<script setup>
import { ref, computed, watch, onBeforeMount, } from 'vue'
import { useI18n } from 'vue-i18n'

const { isAdmin } = useProfile();
const { back } = useBack()
const { notify } = useSnackbar();
const { $ability, $generateSlug } = useNuxtApp();
const { t } = useI18n();
const { items, total, getCategories } = useCategories();
const { categoryId, reasonsDialog, getReasons } = useReasons();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('categories.title', 2)}`
})

const loading = ref(false);
const searchDialog = ref(false);
const createDialog = ref(false);
const page = ref(1);
const perPage = ref(15);
const sortBy = ref(null);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref();
const updateForm = ref();
const form = ref({
  name: '',
  slug: '',
})
const searchForm = ref({
  name: '',
  slug: '',
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  const defaultHeaders = [
    { title: t('categories.name'), key: 'name' },
    { title: t('categories.slug'), key: 'slug' }
  ];

  if ($ability.can('update', 'categories') || $ability.can('delete', 'categories')) {
    defaultHeaders.push({ title: t('options'), key: 'option', align: 'center', sortable: false })
  }

  return defaultHeaders;
})

watch(createDialog, (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
})

watch(updateDialog, (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
    return;
  }
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await searchCategories();
})

watch(perPage, async () => {
  await searchCategories();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchCategories();
  }
})

watch(() => form.value.name, (v) => {
  form.value.slug = $generateSlug(v);
})

onBeforeMount(async () => {
  if ($ability.can('read', 'categories')) {
    await getCategories({});
    return;
  }
  back();
})

const resetForm = () => {
  form.value = {
    name: '',
    slug: ''
  }
}

const searchCategories = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getCategories({
      name: searchForm.value.name,
      slug: searchForm.value.slug,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value,
      sortBy: sortBy.value?.length ? sortBy.value[0] : null
    })
  } catch (err) { }
  finally {
    loading.value = false;
  }
}

const getCategory = async (id) => {
  try {
    const category = await $api(`/api/categories/${id}`, {
      method: 'GET'
    })
    form.value = category
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  }
}

const createCategory = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/categories/', {
      method: 'POST',
      body: form.value
    })
    notify(message, 'success');
    await getCategories({})
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateCategory = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await $api(`/api/categories/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await getCategories({})
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteCategory = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/categories/${this.form.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getCategories({})
    deleteDialog.value = false
    resetForm()
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

// Rules
const nameRequired = (v) => !!v || t('categories.rules.nameRequired');
const slugRequired = (v) => !!v || t('categories.rules.slugRequired');

</script>
