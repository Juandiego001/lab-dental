<template>
  <v-container fluid class="fill-height align-start">
    <v-card class="d-flex flex-column" width="100%" height="100%" flat style="overflow: inherit;">
      <v-card-title class="d-flex justify-space-between">
        <p>{{ $t('warranties.title', 2) }}</p>
        <div>
          <client-only>
            <v-tooltip :text="$t('tooltip.create')" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('create', 'warranties')" class="me-2" icon="mdi-plus"
                  size="small" variant="text" @click="createDialog = !createDialog" />
              </template>
            </v-tooltip>

            <v-tooltip :text="$t('tooltip.search')" location="bottom">
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" v-if="$ability.can('read', 'warranties')" class="me-2" icon="mdi-magnify"
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
            @update:itemsPerPage="v => perPage = v" :disable-sort="true" show-expand :loading="loading">
            <template v-slot:expanded-row="{ columns, item }">
              <tr>
                <td :colspan="columns.length" class="bg-grey-lighten-4 pa-3">
                  <div class="d-flex flex-column ga-1 mb-2">
                    <p class="text-caption text-decoration-underline">{{ $t('warranties.shiptTo') }}</p>
                    <pre class="text-body-2" style="white-space: pre-wrap;">{{ item.shiptTo }}</pre>
                  </div>
                  <div class="d-flex flex-column ga-1 mb-2">
                    <p class="text-caption text-decoration-underline">{{ $t('warranties.problem') }}</p>
                    <pre class="text-body-2" style="white-space: pre-wrap;">{{ item.problem }}</pre>
                  </div>
                  <div class="d-flex flex-column ga-1 mb-2">
                    <p class="text-caption text-decoration-underline">{{ $t('warranties.solution') }}</p>
                    <pre class="text-body-2" style="white-space: pre-wrap;">{{ item.solution }}</pre>
                  </div>
                </td>
              </tr>
            </template>

            <template v-slot:item.invoice="{ item }">
              <span :class="`rounded-lg py-1 px-2
                    ${item.status === 'ACTIVE' && 'bg-primary'}
                    ${item.status === 'APPROVED' && 'bg-success'}
                    ${item.status === 'REJECTED' && 'bg-error'}
                  `">
                {{ item.invoice }}
              </span>
            </template>
            <template v-slot:item.wco="{ item }">
              <span v-if="!item.wco" class="text-gray">-</span>
              <span v-else class="bg-secondary rounded-lg py-1 px-2">{{ item.wco }}</span>
            </template>
            <template v-slot:item.saleDate="{ item }">{{ date.format(item.saleDate, 'fullDate') }}</template>

            <template v-slot:item.option="{ item }">
              <v-tooltip :text="$t('warranties.tooltip.viewUpdate')" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" v-if="$ability.can('update', 'installations') && item.status !== 'APPROVED'"
                    class="my-2 bg-primary me-2" size="small" icon="mdi-pencil"
                    @click="async () => { await getWarranty(item.id); updateDialog = true }" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('warranties.tooltip.approveReject')" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" v-if="isAdmin" class="my-2 me-2 bg-secondary" size="small" icon="mdi-eye"
                    @click="async () => { await getWarranty(item.id); approvalDialog = true }" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('warranties.tooltip.files')" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" class="my-2 bg-secondary me-2" size="small" icon="mdi-image-area"
                    @click="async () => { warrantyId = item.id; await getWarrantyFiles({}); tableDialog = true; }" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('warranties.tooltip.viewPdf')" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" class="my-2 bg-secondary me-2" size="small" icon="mdi-open-in-new"
                    :href="`/api/warranties/${item.id}/pdf`" target="_blank" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('warranties.tooltip.logs')" location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" v-if="isAdmin" class="my-2 bg-secondary me-2" size="small"
                    icon="mdi-file-document" />
                </template>
              </v-tooltip>

              <v-tooltip :text="$t('warranties.tooltip.delete')" location="bottom">
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
  <v-dialog v-model="createDialog" max-width="800" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('warranties.create.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="createDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="createForm" v-model="createModel" @submit.prevent="createWarranty">
          <v-row dense>
            <!-- Equipment Info -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.equipmentInfo') }}
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="equipment" :label="$t('equipments.title')" :items="equipments"
                item-title="modelReference" return-object hide-details="auto" clearable :rules="[equipmentRequired]"
                autocomplete="off" @update:search="(modelReference) => {
                  if (!createDialog) return;
                  getEquipments({
                    equipmentId: equipment.id,
                    modelReference,
                    withPicture: false
                  })
                }" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="equipment.model" :label="$t('equipments.model')" hide-details readonly />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="equipment.reference" :label="$t('equipments.reference')" hide-details readonly />
            </v-col>

            <!-- Distributor -->
            <v-col cols="6" class="mt-2">
              <v-row dense>
                <template v-if="isAdmin">
                  <v-col cols="12" class="text-body-2 text-primary">
                    {{ $t('distributors.title') }}
                  </v-col>
                  <v-col cols="12">
                    <v-autocomplete class="flex-grow-0" v-model="form.distributorId" :label="$t('distributors.title')"
                      :items="distributors" item-title="name" item-value="id" hide-details="auto" clearable
                      autocomplete="off" @update:search="(name) => {
                        getDistributors({ distributorsIds: [form.distributorId], name })
                      }" />
                  </v-col>
                </template>

                <!-- Distributor Contact -->
                <v-col cols="12" class="text-body-2 text-primary">
                  {{ $t('warranties.distributorContact') }}
                </v-col>
                <v-col>
                  <v-autocomplete v-model="contact" :label="$t('warranties.contact')" :items="distributorsContacts"
                    item-title="fullName" hide-details="auto" clearable :readonly="!form.distributorId"
                    :rules="[contactDistributorRequired]" return-object autocomplete="off" @update:search="async (name) => {
                      if (!createDialog) return;
                      await getDistributorsContacts(name)
                    }" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('contacts.fullName')" hide-details readonly
                    :model-value="contact?.fullName" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('contacts.email')" hide-details readonly :model-value="contact?.email" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('contacts.position')" hide-details readonly
                    :model-value="contact?.position" />
                </v-col>
              </v-row>
            </v-col>

            <!-- Distributor Site -->
            <v-col cols="6" class="mt-2">
              <v-row dense>
                <v-col cols="12" class="text-body-2 text-primary">
                  {{ $t('warranties.distributorSite') }}
                </v-col>
                <v-col cols="12">
                  <v-autocomplete v-model="site" :label="`${$t('sites.title')} ${$t('distributors.title')}`"
                    :items="distributorsSites" item-title="name" return-object hide-details="auto" clearable
                    :readonly="!form.distributorId" :rules="[siteDistributorRequired]" autocomplete="off"
                    @update:search="(name) => {
                      if (!createDialog) return;
                      getDistributorsSites(name)
                    }" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('countries')" hide-details :model-value="address?.country?.name" readonly />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('states')" hide-details :model-value="address?.state?.name" readonly />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('cities')" hide-details :model-value="address?.city?.name" readonly />
                </v-col>
              </v-row>
            </v-col>

            <!-- Warranty Info -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.info') }}
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" :label="$t('warranties.serial')" hide-details="auto"
                :rules="[serialRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="6">
              <v-menu v-model="showPicker" :close-on-content-click="false" transition="scale-transition" offset-y
                full-width max-width="290px" min-width="290px">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="form.saleDate" :label="$t('warranties.saleDate')" readonly hide-details="auto"
                    v-bind="props" :rules="[saleDateRequired]" />
                </template>
                <v-date-picker v-model="selectedDate" title="" hide-header @update:model-value="showPicker = false"
                  :max="todayDate" />
              </v-menu>
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.invoice" hide-details="auto" :label="$t('warranties.invoice')"
                :rules="[invoiceRequired]" counter="40" maxlength="40" />
            </v-col>

            <!-- Issue Type -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.issueType') }}
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="reasonsIds" :label="$t('warranties.issueType')" :items="reasons"
                item-title="name" item-value="id" hide-details="auto" clearable multiple chips
                :readonly="!equipment.categoryId" autocomplete="off" :rules="[reasonRequired]" @update:search="(name) => {
                  if (!createDialog && !equipment.categoryId) return;
                  getReasons({ categoryId: equipment.categoryId, name })
                }" />
            </v-col>

            <!-- Shipping Instructions -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.shippingInstructions') }}
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.shiptTo" hide-details="auto" :label="$t('warranties.shiptTo')"
                :rules="[shiptToRequired]" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.problem" hide-details="auto" :label="$t('warranties.problem')"
                :rules="[problemRequired]" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.solution" hide-details="auto" :label="$t('warranties.solution')"
                :rules="[solutionRequired]" />
            </v-col>

            <!-- Parts -->
            <v-col cols="12">
              <div class="d-flex align-center my-4">
                <span class="text-subtitle-2 text-primary">
                  {{ $t('warranties.parts.title', 2) }}
                </span>
                <v-spacer />

                <v-tooltip :text="$t('warranties.tooltip.addPart')" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" color="primary" variant="text" size=" x-small" icon="mdi-plus"
                      @click="partsDialog = true" />
                  </template>
                </v-tooltip>

              </div>

              <v-data-table-server :items="parts" :headers="headersParts" :page="pageParts"
                :items-per-page="perPageParts" :items-length="totalParts" :items-per-page-options="itemsPerPageOptions"
                @update:page="v => pageParts = v" @update:itemsPerPage="v => perPageParts = v"
                @update:sort-by="v => sortByParts = v" density="compact" :loading="loading" show-expand>
                <template v-slot:expanded-row="{ columns, item }">
                  <tr>
                    <td :colspan="columns.length" class="bg-grey-lighten-4 pa-3">
                      <div class="d-flex flex-column ga-3">
                        <p class="text-caption text-decoration-underline">{{ $t('warranties.parts.description') }}</p>
                        <pre class="text-body-2" style="white-space: pre-wrap;">{{ item.description }}</pre>
                      </div>
                    </td>
                  </tr>
                </template>

                <template v-slot:item.option="{ item }">
                  <div class="d-flex align-center justify-center ga-2 my-2">
                    <v-tooltip :text="$t('warranties.tooltip.viewUpdate')" location="bottom">
                      <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" class="bg-primary" size="x-small" icon="mdi-pencil"
                          @click="partData = item; partsDialog = true" />
                      </template>
                    </v-tooltip>

                    <v-tooltip :text="$t('warranties.tooltip.delete')" location="bottom">
                      <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" class="bg-red" size="x-small" icon="mdi-trash-can"
                          @click="partData = item; deletePartDialog = true" />
                      </template>
                    </v-tooltip>
                  </div>
                </template>
              </v-data-table-server>
            </v-col>

            <!-- Media -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.files.title') }}
            </v-col>
            <v-col cols="12">
              <v-file-input v-model="files" :prepend-icon="null" prepend-inner-icon="mdi-paperclip" hide-details="auto"
                :label="$t('warranties.files.title')" multiple chips accept=".mp4, .jpg, .jpeg, .png, .webp, .svg"
                :rules="fileRules">
                <template v-slot:selection="{ fileNames }">
                  <v-chip v-for="fileName in fileNames" :key="fileName" size="small" label>
                    {{ fileName }}
                  </v-chip>
                </template>
              </v-file-input>
            </v-col>

            <v-col class="mt-2 text-end">
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
  <v-dialog v-model="updateDialog" max-width="800" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('warranties.update.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="updateDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="updateForm" v-model="updateModel" @submit.prevent="updateWarranty">
          <v-row dense>
            <!-- Equipment Info -->
            <v-col cols="12" class="text-body-2 text-primary">
              {{ $t('warranties.equipmentInfo') }}
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="equipment" :label="$t('equipments.title')" :items="equipments"
                item-title="modelReference" return-object hide-details="auto" clearable :rules="[equipmentRequired]"
                autocomplete="off" @update:search="(modelReference) => {
                  if (!updateDialog) return;
                  getEquipments({
                    equipmentId: equipment.id,
                    modelReference,
                    withPicture: false
                  })
                }" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="equipment.model" :label="$t('equipments.model')" hide-details readonly />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="equipment.reference" :label="$t('equipments.reference')" hide-details readonly />
            </v-col>

            <!-- Distributor -->
            <v-col cols="6" class="mt-2">
              <v-row dense>
                <template v-if="isAdmin">
                  <v-col cols="12" class="text-body-2 text-primary">
                    {{ $t('distributors.title') }}
                  </v-col>
                  <v-col cols="12">
                    <v-autocomplete class="flex-grow-0" v-model="form.distributorId" :label="$t('distributors.title')"
                      :items="distributors" item-title="name" item-value="id" hide-details="auto" clearable
                      autocomplete="off" @update:search="(name) => {
                        getDistributors({ distributorsIds: [form.distributorId], name })
                      }" />
                  </v-col>
                </template>

                <!-- Distributor Contact -->
                <v-col cols="12" class="text-body-2 text-primary">
                  {{ $t('warranties.distributorContact') }}
                </v-col>
                <v-col>
                  <v-autocomplete v-model="contact" :label="$t('warranties.contact')" :items="distributorsContacts"
                    item-title="fullName" hide-details="auto" clearable :readonly="!form.distributorId"
                    :rules="[contactDistributorRequired]" return-object autocomplete="off" @update:search="async (name) => {
                      if (!updateDialog) return;
                      await getDistributorsContacts(name)
                    }" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('contacts.fullName')" hide-details readonly
                    :model-value="contact?.fullName" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('contacts.email')" hide-details readonly :model-value="contact?.email" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('contacts.position')" hide-details readonly
                    :model-value="contact?.position" />
                </v-col>
              </v-row>
            </v-col>

            <!-- Distributor Site -->
            <v-col cols="6" class="mt-2">
              <v-row dense>
                <v-col cols="12" class="text-body-2 text-primary">
                  {{ $t('warranties.distributorSite') }}
                </v-col>
                <v-col cols="12">
                  <v-autocomplete v-model="site" :label="`${$t('sites.title')} ${$t('distributors.title')}`"
                    :items="distributorsSites" item-value="id" item-title="name" return-object hide-details="auto"
                    clearable :readonly="!form.distributorId" :rules="[siteDistributorRequired]" autocomplete="off"
                    @update:search="(name) => {
                      if (!updateDialog) return;
                      getDistributorsSites(name)
                    }" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('countries')" hide-details :model-value="address?.country?.name" readonly />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('states')" hide-details :model-value="address?.state?.name" readonly />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('cities')" hide-details :model-value="address?.city?.name" readonly />
                </v-col>
              </v-row>
            </v-col>

            <!-- Warranty Info -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.info') }}
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.serial" :label="$t('warranties.serial')" hide-details="auto"
                :rules="[serialRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="6">
              <v-menu v-model="showPicker" :close-on-content-click="false" transition="scale-transition" offset-y
                full-width max-width="290px" min-width="290px">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="form.saleDate" :label="$t('warranties.saleDate')" readonly hide-details="auto"
                    v-bind="props" :rules="[saleDateRequired]" />
                </template>
                <v-date-picker v-model="selectedDate" title="" hide-header @update:model-value="showPicker = false"
                  :max="todayDate" />
              </v-menu>
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.invoice" hide-details="auto" :label="$t('warranties.invoice')"
                :rules="[invoiceRequired]" counter="40" maxlength="40" />
            </v-col>

            <!-- Issue Type -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.issueType') }}
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="reasonsIds" :label="$t('warranties.issueType')" :items="reasons"
                item-title="name" item-value="id" hide-details="auto" clearable multiple chips
                :readonly="!equipment.categoryId" :rules="[reasonRequired]" autocomplete="off" @update:search="(name) => {
                  if (!createDialog && !equipment.categoryId) return;
                  getReasons({ categoryId: equipment.categoryId, name })
                }" />
            </v-col>

            <!-- Shipping Instructions -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.shippingInstructions') }}
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.shiptTo" hide-details="auto" :label="$t('warranties.shiptTo')"
                :rules="[shiptToRequired]" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.problem" hide-details="auto" :label="$t('warranties.problem')"
                :rules="[problemRequired]" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.solution" hide-details="auto" :label="$t('warranties.solution')"
                :rules="[solutionRequired]" />
            </v-col>

            <!-- Parts -->
            <v-col cols="12">
              <div class="d-flex align-center my-4">
                <span class="text-subtitle-2 text-primary">
                  {{ $t('warranties.parts.title', 2) }}
                </span>
                <v-spacer />

                <v-tooltip :text="$t('warranties.tooltip.addPart')" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" color="primary" variant="text" size=" x-small" icon="mdi-plus"
                      @click="partsDialog = true" />
                  </template>
                </v-tooltip>
              </div>

              <v-data-table-server :items="parts" :headers="headersParts" :page="pageParts"
                :items-per-page="perPageParts" :items-length="totalParts" :items-per-page-options="itemsPerPageOptions"
                @update:page="v => pageParts = v" @update:itemsPerPage="v => perPageParts = v"
                @update:sort-by="v => sortByParts = v" density="compact" :loading="loading" show-expand>
                <template v-slot:expanded-row="{ columns, item }">
                  <tr>
                    <td :colspan="columns.length" class="bg-grey-lighten-4 pa-3">
                      <div class="d-flex flex-column ga-3">
                        <p class="text-caption text-decoration-underline">{{ $t('warranties.parts.description') }}</p>
                        <pre class="text-body-2" style="white-space: pre-wrap;">{{ item.description }}</pre>
                      </div>
                    </td>
                  </tr>
                </template>

                <template v-slot:item.option="{ item }">
                  <div class="d-flex align-center justify-center ga-2 my-2">
                    <v-tooltip :text="$t('warranties.tooltip.viewUpdate')" location="bottom">
                      <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" class="bg-primary" size="x-small" icon="mdi-pencil"
                          @click="partData = item; partsDialog = true" />
                      </template>
                    </v-tooltip>

                    <v-tooltip :text="$t('warranties.tooltip.delete')" location="bottom">
                      <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" class="bg-red" size="x-small" icon="mdi-trash-can"
                          @click="partData = item; deletePartDialog = true" />
                      </template>
                    </v-tooltip>

                  </div>
                </template>
              </v-data-table-server>
            </v-col>

            <!-- Recieved At -->
            <v-col v-if="form.receivedAt" cols="12" class="text-body-2 mt-2">
              <p class="text-primary">{{ $t('warranties.receivedAt') }}:
                <span class="font-weight-bold">{{ date.format(form.receivedAt, 'fullDateTime') }}</span>
              </p>
            </v-col>
            <v-col v-if="!isApproved" class="text-end">
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
          {{ $t('warranties.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deleteDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('warranties.delete.message') }}</p>

        <v-btn @click="deleteDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deleteWarranty" class="bg-red">{{ $t('confirm') }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="700" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('warranties.search.title') }}
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
                item-title="modelReference" item-value="id" hide-details="auto" clearable autocomplete="off"
                @update:search="(modelReference) => {
                  getEquipments({ equipmentId: searchForm.equipmentId, modelReference, withPicture: false })
                }" />
            </v-col>

            <!-- Distributors -->
            <v-col v-if="isAdmin" class="d-flex flex-column" cols="12">
              <p class="text-body-2 text-primary pb-2">{{ $t('distributors.title', 2) }}</p>
              <v-autocomplete class="flex-grow-0" v-model="searchForm.distributorId" :label="$t('distributors.title')"
                :items="distributors" item-title="name" item-value="id" hide-details="auto" clearable autocomplete="off"
                @update:search="(name) => {
                  getDistributors({ distributorsIds: [searchForm.distributorId], name })
                }" />
            </v-col>

            <!-- Warranties -->
            <v-col class="mt-2 d-flex flex-column" cols="12">
              <p class="text-body-2 text-primary pb-2">{{ $t('warranties.title', 2) }}</p>
            </v-col>

            <v-col cols="12">
              <v-text-field v-model="searchForm.serial" :label="$t('warranties.serial')" hide-details="auto"
                counter="50" maxlength="50" clearable />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.wcoCode" :label="$t('warranties.wcoCode')" hide-details="auto"
                counter="20" maxlength="20" clearable type="number" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="searchForm.wcoYear" :label="$t('warranties.wcoYear')" hide-details="auto"
                counter="20" maxlength="20" clearable type="number" />
            </v-col>

            <!-- Sale Date -->
            <v-col cols="6">
              <v-menu v-model="searchShowPicker" :close-on-content-click="false" transition="scale-transition" offset-y
                full-width max-width="290px" min-width="290px">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="searchForm.saleDate" :label="$t('warranties.saleDate')" readonly
                    hide-details="auto" v-bind="props" clearable />
                </template>
                <v-date-picker v-model="searchSelectedDate" title="" hide-header
                  @update:model-value="searchShowPicker = false" :max="todayDate" />
              </v-menu>
            </v-col>

            <!-- Invoice -->
            <v-col cols="6">
              <v-text-field v-model="searchForm.invoice" :label="$t('warranties.invoice')" hide-details="auto"
                counter="40" maxlength="40" clearable />
            </v-col>

            <!-- Status -->
            <v-col cols="12">
              <v-select v-model="searchForm.status" item-title="title" item-value="value" :items="warrantiesStatuses"
                hide-details="auto" :label="$t('warranties.statuses.label')" clearable autocomplete="off" />
            </v-col>

            <v-col class="text-end" cols="12">
              <v-btn class="bg-primary" type="submit">{{ $t('search') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Approval Dialog -->
  <v-dialog v-model="approvalDialog" max-width="800" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('warranties.approval.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="approvalDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="approveWarranty">
          <v-row dense>
            <!-- Distributor -->
            <v-col cols="6">
              <v-row dense>
                <v-col cols="12" class="text-body-2 text-primary">
                  {{ $t('distributors.title') }}
                </v-col>
                <v-col cols="12">
                  <v-autocomplete class="flex-grow-0" v-model="form.distributorId" :label="$t('distributors.title')"
                    :items="distributors" item-title="name" item-value="id" hide-details="auto" readonly
                    autocomplete="off" />
                </v-col>

                <!-- Distributor Contact -->
                <v-col cols="12" class="text-body-2 text-primary">
                  {{ $t('warranties.distributorContact') }}
                </v-col>
                <v-col>
                  <v-autocomplete v-model="contact" :label="$t('warranties.contact')" :items="distributorsContacts"
                    item-title="fullName" hide-details="auto" return-object readonly autocomplete="off" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('contacts.fullName')" hide-details readonly
                    :model-value="contact?.fullName" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('contacts.email')" hide-details readonly :model-value="contact?.email" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('contacts.position')" hide-details readonly
                    :model-value="contact?.position" />
                </v-col>
              </v-row>
            </v-col>

            <!-- Distributor Site -->
            <v-col cols="6">
              <v-row dense>
                <v-col cols="12" class="text-body-2 text-primary">
                  {{ $t('warranties.distributorSite') }}
                </v-col>
                <v-col cols="12">
                  <v-autocomplete v-model="site" :label="`${$t('sites.title')} ${$t('distributors.title')}`"
                    :items="distributorsSites" item-value="id" item-title="name" return-object hide-details="auto"
                    readonly autocomplete="off" />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('countries')" hide-details :model-value="address?.country?.name" readonly />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('states')" hide-details :model-value="address?.state?.name" readonly />
                </v-col>
                <v-col cols="12">
                  <v-text-field :label="$t('cities')" hide-details :model-value="address?.city?.name" readonly />
                </v-col>
              </v-row>
            </v-col>

            <!-- Equipment Info -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.equipmentInfo') }}
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="equipment" :label="$t('equipments.title')" :items="equipments"
                item-title="modelReference" return-object hide-details="auto" readonly autocomplete="off" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="equipment.model" :label="$t('equipments.model')" hide-details readonly />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="equipment.reference" :label="$t('equipments.reference')" hide-details readonly />
            </v-col>

            <!-- Warranty Info -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.info') }}
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.saleDate" :label="$t('warranties.saleDate')" readonly hide-details="auto" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.invoice" hide-details="auto" :label="$t('warranties.invoice')" counter="40"
                maxlength="40" readonly />
            </v-col>

            <!-- Issue Type -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.issueType') }}
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="reasonsIds" :label="$t('warranties.issueType')" :items="reasons"
                item-title="name" item-value="id" hide-details="auto" multiple chips readonly autocomplete="off" />
            </v-col>

            <!-- Shipping Instructions -->
            <v-col cols="12" class="text-body-2 text-primary mt-2">
              {{ $t('warranties.shippingInstructions') }}
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.shiptTo" hide-details="auto" :label="$t('warranties.shiptTo')" readonly />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.problem" hide-details="auto" :label="$t('warranties.problem')" readonly />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.solution" hide-details="auto" :label="$t('warranties.solution')" readonly />
            </v-col>

            <!-- Parts -->
            <v-col cols="12">
              <div class="d-flex align-center my-4">
                <span class="text-subtitle-2 text-primary">
                  {{ $t('warranties.parts.title', 2) }}
                </span>
              </div>

              <v-data-table-server :items="parts" :headers="approvalHeadersParts" :page="pageParts"
                :items-per-page="perPageParts" :items-length="totalParts" :items-per-page-options="itemsPerPageOptions"
                @update:page="v => pageParts = v" @update:itemsPerPage="v => perPageParts = v" density="compact"
                :loading="loading" show-expand>
                <template v-slot:expanded-row="{ columns, item }">
                  <tr>
                    <td :colspan="columns.length" class="bg-grey-lighten-4 pa-3">
                      <div class="d-flex flex-column ga-3">
                        <p class="text-caption text-decoration-underline">{{ $t('warranties.parts.description') }}</p>
                        <pre class="text-body-2" style="white-space: pre-wrap;">{{ item.description }}</pre>
                      </div>
                    </td>
                  </tr>
                </template>
              </v-data-table-server>
            </v-col>

            <!-- Recieved At -->
            <v-col v-if="form.receivedAt" cols="12" class="text-body-2 mt-2">
              <p class="text-primary">{{ $t('warranties.receivedAt') }}:
                <span class="font-weight-bold"> {{ date.format(form.receivedAt, 'fullDateTime') }}</span>
              </p>
            </v-col>
            <v-col class="d-flex justify-end mt-2 ga-2">
              <v-btn variant="outlined" @click="approvalDialog = false" @mousedown.prevent :disabled="approveLoading">
                {{ $t('cancel') }}
              </v-btn>
              <v-btn v-if="form.status !== 'REJECTED'" class="bg-error" @click="rejectDialog = true" @mousedown.prevent
                :disabled="approveLoading">
                {{ $t('reject') }}
              </v-btn>
              <v-btn v-if="form.status !== 'APPROVED'" type="submit" class="bg-success" @mousedown.prevent
                :disabled="approveLoading">
                {{ $t('approve') }}
              </v-btn>
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
          {{ $t('warranties.reject.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="rejectDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form ref="rejectForm" @submit.prevent="rejectWarranty">
          <v-row dense>
            <v-col cols="12">
              <v-textarea v-model="rejectComments" :placeholder="$t('warranties.reject.description')" />
            </v-col>
            <v-col class="d-flex justify-end ga-2">
              <v-btn variant="outlined" @click="rejectDialog = false" @mousedown.prevent :disabled="rejectLoading">
                {{ $t('cancel') }}
              </v-btn>
              <v-btn type="submit" class="bg-error" @mousedown.prevent :loading="rejectLoading">
                {{ $t('reject') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Delete Part Dialog -->
  <v-dialog v-model="deletePartDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('warranties.parts.delete.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="deletePartDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="text-center py-6">
        <p class="text-subtitle-1 mb-6 text-center">{{ $t('warranties.parts.delete.message') }}</p>
        <v-btn @click="deletePartDialog = false" variant="outlined">{{ $t('cancel') }}</v-btn>
        <span class="mx-2" />
        <v-btn @click="deletePart(partData.id); deletePartDialog = false" class="bg-red">{{ $t('confirm')
        }}</v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <WarrantiesParts />
  <WarrantiesFiles />
</template>

<script setup>
import { ref, computed, watch, onBeforeMount, } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDate } from 'vuetify'

const { profile, isAdmin } = useProfile();
const { back } = useBack()
const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const { t } = useI18n();
const date = useDate();
const { items: equipments, getEquipments } = useEquipments();
const { items: distributors, getDistributors } = useDistributors();
const { items: parts, partsDialog, partData, remove: deletePart } = useWarrantiesParts();
const { getSites, getAddress } = useSites();
const { getContacts } = useContacts();
const { items: reasons, getReasons } = useReasons();
const { warrantyId, getWarrantyFiles, tableDialog } = useWarrantiesFiles();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('warranties.title', 2)}`
})

