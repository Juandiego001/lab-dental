<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('lists.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">
          <template v-slot:item.option="{ item }">
            <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getList(item.id)"></v-btn>
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
          {{ $t('lists.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="createList">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('lists.name')"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.distributorsIds" :label="$t('lists.distributors')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors" clearable
                multiple chips />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('lists.users')" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" @update:search="getUsers" clearable multiple chips />
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
          {{ $t('lists.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateList">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('lists.name')"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.distributorsIds" :label="$t('lists.distributors')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors" clearable
                multiple chips />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.usersIds" :label="$t('lists.users')" :items="users" item-title="fullName"
                item-value="id" hide-details="auto" @update:search="getUsers" clearable multiple chips />
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
          {{ $t('lists.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="deleteDialog = false"></v-btn>
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
  <v-dialog v-model="searchDialog" max-width="500" persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('lists.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="searchDialog = false"></v-btn>
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
import { useDate } from 'vuetify'

const { t } = useI18n();
const date = useDate();

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
const showPicker = ref(false);
const selectedDate = ref(null);
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
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(createDialog, async (val) => {
  if (val) {
    await getDistributors();
    await getUsers();
  } else {
    resetForm()
  }
})

watch(updateDialog, async (val) => {
  if (val) {
    await getDistributors();
    await getUsers();
  } else {
    resetForm()
  }
})

watch(page, async () => {
  await getLists();
})

watch(perPage, async () => {
  await getLists();
})

onBeforeMount(async () => {
  await getLists();
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
    console.log(err)
  }
}

const getUsers = async (search) => {
  try {
    const data = await $api('/api/users/', {
      query: {
        search,
        page: 1,
        perPage: 15
      },
      method: 'GET'
    })
    users.value = data.items
  } catch (err) {
    console.log(err)
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
    console.log(err)
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
    console.log(err)
  }
}

const createList = async () => {
  try {
    const response = await $api('/api/lists/', {
      method: 'POST',
      body: form.value
    })
    await getLists()
    createDialog.value = false
    resetForm()
  } catch (err) {
    console.log(err)
  }
}

const updateList = async () => {
  try {
    const response = await $api(`/api/lists/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    await getLists()
    updateDialog.value = false
    resetForm()
  } catch (err) {
    console.log(err)
  }
}

const deleteList = async () => {
  try {
    const response = await $api(`/api/lists/${form.value.id}`, {
      method: 'DELETE'
    })
    await getLists()
    deleteDialog.value = false
    resetForm()
  } catch (err) {
    console.log(err);
  }
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getLists()
    searchDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

</script>
