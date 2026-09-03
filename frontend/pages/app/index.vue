<template>
  <v-container class="d-flex flex-column" min-height="100%" fluid>
    <v-tabs v-model="tab" align-tabs="center" fixed-tabs color="primary" class="mb-4">
      <v-tab value="dashboard">Dashboard</v-tab>
      <v-tab value="aligners">{{ $t('aligners.title', 2) }}</v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab" class="d-flex flex-column flex-shrink-0 flex-grow-1 overflow-y-auto">
      <!-- Dashboard -->
      <v-tabs-window-item value="dashboard">
        <div class="d-flex align-center ga-4 justify-center flex-wrap">
          <client-only>
            <NuxtLink v-for="route in routes" style="min-width: 180px; max-width: 250px;"
              class="d-inline-flex align-center justify-space-between w-100 pa-2 text-white rounded-lg text-decoration-none"
              :style="{ background: route.background, cursor: 'pointer' }" :to="route.path">
              <span class="text-h6">{{ $t(`${route.subject}.title`, 2) }}</span>
              <v-icon :icon="route.icon" />
            </NuxtLink>
          </client-only>
        </div>
      </v-tabs-window-item>

      <!-- Alineadoras -->
      <v-tabs-window-item value="aligners"
        :class="tab === 'aligners' ? 'd-flex flex-column flex-shrink-0 flex-grow-1' : ''"
        style="max-width: 1300px; margin: 0 auto; width: 100%;">
        <!-- Resumen general -->
        <v-row no-gutters class="flex-shrink-1 flex-grow-0">
          <v-col cols="12" class="mb-2">
            <h3>{{ $t('aligners.dashboard.generalSummary') }}</h3>
            <p class="text-caption">{{ $t('aligners.dashboard.lastUpdate') }}:
              <client-only>
                <span class="font-weight-bold">
                  {{ updatedAt }}
                </span>
              </client-only>
            </p>
          </v-col>

          <v-col cols="12" :md="isAdmin ? 3 : 6" sm="12" :class="$vuetify.display.mdAndUp ? 'pe-2' : ''">
            <v-text-field id="serial-input" type="text" v-model="semantic" @input="(e) => semantic = e.target.value"
              maxlength="19" :label="$t('aligners.softwareVersion')" hide-details density="compact" max-width="340"
              @update:model-value="handleInput" @blur="handleBlur" :disabled="loading" />
          </v-col>

          <v-col v-if="isAdmin" cols="12" md="3" sm="12" :class="!$vuetify.display.mdAndUp ? 'py-3' : ''">
            <v-autocomplete v-model="distributorId" :label="$t('distributors.title')" :items="distributors"
              item-title="name" item-value="id" hide-details="auto" clearable max-width="340" density="compact"
              :disabled="loading" @update:search="(name) => {
                getDistributors({ distributorsIds: [distributorId], name })
              }" />
          </v-col>

          <v-col cols="12" md="6" sm="12" class="d-flex align-center ga-2"
            :class="!$vuetify.display.mdAndUp ? 'justify-start' : 'justify-end'">
            <v-btn class="bg-primary" prepend-icon="mdi-reload" :loading="loading" @click="getAllAligners"
              size="small">{{ $t('update') }}</v-btn>
          </v-col>
        </v-row>

        <!-- Gráficos -->
        <v-row no-gutters align="center" justify="center" class="flex-shrink-1 flex-grow-0"
          :class="allAligners.length === 0 ? 'mt-2 mb-4' : 'my-10'">
          <v-col v-if="!loading && allAligners.length === 0" cols="12"
            class="d-flex text-subtitle-2 text-grey-darken-1 text-center text-decoration-underline">
            {{ $t('aligners.dashboard.noDataAvailable') }}
          </v-col>
          <v-col v-else-if="loading" class="my-6 d-flex justify-center align-center" cols="12">
            <v-progress-circular :size="100" :width="15" color="primary" indeterminate />
          </v-col>
          <template v-else>
            <v-col lg="4" md="6" sm="12">
              <p class="text-center text-subtitle-2 font-weight-semibold text-uppercase text-grey-darken-1 mb-2">
                {{ $t('aligners.dashboard.connection') }}
              </p>
              <DoughnutChart :key="`conn-${connection.yes}-${connection.no}`"
                :labels="[$t('aligners.dashboard.connected'), $t('aligners.dashboard.disconnected')]"
                :data="[connection.yes, connection.no]" :filters="['connected', 'disconnected']"
                @setFilter="(v) => theFilter = v" />
            </v-col>

            <v-col :class="!$vuetify.display.mdAndUp ? 'py-12' : ''" lg="4" md="6" sm="12" style="">
              <p class="text-center text-subtitle-2 font-weight-semibold text-uppercase text-grey-darken-1 mb-2">
                {{ $t('aligners.dashboard.softwareVersion') }}
              </p>
              <DoughnutChart :key="`software-${software.equal}-${software.lower}-${software.greater}`" :labels="[
                $t('aligners.dashboard.equal'),
                $t('aligners.dashboard.lower'),
                $t('aligners.dashboard.greater')
              ]" :data="[software.equal, software.lower, software.greater]" :filters="[
                'equal',
                'lower',
                'greater'
              ]" :background-color="['#3b82f6', '#f43f5e', '#16a34a']"
                :hover-background-color="['#2563eb', '#e11d48', '#15803d']" @setFilter="(v) => theFilter = v" />
            </v-col>

            <v-col lg="4" md="6" sm="12">
              <p class="text-center text-subtitle-2 font-weight-semibold text-uppercase text-grey-darken-1 mb-2">
                {{ $t('aligners.dashboard.specs') }}
              </p>
              <DoughnutChart :key="`standing-${standing.yes}-${standing.no}`"
                :labels="[$t('aligners.dashboard.standing'), $t('aligners.dashboard.expired')]"
                :data="[standing.yes, standing.no]" :filters="['standing', 'expired']"
                @setFilter="(v) => theFilter = v" />
            </v-col>
          </template>
        </v-row>

        <!-- Detalle -->
        <v-row no-gutters align="center" class="mb-2 flex-shrink-1 flex-grow-0">
          <v-col cols="12" class="mb-2">
            <h3>{{ $t('aligners.dashboard.detailTitle') }}</h3>
          </v-col>

          <v-col cols="12" md="3" sm="12" :class="$vuetify.display.mdAndUp ? 'pe-2' : 'mb-2'">
            <v-select v-model="visualization" :label="$t('aligners.dashboard.visualizationFormat')" density="compact"
              max-width="300" :items="visualizationFormats" hide-details :disabled="loading" />
          </v-col>
          <v-col cols="12" md="3" sm="12">
            <v-select v-model="theFilter" :label="$t('aligners.dashboard.filter')" density="compact" max-width="300"
              :items="filterOptions" hide-details :disabled="loading" />
          </v-col>
        </v-row>

        <!-- Table -->
        <v-data-table v-if="visualization === 'table'" :items="items" :headers="headers" :loading="loading"
          density="compact" class="flex-shrink-1 flex-grow-0">
          <template v-slot:item.createdAt="{ item }">
            <v-chip class="text-caption my-2">
              {{ $dateFormat(new Date(item.createdAt)) }}
            </v-chip>
          </template>
          <template v-slot:item.serialNumber="{ item }">
            <v-chip class="text-caption" :class="`bg-${item.connected ? 'primary' : 'error'}`">
              {{ item.serialNumber }}
            </v-chip>
          </template>
          <template v-slot:item.software="{ item }">
            <v-chip class="text-caption"
              :class="`bg-${item.softwareLabel === 'equal' ? 'primary' : item.softwareLabel === 'lower' ? 'error' : 'success'}`">
              {{ item.software }}
            </v-chip>
          </template>
          <template v-slot:item.specs="{ item }">
            <v-chip class="text-caption" :class="`bg-${item.standing ? 'primary' : 'error'}`">
              {{ item.specsLabel }}
            </v-chip>
          </template>
          <template v-slot:item.option="{ item }">
            <div class="d-flex align-center justify-center ga-2">
              <v-btn v-if="$ability.can('read', 'aligners')" class="my-1 bg-secondary" size="x-small" icon="mdi-eye"
                @click="async () => { loadingView = true; serialNumber = item.serialNumber; await getAligner(); loadingView = false }"
                :loading="serialNumber == item.serialNumber && loadingView" />
              <v-btn v-if="isAdmin" class="my-1 bg-red" size="x-small" icon="mdi-trash-can"
                @click="alignerId = item.id; deleteDialog = true" />
            </div>
          </template>
        </v-data-table>

        <!-- Cards -->
        <v-row v-else no-gutters>
          <v-col v-if="!loading && items.length === 0" cols="12"
            class="d-flex text-subtitle-2 text-grey-darken-1 text-center text-decoration-underline">
            {{ $t('aligners.dashboard.noDataAvailable') }}
          </v-col>
          <v-col v-else-if="loading" class="my-6 d-flex justify-center align-start" cols="12">
            <v-progress-circular :size="100" :width="15" color="primary" indeterminate />
          </v-col>
          <v-col v-else v-for="aligner in items" cols="12" sm="6" md="4" xl="3" class="pa-4">
            <v-card class="d-flex flex-column h-100 border text-left" elevation="0" hover rounded="xl" max-width="350"
              @click="getAlignerDetail(aligner)" :loading="serialNumber == aligner.serialNumber && loadingView">
              <v-card-title class="d-flex align-center justify-space-between pb-0 pt-4">
                <div class="d-flex align-center ga-2">
                  <span class="text-subtitle-1 font-weight-bold text-grey-darken-4">
                    {{ aligner.serialNumber }}
                  </span>

                  <v-btn icon="mdi-content-copy" size="x-small" variant="text" color="grey-darken-1"
                    :title="$t('aligners.dashboard.copySerial')" @click.stop="copyToClipboard(aligner.serialNumber)" />
                </div>

                <!-- Badge de estado -->
                <v-chip size="small" variant="outlined" :class="`bg-${aligner.connected ? 'success' : 'error'}`">
                  {{ aligner.connected ? 'Connected' : 'Disconnected' }}
                </v-chip>
              </v-card-title>

              <!-- Cuerpo principal -->
              <v-card-text class="flex-grow-1 d-flex flex-column ga-4 mt-4">
                <div>
                  <div class="text-caption text-grey-darken-1 text-uppercase font-weight-bold mb-1">
                    {{ $t('aligners.dashboard.location') }}
                  </div>
                  <div class="text-subtitle-2 font-weight-bold text-grey-darken-3">
                    {{ aligner?.branch }}
                  </div>
                  <div class="text-body-2 text-grey-darken-1 text-truncate"
                    :title="`${aligner?.geolocation?.city}, ${aligner?.geolocation?.region}, ${aligner?.geolocation?.country_name}`">
                    {{ aligner?.geolocation?.city || '-' }}, {{ aligner?.geolocation?.region || '-' }}, {{
                      aligner?.geolocation?.country_name || '-' }}
                  </div>
                </div>

                <!-- Fechas -->
                <v-row dense>
                  <v-col cols="6">
                    <div class="text-caption text-grey-darken-1 text-uppercase font-weight-bold mb-1">
                      {{ $t('aligners.dashboard.createdAt') }}
                    </div>
                    <div class="text-body-2 text-grey-darken-3">
                      {{ $dateFormat(new Date(aligner?.createdAt)) }}
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <div class="text-caption text-grey-darken-1 text-uppercase font-weight-bold mb-1">
                      {{ $t('aligners.dashboard.expiration') }}
                    </div>
                    <div class="text-body-2 text-grey-darken-3">
                      {{ aligner?.specsExpiration?.month }}/{{ aligner?.specsExpiration?.year }}
                    </div>
                  </v-col>
                </v-row>

                <!-- Divisor -->
                <v-divider></v-divider>

                <!-- Footer -->
                <v-row dense>
                  <v-col cols="6">
                    <div class="text-caption text-grey-darken-1 text-uppercase font-weight-bold mb-1">
                      Software
                    </div>
                    <v-chip size="small"
                      :class="`bg-${aligner.softwareLabel === 'equal' ? 'primary' : aligner.softwareLabel === 'lower' ? 'error' : 'success'}`">
                      {{ aligner?.version?.semantic }}
                    </v-chip>
                  </v-col>
                  <v-col cols="6">
                    <div class="text-caption text-grey-darken-1 text-uppercase font-weight-bold mb-1">
                      Specs
                    </div>
                    <v-chip size="small" :class="`bg-${aligner.standing ? 'primary' : 'error'}`" class="specs-chips">
                      {{ aligner?.specsLabel }}
                    </v-chip>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

      </v-tabs-window-item>
    </v-tabs-window>


    <v-dialog v-model="deleteDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
      <v-card tile>
        <v-card-title class="bg-primary">
          <v-row class="text-body-1" no-gutters align="center">
            {{ $t('distributors.aligners.delete.title') }}
            <v-spacer />
            <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="deleteDialog = false" />
          </v-row>
        </v-card-title>
        <v-card-text class="text-center">
          <p class="text-subtitle-1 mb-3 text-center">{{ $t('distributors.aligners.delete.message') }}</p>
          <v-btn @click="deleteDialog = false" size="small" variant="outlined" :disabled="loading">
            {{ $t('cancel') }}
          </v-btn>
          <span class="mx-2" />
          <v-btn @click="deleteAligner" class="bg-red" size="small" :loading="loading">{{ $t('confirm') }}</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- <v-card class="me-8" href="http://localhost:1337" width="200" height="200">
        <v-img src="/public/bg_about.png" />
        <v-card-title>Strapi</v-card-title>
      </v-card>

      <v-card class="me-8" href="http://192.168.0.104:4200" width="200" height="200">
        <v-img src="/public/bg_about.png" />
        <v-card-title>Forum</v-card-title>
      </v-card> -->
  </v-container>

  <AlignersModal />