const rejectLoading = ref(false);
const approveLoading = ref(false);
const loading = ref(false);

// Warranties
const searchDialog = ref(false);
const createDialog = ref(false);
const items = ref([]);
const page = ref(1);
const perPage = ref(15);
const sortBy = ref(null);
const total = ref(15);

// Parts
const deletePartDialog = ref(false);
const pageParts = ref(1);
const perPageParts = ref(15);
const sortByParts = ref(null);
const totalParts = ref(15);

// Distributor Contact
const distributorsContacts = ref([]);
const contact = ref(null);

// Distributor Site
const distributorsSites = ref([]);
const site = ref(null)
const address = ref(null)

// Equipment
const equipment = ref({
  id: null,
  modelReference: null,
  model: null,
  reference: null,
  categoryId: null
})

const showPicker = ref(false);
const selectedDate = ref(null);
const updateDialog = ref(false);
const approvalDialog = ref(false);
const rejectDialog = ref(false);
const rejectComments = ref('');
const deleteDialog = ref(false);
const createModel = ref(false);
const updateModel = ref(false);
const files = ref(null);
const reasonsIds = ref([]);
const form = ref({
  id: '',
  distributorId: null,
  saleDate: null,
  invoice: '',
  shiptTo: '',
  problem: '',
  solution: ''
})

