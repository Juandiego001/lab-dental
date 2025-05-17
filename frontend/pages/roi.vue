<template>
    <v-container min-height="100vh" class="justify-center">
        <p class="text-primary text-center py-6">
            <span class="text-h4 me-2">{{ $t('roi.title') }}</span>
            <v-icon class="text-h4">mdi-cash-register</v-icon>
        </p>

        <v-card class="mx-auto" max-width="800">
            <v-card-title class="pa-4">
                <v-row no-gutters class="align-center">
                    <p class="text-h5 text-primary font-weight-bold">{{ $t('roi.settings') }}</p>
                    <v-spacer></v-spacer>
                    <p class="text-subtitle-1 text-primary me-3 font-weight-medium">{{ $t('roi.exchangeRate') }}</p>
                    <v-text-field v-model="exchangeRate" class="font-weight-medium text-primary" density="compact" type="number"
                        variant="outlined" hide-details="auto" max-width="140">
                        <template v-slot:prepend-inner>
                            <p>$</p>
                        </template>
                        <template v-slot:append-inner>
                            <p class="font-weight-bold text-disabled">USD</p>
                        </template>
                    </v-text-field>
                </v-row>
            </v-card-title>
            <v-card-text>
                <v-form>
                    <v-row>
                        <!-- Average number of services per day -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.averageServicesDay') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="servicesDay" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="60">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="servicesDay" color="primary" hide-details="auto" min="1" max="30" step="1"></v-slider>
                        </v-col>

                        <!-- Service sale rate -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.serviceSaleRate') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="servicesSaleRate" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="60">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="servicesSaleRate" color="primary" hide-details="auto" min="1" max="50" step="1"></v-slider>
                        </v-col>

                        <!-- Employee's month salary -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.employeesMonthSalary') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="employeesMonthSalary" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="80">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="employeesMonthSalary" color="primary" hide-details="auto" min="100" max="1500" step="50"></v-slider>
                        </v-col>
                        
                        <!-- Days worked per month -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.daysWorkedMonth') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="daysWorkedMonth" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="60">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="daysWorkedMonth" color="primary" hide-details="auto" min="1" max="30" step="1"></v-slider>
                        </v-col>

                        <!-- Hours of work per day -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.hoursWorkDay') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="hoursWorkedDay" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="60">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="hoursWorkedDay" color="primary" hide-details="auto" min="1" max="24" step="1"></v-slider>
                        </v-col>

                        <!-- Rent of the premises per month -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.rentPremisesMonth') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="rentPremisesMonth" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="80">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="rentPremisesMonth" color="primary" hide-details="auto" min="0" max="50000" step="200"></v-slider>
                        </v-col>

                        <!-- Area of the premises m² -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.areaPremises') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="areaPremises" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="80">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="areaPremises" color="primary" hide-details="auto" min="10" max="2000" step="5"></v-slider>
                        </v-col>

                        <!-- Work site area m² -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.workSiteArea') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="workArea" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="80">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="workArea" color="primary" hide-details="auto" min="10" max="100" step="1"></v-slider>
                        </v-col>


                        <!-- Equipment lease/financial per month -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.equipmentLeaseMonth') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="equipmentLeaseMonth" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="80">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="equipmentLeaseMonth" color="primary" hide-details="auto" min="0" max="1000" step="5"></v-slider>
                        </v-col>

                        <!-- Equipment price -->
                        <v-col cols="12" class="d-flex align-center pb-0">
                            <p class="font-weight-medium text-subtitle-1 text-primary">{{ $t('roi.equipmentPrice') }}</p>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="equipmentPrice" class="text-primary font-weight-medium" density="compact"
                                variant="outlined" hide-details="auto" max-width="80">
                            </v-text-field>
                        </v-col>

                        <v-col cols="12 pt-0">
                            <v-slider v-model="equipmentPrice" color="primary" hide-details="auto" min="5000" max="50000" step="200"></v-slider>
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