</template>

<script setup>
const { $ability } = useNuxtApp();
const { getLastVersion, semantic, getLabelSoftware, serialNumber, getAligner, abortController } = useAligners();
const { items: distributors, getDistributors } = useDistributors();
const { isAdmin, profile } = useProfile();
const { t } = useI18n();
const { notify } = useSnackbar();

definePageMeta({
  layout: 'app',
  middleware: 'private'
})

useHead({
  title: 'SOE Latam | Home'
})


const connection = ref({
  yes: 0,
  no: 0,
})
const software = ref({
  equal: 0,
  lower: 0,
  greater: 0,
})
const standing = ref({
  yes: 0,
  no: 0,
})
const deleteDialog = ref(false);
const loadingView = ref(false);
const loading = ref(false);
const allAligners = ref([]);
const items = ref([]);
const visualization = ref('table');
const theFilter = ref('all');
const tab = ref('dashboard');
const routes = ref([])
const menu = ref([
  {
    title: 'Distributors',
    subject: 'distributors',
    path: '/app/distributors',
    icon: 'mdi-domain',
    background: '#1976D2'
  },
  {
    title: 'Clients',
    subject: 'clients',
    path: '/app/clients',
    icon: 'mdi-account-tie',
    background: '#009688'
  },
  {
    title: 'Sites',
    subject: 'sites',
    path: '/app/sites',
    icon: 'mdi-fireplace-off',
    background: '#FF9800'
  },
  {
    title: 'Users',
    subject: 'users',
    path: '/app/users',
    icon: 'mdi-account',
    background: '#3F51B5'
  },
  {
    title: 'Groups',
    subject: 'groups',
    path: '/app/groups',
    icon: 'mdi-account-group',
    background: '#9C27B0'
  },
  {
    title: 'Brands',
    subject: 'brands',
    path: '/app/brands',
    icon: 'mdi-shield-car',
    background: '#E91E63'
  },
  {
    title: 'Categories',
    subject: 'categories',
    path: '/app/categories',
    icon: 'mdi-shape-outline',
    background: '#4CAF50'
  },
  {
    title: 'Equipments',
    subject: 'equipments',
    path: '/app/equipments',
    icon: 'mdi-car-cog',
    background: '#607D8B'
  },
  {
    title: 'Installations',
    subject: 'installations',
    path: '/app/installations',
    icon: 'mdi-train-car-flatbed-car',
    background: '#00BCD4'
  },
  {
    title: 'Reasons',
    subject: 'reasons',
    path: '/app/reasons',
    icon: 'mdi-file-cancel',
    background: '#F44336'
  },
  {
    title: 'Warranties',
    subject: 'warranties',
    path: '/app/warranties',
    icon: 'mdi-certificate',
    background: '#FFC107' // Amber
  },
  {
    title: 'Lists',
    subject: 'lists',
    path: '/app/lists',
    icon: 'mdi-office-building-cog-outline',
    background: '#673AB7' // Deep Purple
  },
  // {
  //   title: 'Configuration',
  //   subject: 'configuration',
  //   path: '/app/configuration',
  //   icon: 'mdi-cog',
  //   background: '#9E9E9E' // Grey
  // },
  // {
  //   title: 'Forums',
  //   subject: 'forums',
  //   path: 'http://192.168.0.104:4200',
  //   icon: 'mdi-open-in-new',
  //   background: '#03A9F4' // Light Blue
  // },
  // {
  //   title: 'Strapi',
  //   subject: 'strapi',
  //   path: 'http://localhost:1337',
  //   icon: 'mdi-open-in-new',
  //   background: '#2F2E8B' // Strapi Blue
  // }
])
const updatedAt = ref("--:--:--");
const distributorId = ref('');
const alignerId = ref('');