// For search
const searchShowPicker = ref(false);
const searchSelectedDate = ref(null);
const searchForm = ref({
  equipmentId: null,
  distributorId: null,
  wco: null,
  saleDate: null,
  serial: null,
  invoice: null,
  status: null,
})

const isApproved = computed(() => form.value.status === 'APPROVED');
const todayDate = computed(() => (new Date()).toISOString().split('T')[0])

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
  }

  defaultHeaders.push({ title: 'WCO', key: 'wco', align: 'center' });
  defaultHeaders.push({ title: t('warranties.invoice'), key: 'invoice', align: 'center' });

  if ($ability.can('update', 'warranties') || $ability.can('delete', 'warranties')) {
    defaultHeaders.push({ title: t('options'), key: 'option', align: 'center', sortable: false })
  }

  return defaultHeaders;
})

const headersParts = computed(() => [
  { title: t('warranties.parts.partNumber'), key: 'partNumber', align: 'start', sortable: false },
  { title: t('warranties.parts.quantity'), key: 'quantity', align: 'center', sortable: false },
  { title: t('options'), key: 'option', align: 'center', sortable: false }
])

const approvalHeadersParts = computed(() => [
  { title: t('warranties.parts.partNumber'), key: 'partNumber', align: 'start', sortable: false },
  { title: t('warranties.parts.quantity'), key: 'quantity', align: 'center', sortable: false },
])

