<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('users.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getUser(item.id)"></v-btn>
            <span class="mx-2"></span>
            <v-btn class="my-2 bg-red" size="small" icon="mdi-trash-can"
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
          {{ $t('users.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createUser">
          <v-row>
            <v-col v-if="isAdmin" cols="12">
              <v-select v-model="form.role" item-title="title" item-value="value" hide-details="auto"
                :label="$t('users.role.title')" :items="usersRoles" :rules="[roleRequired]"></v-select>
            </v-col>
            <v-col v-if="isAdmin && form.role === 'DISTRIBUTOR'" cols="12">
              <v-autocomplete v-model="form.distributorId" hide-details="auto" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" @update:search="getDistributors" clearable
                :rules="[distributorRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.fullName" hide-details="auto" :label="$t('users.fullName')"
                :rules="[fullNameRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.username" hide-details="auto" :label="$t('users.username')"
                :rules="[usernameRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.email" type="email" hide-details="auto" :label="$t('users.email')"
                :rules="[emailRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.password" type="password" hide-details="auto" label="Password"
                autocomplete="off" :rules="[passwordRequired]"></v-text-field>
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
          {{ $t('users.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateUser">
          <v-row>
            <v-col v-if="isAdmin" cols="12">
              <v-select v-model="form.role" hide-details="auto" :items="usersRoles" item-title="title"
                item-value="value" :label="$t('users.role.title')" :rules="[roleRequired]" />
            </v-col>
            <v-col v-if="isAdmin && form.role === 'DISTRIBUTOR'" cols="12">
              <v-autocomplete v-model="form.distributorId" hide-details="auto" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" @update:search="getDistributors" clearable
                :rules="[distributorRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.fullName" hide-details="auto" :label="$t('users.fullName')"
                :rules="[fullNameRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.username" hide-details="auto" :label="$t('users.username')"
                :rules="[usernameRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.email" type="email" hide-details="auto" :label="$t('users.email')"
                :rules="[emailRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.password" type="password" hide-details="auto" :label="$t('users.password')"
                autocomplete="off"></v-text-field>
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
          {{ $t('users.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('users.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2"></span>
        <v-btn @click="deleteUser" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('users.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <p class="text-subtitle-2 pb-2">{{ $t('users.search.message') }}</p>
        <v-form @submit.prevent="doSearch">
          <v-row no-gutters="">
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('users.search.fields')" hide-details="auto"
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
  title: `SOE Latam | ${t('users.title', 2)}`
})

const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)
const distributors = ref([]);
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
  distributorId: null,
  distributorName: '',
  fullName: '',
  username: '',
  email: '',
  role: ''
})

const isAdmin = computed(() => profile.value.role === 'ADMIN');

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: 'Id', key: 'id', sortable: false },
  { title: t('users.fullName'), key: 'fullName', sortable: false },
  { title: t('users.username'), key: 'username', sortable: false },
  { title: t('users.email'), key: 'email', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

const usersRoles = computed(() => [
  { title: t('users.role.admin'), value: 'ADMIN' },
  { title: t('users.role.distributor'), value: 'DISTRIBUTOR' },
])

watch(createDialog, async (val) => {
  if (val) { if (isAdmin.value) await getDistributors(); }
  else {
    createForm.value.reset();
    resetForm();
  }
})

watch(updateDialog, async (val) => {
  if (val) { if (isAdmin.value) await getDistributors(form.value.distributorName); }
  else {
    updateForm.value.reset();
    resetForm();
  }
})

watch(() => form.value.role, async (val) => {
  if (updateDialog.value) form.value.distributorId = null;
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await getUsers();
})

watch(perPage, async () => {
  await getUsers();
})

onBeforeMount(async () => {
  if (!$ability.can('read', 'users')) {
    navigateTo(history.state?.back || '/login');
    return;
  }
  await getUsers();
})

const resetForm = () => {
  form.value = {
    distributorId: null,
    distributorName: '',
    fullName: '',
    username: '',
    email: '',
    role: ''
  }
}

const getDistributors = async (search) => {
  try {
    const data = await $api('/api/distributors/distributors/users', {
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

const getUsers = async () => {
  try {
    const data = await $api('/api/users/', {
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

const getUser = async (id) => {
  try {
    const user = await $api(`/api/users/${id}`, {
      method: 'GET'
    })
    form.value = user
    nextTick(() => updateDialog.value = true);
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const createUser = async () => {
  try {
    if (!createModel.value) return;
    const { message } = await $api('/api/users/', {
      method: 'POST',
      body: form.value
    })
    show(message, 'success');
    await getUsers()
    createDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const updateUser = async () => {
  try {
    if (!updateModel.value) return;
    const { message } = await $api(`/api/users/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    show(message, 'success');
    await getUsers()
    updateDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const deleteUser = async () => {
  try {
    const { message } = await $api(`/api/users/${form.value.id}`, {
      method: 'DELETE'
    })
    show(message, 'success');
    await getUsers()
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
    await getUsers()
    searchDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

// Rules
const roleRequired = (v) => !!v || t('users.rules.roleRequired');
const distributorRequired = (v) => !!v || t('users.rules.distributorRequired');
const fullNameRequired = (v) => !!v || t('users.rules.fullNameRequired');
const usernameRequired = (v) => !!v || t('users.rules.usernameRequired');
const emailRequired = (v) => !!v || t('users.rules.emailRequired');
const passwordRequired = (v) => !!v || t('users.rules.passwordRequired');

</script>