onBeforeMount(async () => {
  try {
    routes.value = menu.value.filter(item => $ability.can('read', item.subject));
    updatedAt.value = new Date().toTimeString().split(' ')[0];

    await getLastVersion();
    if (isAdmin.value) {
      await getDistributors({});
      distributorId.value = distributors.value[0].id;
    } else {
      distributorId.value = profile.value.distributor_id;
    }
  } catch (err) { }
})

const headers = computed(() => {
  const defaultHeaders = [
    { title: t('distributors.aligners.serial'), key: 'serialNumber', sortable: false },
    { title: t('distributors.aligners.software'), align: 'center', key: 'software' },
    { title: t('distributors.aligners.specs'), align: 'center', key: 'specs', sortable: false },
    { title: t('distributors.aligners.createdAt'), align: 'center', key: 'createdAt' }
  ]

  if (isAdmin.value || $ability.can('read', 'aligners')) {
    defaultHeaders.push(
      { title: t('options'), key: 'option', align: 'center', sortable: false }
    )
  }

  return defaultHeaders;
})

const visualizationFormats = computed(() => [
  {
    title: t('aligners.dashboard.table'),
    value: 'table'
  },
  {
    title: t('aligners.dashboard.cards'),
    value: 'cards'
  },
])

const filterOptions = computed(() => [
  {
    title: t('aligners.dashboard.all'),
    value: 'all'
  },
  {
    title: t('aligners.dashboard.connected'),
    value: 'connected'
  },
  {
    title: t('aligners.dashboard.disconnected'),
    value: 'disconnected'
  },
  {
    title: t('aligners.dashboard.standing'),
    value: 'standing'
  },
  {
    title: t('aligners.dashboard.expired'),
    value: 'expired'
  },
  {
    title: `${t('aligners.dashboard.lowerThan')} ${semantic.value}`,
    value: 'lower'
  },
  {
    title: `${t('aligners.dashboard.greaterThan')} ${semantic.value}`,
    value: 'greater'
  },
  {
    title: `${t('aligners.dashboard.equalTo')} ${semantic.value}`,
    value: 'equal'
  }
])

