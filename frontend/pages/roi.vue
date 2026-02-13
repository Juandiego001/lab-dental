<template>
  <v-container min-height="100%" class="justify-center pa-0 text-center" fluid>
    <v-img width="100%" height="100%" cover class="position-absolute"
      src="/public/roi.webp"></v-img>

    <p
      class="my-8 text-h4 bg-primary font-weight-bold text-white pa-4 d-inline-block text-center rounded-xl position-relative">
      <span class="text-h4 me-2">{{ $t('roi.title') }}</span>
      <v-icon class="text-h4">mdi-cash-register</v-icon>
    </p>

    <v-card class="mx-auto bg-primary mb-10" max-width="900" elevation="10">
      <v-card-title class="pa-4">
        <v-row no-gutters class="align-center">
          <p class="text-h5 font-weight-bold">{{ $t('roi.settings') }}</p>
          <v-spacer />
          <p class="text-subtitle-1 me-3 font-weight-medium">{{ $t('roi.exchangeRate') }}</p>
          <v-text-field v-model.number="exchangeRate" class="font-weight-medium" density="compact" type="number"
            variant="outlined" hide-details="auto" max-width="180" @update:model-value="handleExchangeRate">
            <template v-slot:prepend-inner>
              <p>$</p>
            </template>
            <template v-slot:append-inner>
              <p class="font-weight-bold text-white">USD</p>
            </template>
          </v-text-field>
        </v-row>
      </v-card-title>

      <v-card-text>
        <v-form>
          <v-row>
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.averageServicesDay') }}</p>
              <v-spacer />
              <v-text-field v-model.number="servicesDay" class="font-weight-medium" density="compact" variant="outlined"
                hide-details="auto" max-width="80"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="servicesDay" color="white" hide-details="auto" min="1" max="30" step="1"></v-slider>
            </v-col>

            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.serviceSaleRate') }}</p>
              <v-spacer />
              <v-text-field v-model.number="servicesSaleRate" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="servicesSaleRate" color="white" hide-details="auto" min="1" :max="limits.saleRate"
                step="1"></v-slider>
            </v-col>

            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.employeesMonthSalary') }}</p>
              <v-spacer />
              <v-text-field v-model.number="employeesMonthSalary" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="employeesMonthSalary" color="white" hide-details="auto" min="100" :max="limits.salary"
                step="50"></v-slider>
            </v-col>

            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.daysWorkedMonth') }}</p>
              <v-spacer />
              <v-text-field v-model.number="daysWorkedMonth" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="daysWorkedMonth" color="white" hide-details="auto" min="1" max="30"
                step="1"></v-slider>
            </v-col>

            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.hoursWorkDay') }}</p>
              <v-spacer />
              <v-text-field v-model.number="hoursWorkedDay" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="hoursWorkedDay" color="white" hide-details="auto" min="1" max="24" step="1"></v-slider>
            </v-col>

            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.rentPremisesMonth') }}</p>
              <v-spacer />
              <v-text-field v-model.number="rentPremisesMonth" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="100"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="rentPremisesMonth" color="white" hide-details="auto" min="0" :max="limits.rent"
                step="200"></v-slider>
            </v-col>

            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.areaPremises') }}</p>
              <v-spacer />
              <v-text-field v-model.number="areaPremises" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="areaPremises" color="white" hide-details="auto" min="10" max="2000"
                step="5"></v-slider>
            </v-col>

            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.workSiteArea') }}</p>
              <v-spacer />
              <v-text-field v-model.number="workArea" class="font-weight-medium" density="compact" variant="outlined"
                hide-details="auto" max-width="80"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="workArea" color="white" hide-details="auto" min="10" max="100" step="1"></v-slider>
            </v-col>

            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.equipmentLeaseMonth') }}</p>
              <v-spacer />
              <v-text-field v-model.number="equipmentLeaseMonth" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="100"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="equipmentLeaseMonth" color="white" hide-details="auto" min="0" :max="limits.lease"
                step="5"></v-slider>
            </v-col>

            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.equipmentPrice') }}</p>
              <v-spacer />
              <v-text-field v-model.number="equipmentPrice" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="100"></v-text-field>
            </v-col>
            <v-col cols="12" class="pt-0">
              <v-slider v-model="equipmentPrice" color="white" hide-details="auto" min="5000" :max="limits.price"
                step="200"></v-slider>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <v-divider class="border-opacity-25" color="white"></v-divider>
      <v-card-text class="pa-6">
        <h3 class="text-h4 font-weight-bold text-white mb-4">{{ $t('roi.prediction') || 'Prediction' }}</h3>
        <v-row>
          <v-col cols="12" md="6">
            <v-sheet class="pa-4 rounded-lg bg-transparent text-primary" elevation="2">
              <v-icon size="40" class="mb-2">mdi-trending-up</v-icon>
              <h4 class="text-subtitle-1 font-weight-bold">Gross profit per year</h4>
              <p class="text-h4 font-weight-black">{{ formattedGrossProfit }}</p>
            </v-sheet>
          </v-col>
          <v-col class="d-flex align-items-center justify-center" cols="12" md="6">
            <v-sheet class="d-flex align-center justify-center pa-4 rounded-lg bg-transparent text-primary w-100"
              elevation="2">
              <template v-if="monthsToRecover > 0">
                <div>
                  <v-icon size="40" class="mb-2">mdi-calendar-check</v-icon>
                  <h4 class="text-subtitle-1 font-weight-bold">Months to recover investment</h4>
                  <p class="text-h4 font-weight-black">{{ monthsToRecover }}</p>
                </div>
              </template>
              <p v-else color="error" block
                class="d-flex align-center justify-center text-h6 font-weight-black mt-2 text-button">Investment not
                profitable</p>
            </v-sheet>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, reactive } from 'vue';
