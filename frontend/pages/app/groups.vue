<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('groups.title', 2) }}</p>
        <div>
          <client-only>
            <v-tooltip :text="$t('tooltip.create')" :disabled="loading" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('create', 'groups')" class="me-2" icon="mdi-plus" size="small"
                  variant="text" @click="createDialog = !createDialog" :disabled="loading" />
              </template>
            </v-tooltip>

            <v-tooltip :text="$t('tooltip.search')" :disabled="loading" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('read', 'groups')" class="me-2" icon="mdi-magnify" size="small"
                  variant="text" @click="searchDialog = !searchDialog" :disabled="loading" />
              </template>
            </v-tooltip>
          </client-only>
        </div>
      </v-card-title>
      <v-card-text>
        <client-only>
          <v-data-table-server :items="items" :headers="tableHeaders" :page="page" :items-per-page="perPage"
            :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" :loading="loading"
            :disable-sort="loading" :hide-default-footer="loading">
            <template v-slot:item.option="{ item }">
              <div class="d-flex align-center justify-center ga-2">
                <v-tooltip :text="$t('tooltip.viewUpdate')" :disabled="loading" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" class="my-2 bg-primary" size="small" icon="mdi-pencil"
                      @click="getGroup(item.id)" :loading="loading && loadingUpdate && groupId === item.id"
                      :disabled="loading" />
                  </template>
                </v-tooltip>

                <v-tooltip :text="$t('groups.permissions.title')" :disabled="loading" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" class="my-2 mx-2 bg-secondary" size="small" icon="mdi-shield-edit"
                      @click="form = item; getPermissions()"
                      :loading="loading && loadingPermissions && groupId === item.id" :disabled="loading" />
                  </template>
                </v-tooltip>

                <v-tooltip :text="$t('tooltip.delete')" :disabled="loading" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" v-if="item.id !== 1" class="my-2 bg-red" size="small" icon="mdi-trash-can"
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
          {{ $t('groups.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" icon="mdi-close" size="small" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createGroup">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('groups.name')" :rules="[nameRequired]"
                counter="30" maxlength="30" />
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" clearable :rules="[distributorRequired]"
                @update:search="(name) => {
                  if (!createDialog) return;
                  getDistributors({ distributorsIds: [form.distributorId], name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('users.title', 2)" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" clearable multiple chips :readonly="isAdmin && !form.distributorId"
                :rules="[usersRequired]" @update:search="(fullName) => {
                  if (!createDialog) return;
                  getUsers({ distributorId: form.distributorId, usersIds: form.usersIds, fullName, isMain: true })
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
          {{ $t('groups.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateGroup">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('groups.name')" :rules="[nameRequired]"
                counter="30" maxlength="30" />
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" clearable :rules="[distributorRequired]"
                @update:search="(name) => {
                  if (!updateDialog) return;
                  getDistributors({ distributorsIds: [form.distributorId], name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('users.title', 2)" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" clearable multiple chips :readonly="isAdmin && !form.distributorId"
                :rules="[usersRequired]" @update:search="(fullName) => {
                  if (!updateDialog) return;
                  getUsers({ distributorId: form.distributorId, usersIds: form.usersIds, fullName, isMain: true })
                }" />
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
          {{ $t('groups.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('groups.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteGroup" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('groups.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="doSearch">
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

            <!-- Groups -->
            <v-col cols="12">
              <p class="text-body-2 text-primary">{{ $t('groups.title', 2) }}</p>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="searchForm.name" :label="$t('groups.name')" hide-details="auto" clearable
                counter="30" maxlength="30" />
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

  <!-- Permissions Dialog -->
  <v-dialog v-model="permissionsDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('groups.permissions.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="permissionsDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-data-table :items="itemsPermissions" :headers="headersPermissions" :page="pagePermissions"
          :items-per-page="perPagePermissions" :items-length="totalPermissions"
          :items-per-page-options="itemsPerPageOptions" @update:page="v => pagePermissions = v"
          @update:itemsPerPage="v => perPagePermissions = v" :disable-sort="true" density="compact" :loading="loading"
          :hide-default-footer="loading">
          <template v-slot:item.moduleName="{ item }">
            <span class="text-capitalize">{{ item.moduleName }}</span>
          </template>
          <template v-slot:item.read="{ item }">
            <v-checkbox-btn v-if="!disablePermission(item, 'read')" style="justify-self: center;" color="primary"
              :model-value="item.read" :ripple="false" hide-details="auto" density="compact"
              @update:modelValue="v => updatePermissions(v, item, 'read')" :disabled="loading" />
            <span v-else>-</span>
          </template>
          <template v-slot:item.create="{ item }">
            <v-checkbox-btn v-if="!disablePermission(item, 'create')" style="justify-self: center;" color="primary"
              :model-value="item.create" :ripple="false" hide-details="auto" density="compact"
              @update:modelValue="v => updatePermissions(v, item, 'create')" :disabled="loading" />
            <span v-else>-</span>
          </template>
          <template v-slot:item.update="{ item }">
            <v-checkbox-btn v-if="!disablePermission(item, 'update')" style="justify-self: center;" color="primary"
              :model-value="item.update" :ripple="false" hide-details="auto" density="compact"
              @update:modelValue="v => updatePermissions(v, item, 'update')" :disabled="loading" />
            <span v-else>-</span>
          </template>
          <template v-slot:item.delete="{ item }">
            <v-checkbox-btn v-if="!disablePermission(item, 'delete')" style="justify-self: center;" color="primary"
              :model-value="item.delete" :ripple="false" hide-details="auto" density="compact"
              @update:modelValue="v => updatePermissions(v, item, 'delete')" :disabled="loading" />
            <span v-else>-</span>
          </template>
        </v-data-table>
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
const { items: distributors, getDistributors } = useDistributors();
const { items: users, getUsers } = useUsers();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('groups.title', 2)}`
})

const loading = ref(false);
const groupId = ref(null);
const loadingUpdate = ref(false);
const loadingPermissions = ref(false);
const searchDialog = ref(false);
const createDialog = ref(false);

/* Groups */
const items = ref([]);
const page = ref(1);
const perPage = ref(15);
const sortBy = ref(null);
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
  distributorName: '',
  usersIds: []
})
const searchForm = ref({
  distributorId: null,
  name: ''
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const tableHeaders = computed(() => {
  if (isAdmin.value) {
    return [
      { title: t('groups.name'), key: 'name' },
      { title: t('distributors.title'), key: 'distributorName' },
      { title: t('options'), key: 'option', align: 'center', sortable: false }
    ]
  }

  return [
    { title: t('groups.name'), key: 'name', sortable: false },
    { title: t('options'), key: 'option', align: 'center', sortable: false }
  ]
})

const headersPermissions = computed(() => [
  { title: t('modules.title'), key: 'moduleName', align: 'center', sortable: false },
  { title: t('groups.permissions.read'), key: 'read', align: 'center', sortable: false },
  { title: t('groups.permissions.create'), key: 'create', align: 'center', sortable: false },
  { title: t('groups.permissions.update'), key: 'update', align: 'center', sortable: false },
  { title: t('groups.permissions.delete'), key: 'delete', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
  if (isAdmin.value) {
    await getDistributors({});
    return;
  }
  await getUsers({ distributorId: form.value.distributorId, isMain: true });
})

watch(updateDialog, async (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
    return;
  }
  if (isAdmin.value) await getDistributors({ distributorsIds: [form.value.distributorId] });
})

watch(() => form.value.distributorId, async (val, prev) => {
  if (!val) return;
  if (prev && prev !== form.value.distributorId) delete form.value.usersIds;
  await getUsers({ distributorId: form.value.distributorId, usersIds: form.value.usersIds, isMain: true });
})

watch(searchDialog, async (val) => {
  if (val && isAdmin.value) await getDistributors({ distributorsIds: [searchForm.value.distributorId] });
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(permissionsDialog, (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await getGroups();
})

watch(perPage, async () => {
  await getGroups();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await getGroups();
  }
})

watch(pagePermissions, async () => {
  await getPermissions();
})

watch(perPagePermissions, async () => {
  await getPermissions();
})

onBeforeMount(async () => {
  if ($ability.can('read', 'groups')) {
    await getGroups();
    return;
  }
  back();
})

const resetForm = () => {
  form.value = {
    name: '',
    distributorId: null,
    distributorName: '',
    usersIds: null
  }
}

const getGroups = async () => {
  try {
    loading.value = true;
    const data = await $api('/api/groups/search', {
      body: {
        distributorId: searchForm.value.distributorId,
        name: searchForm.value.name,
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

const getGroup = async (id) => {
  try {
    loading.value = true;
    loadingUpdate.value = true;
    groupId.value = id;
    const data = await $api(`/api/groups/${id}`, {
      method: 'GET'
    })
    form.value = data
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
    loadingUpdate.value = false;
  }
}

const createGroup = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/groups/', {
      method: 'POST',
      body: form.value
    })
    notify(message, 'success');
    await getGroups()
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateGroup = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await $api(`/api/groups/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await getGroups()
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteGroup = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/groups/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getGroups()
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
    await getGroups()
    searchDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getPermissions = async (search) => {
  try {
    loading.value = true;
    loadingPermissions.value = true;
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
    notify(err, 'error');
  } finally {
    loading.value = false;
    loadingPermissions.value = false;
  }
}

const updatePermissions = async (v, item, action) => {
  try {
    loading.value = true;
    item[action] = v;
    const { message } = await $api('/api/permissions/', {
      method: 'PUT',
      body: item
    })
    notify(message, 'success');
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const modulesOnlyRead = ['brands', 'categories', 'equipments', 'aligners'];
const modulesBan = ['distributors', 'lists', 'reasons'];

const disablePermission = (permission, action) => {
  if (form.value.id == 1) return true;

  if (!isAdmin.value &&
    ['equipments', 'brands', 'categories', 'aligners'].includes(permission.moduleName) &&
    ['create', 'update', 'delete'].includes(action)) return true;

  if (form.value.distributorId !== 1 &&
    modulesOnlyRead.includes(permission.moduleName) &&
    ['create', 'update', 'delete'].includes(action)
  ) return true;

  if (form.value.distributorId !== 1 &&
    modulesBan.includes(permission.moduleName) &&
    ['read', 'create', 'update', 'delete'].includes(action)
  ) return true;

  return false;
}

// Rules
const nameRequired = (v) => !!v || t('groups.rules.nameRequired');
const distributorRequired = (v) => !!v || t('groups.rules.distributorRequired');
const usersRequired = (v) => (v && v.length > 0) || t('groups.rules.usersRequired');

</script>