watch(semantic, async (v) => {
  if (!v) return;
  await getSoftwareStats();
})

watch(distributorId, async (v) => {
  if (!v) return;
  await getAllAligners();
})

watch(theFilter, (v) => {
  if (v === 'all') {
    items.value = [...allAligners.value];
  } else if (v === 'connected') {
    items.value = [...allAligners.value.filter((e) => e.connected)]
  } else if (v === 'disconnected') {
    items.value = [...allAligners.value.filter((e) => !e.connected)]
  } else if (v === 'standing') {
    items.value = [...allAligners.value.filter((e) => e.standing)]
  } else if (v === 'expired') {
    items.value = [...allAligners.value.filter((e) => !e.standing)]
  } else if (v === 'lower') {
    items.value = [...allAligners.value.filter((e) => e.software < semantic.value)]
  } else if (v === 'equal') {
    items.value = [...allAligners.value.filter((e) => e.software === semantic.value)]
  } else if (v === 'greater') {
    items.value = [...allAligners.value.filter((e) => e.software > semantic.value)]
  }
})

const resetStats = () => {
  connection.value = {
    yes: 0,
    no: 0
  }
  software.value = {
    equal: 0,
    lower: 0,
    greater: 0
  }

  standing.value = {
    yes: 0,
    no: 0
  }
}

