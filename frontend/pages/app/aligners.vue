<template>
  <v-card class="h-50 w-100" flat>
    <v-card-title class="text-center">
      <h1>{{ $t('aligners.title', 2) }}</h1>
      <h6>{{ $t('aligners.message') }}</h6>
    </v-card-title>
    <v-card-text>
      <v-form ref="searchForm" v-model="searchModel" @submit.prevent="getAligner"
        class="d-flex align-center justify-center ga-4 mx-auto w-100" style="max-width: 800px;">
        <v-text-field v-model="serialNumber" class="w-100" hide-details="auto" style="max-width: 500px;"
          append-inner-icon="mdi-magnify" :placeholder="$t('aligners.serialNumber')" :rules="[serialNumberRequired]"
          :readonly="loading" :disabled="loading" clearable @keydown.space.prevent autocomplete="off">
          <template v-slot:append-inner>
            <v-btn v-if="!loading" icon="mdi-magnify" @click="getAligner" size="small" flat variant="text" />
            <v-progress-circular v-else :size="30" indeterminate class="v-progress-circular--disable-shrink" />
          </template>
        </v-text-field>
      </v-form>
    </v-card-text>
  </v-card>

  <AlignersModal />
</template>

<script setup>
const { back } = useBack()
const { t } = useI18n();
const { $ability } = useNuxtApp();
const { notify } = useSnackbar();
const { serialNumber, getAligner: getAlignerData } = useAligners();

const loading = ref(false);
const searchModel = ref(false);

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('aligners.title', 2)}`
})

onBeforeMount(async () => {
  if ($ability.can('read', 'aligners')) {
    return;
  }
  back();
})

const getAligner = async () => {
  try {
    if (!searchModel.value) return;
    loading.value = true;
    await getAlignerData();
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}


const serialNumberRequired = (v) => !!v || t('aligners.rules.serialNumberRequired');
</script>