<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('lists.title', 2) }}</v-card-title>
      <v-card-text>
        <client-only>
          <v-data-table :items="items" :headers="headers" :page="page" :items-per-page="perPage" :items-length="total"
            :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" :disable-sort="true">
            <template v-slot:item.isMain="{ item }">
              <v-icon v-if="item.isMain" icon="mdi-check-bold" color="success"></v-icon>
            </template>
            <template v-slot:item.option="{ item }">
              <div class="d-flex justify-center align-center ga-2">
                <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getList(item.id)"></v-btn>
                <v-btn v-if="!item.isMain" class="my-2 bg-red" size="small" icon="mdi-trash-can"
                  @click="form.id = item.id; deleteDialog = true"></v-btn>
              </div>
            </template>
          </v-data-table>
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
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createList">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('lists.name')"
                :rules="[nameRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.distributorsIds" :label="$t('lists.distributors')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors" clearable
                multiple chips :rules="[distributorsRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('lists.users')" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" @update:search="getUsers" clearable multiple chips
                :rules="[usersRequired]" />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="createDialog = false">{{ $t('cancel') }}</v-btn>
              <span class="mx-1"></span>
              <v-btn type="submit" class="bg-primary">{{ $t('confirm') }}</v-btn>
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
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateList">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('lists.name')" :rules="[nameRequired]"
                :readonly="form.isMain"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.distributorsIds" :label="$t('lists.distributors')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors"
                :clearable="!form.isMain" multiple chips :rules="[distributorsRequired]" :readonly="form.isMain" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('lists.users')" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" @update:search="getUsers" :clearable="!form.isMain" multiple chips
                :rules="[usersRequired]" :readonly="form.isMain" />
            </v-col>
            <v-col v-if="!form.isMain" class="text-end">
              <v-btn variant="outlined" @click="updateDialog = false">{{ $t('cancel') }}</v-btn>
              <span class="mx-1"></span>
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
        <v-row no-gutters align="center">
          {{ $t('lists.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('lists.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2"></span>
        <v-btn @click="deleteList" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('lists.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <p class="text-subtitle-2 pb-2">{{ $t('lists.search.message') }}</p>
        <v-form @submit.prevent="doSearch">
          <v-row no-gutters="">
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('lists.search.fields')" hide-details="auto"
                prepend-inner-icon="mdi-magnify" clearable></v-text-field>
            </v-col>
            <v-col class="text-end mt-4" cols="12">
              <v-btn class="bg-primary" type="submit">{{ $t('search') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onBeforeMount, useTemplateRef, toRefs } from 'vue'
import { searchMixin } from '~/mixins/searchMixin'
import { createMixin } from '~/mixins/createMixin'
import { useI18n } from 'vue-i18n'

const { back } = useBack()
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { t } = useI18n();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('installations.title', 2)}`
})

const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)
const distributors = ref([]);
const users = ref([]);
const items = ref([]);
const search = ref('');
const page = ref(1);
const perPage = ref(15);
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
  { title: 'Id', key: 'id', align: 'center', sortable: false },
  { title: t('lists.name'), key: 'name', align: 'center', sortable: false },
  { title: t('lists.isMain'), key: 'isMain', align: 'center', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (val) {
    await getDistributors();
    await getUsers();
  } else {
    createForm.value.reset();
    resetForm()
  }
})

watch(updateDialog, async (val) => {
  if (val) {
    await getDistributors();
    await getUsers();
  } else {
    updateForm.value.reset();
    resetForm()
  }
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

const getDistributors = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value) return;
    const data = await $api('/api/lists/distributors', {
      body: {
        search,
        distributorsIds: form.value.distributorsIds
      },
      method: 'POST'
    })
    distributors.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getUsers = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value) return;

    let data;
    if (createDialog.value || (updateDialog.value && !form.value.isMain)) {
      data = await $api('/api/users/admins', {
        body: {
          search,
          usersIds: form.value.usersIds
        },
        method: 'POST'
      })
    }

    if (updateDialog.value && form.value.isMain) {
      data = await $api('/api/lists/users', {
        body: {
          search,
          usersIds: form.value.usersIds
        },
        method: 'POST'
      })
    }

    users.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getLists = async () => {
  try {
    const data = await $api('/api/lists/', {
      query: {
        search: search.value,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    items.value = data.items
    total.value = data.total
  } catch (err) {
    notify(err, 'error');
  }
}

const getList = async (id) => {
  try {
    const data = await $api(`/api/lists/${id}`, {
      method: 'GET'
    })
    form.value = data
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  }
}

const createList = async () => {
  try {
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
  }
}

const updateList = async () => {
  try {
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
  }
}

const deleteList = async () => {
  try {
    const { message } = await $api(`/api/lists/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getLists()
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getLists()
    searchDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

// Rules
const nameRequired = (v) => !!v || t('lists.rules.nameRequired');
const distributorsRequired = (v) => (v && v.length > 0) || t('lists.rules.distributorsRequired');
const usersRequired = (v) => (v && v.length > 0) || t('lists.rules.usersRequired');

</script>
