<template>
  <v-container fluid class="fill-height align-start">
    <v-card class="d-flex flex-column" width="100%" height="100%" flat>
      <v-card-title>{{ $t('installations.title', 2) }}</v-card-title>
      <v-card-text>
        <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
          :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
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
              icon="mdi-pencil" @click="getInstallation(item.id, true)"></v-btn>
            <v-btn v-if="$ability.can('delete', 'installations')" class="my-2 bg-red me-2" size="small"
              icon="mdi-trash-can" @click="form.id = item.id"></v-btn>
            <v-btn v-if="isAdmin" class="my-2 bg-secondary" size="small" icon="mdi-eye"
              @click="getInstallation(item.id, false)"></v-btn>
          </template>
        </v-data-table-server>
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
              <v-file-input v-model="formatPicture" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.formatPicture')" chips :rules="[formatPictureRequired]" />
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
              <v-file-input v-model="formatPicture" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.formatPicture')" chips />
            </v-col>
            <v-col cols="12">
              <v-img v-if="form.installationFormatFile.path"
                :src="`/api/files?path=${form.installationFormatFile.path}&v=${Date.now()}`" />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="serialPicture" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.serialPicture')" chips />
            </v-col>
            <v-col cols="12">
              <v-img v-if="form.installationSerialFile.path"
                :src="`/api/files?path=${form.installationSerialFile.path}&v=${Date.now()}`" />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="installationPictures" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.installationPictures')" multiple chips>
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
                item-title="serialModel" item-value="id" hide-details="auto" @update:search="getEquipments" readonly />
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" @update:search="getDistributors" readonly />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteDistributorId"
                :label="`${$t('sites.title')} ${$t('distributors.title')}`" :items="distributorsSites" item-title="name"
                item-value="id" hide-details="auto" @update:search="getDistributorsSites" readonly />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                item-value="id" hide-details="auto" @update:search="getClients" readonly />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteClientId" :label="`${$t('sites.title')} ${$t('clients.title')}`"
                :items="clientsSites" item-title="name" item-value="id" hide-details="auto"
                @update:search="getClientsSites" readonly />
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
              <v-file-input v-model="formatPicture" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.formatPicture')" chips readonly />
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
const { show } = useSnackbar();
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
const formatPicture = ref(null);
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

const isAdmin = computed(() => profile.value.role === 'ADMIN');

