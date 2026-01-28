<template>
  <v-container fluid class="fill-height align-start">
    <v-card class="d-flex flex-column" width="100%" height="100%" flat>
      <v-card-title>{{ $t('installations.title', 2) }}</v-card-title>
      <v-card-text>
        <client-only>
          <v-data-table :items="items" :headers="headers" :page="page" :items-per-page="perPage" :items-length="total"
            :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" :disable-sort="true">
            <template v-slot:item.serial="{ item }">
              <span :class="`rounded-lg py-1 px-2
                  ${item.status === 'ACTIVE' && 'bg-primary'}
                  ${item.status === 'APPROVED' && 'bg-success'}
                  ${item.status === 'REJECTED' && 'bg-error'}
                `">
                {{ item.serial }}
              </span>
            </template>
            <template v-slot:item.installedDate="{ item }">{{ date.format(item.installedDate, 'fullDate') }}</template>
            <template v-slot:item.option="{ item }">
              <v-btn v-if="$ability.can('update', 'installations')" class="my-2 bg-primary me-2" size="small"
                icon="mdi-pencil" @click="async () => { await getInstallation(item.id); updateDialog = true }" />
              <v-btn v-if="$ability.can('delete', 'installations')" class="my-2 bg-red me-2" size="small"
                icon="mdi-trash-can" @click="form.id = item.id"></v-btn>
              <v-btn v-if="isAdmin" class="my-2 bg-secondary" size="small" icon="mdi-eye"
                @click="async () => { await getInstallation(item.id); approvalDialog = true }"></v-btn>
            </template>
          </v-data-table>
        </client-only>
      </v-card-text>
      <v-card-actions class="w-100 d-flex align-center justify-end ga-2 flex-wrap">
        <p class="text-body-2 rounded-lg bg-grey py-1 px-2">Installation statuses</p>
        <p class="d-inline-block py-1 px-2 rounded-lg bg-primary text-caption">Active</p>
        <p class="d-inline-block py-1 px-2 rounded-lg bg-success text-caption">Approved</p>
        <p class="d-inline-block py-1 px-2 rounded-lg bg-error text-caption">Rejected</p>
      </v-card-actions>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.create.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createInstallation">
          <v-row>
            <v-col cols="12">
              <v-autocomplete v-model="form.equipmentId" :label="$t('equipments.title')" :items="equipments"
                item-title="serialModel" item-value="id" hide-details="auto" @update:search="getEquipments" clearable
                :rules="[equipmentRequired]" />
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors" clearable
                :rules="[distributorRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteDistributorId"
                :label="`${$t('sites.title')} ${$t('distributors.title')}`" :items="distributorsSites" item-title="name"
                item-value="id" hide-details="auto" @update:search="getDistributorsSites" clearable
                :readonly="isAdmin && !form.distributorId" :rules="[siteDistributorRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                item-value="id" hide-details="auto" @update:search="getClients" clearable
                :readonly="isAdmin && !form.distributorId" :rules="[clientRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteClientId" :label="`${$t('sites.title')} ${$t('clients.title')}`"
                :items="clientsSites" item-title="name" item-value="id" hide-details="auto"
                @update:search="getClientsSites" clearable :readonly="!form.clientId" :rules="[siteClientRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" :label="$t('installations.serial')" hide-details="auto"
                :rules="[serialRequired]"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-menu v-model="showPicker" :close-on-content-click="false" transition="scale-transition" offset-y
                full-width max-width="290px" min-width="290px">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="form.installedDate" :label="$t('installations.installedDate')" readonly
                    hide-details="auto" v-bind="props" :rules="[installedDateRequired]"></v-text-field>
                </template>
                <v-date-picker v-model="selectedDate" title="" hide-header @update:model-value="showPicker = false"
                  :max="todayDate"></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="serialPicture" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.serialPicture')" chips :rules="[serialPictureRequired]" />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="installationPictures" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.installationPictures')" multiple chips
                :rules="[installationPicturesRequired]">
                <template v-slot:selection="{ fileNames }">
                  <v-chip v-for="fileName in fileNames" :key="fileName" size="small" label>
                    {{ fileName }}
                  </v-chip>
                </template>
              </v-file-input>
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
  <v-dialog v-model="updateDialog" max-width="600" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.update.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateInstallation">
          <v-row>
            <v-col cols="12">
              <v-autocomplete v-model="form.equipmentId" :label="$t('equipments.title')" :items="equipments"
                item-title="serialModel" item-value="id" hide-details="auto" @update:search="getEquipments"
                :clearable="!isApproved" :rules="[equipmentRequired]" :readonly="isApproved" />
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors"
                :clearable="!isApproved" :rules="[distributorRequired]" :readonly="isApproved" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteDistributorId"
                :label="`${$t('sites.title')} ${$t('distributors.title')}`" :items="distributorsSites" item-title="name"
                item-value="id" hide-details="auto" @update:search="getDistributorsSites" :clearable="!isApproved"
                :readonly="(isAdmin && !form.distributorId) || isApproved" :rules="[siteDistributorRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                item-value="id" hide-details="auto" @update:search="getClients" :clearable="!isApproved"
                :readonly="(isAdmin && !form.distributorId) || isApproved" :rules="[clientRequired]" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteClientId" :label="`${$t('sites.title')} ${$t('clients.title')}`"
                :items="clientsSites" item-title="name" item-value="id" hide-details="auto"
                @update:search="getClientsSites" :clearable="!isApproved" :readonly="!form.clientId || isApproved"
                :rules="[siteClientRequired]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" :label="$t('installations.serial')" hide-details="auto"
                :rules="[serialRequired]" :readonly="isApproved"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-menu v-model="showPicker" :close-on-content-click="false" transition="scale-transition" offset-y
                full-width max-width="290px" min-width="290px">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="form.installedDate" :label="$t('installations.installedDate')" readonly
                    hide-details="auto" v-bind="!isApproved && props" :rules="[installedDateRequired]"></v-text-field>
                </template>
                <v-date-picker v-model="selectedDate" title="" hide-header @update:model-value="showPicker = false"
                  :max="todayDate" :readonly="isApproved"></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12">
              <v-img v-if="form.installationFormatFile.path"
                :src="`/api/files?path=${form.installationFormatFile.path}&v=${Date.now()}`" />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="serialPicture" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.serialPicture')" chips :readonly="isApproved" />
            </v-col>
            <v-col cols="12">
              <v-img v-if="form.installationSerialFile.path"
                :src="`/api/files?path=${form.installationSerialFile.path}&v=${Date.now()}`" />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="installationPictures" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.installationPictures')" multiple chips
                :readonly="isApproved">
                <template v-slot:selection="{ fileNames }">
                  <v-chip v-for="fileName in fileNames" :key="fileName" size="small" label>
                    {{ fileName }}
                  </v-chip>
                </template>
              </v-file-input>
            </v-col>
            <v-col cols="12">
              <v-carousel>
                <v-carousel-item v-for="picture of form.installationEvidencesFiles"
                  :src="`/api/files?path=${picture.path}&v=${Date.now()}`" cover></v-carousel-item>
              </v-carousel>
            </v-col>
            <v-col v-if="!isApproved" class="text-end">
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
  <v-dialog v-model="deleteDialog" max-width="600" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.delete.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('installations.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2"></span>
        <v-btn @click="deleteInstallation" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="600" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.search.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <p class="text-subtitle-2 pb-2">{{ $t('installations.search.message') }}</p>
        <v-form @submit.prevent="doSearch">
          <v-row no-gutters="">
            <v-col cols="12">
              <v-text-field v-model="search" :label="$t('installations.search.fields')" hide-details="auto"
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

  <!-- Approval Installations Dialog -->
  <v-dialog v-model="approvalDialog" max-width="600" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.approval.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="approvalDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="approveForm" @submit.prevent="approveInstallation">
          <v-row>
            <v-col cols="12">
              <v-autocomplete v-model="form.equipmentId" :label="$t('equipments.title')" :items="equipments"
                item-title="serialModel" item-value="id" hide-details="auto"
                @update:search="async (search) => { await getEquipments(search); }" readonly />
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="async (search) => { await getDistributors(search) }" readonly />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteDistributorId"
                :label="`${$t('sites.title')} ${$t('distributors.title')}`" :items="distributorsSites" item-title="name"
                item-value="id" hide-details="auto" @update:search="async (search) => { await getDistributorsSites(search) }" readonly />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                item-value="id" hide-details="auto" @update:search="async (search) => { await getClients(search) }" readonly />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteClientId" :label="`${$t('sites.title')} ${$t('clients.title')}`"
                :items="clientsSites" item-title="name" item-value="id" hide-details="auto"
                @update:search="async (search) => { await getClientsSites(search) }" readonly />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" :label="$t('installations.serial')" hide-details="auto"
                readonly></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.installedDate" :label="$t('installations.installedDate')" hide-details="auto"
                readonly></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-img v-if="form.installationFormatFile.path"
                :src="`/api/files?path=${form.installationFormatFile.path}&v=${Date.now()}`" />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="serialPicture" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.serialPicture')" chips readonly />
            </v-col>
            <v-col cols="12">
              <v-img v-if="form.installationSerialFile.path"
                :src="`/api/files?path=${form.installationSerialFile.path}&v=${Date.now()}`" />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="installationPictures" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.installationPictures')" multiple chips readonly>
                <template v-slot:selection="{ fileNames }">
                  <v-chip v-for="fileName in fileNames" :key="fileName" size="small" label>
                    {{ fileName }}
                  </v-chip>
                </template>
              </v-file-input>
            </v-col>
            <v-col cols="12">
              <v-carousel>
                <v-carousel-item v-for="picture of form.installationEvidencesFiles"
                  :src="`/api/files?path=${picture.path}&v=${Date.now()}`" cover></v-carousel-item>
              </v-carousel>
            </v-col>
            <v-col class="d-flex justify-end ga-2">
              <v-btn variant="outlined" @click="approvalDialog = false">{{ $t('cancel') }}</v-btn>
              <v-btn class="bg-error" @click="rejectDialog = true">{{ $t('reject') }}</v-btn>
              <v-btn type="submit" class="bg-success">{{ $t('approve') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Reject Comments Dialog -->
  <v-dialog v-model="rejectDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.reject.title') }}
          <v-spacer></v-spacer>
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="rejectDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="rejectForm" @submit.prevent="rejectInstallation">
          <v-row>
            <v-col cols="12">
              <v-textarea v-model="rejectComments" :placeholder="$t('installations.reject.description')"></v-textarea>
            </v-col>
            <v-col class="d-flex justify-end ga-2">
              <v-btn variant="outlined" @click="rejectDialog = false">{{ $t('cancel') }}</v-btn>
              <v-btn type="submit" class="bg-error">{{ $t('reject') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onBeforeMount, toRefs } from 'vue'
import { searchMixin } from '~/mixins/searchMixin'
import { createMixin } from '~/mixins/createMixin'
import { useI18n } from 'vue-i18n'
import { useDate } from 'vuetify'

const { back } = useBack()
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { profile } = useProfile();
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
const equipments = ref([]);
const distributors = ref([]);
const distributorsSites = ref([]);
const clients = ref([]);
const clientsSites = ref([]);
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
const approveForm = ref();
const serialPicture = ref(null);
const installationPictures = ref(null);
const showPicker = ref(false);
const selectedDate = ref(null);
const approvalDialog = ref(false);
const rejectDialog = ref(false);
const rejectComments = ref('');
const form = ref({
  equipmentId: '',
  equipmentSerialModel: '',
  distributorId: '',
  distributorName: '',
  siteDistributorId: '',
  siteDistributorName: '',
  clientId: '',
  clientName: '',
  siteClientId: '',
  siteClientName: '',
  serial: '',
  installedDate: null,
  installationFormatFile: { originalName: '', path: '' },
  installationSerialFile: { originalName: '', path: '' },
  installationEvidencesFiles: []
})

const isApproved = computed(() => form.value.status === 'APPROVED');
const isAdmin = computed(() => profile.value.role === 'ADMIN');
const todayDate = computed(() => (new Date()).toISOString().split('T')[0])

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  const defaultHeaders = [
    { title: 'Id', key: 'id', align: 'center', sortable: false },
    { title: t('equipments.title'), key: 'equipmentSerialModel', align: 'center', sortable: false },
    { title: t('installations.serial'), key: 'serial', align: 'center', sortable: false },
    { title: t('installations.installedDate'), key: 'installedDate', align: 'center', sortable: false },
  ]

  if ($ability.can('update', 'installations') || $ability.can('delete', 'installations')) {
    defaultHeaders.push({ title: t('options'), key: 'option', align: 'center', sortable: false })
  }

  return defaultHeaders;
})

watch(createDialog, async (val) => {
  if (val) {
    await getEquipments();
    if (isAdmin.value) {
      await getDistributors();
    } else {
      await getDistributorsSites();
      await getClients();
    }
  } else {
    createForm.value.reset();
    resetForm();
  }
})

watch(updateDialog, async (val) => {
  if (val) {
    await getEquipments(form.value.equipmentSerialModel);
    if (isAdmin.value) await getDistributors(form.value.distributorName);
    await getDistributorsSites(form.value.siteDistributorName);
    await getClients(form.value.clientName);
  } else {
    updateForm.value.reset();
    resetForm();
  }
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(approvalDialog, async (val) => {
  if (val) {
    await getEquipments(form.value.equipmentSerialModel);
    if (isAdmin.value) await getDistributors(form.value.distributorName);
    await getDistributorsSites(form.value.siteDistributorName);
    await getClients(form.value.clientName);
  } else {
    approveForm.value.reset();
    resetForm();
  }
})

watch(rejectDialog, async (val) => {
  if (!val) rejectComments.value = '';
})

watch(page, async () => {
  await getInstallations();
})

watch(perPage, async () => {
  await getInstallations();
})

watch(() => form.value.distributorId, async (val, prev) => {
  if (!val) {
    form.value.siteDistributorId = null;
    form.value.siteDistributorName = null;
    form.value.clientId = null;
    form.value.clientName = null;
    return;
  }

  if (!prev || prev === form.value.clientId) {
    await getDistributorsSites(form.value.siteDistributorName);
    await getClients(form.value.clientName);
    return;
  }

  // There is a new clientId but the prev one it's different from the original
  form.value.siteDistributorId = null;
  form.value.siteDistributorName = null;
  form.value.clientId = null;
  form.value.clientName = null;
  await getDistributorsSites();
  await getClients();
})

watch(() => form.value.clientId, async (val, prev) => {
  if (!val) {
    form.value.siteClientId = null;
    form.value.siteClientName = null;
    return;
  }

  if (!prev || prev === form.value.clientId) {
    await getClientsSites(form.value.siteClientName);
    return;
  }

  // There is a new clientId but the prev one it's different from the original
  form.value.siteClientId = null;
  form.value.siteClientName = null;
  await getClientsSites();
})

watch(selectedDate, async (val) => {
  if (val) form.value.installedDate = date.format(val, 'fullDate');
})

onBeforeMount(async () => {
  if ($ability.can('read', 'installations')) {
    await getInstallations();
    return;
  }

  back();
})

const resetForm = () => {
  selectedDate.value = null
  serialPicture.value = null;
  installationPictures.value = null;
  form.value = {
    equipmentId: '',
    distributorId: '',
    siteDistributorId: '',
    clientId: '',
    siteClientId: '',
    serial: '',
    installedDate: null,
    installationFormatFile: { originalName: '', path: '' },
    installationSerialFile: { originalName: '', path: '' },
    installationEvidencesFiles: []
  }
}

const getEquipments = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value && !approvalDialog.value) return;
    const data = await $api('/api/equipments/', {
      query: {
        search: search || form.value.equipmentSerialModel,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    equipments.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getDistributors = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value && approvalDialog.value) return;
    const data = await $api('/api/distributors/', {
      query: {
        search: search || form.value.distributorName,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    distributors.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getDistributorsSites = async (search) => {
  try {
    if (!form.value.distributorId && !profile.value.distributor_id) return;
    const data = await $api(`/api/sites/distributors/${form.value.distributorId || profile.value.distributor_id}`, {
      query: {
        search: search || form.value.siteDistributorName,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    distributorsSites.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getClients = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value && !approvalDialog.value) return;
    if (!form.value.distributorId && !profile.value.distributor_id) return;
    const data = await $api(`/api/distributors/${form.value.distributorId || profile.value.distributor_id}/clients`, {
      query: {
        search: search || form.value.clientName,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    clients.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getClientsSites = async (search) => {
  try {
    if (!form.value.clientId) return;
    const data = await $api(`/api/sites/clients/${form.value.clientId}`, {
      query: {
        search: search || form.value.siteClientName,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    clientsSites.value = data.items
  } catch (err) {
    notify(err, 'error');
  }
}

const getInstallations = async () => {
  try {
    const data = await $api('/api/installations/', {
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

const getInstallation = async (id) => {
  try {
    const data = await $api(`/api/installations/${id}`, {
      method: 'GET'
    })
    form.value = data;
    selectedDate.value = new Date(form.value.installedDate);
  } catch (err) {
    notify(err, 'error');
  }
}

const createInstallation = async () => {
  try {
    if (!createModel.value) return;

    const formData = new FormData();

    formData.append('serialPicture', serialPicture.value);

    for (const installationPicture of installationPictures.value) {
      formData.append('installationPictures', installationPicture);
    }

    for (const [key, value] of Object.entries(form.value)) {
      formData.append(key, value);
    }

    if (!form.value.distributorId) {
      formData.set('distributorId', profile.value.distributor_id);
    }

    const { message } = await $api('/api/installations/', {
      method: 'POST',
      body: formData
    })
    notify(message, 'success');
    await getInstallations()
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

const updateInstallation = async () => {
  try {
    if (!updateModel.value) return;

    const formData = new FormData();

    if (serialPicture.value) formData.append('serialPicture', serialPicture.value);
    if (installationPictures.value) {
      for (const installationPicture of installationPictures.value) {
        formData.append('installationPictures', installationPicture);
      }
    }

    for (const [key, value] of Object.entries(form.value)) {
      formData.append(key, value);
    }

    if (!form.value.distributorId) {
      formData.set('distributorId', profile.value.distributor_id);
    }

    const { message } = await $api(`/api/installations/${form.value.id}`, {
      method: 'PUT',
      body: formData
    })
    notify(message, 'success');
    await getInstallations()
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

const deleteInstallation = async () => {
  try {
    const { message } = await $api(`/api/installations/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getInstallations()
    deleteDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

