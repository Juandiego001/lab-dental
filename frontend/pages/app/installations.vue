<template>
  <v-container fluid class="fill-height align-start">
    <v-card class="d-flex flex-column" width="100%" height="100%" flat style="overflow: inherit;">
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('installations.title', 2) }}</p>
        <div>
          <client-only>
            <v-tooltip :text="$t('tooltip.create')" :disabled="loading" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('create', 'installations')" class="me-2" icon="mdi-plus"
                  size="small" variant="text" @click="createDialog = !createDialog" />
              </template>
            </v-tooltip>

            <v-tooltip :text="$t('tooltip.search')" :disabled="loading" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('read', 'installations')" class="me-2" icon="mdi-magnify"
                  size="small" variant="text" @click="searchDialog = !searchDialog" />
              </template>
            </v-tooltip>
          </client-only>
        </div>
      </v-card-title>
      <v-card-text>
        <client-only>
          <v-data-table-server :items="items" :headers="headers" :page="page" :items-per-page="perPage"
            :items-length="total" :items-per-page-options="itemsPerPageOptions" @update:page="v => page = v"
            @update:itemsPerPage="v => perPage = v" @update:sort-by="v => sortBy = v" :loading="loading">
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
              <v-tooltip :text="$t('tooltip.viewUpdate')" :disabled="loading" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" v-if="$ability.can('update', 'installations')" class="my-2 bg-primary me-2"
                    size="small" icon="mdi-pencil"
                    @click="async () => { await getInstallation(item.id); updateDialog = true }" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('tooltip.approveReject')" :disabled="loading" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" v-if="isAdmin" class="my-2 me-2 bg-secondary" size="small" icon="mdi-eye"
                    @click="async () => { await getInstallation(item.id); approvalDialog = true }" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('tooltip.delete')" :disabled="loading" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" v-if="$ability.can('delete', 'installations')" class="my-2 bg-red" size="small"
                    icon="mdi-trash-can" @click="form.id = item.id; deleteDialog = true" />
                </template>
              </v-tooltip>
            </template>
          </v-data-table-server>
        </client-only>
      </v-card-text>
      <v-card-actions class="w-100 d-flex align-center justify-end ga-2 flex-wrap">
        <p class="text-body-2 rounded-lg bg-grey py-1 px-2">{{ $t("installations.statuses.title") }}</p>
        <p class="d-inline-block py-1 px-2 rounded-lg bg-primary text-caption">{{ $t("installations.statuses.active") }}
        </p>
        <p class="d-inline-block py-1 px-2 rounded-lg bg-success text-caption">
          {{ $t("installations.statuses.approved") }}
        </p>
        <p class="d-inline-block py-1 px-2 rounded-lg bg-error text-caption">{{ $t("installations.statuses.rejected") }}
        </p>
      </v-card-actions>
    </v-card>
  </v-container>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createInstallation">
          <v-row dense>
            <v-col cols="12">
              <v-autocomplete v-model="form.equipmentId" :label="$t('equipments.title')" :items="equipments"
                item-title="modelReference" item-value="id" hide-details="auto" clearable :rules="[equipmentRequired]"
                @update:search="(modelReference) => {
                  if (!createDialog) return;
                  getEquipments({
                    equipmentId: form.equipmentId,
                    modelReference,
                    withPicture: false
                  })
                }" />
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
              <v-autocomplete v-model="form.siteDistributorId"
                :label="`${$t('sites.title')} ${$t('distributors.title')}`" :items="distributorsSites" item-title="name"
                item-value="id" hide-details="auto" clearable :readonly="isAdmin && !form.distributorId"
                :rules="[siteDistributorRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getDistributorsSites(name)
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                item-value="id" hide-details="auto" clearable :readonly="isAdmin && !form.distributorId"
                :rules="[clientRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getClients({ distributorId: form.distributorId, clientId: form.clientId, name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteClientId" :label="`${$t('sites.title')} ${$t('clients.title')}`"
                :items="clientsSites" item-title="name" item-value="id" hide-details="auto" :readonly="!form.clientId"
                :rules="[siteClientRequired]" @update:search="(name) => {
                  if (!createDialog) return;
                  getClientsSites(name)
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" :label="$t('installations.serial')" hide-details="auto"
                :rules="[serialRequired]" counter="30" maxlength="30" />
            </v-col>
            <v-col cols="12">
              <v-menu v-model="showPicker" :close-on-content-click="false" transition="scale-transition" offset-y
                full-width max-width="290px" min-width="290px">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="form.installedDate" :label="$t('installations.installedDate')" readonly
                    hide-details="auto" v-bind="props" :rules="[installedDateRequired]" />
                </template>
                <v-date-picker v-model="selectedDate" title="" hide-header @update:model-value="showPicker = false"
                  :max="todayDate" />
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
              <v-btn variant="outlined" @click="createDialog = false" @mousedown.prevent :disabled="loading">{{
                $t('cancel') }}</v-btn>
              <span class="mx-1"></span>
              <v-btn type="submit" class="bg-primary" @mousedown.prevent :loading="loading">{{ $t('register') }}</v-btn>
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
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateInstallation">
          <v-row dense>
            <v-col cols="12">
              <v-autocomplete v-model="form.equipmentId" :label="$t('equipments.title')" :items="equipments"
                item-title="modelReference" item-value="id" hide-details="auto" :clearable="!isApproved"
                :rules="[equipmentRequired]" :readonly="isApproved" @update:search="(modelReference) => {
                  if (!updateDialog) return;
                  getEquipments({
                    equipmentId: form.equipmentId,
                    modelReference,
                    withPicture: false
                  })
                }" />
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" :clearable="!isApproved"
                :rules="[distributorRequired]" :readonly="isApproved" @update:search="(name) => {
                  if (!updateDialog) return;
                  getDistributors({ distributorsIds: [form.distributorId], name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteDistributorId"
                :label="`${$t('sites.title')} ${$t('distributors.title')}`" :items="distributorsSites" item-title="name"
                item-value="id" hide-details="auto" :clearable="!isApproved"
                :readonly="(isAdmin && !form.distributorId) || isApproved" :rules="[siteDistributorRequired]"
                @update:search="(name) => {
                  if (!updateDialog) return;
                  getDistributorsSites(name)
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                item-value="id" hide-details="auto" :clearable="!isApproved"
                :readonly="(isAdmin && !form.distributorId) || isApproved" :rules="[clientRequired]" @update:search="(name) => {
                  if (!updateDialog) return;
                  getClients({ distributorId: form.distributorId, clientId: form.clientId, name })
                }" />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteClientId" :label="`${$t('sites.title')} ${$t('clients.title')}`"
                :items="clientsSites" item-title="name" item-value="id" hide-details="auto" :clearable="!isApproved"
                :readonly="!form.clientId || isApproved" :rules="[siteClientRequired]" @update:search="(name) => {
                  if (!updateDialog) return;
                  getClientsSites(name)
                }" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" :label="$t('installations.serial')" hide-details="auto"
                :rules="[serialRequired]" :readonly="isApproved" counter="30" maxlength="30" />
            </v-col>
            <v-col cols="12">
              <v-menu v-model="showPicker" :close-on-content-click="false" transition="scale-transition" offset-y
                full-width max-width="290px" min-width="290px">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="form.installedDate" :label="$t('installations.installedDate')" readonly
                    hide-details="auto" v-bind="!isApproved && props" :rules="[installedDateRequired]" />
                </template>
                <v-date-picker v-model="selectedDate" title="" hide-header @update:model-value="showPicker = false"
                  :max="todayDate" :readonly="isApproved" />
              </v-menu>
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="serialPicture" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.serialPicture')" chips :readonly="isApproved" />
            </v-col>
            <v-col cols="12">
              <v-img v-if="form.installationSerialFile.path"
                :src="`/api/files?path=${form.installationSerialFile.path}`" />
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
                  :src="`/api/files?path=${picture.path}`" cover />
              </v-carousel>
            </v-col>
            <v-col v-if="!isApproved" class="text-end">
              <v-btn variant="outlined" @click="updateDialog = false" @mousedown.prevent :disabled="loading">{{
                $t('cancel') }}</v-btn>
              <span class="mx-1" />
              <v-btn type="submit" class="bg-primary" @mousedown.prevent :loading="loading">{{ $t('register') }}</v-btn>
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
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('installations.delete.message') }}</p>
        <v-btn @click="deleteDialog = false" variant="outlined" :disabled="loading">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteInstallation" class="bg-red" :loading="loading">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Approval Installations Dialog -->
  <v-dialog v-model="approvalDialog" max-width="600" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.approval.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="approvalDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="approveForm" @submit.prevent="approveInstallation">
          <v-row dense>
            <v-col cols="12">
              <v-autocomplete v-model="form.equipmentId" :label="$t('equipments.title')" :items="equipments"
                item-title="modelReference" item-value="id" hide-details="auto" readonly />
            </v-col>
            <v-col v-if="isAdmin" cols="12">
              <v-autocomplete v-model="form.distributorId" :label="$t('distributors.title')" :items="distributors"
                item-title="name" item-value="id" hide-details="auto" readonly />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteDistributorId"
                :label="`${$t('sites.title')} ${$t('distributors.title')}`" :items="distributorsSites" item-title="name"
                item-value="id" hide-details="auto" readonly />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.clientId" :label="$t('clients.title')" :items="clients" item-title="name"
                item-value="id" hide-details="auto" readonly />
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="form.siteClientId" :label="`${$t('sites.title')} ${$t('clients.title')}`"
                :items="clientsSites" item-title="name" item-value="id" hide-details="auto" readonly />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" :label="$t('installations.serial')" hide-details="auto" readonly />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.installedDate" :label="$t('installations.installedDate')" hide-details="auto"
                readonly />
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="serialPicture" :prepend-icon="null" prepend-inner-icon="mdi-paperclip"
                hide-details="auto" :label="$t('installations.serialPicture')" chips readonly />
            </v-col>
            <v-col cols="12">
              <v-img v-if="form.installationSerialFile.path"
                :src="`/api/files?path=${form.installationSerialFile.path}`" />
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
                  :src="`/api/files?path=${picture.path}`" cover />
              </v-carousel>
            </v-col>
            <v-col class="d-flex justify-end ga-2">
              <v-btn variant="outlined" @click="approvalDialog = false" @mousedown.prevent :disabled="approveLoading">{{
                $t('cancel') }}</v-btn>
              <v-btn class="bg-error" @click="rejectDialog = true" @mousedown.prevent :disabled="approveLoading">{{
                $t('reject') }}</v-btn>
              <v-btn type="submit" class="bg-success" @mousedown.prevent :loading="approveLoading">{{ $t('approve')
              }}</v-btn>
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
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="rejectDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="rejectForm" @submit.prevent="rejectInstallation">
          <v-row dense>
            <v-col cols="12">
              <v-textarea v-model="rejectComments" :placeholder="$t('installations.reject.description')"></v-textarea>
            </v-col>
            <v-col class="d-flex justify-end ga-2">
              <v-btn variant="outlined" @click="rejectDialog = false" @mousedown.prevent :disabled="rejectLoading">{{
                $t('cancel') }}</v-btn>
              <v-btn type="submit" class="bg-error" @mousedown.prevent :loading="rejectLoading">{{ $t('reject')
              }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="700" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('installations.search.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="searchDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="doSearch">
          <v-row dense>
            <!-- Equipments -->
            <v-col cols="12">
              <p class="text-body-2 text-primary">{{ $t('equipments.title', 2) }}</p>
            </v-col>
            <v-col class="pb-4" cols="12">
              <v-autocomplete v-model="searchForm.equipmentId" :label="$t('equipments.title')" :items="equipments"
                item-title="modelReference" item-value="id" hide-details="auto" clearable @update:search="(modelReference) => {
                  getEquipments({ equipmentId: searchForm.equipmentId, modelReference, withPicture: false })
                }" />
            </v-col>

            <!-- Distributors -->
            <v-col v-if="isAdmin" class="d-flex flex-column" cols="6">
              <p class="text-body-2 text-primary pb-2">{{ $t('distributors.title', 2) }}</p>
              <v-autocomplete class="flex-grow-0" v-model="searchForm.distributorId" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" hide-details="auto" clearable @update:search="(name) => {
                  getDistributors({ distributorsIds: [searchForm.distributorId], name })
                }" />
            </v-col>

            <!-- Clients -->
            <v-col class="d-flex flex-column" cols="6">
              <p class="text-body-2 text-primary pb-2">{{ $t('clients.title', 2) }}</p>
              <v-autocomplete class="flex-grow-0" v-model="searchForm.clientId" :label="$t('clients.title')"
                :items="clients" item-title="name" item-value="id" hide-details="auto" clearable @update:search="(name) => {
                  getClients({ distributorId: searchForm.distributorId, clientId: searchForm.clientId, name })
                }" />
            </v-col>

            <!-- Installations -->
            <v-col class="mt-2 d-flex flex-column" cols="12">
              <p class="text-body-2 text-primary pb-2">{{ $t('installations.title', 2) }}</p>
            </v-col>

            <v-col cols="6">
              <v-text-field v-model="searchForm.serial" :label="$t('installations.serial')" hide-details="auto"
                counter="30" maxlength="30" clearable />
            </v-col>

            <v-col cols="6">
              <v-select v-model="searchForm.status" item-title="title" item-value="value" :items="installationStatuses"
                hide-details="auto" :label="$t('installations.statuses.label')" clearable />
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
import { ref, computed, watch, onBeforeMount } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDate } from 'vuetify'