const warrantiesStatuses = computed(() => [
  {
    title: t('warranties.statuses.active'),
    value: "ACTIVE"
  },
  {
    title: t('warranties.statuses.approved'),
    value: "APPROVED"
  },
  {
    title: t('warranties.statuses.rejected'),
    value: "REJECTED"
  }
])

watch(selectedDate, async (val) => {
  if (val) form.value.saleDate = date.format(val, 'fullDate');
})

watch(searchSelectedDate, async (val) => {
  if (val) searchForm.value.saleDate = date.format(val, 'fullDate');
})

watch(createDialog, async (val) => {
  if (!val) {
    resetForm();
    return;
  }
  await getEquipments({ withPicture: false });
  if (!isAdmin.value) {
    form.value.distributorId = profile.value.distributor_id;
    await getDistributorsSites();
    await getDistributorsContacts();
  } else {
    await getDistributors({});
  }
})

watch(updateDialog, async (val) => {
  if (!val) {
    resetForm();
    return;
  }
  await getEquipments({ equipmentId: form.value.equipmentId, withPicture: false });
  if (isAdmin.value) {
    await getDistributors({ distributorsIds: [form.value.distributorId] });
  } else {
    form.value.distributorId = profile.value.distributor_id
  }
  await getDistributorsSites();
  await getReasons({ reasonsIds: reasonsIds.value });
})