import { useI18n } from 'vue-i18n'
const { t } = useI18n();

useHead({
  title: `SOE Latam | ${t('roi.title')}`
})

// Variables de estado (Refs)
const exchangeRate = ref(1);
const servicesDay = ref(15);
const servicesSaleRate = ref(20);
const employeesMonthSalary = ref(1000);
const daysWorkedMonth = ref(20);
const hoursWorkedDay = ref(8);
const rentPremisesMonth = ref(1000);
const areaPremises = ref(25);
const workArea = ref(50);
const equipmentLeaseMonth = ref(50);
const equipmentPrice = ref(10000);

// Límites dinámicos basados en la tasa de cambio (mimic de index.js)
const limits = reactive({
  saleRate: 50,
  salary: 1500,
  rent: 50000,
  lease: 1000,
  price: 50000
});

// Función para manejar el cambio en la tasa (Exchange Rate)
const handleExchangeRate = (val) => {
  const rate = val || 1;
  // Actualizar máximos
  limits.price = 50000 * rate;
  limits.lease = 1000 * rate;
  limits.rent = 50000 * rate;
  limits.salary = 1500 * rate;
  limits.saleRate = 50 * rate;

  // Actualizar valores actuales (según lógica original)
  equipmentPrice.value = 10000 * rate;
  equipmentLeaseMonth.value = 50 * rate;
  rentPremisesMonth.value = 1000 * rate;
  employeesMonthSalary.value = 1000 * rate;
  servicesSaleRate.value = 20 * rate;
};

// --- LÓGICA DE CÁLCULO (Computed) ---

const grossProfitPerYear = computed(() => {
  // Traduciendo netcalc(a, b, c, d, e, f, g, h, i, j)
  const a = servicesDay.value;
  const b = servicesSaleRate.value;
  const c = employeesMonthSalary.value;
  const d = daysWorkedMonth.value;
  const e = hoursWorkedDay.value;
  const f = rentPremisesMonth.value;
  const g = areaPremises.value;
  const h = workArea.value;
  const i = equipmentLeaseMonth.value;

  const c1 = a * b;
  const d1 = c / (d * e);
  const e1 = a * d1;
  const r1 = f / g;
  const t1 = r1 * h;
  const f1 = t1 / 720;
  const g1 = a * f1;
  const h1 = e1 + g1;
  const i1 = c1 - h1;
  const k1 = i1 - (i / 30);
  const l1 = k1 * d;
  const u1 = l1 * 12;

  return u1;
});

const monthsToRecover = computed(() => {
  const net = grossProfitPerYear.value;
  if (net <= 0) return -1;
  // Traduciendo yearcalc(k, m)
  return Math.round((equipmentPrice.value / net) * 12);
});

// Formateo de moneda
const formattedGrossProfit = computed(() => {
  return new Intl.NumberFormat('en-US', {
    style: 'decimal',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(grossProfitPerYear.value);
});
</script>