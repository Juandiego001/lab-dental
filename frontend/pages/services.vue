<template>
  <v-container min-height="100%" class="justify-center text-center" fluid>
    <v-row class="my-8 justify-center">
      <v-col class="my-4" cols="12">
        <p class="text-h4 bg-primary font-weight-bold text-white pa-4 d-inline-block text-center rounded-xl">{{ $t('services.title') }}</p>
      </v-col>

      <v-col class="d-flex justify-center align-center" md="4" cols="12">
        <v-card class="bg-primary">
          <v-card-title>
            <v-icon class="text-h2" size="x-large">mdi-train-car-flatbed-car</v-icon>
            <p class="text-h5">{{ $t('services.installations.title') }}</p>
          </v-card-title>
          <v-card-text>{{ $t('services.installations.description') }}</v-card-text>
        </v-card>
      </v-col>

      <v-col class="d-flex justify-center align-center" md="4" cols="12">
        <v-card class="bg-primary">
          <v-card-title>
            <v-icon class="text-h2" size="x-large">mdi-car-cog</v-icon>
            <p class="text-h5">{{ $t('services.equipments.title') }}</p>
          </v-card-title>
          <v-card-text>{{ $t('services.equipments.description') }}</v-card-text>
        </v-card>
      </v-col>

      <v-col class="d-flex justify-center align-center" md="4" cols="12">
        <v-card class="bg-primary">
          <v-card-title>
            <v-icon class="text-h2" size="x-large">mdi-certificate</v-icon>
            <p class="text-h5">{{ $t('services.warranties.title') }}</p>
          </v-card-title>
          <v-card-text>{{ $t('services.warranties.description') }}</v-card-text>
        </v-card>
      </v-col>

      <v-col class="d-flex justify-center align-center" md="4" cols="12">
        <v-card class="bg-primary">
          <v-card-title>
            <v-icon class="text-h2" size="x-large">mdi-book-cog</v-icon>
            <p class="text-h5">{{ $t('services.manuals.title') }}</p>
          </v-card-title>
          <v-card-text>{{ $t('services.manuals.description') }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>

</script>