const doSearch = async () => {
  try {
    page.value = 1
    perPage.value = 15
    await getInstallations()
    searchDialog.value = false
  } catch (err) {
    notify(err, 'error');
  }
}

const approveInstallation = async () => {
  try {
    const { message } = await $api(`/api/installations/approve/${form.value.id}`, {
      method: 'PATCH'
    })
    notify(message, 'success');
    await getInstallations();
    approvalDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  }
}

const rejectInstallation = async () => {
  try {
    const { message } = await $api(`/api/installations/reject/${form.value.id}`, {
      method: 'POST',
      body: { rejectComments: rejectComments.value }
    })
    notify(message, 'success');
    await getInstallations();
    rejectDialog.value = false;
    approvalDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  }
}

// Rules
const equipmentRequired = (v) => !!v || t('installations.rules.equipmentRequired');
const distributorRequired = (v) => !!v || t('installations.rules.distributorRequired');
const siteDistributorRequired = (v) => !!v || t('installations.rules.siteDistributorRequired');
const clientRequired = (v) => !!v || t('installations.rules.clientRequired');
const siteClientRequired = (v) => !!v || t('installations.rules.siteClientRequired');
const serialRequired = (v) => !!v || t('installations.rules.serialRequired');
const installedDateRequired = (v) => !!v || t('installations.rules.installedDateRequired');
const serialPictureRequired = (v) => !!v || t('installations.rules.serialPictureRequired');
const installationPicturesRequired = (v) => (v && v.length > 0) || t('installations.rules.installationPicturesRequired');

</script>
