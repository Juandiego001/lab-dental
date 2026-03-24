<template>
  <v-dialog v-model="dialog" max-width="900" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('contacts.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="dialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="pb-2">
        <v-row class="ma-0 mb-2">
          <v-spacer />
          <v-btn class="me-2" icon="mdi-plus" size="x-small" @click="createDialog = !createDialog" />
          <v-btn icon="mdi-magnify" size="x-small" @click="searchDialog = !searchDialog" />
        </v-row>
        <client-only>
          <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
            :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" :loading="loading"
            density="compact">
            <template v-slot:item.option="{ item }">
              <div class="d-flex align-center justify-center ga-2">
                <v-btn class="my-1 bg-primary" size="x-small" icon="mdi-pencil" @click="getContact(item.id)" />
                <v-btn class="my-1 bg-red" size="x-small" icon="mdi-trash-can"
                  @click="form.id = item.id; deleteDialog = true" />
              </div>
            </template>

            <template v-slot:item.fullName="{ item }">
              <div class="d-inline-flex" style="max-width: 240px;">
                <span class="text-caption text-truncate" :title="item.fullName">
                  {{ item.fullName }}
                </span>
              </div>
            </template>

            <template v-slot:item.email="{ item }">
              <div class="d-inline-flex" style="max-width: 240px;">
                <span class="text-caption text-truncate" :title="item.email">
                  {{ item.email }}
                </span>
              </div>
            </template>

            <template v-slot:item.phone="{ item }">
              <span class="text-caption">
                {{ item.phone }}
              </span>
            </template>
          </v-data-table-server>
        </client-only>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('contacts.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createContact">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.fullName" hide-details="auto" :label="$t('contacts.fullName')"
                :rules="[nameRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.email" hide-details="auto" :label="$t('contacts.email')" counter="150"
                maxlength="150" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.phone" hide-details="auto" :label="$t('contacts.phone')" counter="20"
                maxlength="20" />
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

  <!-- Update Dialog -->
  <v-dialog v-model="updateDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('contacts.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateContact">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.fullName" hide-details="auto" :label="$t('contacts.fullName')"
                :rules="[nameRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.email" hide-details="auto" :label="$t('contacts.email')" counter="150"
                maxlength="150" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.phone" hide-details="auto" :label="$t('contacts.phone')" counter="20"
                maxlength="20" />
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

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row class="text-body-1" no-gutters align="center">
          {{ $t('contacts.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchContacts(1, 15);
          searchDialog = false;
        }">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="searchForm.fullName" :label="$t('contacts.fullName')" hide-details="auto"
                counter="50" maxlength="50" clearable />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="searchForm.email" :label="$t('contacts.email')" hide-details="auto" counter="50"
                maxlength="50" clearable />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="searchForm.phone" :label="$t('contacts.phone')" hide-details="auto" counter="50"
                maxlength="50" clearable />
            </v-col>
            <v-col class="mt-3 text-end" cols="12">
              <v-btn class="bg-primary" size="small" type="submit" @mousedown.prevent :loading="loading">
                {{ $t('search') }}
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
          {{ $t('contacts.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center">
        <p class="text-subtitle-1 mb-3 text-center">{{ $t('contacts.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" size="small" variant="outlined" :disabled="loading">{{ $t('cancel')
        }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteContact" class="bg-red" size="small" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onBeforeMount, } from 'vue'
import { useI18n } from 'vue-i18n'

const { notify } = useSnackbar();
const { t } = useI18n();

const {
  items,
  total,
  getContacts,
  dialog,
  distributorId
} = useContacts();

const loading = ref(false)
const searchDialog = ref(false)
const createDialog = ref(false)

const page = ref(1)
const perPage = ref(15)
const sortBy = ref(null)

const updateDialog = ref(false)
const deleteDialog = ref(false)

const createModel = ref(false)
const updateModel = ref(false)
const createForm = ref()
const updateForm = ref()
const form = ref({
  fullName: '',
  email: '',
  phone: '',
})
const searchForm = ref({
  name: '',
})

const resetForm = () => {
  form.value = {
    fullName: '',
    email: '',
    phone: '',
  }
}

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: t('contacts.fullName'), key: 'fullName' },
  { title: t('contacts.email'), align: 'center', key: 'email' },
  { title: t('contacts.phone'), align: 'center', key: 'phone' },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

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
  }
})

watch(deleteDialog, (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await searchContacts();
})

watch(perPage, async () => {
  await searchContacts();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchContacts();
  }
})

const searchContacts = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getContacts({
      fullName: searchForm.value.fullName,
      email: searchForm.value.email,
      phone: searchForm.value.phone,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value,
      sortBy: sortBy.value?.length ? sortBy.value[0] : null
    });
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getContact = async (id) => {
  try {
    loading.value = true;
    const contact = await $api(`/api/distributors/contacts/${id}`, {
      method: 'GET'
    })
    form.value = contact
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const createContact = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/distributors/contacts', {
      method: 'POST',
      body: {
        distributorId: distributorId.value,
        ...form.value
      }
    })
    notify(message, 'success');
    await getContacts({});
    createDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateContact = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await $api(`/api/distributors/contacts/${form.value.id}`, {
      method: 'PUT',
      body: {
        distributorId: distributorId.value,
        ...form.value
      }
    })
    notify(message, 'success');
    await getContacts({});
    updateDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteContact = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/distributors/contacts/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getContacts({});
    deleteDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const nameRequired = (v) => !!v || t('contacts.rules.fullNameRequired');
</script>