<template>
  <v-container fluid class="fill-height justify-center bg-primary">
    <v-card max-width="800" flat class="my-6 pa-6 bg-transparent" elevation="10">
      <v-card-title class="text-h3 text-center">{{ $t('terms.title') }}</v-card-title>
      <v-card-text>
        <h3 class="mb-2">{{ $t('terms.acceptanceTerms.title') }}</h3>
        <p class="mb-3">{{ $t('terms.acceptanceTerms.description') }}</p>

        <h3 class="mb-2">{{ $t('terms.platformDescription.title') }}</h3>
        <p class="mb-1">{{ $t('terms.platformDescription.description') }}</p>
        <ul class="ms-5 mb-3">
          <li v-html="$t('terms.platformDescription.list.bullet1')"></li>
          <li v-html="$t('terms.platformDescription.list.bullet2')"></li>
          <li v-html="$t('terms.platformDescription.list.bullet3')"></li>
        </ul>

        <h3 class="mb-2">{{ $t('terms.registrationAccess.title') }}</h3>
        <p class="mb-3">{{ $t('terms.registrationAccess.description') }}</p>

        <h3 class="mb-2">{{ $t('terms.acceptableUse.title') }}</h3>
        <p class="mb-1">{{ $t('terms.acceptableUse.description') }}</p>
        <ul class="ms-5 mb-3">
          <li>{{ $t('terms.acceptableUse.list.bullet1') }}</li>
          <li>{{ $t('terms.acceptableUse.list.bullet2') }}</li>
          <li>{{ $t('terms.acceptableUse.list.bullet3') }}</li>
        </ul>

        <h3 class="mb-2">{{ $t('terms.issuanceCertificates.title') }}</h3>
        <p v-html="$t('terms.issuanceCertificates.description')" class="mb-3"></p>

        <h3 class="mb-2">{{ $t('terms.availabilityManuals.title') }}</h3>
        <p class="mb-3">{{ $t('terms.availabilityManuals.description') }}</p>

        <h3 class="mb-2">{{ $t('terms.responsibilities.title') }}</h3>
        <p class="mb-1">{{ $t('terms.responsibilities.description') }}</p>
        <ul class="ms-5 mb-3">
          <li>{{ $t('terms.responsibilities.list.bullet1') }}</li>
          <li>{{ $t('terms.responsibilities.list.bullet2') }}</li>
          <li>{{ $t('terms.responsibilities.list.bullet3') }}</li>
        </ul>

        <h3 class="mb-2">{{ $t('terms.modifications.title') }}</h3>
        <p class="mb-3">{{ $t('terms.modifications.description') }}</p>

        <h3 class="mb-2">{{ $t('terms.intellectualProperty.title') }}</h3>
        <p class="mb-3">{{ $t('terms.intellectualProperty.description') }}</p>

        <h3 class="mb-2">{{ $t('terms.governingLaw.title') }}</h3>
        <p class="mb-3">{{ $t('terms.governingLaw.description') }}</p>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {

}
</script>
