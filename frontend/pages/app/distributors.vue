<template>
  <v-container fluid class="fill-height align-start">
    <Contacts />
    <v-card width="100%" flat>
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('distributors.title', 2) }}</p>
        <div>
          <client-only>
            <v-btn v-if="$ability.can('create', 'distributors')" class="me-2" icon="mdi-plus" size="small"
              variant="text" @click="createDialog = !createDialog" />
            <v-btn v-if="$ability.can('read', 'distributors')" class="me-2" icon="mdi-magnify" size="small"
              variant="text" @click="searchDialog = !searchDialog" />
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
                <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getDistributor(item.id)" />
                <v-btn class="my-2 bg-red" size="small" icon="mdi-trash-can"
                  @click="form.id = item.id; deleteDialog = true" />
                <v-btn class="my-2 bg-secondary" size="small" icon="mdi-account-box"
                  @click="async () => { distributorId = item.id; await getContacts({}); dialog = true }" />
              </div>
            </template>
          </v-data-table-server>
        </client-only>
      </v-card-text>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('distributors.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createDistributor">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('distributors.name')"
                :rules="[nameRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col>
              <v-autocomplete v-model="form.brandsIds" hide-details="auto" :label="$t('brands.title', 1)"
                :items="brands" item-title="name" item-value="id" clearable multiple chips @update:search="(name) => {
                  if (!createDialog) return;
                  getBrands({ brandsIds: form.brandsIds, name })
                }" />
            </v-col>

            <!-- Emails -->
            <v-col cols="12">
              <div class="d-flex align-center">
                <span class="text-subtitle-2 text-primary">{{ $t('distributors.emails.title', 2) }}</span>
                <v-spacer />
                <v-btn color="primary" variant="text" size="x-small" icon="mdi-plus" @mousedown.prevent
                  @click="addEmailField" />
              </div>

              <v-slide-y-transition group>
                <div v-for="(emailObj, index) in form.emails.filter(e => e.status !== 'INACTIVE')" :key="index"
                  class="mb-2">
                  <v-text-field v-if="emailObj.status == 'ACTIVE'" v-model="emailObj.email" hide-details="auto"
                    :label="`${$t('distributors.emails.title')} ${index + 1}`" type="email" append-icon="mdi-delete"
                    @click:append="removeEmailField(index)" counter="150" maxlength="150" />
                </div>
              </v-slide-y-transition>
            </v-col>

            <!-- Phones -->
            <v-col cols="12">
              <div class="d-flex align-center">
                <span class="text-subtitle-2 text-primary">{{ $t('distributors.phones.title', 2) }}</span>
                <v-spacer />
                <v-btn color="primary" variant="text" size="x-small" icon="mdi-plus" @mousedown.prevent
                  @click="addPhoneField" />
              </div>

              <v-slide-y-transition group>
                <div v-for="(phoneObj, index) in form.phones.filter(e => e.status !== 'INACTIVE')" :key="index"
                  class="mb-2">
                  <v-text-field v-if="phoneObj.status == 'ACTIVE'" v-model="phoneObj.phone" hide-details="auto"
                    :label="`${$t('distributors.phones.title')} ${index + 1}`" append-icon="mdi-delete"
                    @click:append="removePhoneField(index)" counter="20" maxlength="20" />
                </div>
              </v-slide-y-transition>
            </v-col>

            <v-col cols="12" class="mb-2">
              <v-textarea v-model="form.notes" hide-details="auto" :label="$t('distributors.notes')" counter="200"
                maxlength="200" no-resize />
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
          {{ $t('distributors.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateDistributor">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('distributors.name')"
                :rules="[nameRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-autocomplete v-model="form.brandsIds" hide-details="auto" :label="$t('brands.title', 1)" :items="brands"
              item-title="name" item-value="id" clearable multiple chips @update:search="(name) => {
                if (!updateDialog) return;
                getBrands({ brandsIds: form.brandsIds, name })
              }" />

            <!-- Emails -->
            <v-col cols="12">
              <div class="d-flex align-center">
                <span class="text-subtitle-2 text-primary">{{ $t('distributors.emails.title', 2) }}</span>
                <v-spacer />
                <v-btn color="primary" variant="text" size="x-small" icon="mdi-plus" @mousedown.prevent
                  @click="addEmailField" />
              </div>

              <v-slide-y-transition group>
                <div v-for="(emailObj, index) in form.emails.filter(e => e.status !== 'INACTIVE')" :key="index"
                  class="mb-2">
                  <v-text-field v-if="emailObj.status == 'ACTIVE'" v-model="emailObj.email" hide-details="auto"
                    :label="`${$t('distributors.emails.title')} ${index + 1}`" type="email" append-icon="mdi-delete"
                    @click:append="removeEmailField(index)" counter="150" maxlength="150" />
                </div>
              </v-slide-y-transition>
            </v-col>

            <!-- Phones -->
            <v-col cols="12">
              <div class="d-flex align-center">
                <span class="text-subtitle-2 text-primary">{{ $t('distributors.phones.title', 2) }}</span>
                <v-spacer />
                <v-btn color="primary" variant="text" size="x-small" icon="mdi-plus" @mousedown.prevent
                  @click="addPhoneField" />
              </div>

              <v-slide-y-transition group>
                <div v-for="(phoneObj, index) in form.phones.filter(e => e.status !== 'INACTIVE')" :key="index"
                  class="mb-2">
                  <v-text-field v-if="phoneObj.status == 'ACTIVE'" v-model="phoneObj.phone" hide-details="auto"
                    :label="`${$t('distributors.phones.title')} ${index + 1}`" append-icon="mdi-delete"
                    @click:append="removePhoneField(index)" counter="20" maxlength="20" />
                </div>
              </v-slide-y-transition>
            </v-col>

            <v-col cols="12" class="mb-2">
              <v-textarea v-model="form.notes" hide-details="auto" :label="$t('distributors.notes')" counter="200"
                maxlength="200" no-resize />
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
          {{ $t('distributors.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('distributors.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined" :disabled="loading">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteDistributor" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('distributors.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="async () => {
          await searchDistributors(1, 15);
          searchDialog = false;
        }">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="searchForm.name" :label="$t('distributors.name')" hide-details="auto"
                prepend-inner-icon="mdi-magnify" counter="50" maxlength="50" clearable />
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
import { ref, computed, watch, onBeforeMount, } from 'vue'
import { useI18n } from 'vue-i18n'

const { back } = useBack();
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { t } = useI18n();
const { items, total, getDistributors } = useDistributors();
const { distributorId, dialog, getContacts } = useContacts();
const { items: brands, getBrands } = useBrands();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('distributors.title', 2)}`
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
  emails: [],
  phones: [],
  brandsIds: []
})
const searchForm = ref({
  name: ''
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: t('distributors.name'), key: 'name' },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
  await getBrands({});
})

watch(updateDialog, async (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
  }
  await getBrands({ brandsIds: form.value.brandsIds });
})

watch(deleteDialog, (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await searchDistributors();
})

watch(perPage, async () => {
  await searchDistributors();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await searchDistributors();
  }
})

onBeforeMount(async () => {
  if ($ability.can('read', 'distributors')) {
    await getDistributors({})
    return;
  }
  back();
})

const resetForm = () => {
  form.value = {
    name: '',
    emails: [],
    phones: [],
    brandsIds: []
  }
}

const searchDistributors = async (defPage, defPerPage) => {
  try {
    loading.value = true;
    await getDistributors({
      name: searchForm.value.name,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value,
      sortBy: sortBy.value?.length ? sortBy.value[0] : null
    });
  } catch (err) { }
  finally {
    loading.value = false;
  }
}

const getDistributor = async (id) => {
  try {
    const user = await $api(`/api/distributors/${id}`, {
      method: 'GET'
    })
    form.value = user
    updateDialog.value = true
  } catch (err) {
    notify(err, 'error');
  }
}

const createDistributor = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    const { message } = await $api('/api/distributors/', {
      method: 'POST',
      body: form.value
    })

    notify(message, 'success');
    await getDistributors({});
    createDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateDistributor = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;
    const { message } = await $api(`/api/distributors/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await getDistributors({
      name: searchForm.value.name,
      page: page.value,
      perPage: perPage.value
    });
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteDistributor = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/distributors/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getDistributors({});
    deleteDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const addEmailField = () => {
  if (updateDialog.value) {
    const lastIndex = form.value.emails.findLastIndex(e => e.status === 'ACTIVE');
    form.value.emails.splice(lastIndex + 1, 0, { email: '', status: 'ACTIVE' });
  } else {
    form.value.emails.push({ email: '', status: 'ACTIVE' });
  }
}

const removeEmailField = (index) => {
  if (form.value.emails.length <= 0) return;

  const deletedEmail = form.value.emails.splice(index, 1)[0];
  if (updateDialog.value && deletedEmail.id) {
    deletedEmail.status = 'INACTIVE';
    form.value.emails.push(deletedEmail);
  }
}

const addPhoneField = () => {
  if (updateDialog.value) {
    const lastIndex = form.value.phones.findLastIndex(e => e.status === 'ACTIVE');
    form.value.phones.splice(lastIndex + 1, 0, { phone: '', status: 'ACTIVE' })
  } else {
    form.value.phones.push({ phone: '', status: 'ACTIVE' });
  }
}

const removePhoneField = (index) => {
  if (form.value.phones.length <= 0) return;

  const deletedPhone = form.value.phones.splice(index, 1)[0];
  if (updateDialog.value && deletedPhone.id) {
    deletedPhone.status = 'INACTIVE';
    form.value.phones.push(deletedPhone);
  }
}

// Rules
const nameRequired = (v) => !!v || t('distributors.rules.nameRequired');

</script>
