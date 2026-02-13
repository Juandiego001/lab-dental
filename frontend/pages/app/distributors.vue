<template>
  <v-container fluid class="fill-height align-start">
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
            @update:itemsPerPage="v => perPage = v" :disable-sort="true">
            <template v-slot:item.option="{ item }">
              <div class="d-flex align-center justify-center ga-2">
                <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getDistributor(item.id)" />
                <v-btn class="my-2 bg-red" size="small" icon="mdi-trash-can"
                  @click="form.id = item.id; deleteDialog = true" />
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
            <v-col class="text-end">
              <v-btn variant="outlined" @click="createDialog = false">{{ $t('cancel') }}</v-btn>
              <span class="mx-1" />
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
            <v-col class="text-end">
              <v-btn variant="outlined" @click="updateDialog = false">{{ $t('cancel') }}</v-btn>
              <span class="mx-1" />
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
          {{ $t('distributors.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('distributors.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteDistributor" class="bg-red">{{ $t('confirm') }}</v-btn>
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
import { useI18n } from 'vue-i18n'

const { back } = useBack();
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { t } = useI18n();
const { items, total, getDistributors } = useDistributors();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('distributors.title', 2)}`
})

const searchDialog = ref(false);
const createDialog = ref(false);
const page = ref(1);
const perPage = ref(15);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const createModel = ref(false);
const updateModel = ref(false);
const createForm = ref();
const updateForm = ref();
const form = ref({
  name: ''
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
  { title: t('distributors.name'), key: 'name', sortable: false },
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
  await searchDistributors();
})

watch(perPage, async () => {
  await searchDistributors();
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
    name: ''
  }
}

const searchDistributors = async (defPage, defPerPage) => {
  try {
    await getDistributors({
      name: searchForm.value.name,
      page: defPage || page.value,
      perPage: defPerPage || perPage.value
    });
  } catch (err) { }
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
  }
}

const updateDistributor = async () => {
  try {
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
  }
}

const deleteDistributor = async () => {
  try {
    const { message } = await $api(`/api/distributors/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getDistributors({});
    deleteDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  }
}


// Rules
const nameRequired = (v) => !!v || t('distributors.rules.nameRequired');

</script>
