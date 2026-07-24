<template>
  <v-container fluid class="fill-height justify-center">
    <v-card max-width="700" class="pa-3 bg-primary" elevation="10">
      <v-card-title class="text-center">
        <p class="text-h4 pt-2 pb-8">{{ $t('contact.us') }}</p>
      </v-card-title>

      <v-card-text>
        <v-form>
          <v-row class="justify-center align-center">
            <v-col cols="6">
              <v-text-field :label="$t('email')" hide-details="auto" autocomplete="off" />
            </v-col>

            <v-col cols="6">
              <v-text-field :label="$t('phone')" hide-details="auto" autocomplete="off" />
            </v-col>

            <v-col cols="12">
              <v-text-field :label="$t('name')" hide-details="auto" autocomplete="off" />
            </v-col>

            <v-col cols="12">
              <v-textarea :label="$t('message')" hide-details="auto" />
            </v-col>

            <v-col class="text-end" cols="12">
              <v-btn type="submit" variant="outlined">{{ $t('send') }}</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>

</script>
