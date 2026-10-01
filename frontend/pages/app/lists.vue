<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('lists.title', 2) }}</p>
        <div>
          <client-only>
            <v-tooltip :text="$t('tooltip.create')" :disabled="loading" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('create', 'lists')" class="me-2" icon="mdi-plus" size="small"
                  variant="text" @click="createDialog = !createDialog" :disabled="loading" />
              </template>
            </v-tooltip>

            <v-tooltip :text="$t('tooltip.search')" :disabled="loading" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('read', 'lists')" class="me-2" icon="mdi-magnify" size="small"
                  variant="text" @click="searchDialog = !searchDialog" :disabled="loading" />
              </template>
            </v-tooltip>
          </client-only>
        </div>
      </v-card-title>
      <v-card-text>
        <client-only>
          <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
            :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" :loading="loading">
            <template v-slot:item.isMain="{ item }">
              <v-icon v-if="item.isMain" icon="mdi-check-bold" color="success"></v-icon>
            </template>
            <template v-slot:item.option="{ item }">
              <div class="d-flex justify-center align-center ga-2">
                <v-tooltip :text="$t('tooltip.viewUpdate')" :disabled="loading" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" class="my-2 bg-primary" size="small" icon="mdi-pencil"
                      @click="getList(item.id)" :loading="loading && listId === item.id" :disabled="loading" />
                  </template>
                </v-tooltip>

                <v-tooltip :text="$t('tooltip.delete')" :disabled="loading" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" v-if="!item.isMain" class="my-2 bg-red" size="small" icon="mdi-trash-can"
                      @click="form.id = item.id; deleteDialog = true" :disabled="loading" />
                  </template>
                </v-tooltip>
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
          {{ $t('lists.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createList">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('lists.name')" :rules="[nameRequired]"
                counter="30" maxlength="30" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.distributorsIds" :label="$t('lists.distributors')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" clearable multiple chips
                :rules="[distributorsRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getDistributors({ distributorsIds: form.distributorsIds, name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('lists.users')" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" clearable multiple chips :rules="[usersRequired]" @update:search="(fullName) => {
                  if (!createDialog) return;
                  getUsers({ usersIds: form.usersIds, fullName });
                }" />
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
          {{ $t('lists.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateList">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('lists.name')" :rules="[nameRequired]"
                :readonly="form.isMain" counter="30" maxlength="30" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.distributorsIds" :label="$t('lists.distributors')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" :clearable="!form.isMain" multiple chips
                :rules="[distributorsRequired]" :readonly="form.isMain" @update:search="(name) => {
                  if (!updateDialog) return;
                  getDistributors({ distributorsIds: form.distributorsIds, name });
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('lists.users')" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" :clearable="!form.isMain" multiple chips :rules="[usersRequired]"
                :readonly="form.isMain" @update:search="(fullName) => {
                  if (!updateDialog) return;
                  getUsers({ usersIds: form.usersIds, fullName });
                }" />
            </v-col>
            <v-col v-if="!form.isMain" class="text-end">
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
          {{ $t('lists.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('lists.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined" :disabled="loading">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteList" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('lists.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="doSearch">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('lists.search.message')" hide-details="auto"
                prepend-inner-icon="mdi-magnify" clearable />
            </v-col>
            <v-col class="text-end" cols="12">
              <v-btn class="bg-primary" type="submit" @mousedown.prevent :loading="loading">{{ $t('search') }}</v-btn>
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
const { $ability } = useNuxtApp();
const { t } = useI18n();
const { items: users, getUsers } = useUsers();
const { items: distributors, getDistributors } = useDistributors();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('installations.title', 2)}`
})

const loading = ref(false);
const listId = ref(null);
const searchDialog = ref(false);
const createDialog = ref(false);
const items = ref([]);
const search = ref('');
const page = ref(1);
const perPage = ref(15);
const sortBy = ref(null);
const total = ref(15);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref();
const updateForm = ref();
const form = ref({
  name: '',
  distributorsIds: [],
  usersIds: [],
  slug: ''
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: t('lists.name'), key: 'name', sortable: !loading.value },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm()
    return;
  }
  await getDistributors({});
  await getUsers({});
})

watch(updateDialog, async (val) => {
  if (!val) {
    listId.value = null;
    updateForm.value.reset();
    resetForm()
    return;
  }
  await getDistributors({
    distributorsIds: form.value.distributorsIds
  });
  await getUsers({
    usersIds: form.value.usersIds
  });
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await getLists();
})

watch(perPage, async () => {
  await getLists();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await getLists();
  }
})

onBeforeMount(async () => {
  if ($ability.can('read', 'lists')) {
    await getLists();
    return;
  }
  back();
})

const resetForm = () => {
  form.value = {
    name: '',
    slug: '',
    distributorsIds: [],
    usersIds: [],
  }
}

const getLists = async () => {
  try {
    loading.value = true;
    const data = await $api('/api/lists/search', {
      body: {
        search: search.value,
        page: page.value,
        perPage: perPage.value,
        sortBy: sortBy.value?.length ? sortBy.value[0] : null
      },
      method: 'POST'
    })
    items.value = data.items
    total.value = data.total
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getList = async (id) => {
  try {
    loading.value = true;
    listId.value = id;
    const data = await $api(`/api/lists/${id}`, {
      method: 'GET'
    })
    form.value = data
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const createList = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/lists/', {
      method: 'POST',
      body: form.value
    })
    notify(message, 'success');
    await getLists()
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateList = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await $api(`/api/lists/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await getLists()
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteList = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/lists/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getLists()
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const doSearch = async () => {
  try {
    loading.value = true;
    page.value = 1
    perPage.value = 15
    await getLists()
    searchDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

// Rules
const nameRequired = (v) => !!v || t('lists.rules.nameRequired');
const distributorsRequired = (v) => (v && v.length > 0) || t('lists.rules.distributorsRequired');
const usersRequired = (v) => (v && v.length > 0) || t('lists.rules.usersRequired');

</script>