const { back } = useBack()
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { profile, isAdmin } = useProfile();
const { t } = useI18n();
const date = useDate();
const { items: equipments, getEquipments } = useEquipments();
const { items: distributors, getDistributors } = useDistributors();
const { items: clients, getClients } = useClients();
const { getSites } = useSites();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('installations.title', 2)}`
})

const rejectLoading = ref(false);
const approveLoading = ref(false);
const loading = ref(false);
const searchDialog = ref(false);
const createDialog = ref(false);
const distributorsSites = ref([]);
const clientsSites = ref([]);
const items = ref([]);
const page = ref(1);
const perPage = ref(15);
const sortBy = ref(null);
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
  equipmentId: null,
  equipmentModelReference: '',
  distributorId: null,
  distributorName: '',
  siteDistributorId: null,
  siteDistributorName: '',
  clientId: null,
  clientName: '',
  siteClientId: null,
  siteClientName: '',
  serial: '',
  installedDate: null,
  installationSerialFile: { originalName: '', path: '' },
  installationEvidencesFiles: []
})
const searchForm = ref({
  equipmentId: null,
  distributorId: null,
  clientId: null,
  serial: null,
  status: null,
})

const isApproved = computed(() => form.value.status === 'APPROVED');
const todayDate = computed(() => (new Date()).toISOString().split('T')[0])

const installationStatuses = computed(() => [
  {
    title: t('installations.statuses.active'),
    value: "ACTIVE"
  },
  {
    title: t('installations.statuses.approved'),
    value: "APPROVED"
  },
  {
    title: t('installations.statuses.rejected'),
    value: "REJECTED"
  }
])

const itemsPerPageOptions = computed(() => [
  { value: 15, title: '15' },
  { value: 25, title: '25' },
  { value: 50, title: '50' },
  { value: 100, title: '100' }
])

const headers = computed(() => {
  const defaultHeaders = [
    { title: t('equipments.title'), key: 'equipmentModelReference' },
  ]

  if (isAdmin.value) {
    defaultHeaders.push({ title: t('distributors.title'), key: 'distributorName' });
  } else {
    defaultHeaders.push({ title: t('clients.title'), key: 'clientName' });
  }

  defaultHeaders.push({ title: t('installations.serial'), key: 'serial', align: 'center' });
  defaultHeaders.push({ title: t('installations.installedDate'), key: 'installedDate', align: 'center' });

  if (isAdmin.value) {
    defaultHeaders.push({ title: t('installations.expirationDate'), key: 'expirationDate', align: 'center' });
  }

  if ($ability.can('update', 'installations') || $ability.can('delete', 'installations')) {
    defaultHeaders.push({ title: t('options'), key: 'option', align: 'center', sortable: false })
  }

  return defaultHeaders;
})

watch(createDialog, async (val) => {
  if (!val) {
    createForm.value.reset();
    resetForm();
    return;
  }
  await getEquipments({ withPicture: false });
  if (isAdmin.value) {
    await getDistributors({});
  } else {
    await getDistributorsSites();
    await getClients({});
  }
})

watch(updateDialog, async (val) => {
  if (!val) {
    updateForm.value.reset();
    resetForm();
    return;
  }
  await getEquipments({ equipmentId: form.value.equipmentId, withPicture: false });
  if (isAdmin.value) {
    await getDistributors({ distributorsIds: [form.value.distributorId] });
  }
  await getDistributorsSites();
  await getClients({ clientId: form.value.clientId });
  await getClientsSites();
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(approvalDialog, async (val) => {
  if (!val) {
    approveForm.value.reset();
    resetForm();
    return;
  }
  await getEquipments({ equipmentId: form.value.equipmentId, withPicture: false });
  if (isAdmin.value) {
    await getDistributors({ distributorsIds: [form.value.distributorId] });
  }
  await getDistributorsSites();
  await getClients({ clientId: form.value.clientId });
  await getClientsSites();
})

watch(rejectDialog, async (val) => {
  if (!val) rejectComments.value = '';
})

watch(searchDialog, async (val) => {
  if (!val) return;
  getEquipments({
    equipmentId: searchForm.value.equipmentId,
    withPicture: false
  });
  getDistributors({
    distributorsIds: [searchForm.value.distributorId]
  });
  getClients({
    clientId: searchForm.value.clientId
  });
})

watch(page, async () => {
  await getInstallations();
})

watch(perPage, async () => {
  await getInstallations();
})

watch(sortBy, async (v) => {
  if (v && v.length) {
    await getInstallations();
  }
})

watch(() => form.value.distributorId, async (val, prev) => {
  if (!updateDialog.value && !createDialog.value) return;
  form.value.siteDistributorId = null;
  form.value.siteDistributorName = null;
  form.value.clientId = null;
  form.value.clientName = null;
  await getDistributorsSites(form.value.siteDistributorName);
  await getClients({ distributorId: form.value.distributorId });
})

watch(() => form.value.clientId, async (val, prev) => {
  if (!updateDialog.value && !createDialog.value) return;
  form.value.siteClientId = null;
  form.value.siteClientName = null;
  await getClientsSites(form.value.siteClientName);
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
    equipmentId: null,
    distributorId: null,
    siteDistributorId: null,
    clientId: null,
    siteClientId: null,
    serial: '',
    installedDate: null,
    installationSerialFile: { originalName: '', path: '' },
    installationEvidencesFiles: []
  }
}

const getDistributorsSites = async (name) => {
  try {
    loading.value = true;
    if (!form.value.distributorId && !profile.value.distributor_id) return;
    const data = await getSites({
      siteId: form.value.siteDistributorId,
      distributorId: form.value.distributorId || profile.value.distributor_id,
      name
    })
    distributorsSites.value = data.items
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getClientsSites = async (name) => {
  try {
    loading.value = true;
    if (!form.value.clientId) return;
    const data = await getSites({
      siteId: form.value.siteClientId,
      clientId: form.value.clientId,
      name,
    })
    clientsSites.value = data.items
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getInstallations = async () => {
  try {
    loading.value = true;
    const data = await $api('/api/installations/search', {
      body: {
        equipmentId: searchForm.value.equipmentId,
        distributorId: searchForm.value.distributorId,
        clientId: searchForm.value.clientId,
        serial: searchForm.value.serial,
        status: searchForm.value.status,
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

const getInstallation = async (id) => {
  try {
    loading.value = true;
    const data = await $api(`/api/installations/${id}`, {
      method: 'GET'
    })
    form.value = data;
    selectedDate.value = new Date(form.value.installedDate);
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const createInstallation = async () => {
  try {
    loading.value = true;
    const { valid } = await createForm.value.validate();
    if (!valid) {
      notify(t('missingRequiredFields'), 'error');
      return
    };
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
  } finally {
    loading.value = false;
  }
}

const updateInstallation = async () => {
  try {
    loading.value = true;
    const { valid } = await updateForm.value.validate();
    if (!valid) {
      notify(t('missingRequiredFields'), 'error');
      return
    };
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
  } finally {
    loading.value = false;
  }
}

const deleteInstallation = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/installations/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getInstallations()
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
    await getInstallations()
    searchDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const approveInstallation = async () => {
  try {
    approveLoading.value = true;
    const { message } = await $api(`/api/installations/approve/${form.value.id}`, {
      method: 'PATCH'
    })
    notify(message, 'success');
    await getInstallations();
    approvalDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    approveLoading.value = false;
  }
}

const rejectInstallation = async () => {
  try {
    rejectLoading.value = true;
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
  } finally {
    rejectLoading.value = false;
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
