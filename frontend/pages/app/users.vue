<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('users.title', 2) }}</p>
        <div>
          <client-only>
            <v-btn v-if="$ability.can('create', 'users')" class="me-2" icon="mdi-plus" size="small" variant="text"
              @click="createDialog = !createDialog" />
            <v-btn v-if="$ability.can('read', 'users')" class="me-2" icon="mdi-magnify" size="small" variant="text"
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
                <v-btn v-if="$ability.can('update', 'users')" class="my-2 bg-primary" size="small" icon="mdi-pencil"
                  @click="getUser(item.id)" />
                <v-btn v-if="$ability.can('delete', 'users')" class="my-2 bg-red" size="small" icon="mdi-trash-can"
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
          {{ $t('users.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createUser">
          <v-row dense>
            <v-col v-if="isAdmin" cols="12">
              <v-select v-model="form.role" item-title="title" item-value="value" hide-details="auto"
                :label="$t('users.role.title')" :items="roles" :rules="[roleRequired]" />
            </v-col>
            <v-col v-if="isAdmin && form.role === 'DISTRIBUTOR'" cols="12">
              <v-autocomplete v-model="form.distributorId" hide-details="auto" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" clearable :rules="[distributorRequired]"
                @update:search="(name) => {
                  if (!createDialog) return;
                  getDistributors({ distributorsIds: [form.distributorId], name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.fullName" hide-details="auto" :label="$t('users.fullName')"
                :rules="[fullNameRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.username" hide-details="auto" :label="$t('users.username')"
                :rules="[usernameRequired]" counter="20" maxlength="20" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.email" type="email" hide-details="auto" :label="$t('users.email')"
                :rules="[emailRequired]" counter="150" maxlength="150" />
            </v-col>
            <v-col cols="12">
              <v-select v-model="form.language" item-title="title" item-value="value" hide-details="auto"
                :label="$t('users.language')" :items="languages" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.password" hide-details="auto" :label="$t('users.password')" autocomplete="off"
                :rules="passwordRules" maxlength="50" :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword" />
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
          {{ $t('users.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateUser">
          <v-row dense>
            <v-col v-if="isAdmin" cols="12">
              <v-select v-model="form.role" hide-details="auto" :items="roles" item-title="title" item-value="value"
                :label="$t('users.role.title')" :rules="[roleRequired]" />
            </v-col>
            <v-col v-if="isAdmin && form.role === 'DISTRIBUTOR'" cols="12">
              <v-autocomplete v-model="form.distributorId" hide-details="auto" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" clearable :rules="[distributorRequired]"
                @update:search="(name) => {
                  if (!updateDialog) return;
                  getDistributors({ distributorsIds: [form.distributorId], name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.fullName" hide-details="auto" :label="$t('users.fullName')"
                :rules="[fullNameRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.username" hide-details="auto" :label="$t('users.username')"
                :rules="[usernameRequired]" counter="20" maxlength="20" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.email" type="email" hide-details="auto" :label="$t('users.email')"
                :rules="[emailRequired]" counter="250" maxlength="250" />
            </v-col>
            <v-col cols="12">
              <v-select v-model="form.language" item-title="title" item-value="value" hide-details="auto"
                :label="$t('users.language')" :items="languages" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.password" hide-details="auto" :label="$t('users.password')" autocomplete="off"
                :rules="passwordNotRequiredRules" maxlength="50" :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword" />
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
          {{ $t('users.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('users.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined" :disabled="loading">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteUser" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="700" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('users.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchUsers(1, 15);
          searchDialog = false
        }">
          <v-row dense>
            <!-- Distributors -->
            <template v-if="isAdmin">
              <v-col cols="12">
                <p class="text-body-2 text-primary">{{ $t('distributors.title', 2) }}</p>
              </v-col>
              <v-col class="pb-4" cols="12">
                <v-autocomplete v-model="searchForm.distributorId" :label="$t('distributors.title')"
                  :items="distributors" item-title="name" item-value="id" hide-details="auto" clearable
                  @update:search="(name) => getDistributors({ distributorsIds: [searchForm.distributorId], name })" />
              </v-col>
            </template>

            <!-- Users -->
            <v-col cols="12">
              <p class="text-body-2 text-primary">{{ $t('users.title', 2) }}</p>
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-select v-model="searchForm.role" hide-details="auto" :items="roles" item-title="title"
                item-value="value" :label="$t('users.role.title')" clearable />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.fullName" :label="$t('users.fullName')" hide-details="auto" clearable
                counter="50" maxlength="50" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.username" :label="$t('users.username')" hide-details="auto" clearable
                counter="20" maxlength="20" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="searchForm.email" :label="$t('users.email')" hide-details="auto" clearable
                counter="150" maxlength="150" />
            </v-col>

            <!-- Search Button -->
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
import { ref, computed, watch, onBeforeMount, } from 'vue'
import { useI18n } from 'vue-i18n'

const { back } = useBack()
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { isAdmin } = useProfile();
const { t } = useI18n();
const { items: allDistributors, getDistributors } = useDistributors();
const { items, total, getUsers } = useUsers();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('users.title', 2)}`
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
const showPassword = ref(false);
const form = ref({
  distributorId: null,
  distributorName: '',
  fullName: '',
  username: '',
  email: '',
  language: '',
  role: ''
})
const searchForm = ref({
  distributorId: null,
  role: '',
  fullName: '',
  username: '',
  email: '',
})

const languages = computed(() => [
  { title: 'Español', value: 'es' },
  { title: 'English', value: 'en' }
])

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const distributors = computed(() => {
  return allDistributors.value.filter((distributor) => distributor.id !== 1);
})

const headers = computed(() => {
  const defaultHeaders = [
    { title: t('users.fullName'), key: 'fullName' },
    { title: t('users.username'), key: 'username', align: 'center' },
    { title: t('users.email'), key: 'email', align: 'center' },
  ]

  if ($ability.can('update', 'users') || $ability.can('delete', 'users')) {
    defaultHeaders.push({ title: t('options'), key: 'option', align: 'center', sortable: false })
  }

  return defaultHeaders;
})

const roles = computed(() => [
  { title: t('users.role.admin'), value: 'ADMIN' },
  { title: t('users.role.distributor'), value: 'DISTRIBUTOR' },
])

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
  if (isAdmin.value) await getDistributors({});
})

watch(updateDialog, async (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
    return;
  }
  if (isAdmin.value) await getDistributors({ distributorsIds: [form.value.distributorId] })
})

watch(searchDialog, async (val) => {
  if (val && isAdmin.value) await getDistributors({
    distributorsIds: [searchForm.value.distributorId]
  });
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await searchUsers();
})

watch(perPage, async () => {
  await searchUsers();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchUsers();
  }
})

onBeforeMount(async () => {
  if ($ability.can('read', 'users')) {
    await getUsers({ isMain: true });
    return;
  }
  back();
})

const resetForm = () => {
  form.value = {
    distributorId: null,
    distributorName: '',
    fullName: '',
    username: '',
    email: '',
    language: '',
    role: ''
  }
}

const searchUsers = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getUsers({
      distributorId: searchForm.value.distributorId,
      role: searchForm.value.role,
      fullName: searchForm.value.fullName,
      username: searchForm.value.username,
      email: searchForm.value.email,
      isMain: true,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value,
      sortBy: sortBy.value?.length ? sortBy.value[0] : null
    })
  } catch (err) { }
  finally {
    loading.value = false;
  }
}

const getUser = async (id) => {
  try {
    const user = await $api(`/api/users/${id}`, {
      method: 'GET'
    })
    form.value = user
    updateDialog.value = true;
  } catch (err) {
    notify(err, 'error');
  }
}

const createUser = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/users/', {
      method: 'POST',
      body: form.value
    })
    notify(message, 'success');
    await getUsers({ isMain: true })
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateUser = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await $api(`/api/users/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await getUsers({
      isMain: true,
    })
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteUser = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/users/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getUsers({
      isMain: true,
    })
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

// Rules
const roleRequired = (v) => !!v || t('users.rules.roleRequired');
const distributorRequired = (v) => !!v || t('users.rules.distributorRequired');
const fullNameRequired = (v) => !!v || t('users.rules.fullNameRequired');
const usernameRequired = (v) => !!v || t('users.rules.usernameRequired');
const emailRequired = (v) => !!v || t('users.rules.emailRequired');
const passwordRules = [
  v => !!v || t('passwordRules.required'),
  v => /[A-Z]/.test(v) || t('passwordRules.requiredUpper'),
  v => /[a-z]/.test(v) || t('passwordRules.requiredLower'),
  v => /[^a-zA-Z\d]/.test(v) || t('passwordRules.requiredSpecial'),
  v => /\d/.test(v) || t('passwordRules.requiredNumber'),
  v => (v && v.length >= 10) || t('passwordRules.minLength10'),
  v => (v && v.length <= 24) || t('passwordRules.maxLength24'),
]
const passwordNotRequiredRules = [
  v => !v || /[A-Z]/.test(v) || t('passwordRules.requiredUpper'),
  v => !v || /[a-z]/.test(v) || t('passwordRules.requiredLower'),
  v => !v || /[^a-zA-Z\d]/.test(v) || t('passwordRules.requiredSpecial'),
  v => !v || /\d/.test(v) || t('passwordRules.requiredNumber'),
  v => !v || (v && v.length >= 10) || t('passwordRules.minLength10'),
  v => !v || (v && v.length <= 24) || t('passwordRules.maxLength24'),
]

</script>