const getStats = () => {
  for (let aligner of allAligners.value) {
    if (aligner.connected) {
      connection.value.yes += 1;
    } else {
      connection.value.no += 1;
    }

    if (aligner.softwareLabel == "equal") {
      software.value.equal += 1;
    } else if (aligner.softwareLabel == "lower") {
      software.value.lower += 1;
    } else {
      software.value.greater += 1;
    }

    if (aligner.standing) {
      standing.value.yes += 1;
    } else {
      standing.value.no += 1;
    }
  }
};

const getSoftwareStats = async () => {
  let theAligners = [];

  software.value = {
    equal: 0,
    lower: 0,
    greater: 0,
  }

  for (let aligner of allAligners.value) {
    let softwareLabel = await getLabelSoftware(aligner.software);
    theAligners.push({
      ...aligner,
      softwareLabel,
    })

    if (softwareLabel == "equal") {
      software.value.equal += 1;
    } else if (softwareLabel == "lower") {
      software.value.lower += 1;
    } else {
      software.value.greater += 1;
    }
  }

  allAligners.value = theAligners;
  items.value = theAligners;
}

const getAllAligners = async () => {
  try {
    loading.value = true;
    allAligners.value = [];
    items.value = [];
    abortController.value = new AbortController();

    const response = await $api(`/api/distributors/aligners/${distributorId.value}`, {
      method: 'GET',
      responseType: 'stream',
      signal: abortController.value.signal
    });

    // Obtenemos el lector del stream
    const reader = response.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split('\n\n');
      buffer = events.pop();

      for (const event of events) {
        if (event.trim().startsWith('data:')) {
          const dataStr = event.replace(/^data:/, '').trim();

          if (dataStr) {
            const aligner = JSON.parse(dataStr);
            let standing = false;
            let specsLabel = null;
            if (aligner.specs) {
              specsLabel = `${aligner?.specs?.name} ${aligner?.specs?.month}/${aligner?.specs?.year}`
              standing = new Date(aligner?.specs?.year, aligner?.specs?.month) <
                new Date(
                  aligner?.specsExpiration?.year,
                  aligner?.specsExpiration?.month
                )
            }

            // Formateamos los datos justo cuando llegan
            const formattedAligner = {
              ...aligner,
              specsLabel,
              software: aligner.version.semantic,
              softwareLabel: await getLabelSoftware(aligner.version.semantic),
              standing
            };

            // Agregamos al array reactivo, la UI se actualizará uno por uno
            allAligners.value.push(formattedAligner);
            items.value.push(formattedAligner); // O igualarlo a allAligners.value si no hay filtros activos
          }
        }
      }
    }

    // Estas acciones suceden cuando el stream ha terminado completamente
    updatedAt.value = new Date().toTimeString().split(' ')[0];
    resetStats();
    getStats();

  } catch (err) {
    if (err.name === 'AbortError' || err.message === 'The user aborted a request.') {
      return; // Salimos silenciosamente
    }

    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const handleInput = (value) => {
  if (!value) return
  semantic.value = value
    .replace(/[^0-9.]/g, '')
    .replace(/\.{2,}/g, '.')
}


const handleBlur = () => {
  if (!semantic.value) return
  semantic.value = semantic.value.replace(/^\.+|\.+$/g, '')
}

const deleteAligner = async () => {
  try {
    loading.value = true;
    const { message } = await $api(`/api/distributors/aligners/${alignerId.value}`, {
      method: 'DELETE'
    })
    notify(message, 'success');
    await getAllAligners();
    deleteDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const getAlignerDetail = async (aligner) => {
  if (!$ability.can('read', 'aligners')) {
    notify(t('aligners.dashboard.requestPermissionsMessage'), 'warning');
    return;
  }
  loadingView.value = true;
  serialNumber.value = aligner.serialNumber;
  await getAligner();
  loadingView.value = false;
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    notify(t('aligners.copiedSerialMessage', 'success'))
  } catch (err) { }
};
</script>

<style>
.v-window__container {
  flex-shrink: 0;
  flex-grow: 1;
}

.specs-chips .v-chip__content {
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
