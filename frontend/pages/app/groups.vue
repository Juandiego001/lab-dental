<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('groups.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="tableHeaders" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getGroup(item.id)"></v-btn>
            <v-btn class="my-2 mx-2 bg-secondary" size="small" icon="mdi-shield-edit"
              @click="form.id = item.id; getPermissions()"></v-btn>
            <v-btn v-if="item.id !== 1" class="my-2 bg-red" size="small" icon="mdi-trash-can"
              @click="form.id = item.id; deleteDialog = true"></v-btn>
          </template>
        </v-data-table-server>
      </v-card-text>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('groups.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" size="small" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createGroup">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('groups.name')"
                :rules="[nameRequired]"></v-text-field>
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors" clearable
                :rules="[distributorRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('users.title', 2)" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" @update:search="getUsers" clearable multiple chips
                :readonly="isAdmin && !form.distributorId" :rules="[usersRequired]" />
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
  <v-dialog v-model="updateDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('groups.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateGroup">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('groups.name')"
                :rules="[nameRequired]"></v-text-field>
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors" clearable
                :rules="[distributorRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('users.title', 2)" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" @update:search="getUsers" clearable multiple chips
                :readonly="isAdmin && !form.distributorId" :rules="[usersRequired]" />
            </v-col>
            <v-col class="text-end">
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
  <v-dialog v-model="deleteDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('groups.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('groups.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2"></span>
        <v-btn @click="deleteGroup" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('groups.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <p class="text-subtitle-2 pb-2">{{ $t('groups.search.message') }}</p>
        <v-form @submit.prevent="doSearch">
          <v-row no-gutters="">
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('groups.search.fields')" hide-details="auto"
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

  <!-- Permissions Dialog -->
  <v-dialog v-model="permissionsDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('groups.permissions.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="permissionsDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-data-table-server :items="itemsPermissions" :headers="headersPermissions" :page="pagePermissions"
          :items-per-page="perPagePermissions" :items-length="totalPermissions"
          :items-per-page-options="itemsPerPageOptions" @update:page="v => pagePermissions = v"
          @update:itemsPerPage="v => perPagePermissions = v" :disable-sort="true" density="compact">
          <template v-slot:item.moduleName="{ item }">
            <span class="text-capitalize">{{ item.moduleName }}</span>
          </template>
          <template v-slot:item.read="{ item }">
            <v-checkbox-btn color="primary" :model-value="item.read" :ripple="false" hide-details="auto"
              density="compact" @update:modelValue="v => updatePermissions(v, item, 'read')"
              :disabled="form.id === 1" />
          </template>
          <template v-slot:item.create="{ item }">
            <v-checkbox-btn color="primary" :model-value="item.create" :ripple="false" hide-details="auto"
              density="compact" @update:modelValue="v => updatePermissions(v, item, 'create')"
              :disabled="form.id === 1" />
          </template>
          <template v-slot:item.update="{ item }">
            <v-checkbox-btn color="primary" :model-value="item.update" :ripple="false" hide-details="auto"
              density="compact" @update:modelValue="v => updatePermissions(v, item, 'update')"
              :disabled="form.id === 1" />
          </template>
          <template v-slot:item.delete="{ item }">
            <v-checkbox-btn color="primary" :model-value="item.delete" :ripple="false" hide-details="auto"
              density="compact" @update:modelValue="v => updatePermissions(v, item, 'delete')"
              :disabled="form.id === 1" />
          </template>
        </v-data-table-server>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onBeforeMount, } from 'vue'
import { toRefs } from 'vue'
import { searchMixin } from '~/mixins/searchMixin'
import { createMixin } from '~/mixins/createMixin'
import { useI18n } from 'vue-i18n'
const { show } = useSnackbar();
const { $ability } = useNuxtApp();
const { profile } = useProfile();
const { t } = useI18n();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('groups.title', 2)}`
})

const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)
const users = ref([]);
const distributors = ref([]);

/* Groups */
const items = ref([]);
const search = ref('');
const page = ref(1);
const perPage = ref(15);
const total = ref(15);

/* Permissions */
const itemsPermissions = ref([]);
const pagePermissions = ref(1);
const perPagePermissions = ref(15);
const totalPermissions = ref(15);

const updateDialog = ref(false);
const deleteDialog = ref(false);
const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref();
const updateForm = ref();
const permissionsDialog = ref(false);
const form = ref({
  name: '',
  distributorId: '',
  distributorName: '',
  usersIds: null
})

const isAdmin = computed(() => profile.value.role === 'ADMIN');

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const tableHeaders = computed(() => {
  if (isAdmin.value) {
    return [
      { title: 'Id', key: 'id', sortable: false },
      { title: t('groups.name'), key: 'name', sortable: false },
      { title: t('distributors.title'), key: 'distributorName', sortable: false },
      { title: t('options'), key: 'option', align: 'center', sortable: false }
    ]
  }

  return [
    { title: 'Id', key: 'id', align: 'center', sortable: false },
    { title: t('groups.name'), key: 'name', align: 'center', sortable: false },
    { title: t('options'), key: 'option', align: 'center', sortable: false }
  ]
})

const headersPermissions = computed(() => [
  { title: t('modules.title'), key: 'moduleName', sortable: false },
  { title: t('groups.permissions.read'), key: 'read', sortable: false },
  { title: t('groups.permissions.create'), key: 'create', sortable: false },
  { title: t('groups.permissions.update'), key: 'update', sortable: false },
  { title: t('groups.permissions.delete'), key: 'delete', sortable: false }
])

watch(createDialog, async (val) => {
  if (val) {
    if (isAdmin) {
      await getDistributors();
    } else {
      await getUsers();
    }
  } else {
    createForm.value.reset();
    resetForm();
  }
})

watch(updateDialog, async (val) => {
  if (val) {
    if (isAdmin.value) await getDistributors(form.value.distributorName);
    await getUsers();
  } else {
    updateForm.value.reset();
    resetForm();
  }
})

watch(() => form.value.distributorId, async (val) => {
  if (val) await getUsers();
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await getGroups();
})

watch(perPage, async () => {
  await getGroups();
})

watch(pagePermissions, async () => {
  await getPermissions();
})

watch(perPagePermissions, async () => {
  await getPermissions();
})

onBeforeMount(async () => {
  if (!$ability.can('read', 'groups')) {
    navigateTo(history.state?.back || '/login');
    return;
  }
  await getGroups();
})

const resetForm = () => {
  form.value = {
    name: '',
    distributorId: '',
    distributorName: '',
    usersIds: null
  }
}

const getGroups = async () => {
  try {
    const data = await $api('/api/groups/', {
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
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getGroup = async (id) => {
  try {
    const data = await $api(`/api/groups/${id}`, {
      method: 'GET'
    })
    form.value = data
    updateDialog.value = true
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const createGroup = async () => {
  try {
    if (!createModel.value) return;
    const { message } = await $api('/api/groups/', {
      method: 'POST',
      body: form.value
    })
    show(message, 'success');
    await getGroups()
    createDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const updateGroup = async () => {
  try {
    if (!updateModel.value) return;
    const { message } = await $api(`/api/groups/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    show(message, 'success');
    await getGroups()
    updateDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const deleteGroup = async () => {
  try {
    const { message } = await $api(`/api/groups/${form.value.id}`, {
      method: 'DELETE'
    })
    show(message, 'success');
    await getGroups()
    deleteDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getGroups()
    searchDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getDistributors = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value) return;
    const data = await $api('/api/distributors/', {
      query: {
        search,
        page: 1,
        perPage: 15
      },
      method: 'GET'
    })
    distributors.value = data.items
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getUsers = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value) return;
    let data;
    if (form.value.distributorId) {
      data = await $api(`/api/distributors/${form.value.distributorId}/users`, {
        query: {
          search,
          page: 1,
          perPage: 15
        },
        method: 'GET'
      })
    } else {
      data = await $api(`/api/users`, {
        query: {
          search,
          page: 1,
          perPage: 15
        },
        method: 'GET'
      })
    }
    users.value = data.items
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getPermissions = async (search) => {
  try {
    const data = await $api(`/api/permissions/groups/${form.value.id}`, {
      query: {
        search,
        page: pagePermissions.value,
        perPage: perPagePermissions.value
      },
      method: 'GET'
    })
    permissionsDialog.value = true;
    itemsPermissions.value = data.items
    totalPermissions.value = data.total
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const updatePermissions = async (v, item, action) => {
  try {
    item[action] = v;
    const { message } = await $api('/api/permissions/', {
      method: 'PUT',
      body: item
    })
    show(message, 'success');
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

// Rules
const nameRequired = (v) => !!v || t('groups.rules.nameRequired');
const distributorRequired = (v) => !!v || t('groups.rules.distributorRequired');
const usersRequired = (v) => (v && v.length > 0) || t('groups.rules.usersRequired');

</script>
