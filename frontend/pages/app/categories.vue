<template>
  <v-container fluid class="fill-height align-start">
    <v-card width="100%" flat>
      <v-card-title>{{ $t('categories.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
        :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
          @update:itemsPerPage="v => perPage = v" :disable-sort="true">

          <template v-slot:item.option="{ item }">
            <v-btn class="my-2 bg-primary" size="small" icon="mdi-pencil" @click="getCategory(item.id)"></v-btn>
            <span class="mx-2"></span>
            <v-btn class="my-2 bg-red" size="small" icon="mdi-trash-can"
              @click="form.id = item.id; deleteDialog = true"></v-btn>
          </template>

        </v-data-table-server>
      </v-card-text>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('categories.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="createCategory">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('categories.name')"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.slug" hide-details="auto" :label="$t('categories.slug')"></v-text-field>
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

  <!-- Update Dialog -->
  <v-dialog v-model="updateDialog" max-width="500">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('update.category') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateCategory">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="form.name" hide-details="auto" :label="$t('category.name')"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.slug" hide-details="auto" :label="$t('category.slug')"></v-text-field>
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
  <v-dialog v-model="deleteDialog" max-width="500">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('categories.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('categories.delete.message') }}</p>

        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2"></span>
        <v-btn @click="deleteCategory" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('categories.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <p class="text-subtitle-2 pb-2">{{ $t('categories.search.message') }}</p>
        <v-form @submit.prevent="doSearch">
          <v-row no-gutters="">
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('categories.search.fields')" hide-details="auto"
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
const { t } = useI18n();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('categories.title', 2)}`
})

const { searchDialog } = toRefs(searchMixin)
const { createDialog } = toRefs(createMixin)
const items = ref([]);
const search = ref('');
const page = ref(1);
const perPage = ref(15);
const total = ref(15);
const updateDialog = ref(false);
const deleteDialog = ref(false);
const form = ref({
  id: '',
  name: '',
  slug: '',
  status: '',
  createdAt: '',
  updatedAt: ''
})

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: 'Id', key: 'id', sortable: false },
  { title: t('categories.name'), key: 'name', sortable: false },
  { title: t('categories.slug'), key: 'slug', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

watch(page, async () => {
  await getCategories();
})

watch(perPage, async () => {
  await getCategories();
})

onBeforeMount(async () => {
  await getCategories();
})

const getCategories = async () => {
  try {
    const data = await $fetch('/api/categories/', {
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

const getCategory = async (id) => {
  try {
    const category = await $fetch(`/api/categories/${id}`, {
      method: 'GET'
    })
    form.value = category
    updateDialog.value = true
  } catch (err) {
    console.log(err)
  }
}

const createCategory = async () => {
  try {
    const response = await $fetch('/api/categories/', {
      method: 'POST',
      body: form.value
    })
    await getCategories()
    createDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

const updateCategory = async () => {
  try {
    const response = await $fetch(`/api/categories/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    await getCategories()
    updateDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

const deleteCategory = async () => {
  const response = await $fetch(`/api/categories/${this.form.id}`, {
    method: 'DELETE'
  })
  await getCategories()
  deleteDialog.value = false
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getCategories()
    searchDialog.value = false
  } catch (err) {
    console.log(err)
  }
}

</script>
