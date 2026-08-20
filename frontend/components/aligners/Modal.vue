<template>
  <v-dialog v-model="viewAligner" max-width="900" scrollable persistent>
    <v-card tile>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          <v-icon icon="mdi-car-wrench" class="me-2" />
          <span>{{ alignerData?.serialNumber }}</span>
          <v-spacer />

          <div class="d-flex align-center ga-2">
            <v-btn class="bg-primary" size="small" icon="mdi-reload" @click="reloadAligner" :loading="loading" />
            <v-btn class="bg-primary" size="small" icon="mdi-close" @click="viewAligner = false" />
          </div>
        </v-row>
      </v-card-title>

      <v-card-text>
        <v-row dense>
          <v-col class="text-success" cols="12">
            <div v-if="alignerData?.connected"
              class="d-inline-flex align-center py-1 px-1 bg-success text-white ga-1 rounded">
              <v-icon size="small">mdi-check</v-icon>
              <span class="text-caption">{{ $t('aligners.connectedLabel') }}</span>
            </div>
            <div v-else class="d-inline-flex align-center py-1 px-1 bg-error text-white ga-1 rounded">
              <v-icon size="small">mdi-close-thick</v-icon>
              <span class="text-caption">{{ $t('aligners.disconnectedLabel') }}</span>
            </div>
          </v-col>

          <v-col cols="12">
            <p class="text-primary">{{ $t('aligners.systemTitle') }}</p>
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.softwareVersion')" :model-value="alignerData?.version?.semantic" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.specsVersion')"
              :model-value="`${alignerData?.specs?.name} ${alignerData?.specs?.month}/${alignerData?.specs?.year}`"
              readonly hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.specsExpiration')"
              :model-value="`${alignerData?.specsExpiration?.month}/${alignerData?.specsExpiration?.year}`" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.systemClass')" :model-value="alignerData?.systemClass" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.boardClass')" :model-value="alignerData?.boardClass" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.updateState')" :model-value="alignerData?.updateState?.state" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.loggingLevel')" :model-value="alignerData?.logLevel" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.currentProcedure')"
              :model-value="alignerData?.updateState?.readyToInstall?.software ? 'No' : 'Yes'" readonly hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.softwareReadyToDownload')"
              :model-value="alignerData?.pendingSoftwareDownload" readonly hide-details />
          </v-col>

          <v-col class="mt-4" cols="12">
            <p class="text-primary">{{ $t('aligners.locationTitle') }}</p>
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.continent')" :model-value="alignerData?.geolocation?.continent_name"
              readonly hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.region')" :model-value="alignerData?.geolocation?.region" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.country')" :model-value="alignerData?.geolocation?.country_name" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.city')" :model-value="alignerData?.geolocation?.city" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.timeZoneName')" :model-value="alignerData?.geolocation?.time_zone.name"
              readonly hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.timeZoneOffset')"
              :model-value="alignerData?.geolocation?.time_zone.offset" readonly hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.localTime')"
              :model-value="alignerDateFormat(alignerData?.geolocation?.time_zone.current_time)" readonly
              hide-details />
          </v-col>

          <v-col class="mt-4" cols="12">
            <p class="text-primary">{{ $t('aligners.hardwareTitle') }}</p>
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.address')" :model-value="alignerData?.address" readonly hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.remotePort')" :model-value="alignerData?.remotePort" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.connectionCount')" :model-value="alignerData?.connectCount" readonly
              hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.cameraCount')" :model-value="alignerData?.boardFeatures?.numCameras"
              readonly hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.accelerometerCount')" :model-value="alignerData?.boardFeatures?.numAccel"
              readonly hide-details />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.connected')" :model-value="alignerData?.connected ? 'Yes' : 'No'"
              readonly hide-details :class="alignerData?.connected ? 'bg-success' : 'bg-error'" />
          </v-col>

          <v-col cols="6">
            <v-text-field :label="$t('aligners.ddEnabled')"
              :model-value="alignerData?.boardFeatures?.isDDAligner ? 'Yes' : 'No'" readonly hide-details />
          </v-col>
        </v-row>
      </v-card-text>
      <v-divider />
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn variant="outlined" @click="viewAligner = false">
          {{ $t('cancel') }}
        </v-btn>
        <v-btn v-if="isConnected" variant="outlined" class="bg-success" @click="activate" :disabled="loading">
          {{ $t('aligners.activate') }}
        </v-btn>
        <v-btn v-if="showStage" variant="outlined" class="bg-primary" @click="stage" :disabled="loading">
          {{ `${$t('aligners.stage')} ${semantic}` }}
        </v-btn>
        <v-btn v-if="showUnstage" variant="outlined" class="bg-info" @click="unstage" :disabled="loading">
          {{ `${$t('aligners.unstage')} ${semantic}` }}
        </v-btn>
        <v-btn v-if="isConnected" variant="outlined" class="bg-secondary" @click="checkCloud" :disabled="loading">
          {{ $t('aligners.check') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
const { t } = useI18n();
const { notify } = useSnackbar()

const { alignerData, viewAligner, sendStage, getAligner, sendUnstage, sendCloud, semantic, sendActivate, getLastVersion } = useAligners();

const loading = ref(false);

const showStage = computed(() => {
  return alignerData.value?.updateState && alignerData.value?.updateState.state === 'READY_TO_INSTALL' && !alignerData.value?.pendingSoftwareDownload
})
const showUnstage = computed(() => {
  return alignerData.value?.pendingSoftwareDownload
})
const isConnected = computed(() => {
  return alignerData.value?.connected
})


const alignerDateFormat = (theDate) => {
  const fecha = new Date(theDate);

  // Configuras cómo quieres que se vea
  const opciones = {
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };

  // Formateamos en español
  return fecha.toLocaleDateString("es-ES", opciones);
};

const stage = async () => {
  try {
    loading.value = true;
    const message = await sendStage();

    let seconds = 0;
    while (!showUnstage.value) {
      await getAligner();
      await new Promise((res) => setTimeout(res, 1000));
      seconds += 1;
      if (seconds >= 5) throw new Error(t('aligners.commandError'));
    }

    notify(message, 'success');
  } catch (err) {
    notify(err, 'error')
  } finally {
    loading.value = false;
  }
}

const unstage = async () => {
  try {
    loading.value = true;
    const message = await sendUnstage();

    let seconds = 0;
    while (!showStage.value) {
      await getAligner();
      await new Promise((res) => setTimeout(res, 1000));
      seconds += 1;
      if (seconds >= 5) throw new Error(t('aligners.commandError'));
    }

    notify(message, 'success')
  } catch (err) {
    notify(err, 'error')
  } finally {
    loading.value = false;
  }
}

const checkCloud = async () => {
  try {
    loading.value = true;
    await sendCloud();
    await new Promise((res) => setTimeout(res, 2000));
    await getAligner();
  } catch (err) {
    notify(err, 'error')
  } finally {
    loading.value = false;
  }
}

const activate = async () => {
  try {
    loading.value = true;
    await sendActivate();
    await new Promise((res) => setTimeout(res, 2000));
    await getAligner();
  } catch (err) {
    notify(err, 'error')
  } finally {
    loading.value = false;
  }
}

const reloadAligner = async () => {
  try {
    loading.value = true;
    await getLastVersion();
    await getAligner();
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}


</script>