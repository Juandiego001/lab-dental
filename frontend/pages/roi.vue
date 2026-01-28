<template>
  <v-container min-height="100%" class="justify-center pa-0 text-center" fluid>
    <v-img width="100%" height="100%" cover class="position-absolute"
      src="/public/red-steel-tool-box-garage.jpg"></v-img>

    <p
      class="my-8 text-h4 bg-primary font-weight-bold text-white pa-4 d-inline-block text-center rounded-xl position-relative">
      <span class="text-h4 me-2">{{ $t('roi.title') }}</span>
      <v-icon class="text-h4">mdi-cash-register</v-icon>
    </p>

    <v-card class="mx-auto bg-primary" max-width="900">
      <v-card-title class="pa-4">
        <v-row no-gutters class="align-center">
          <p class="text-h5  font-weight-bold">{{ $t('roi.settings') }}</p>
          <v-spacer></v-spacer>
          <p class="text-subtitle-1  me-3 font-weight-medium">{{ $t('roi.exchangeRate') }}</p>
          <v-text-field v-model="exchangeRate" class="font-weight-medium " density="compact" type="number"
            variant="outlined" hide-details="auto" max-width="180">
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
            <!-- Average number of services per day -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.averageServicesDay') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="servicesDay" class="font-weight-medium" density="compact" variant="outlined"
                hide-details="auto" max-width="60">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="servicesDay" color="white" hide-details="auto" min="1" max="30" step="1"></v-slider>
            </v-col>

            <!-- Service sale rate -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.serviceSaleRate') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="servicesSaleRate" class="font-weight-medium" density="compact" variant="outlined"
                hide-details="auto" max-width="60">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="servicesSaleRate" color="white" hide-details="auto" min="1" max="50"
                step="1"></v-slider>
            </v-col>

            <!-- Employee's month salary -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.employeesMonthSalary') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="employeesMonthSalary" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="employeesMonthSalary" color="white" hide-details="auto" min="100" max="1500"
                step="50"></v-slider>
            </v-col>

            <!-- Days worked per month -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.daysWorkedMonth') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="daysWorkedMonth" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="60">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="daysWorkedMonth" color="white" hide-details="auto" min="1" max="30"
                step="1"></v-slider>
            </v-col>

            <!-- Hours of work per day -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.hoursWorkDay') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="hoursWorkedDay" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="60">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="hoursWorkedDay" color="white" hide-details="auto" min="1" max="24"
                step="1"></v-slider>
            </v-col>

            <!-- Rent of the premises per month -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.rentPremisesMonth') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="rentPremisesMonth" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="rentPremisesMonth" color="white" hide-details="auto" min="0" max="50000"
                step="200"></v-slider>
            </v-col>

            <!-- Area of the premises m² -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.areaPremises') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="areaPremises" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="areaPremises" color="white" hide-details="auto" min="10" max="2000"
                step="5"></v-slider>
            </v-col>

            <!-- Work site area m² -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.workSiteArea') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="workArea" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="workArea" color="white" hide-details="auto" min="10" max="100" step="1"></v-slider>
            </v-col>


            <!-- Equipment lease/financial per month -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.equipmentLeaseMonth') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="equipmentLeaseMonth" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="equipmentLeaseMonth" color="white" hide-details="auto" min="0" max="1000"
                step="5"></v-slider>
            </v-col>

            <!-- Equipment price -->
            <v-col cols="12" class="d-flex align-center pb-0">
              <p class="font-weight-medium text-subtitle-1">{{ $t('roi.equipmentPrice') }}</p>
              <v-spacer></v-spacer>
              <v-text-field v-model="equipmentPrice" class="font-weight-medium" density="compact"
                variant="outlined" hide-details="auto" max-width="80">
              </v-text-field>
            </v-col>

            <v-col cols="12 pt-0">
              <v-slider v-model="equipmentPrice" color="white" hide-details="auto" min="5000" max="50000"
                step="200"></v-slider>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { onBeforeMount } from 'vue';

const exchangeRate = ref(0);
const servicesDay = ref(15);
const servicesSaleRate = ref(20);
const employeesMonthSalary = ref(1000)
const daysWorkedMonth = ref(20);
const hoursWorkedDay = ref(8);
const rentPremisesMonth = ref(8);
const areaPremises = ref(25);
const workArea = ref(50);
const equipmentLeaseMonth = ref(50);
const equipmentPrice = ref(10000);


</script>