watch(approvalDialog, async (val) => {
  if (!val) {
    resetForm();
    return;
  }
  await getEquipments({ equipmentId: form.value.equipmentId, withPicture: false });
  if (isAdmin.value) {
    await getDistributors({ distributorsIds: [form.value.distributorId] });
  }
  await getDistributorsSites();
  await getReasons({ reasonsIds: reasonsIds.value });
})

watch(deleteDialog, async (val) => {
  if (!val) resetForm();
})

watch(page, async () => {
  await getEquipments();
})

watch(perPage, async () => {
  await getEquipments();
})

watch(site, async (v) => {
  if (!v) return;
  form.value.siteId = v.id;
  address.value = await getAddress({ addressId: site.value.addressId });
})

watch(() => equipment.value.categoryId, async (v) => {
  if (!v) return;
  await getReasons({ categoryId: v });
})

onBeforeMount(async () => {
  if ($ability.can('read', 'warranties')) {
    await getWarranties();
    return;
  }
  back();
})

watch(() => form.value.distributorId, async (val, prev) => {
  if (!val || (!updateDialog.value && !createDialog.value)) return;
  contact.value = null;
  site.value = null;
  address.value = null;
  await getDistributorsSites();
  await getDistributorsContacts();
})

watch(partsDialog, (v) => {
  if (!v) {
    resetPartData();
    return;
  }
})

