<template>
  <v-container fluid class="fill-height justify-center pa-0 position-relative">
    <v-img width="100%" height="100%" cover class="position-absolute" src="/public/login_bg.png"
      style="filter:brightness(40%);"></v-img>
    <v-card max-width="400" class="bg-transparent px-6 pb-6" elevation="12">
      <v-card-title class="text-center text-h6 text-white py-4">{{ $t('recoverPassword.title') }}</v-card-title>
      <v-form @submit.prevent="sendEmail">
        <v-row>
          <v-col cols="12">
            <v-text-field class="text-white" v-model="email" :label="$t('recoverPassword.email')" hide-details="auto"
              type="email" variant="outlined">
            </v-text-field>
          </v-col>

          <v-col cols="12" class="text-end">
            <NuxtLink to="/login" class="text-caption text-white text-decoration-none">
              {{ $t('recoverPassword.backToLogin') }}
            </NuxtLink>
          </v-col>

          <v-col cols="12">
            <v-btn class="text-white" block variant="outlined" type="submit">{{ $t('send') }}</v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n();

definePageMeta({
  layout: 'account'
})

useHead({
  title: `SOE Latam | ${t('recoverPassword.title')}`
})

const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const email = ref('')

const sendEmail = async () => {
  try {
    const response = await $api('/api/users/login', {
      method: 'POST',
      body: {
        email: email.value,
        password: password.value
      }
    })
    const { abilities } = await $api('/api/users/profile', { method: 'GET' });
    $ability.update(abilities);
    notify(response.message, 'success')
    navigateTo('/app');
  } catch (err) {
    notify(err, 'error');
  }
}
</script>
