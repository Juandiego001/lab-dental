<template>
  <v-dialog v-model="partsDialog" max-width="500" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card>
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ partData.id ? $t('warranties.parts.update') : $t('warranties.parts.create') }}
          <v-spacer />
          <v-btn class="bg-primary" size="x-small" icon="mdi-close" @click="partsDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form v-model="formModel" @submit.prevent="savePart">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="form.partNumber" hide-details="auto" :label="$t('warranties.parts.partNumber')"
                :rules="[partNumberRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.description" hide-details="auto" :label="$t('warranties.parts.description')"
                :rules="[descriptionRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.invoiceParts" hide-details="auto" :label="$t('warranties.parts.invoiceParts')"
                :rules="[invoicePartsRequired]" counter="50" maxlength="50" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.quantity" hide-details="auto" :label="$t('warranties.parts.quantity')"
                :rules="[quantityRequired]" counter="50" maxlength="50" type="number" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.price" hide-details="auto" :label="$t('warranties.parts.price')"
                :rules="[priceRequired]" type="number" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.total" hide-details :label="$t('warranties.parts.total')" readonly />
            </v-col>
            <v-col class="text-end">
              <v-btn variant="outlined" @click="partsDialog = false" @mousedown.prevent :disabled="loading">
                {{ $t('cancel') }}
              </v-btn>
              <span class="mx-1" />
              <v-btn type="submit" class="bg-primary" @mousedown.prevent :loading="loading">
                {{ $t('confirm') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n();
const { $isNum } = useNuxtApp();
const { items: parts, partsDialog, partData } = useWarrantiesParts();
const loading = ref(false);
const { notify } = useSnackbar();
const formModel = ref(false);
const form = ref({
  partNumber: null,
  description: null,
  invoiceParts: null,
  quantity: null,
  price: null,
  total: null,
});


const setTotal = () => {
  if (!$isNum(form.value.quantity)) return;
  if (!$isNum(form.value.price)) return;

  form.value.total = parseFloat(form.value.quantity) * parseFloat(form.value.price);
}

watch(partsDialog, (v) => {
  if (!v) {
    resetForm();
    return
  }
  form.value = { ...partData.value };
})

watch(() => form.value.quantity, () => setTotal());
watch(() => form.value.price, () => setTotal());

const resetForm = () => {
  form.value = {
    partNumber: null,
    description: null,
    invoiceParts: null,
    quantity: null,
    price: null,
    total: null
  }
}


const savePart = () => {
  try {
    loading.value = true;
    if (!formModel.value) return;
    if (form.value.id) {
      // Updating
      let partIndex = parts.value.findIndex((e) => e.id === form.value.id);
      parts.value[partIndex] = { ...form.value };
    } else {
      // Creating
      form.value.id = Date.now();
      parts.value = [...parts.value, { ...form.value }];
    }

    partsDialog.value = false;
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}


const partNumberRequired = (v) => !!v || t('warranties.parts.rules.partNumberRequired');
const descriptionRequired = (v) => !!v || t('warranties.parts.rules.descriptionRequired');
const invoicePartsRequired = (v) => !!v || t('warranties.parts.rules.invoicePartsRequired');
const quantityRequired = (v) => !!v || t('warranties.parts.rules.quantityRequired');
const priceRequired = (v) => !!v || t('warranties.parts.rules.priceRequired');
</script>