watch(deletePartDialog, (v) => {
  if (!v) {
    resetPartData();
    return;
  }
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
})

const resetPartData = () => {
  partData.value = {
    partNumber: null,
    description: null,
    quantity: null
  }
}

const resetForm = () => {
  form.value = {
    id: '',
    distributorId: null,
    saleDate: null,
    invoice: '',
    shiptTo: '',
    problem: '',
    solution: '',
  }

  reasonsIds.value = [];
  equipment.value = {
    id: null,
    modelReference: null,
    model: null,
    reference: null,
  }

  contact.value = null;
  site.value = null;
  address.value = null;
  parts.value = new Array(0);
  files.value = [];

  selectedDate.value = null;
}

const getWarranties = async () => {
  try {
    loading.value = true;
    const data = await $api('/api/warranties/search', {
      body: {
        distributorId: searchForm.value.distributorId,
        equipmentId: searchForm.value.equipmentId,
        wcoCode: searchForm.value.wcoCode,
        wcoYear: searchForm.value.wcoYear,
        saleDate: searchForm.value.saleDate,
        invoice: searchForm.value.invoice,
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

const getWarranty = async (id) => {
  try {
    loading.value = true;
    const data = await $api(`/api/warranties/${id}`, {
      method: 'GET'
    })

    form.value = data;
    contact.value = data.contact;
    site.value = data.site;
    equipment.value = data.equipment;
    parts.value = data.parts;
    reasonsIds.value = data.reasonsIds;
    selectedDate.value = new Date(form.value.saleDate);
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = true;
  }
}

const createWarranty = async () => {
  try {
    loading.value = true;
    if (!createModel.value) return;
    if (parts.value && !parts.value.length) {
      notify(t('warranties.rules.warrantyMissingParts'), 'error');
      return;
    };

    const formData = new FormData();
    formData.append('equipmentId', equipment.value.id);
    formData.append('contactId', contact.value.id);

    for (const eachReason of reasonsIds.value) {
      formData.append('reasonsIds', eachReason);
    }

    formData.append('parts', JSON.stringify(parts.value));
    for (const warrantyFile of files.value) {
      formData.append('warrantyFiles', warrantyFile);
    }

    for (const [key, value] of Object.entries(form.value)) {
      formData.append(key, value);
    }

    if (!form.value.distributorId) {
      formData.set('distributorId', profile.value.distributor_id);
    }

    const { message } = await $api('/api/warranties', {
      method: 'POST',
      body: formData
    })
    notify(message, 'success');
    await getWarranties()
    createDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const updateWarranty = async () => {
  try {
    loading.value = true;
    if (!updateModel.value) return;

    // Complete form before sending
    form.value.equipmentId = equipment.value.id;
    form.value.contactId = contact.value.id;
    form.value.parts = parts.value;
    form.value.reasonsIds = reasonsIds.value;

    if (!form.value.distributorId) {
      form.value.distributorId = profile.value.distributor_id;
    }

    const { message } = await $api(`/api/warranties/${form.value.id}`, {
      method: 'PUT',
      body: form.value
    })
    notify(message, 'success');
    await getWarranties()
    updateDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const deleteWarranty = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/warranties/${form.value.id}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getWarranties()
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
    await getWarranties()
    searchDialog.value = false
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getDistributorsSites = async (name) => {
  try {
    loading.value = true;
    if (!form.value.distributorId && !profile.value.distributor_id) return;
    const data = await getSites({
      siteId: site.value?.id,
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

const getDistributorsContacts = async (name) => {
  try {
    loading.value = true;
    if (!form.value.distributorId && !profile.value.distributor_id) return;
    const data = await getContacts({
      theDistributorId: form.value.distributorId || profile.value.distributor_id,
      contactsIds: contact.value ? [contact.value.id] : [],
      name
    })
    distributorsContacts.value = data.items
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const approveWarranty = async () => {
  try {
    approveLoading.value = true;
    const { message } = await $api(`/api/warranties/approve/${form.value.id}`, {
      method: 'PATCH'
    })
    notify(message, 'success');
    await getWarranties();
    approvalDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    approveLoading.value = false;
  }
}

const rejectWarranty = async () => {
  rejectLoading.value = true;
  try {
    rejectLoading.value = true;
    const { message } = await $api(`/api/warranties/reject/${form.value.id}`, {
      method: 'POST',
      body: { rejectComments: rejectComments.value }
    })
    notify(message, 'success');
    await getWarranties();
    rejectDialog.value = false;
    approvalDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    rejectLoading.value = false;
  }
}

// Rules
const allowedMimeTypes = [
  'video/mp4',
  'image/jpeg',
  'image/png',
  'image/webp',
  'image/svg+xml'
];

const max50MB = 50 * 1024 * 1024;

const fileRules = [
  (value) => {
    if (!value || !value.length) {
      return t('warranties.files.rules.filesRequired')
    }

    for (let i = 0; i < value.length; i++) {
      const file = value[i]

      if (!allowedMimeTypes.includes(file.type)) {
        return t('warranties.files.rules.invalidFileType')
      }

      if (file.size > max50MB) {
        return t('warranties.files.rules.max50MBExceed')
      }
    }

    return true
  }
]

const siteDistributorRequired = (v) => !!v || t('warranties.rules.siteDistributorRequired');
const contactDistributorRequired = (v) => !!v || t('warranties.rules.contactDistributorRequired');
const equipmentRequired = (v) => !!v || t('warranties.rules.equipmentRequired');
const saleDateRequired = (v) => !!v || t('warranties.rules.saleDateRequired');
const invoiceRequired = (v) => !!v || t('warranties.rules.invoiceRequired');
const reasonRequired = (v) => !!v || t('warranties.rules.reasonRequired');
const shiptToRequired = (v) => !!v || t('warranties.rules.shiptToRequired');
const problemRequired = (v) => !!v || t('warranties.rules.problemRequired');
const solutionRequired = (v) => !!v || t('warranties.rules.solutionRequired');
const serialRequired = (v) => !!v || t('warranties.rules.serialRequired');
</script>