const todayDate = computed(() => (new Date()).toISOString().split('T')[0])

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => [
  { title: 'Id', key: 'id', align: 'center', sortable: false },
  { title: t('equipments.title'), key: 'equipmentSerialModel', align: 'center', sortable: false },
  { title: t('installations.serial'), key: 'serial', align: 'center', sortable: false },
  { title: t('installations.installedDate'), key: 'installedDate', align: 'center', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

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
    if (isAdmin.value) {
      await getDistributors(form.value.distributorName);
    }
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
    if (isAdmin.value) {
      await getDistributors(form.value.distributorName);
    }
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

watch(() => form.value.distributorId, async (val) => {
  if (val) {
    if (approvalDialog.value || updateDialog.value || createDialog.value) {
      await getDistributorsSites();
      await getClients();
    } else {
      await getDistributorsSites(form.value.siteDistributorName);
      await getClients(form.value.clientName);
    }
    nextTick(() => {
      if (form.value.siteDistributorId && !(distributorsSites.value.map(e => e.id)).includes(form.value.siteDistributorId)) {
        form.value.siteDistributorId = '';
        form.value.siteDistributorName = '';
      }
      if (form.value.clientId && !(clients.value.map(e => e.id)).includes(form.value.clientId)) {
        form.value.clientId = '';
        form.value.clientName = '';
      }
    })
  } else {
    form.value.siteDistributorId = '';
    form.value.siteDistributorName = '';
    form.value.clientId = '';
    form.value.clientName = '';
  }
})

watch(() => form.value.clientId, async (val) => {
  if (val) {
    if (approvalDialog.value || updateDialog.value || createDialog.value) await getClientsSites();
    else await getClientsSites(form.value.siteClientName);
    nextTick(() => {
      if (form.value.siteClientId && !(clientsSites.value.map(e => e.id)).includes(form.value.siteClientId)) {
        form.value.siteClientId = '';
        form.value.siteClientName = '';
      }
    })
  } else {
    form.value.siteClientId = '';
    form.value.siteClientName = '';
  }
})

watch(selectedDate, async (val) => {
  if (val) form.value.installedDate = date.format(val, 'fullDate');
})

onBeforeMount(async () => {
  if (!$ability.can('read', 'installations')) {
    navigateTo(history.state?.back || '/login');
    return;
  }
  await getInstallations();
})

const resetForm = () => {
  selectedDate.value = null
  formatPicture.value = null;
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
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    equipments.value = data.items
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getDistributors = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value && approvalDialog.value) return;
    const data = await $api('/api/distributors/', {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    distributors.value = data.items
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getDistributorsSites = async (search) => {
  try {
    if (!form.value.distributorId && !profile.value.distributor_id) return;
    const data = await $api(`/api/sites/distributors/${form.value.distributorId || profile.value.distributor_id}`, {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    distributorsSites.value = data.items
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getClients = async (search) => {
  try {
    if (!createDialog.value && !updateDialog.value && !approvalDialog.value) return;
    if (!form.value.distributorId && !profile.value.distributor_id) return;
    const data = await $api(`/api/distributors/${form.value.distributorId || profile.value.distributor_id}/clients`, {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    clients.value = data.items
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getClientsSites = async (search) => {
  try {
    if (!form.value.clientId) return;
    const data = await $api(`/api/sites/clients/${form.value.clientId}`, {
      query: {
        search,
        page: page.value,
        perPage: perPage.value
      },
      method: 'GET'
    })
    clientsSites.value = data.items
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
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
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const getInstallation = async (id, isUpdating) => {
  try {
    const data = await $api(`/api/installations/${id}`, {
      method: 'GET'
    })
    form.value = data
    nextTick(() => {
      selectedDate.value = new Date(form.value.installedDate);
      if (isUpdating) updateDialog.value = true;
      else approvalDialog.value = true;
    });
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const createInstallation = async () => {
  try {
    if (!createModel.value) return;

    const formData = new FormData();

    formData.append('formatPicture', formatPicture.value);
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
    show(message, 'success');
    await getInstallations()
    createDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const updateInstallation = async () => {
  try {
    if (!updateModel.value) return;

    const formData = new FormData();

    if (formatPicture.value) formData.append('formatPicture', formatPicture.value);
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
    show(message, 'success');
    await getInstallations()
    updateDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const deleteInstallation = async () => {
  try {
    const { message } = await $api(`/api/installations/${form.value.id}`, {
      method: 'DELETE'
    })
    show(message, 'success');
    await getInstallations()
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
    await getInstallations()
    searchDialog.value = false
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const approveInstallation = async () => {
  try {
    const { message } = await $api(`/api/installations/approve/${form.value.id}`, {
      method: 'PATCH'
    })
    show(message, 'success');
    await getInstallations();
    approvalDialog.value = false;
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
  }
}

const rejectInstallation = async () => {
  try {
    const { message } = await $api(`/api/installations/reject/${form.value.id}`, {
      method: 'POST',
      body: { rejectComments: rejectComments.value }
    })
    show(message, 'success');
    await getInstallations();
    rejectDialog.value = false;
    approvalDialog.value = false;
  } catch (err) {
    const errorMessage = err.data?.message || err;
    show(errorMessage, 'error');
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
const formatPictureRequired = (v) => !!v || t('installations.rules.formatPictureRequired');
const serialPictureRequired = (v) => !!v || t('installations.rules.serialPictureRequired');
const installationPicturesRequired = (v) => (v && v.length > 0) || t('installations.rules.installationPicturesRequired');

</script>
