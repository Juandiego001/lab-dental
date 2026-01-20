<template>
  <v-container fluid class="fill-height justify-center pa-0 position-relative">
    <v-img width="100%" height="100%" cover class="position-absolute" src="/public/login_bg.png"
      style="filter:brightness(40%);"></v-img>
    <v-card max-width="400" class="bg-transparent px-6 pb-6" elevation="12">
      <v-card-title class="text-center text-h4 text-white py-4">Log In</v-card-title>
      <v-form @submit.prevent="logIn">
        <v-row>
          <v-col cols="12">
            <v-text-field class="text-white" v-model="email" :label="$t('login.emailUsername')" hide-details="auto"
              type="email" variant="outlined">
            </v-text-field>
          </v-col>

          <v-col cols="12 pb-0">
            <v-text-field class="text-white" v-model="password" :label="$t('login.password')" hide-details="auto"
              variant="outlined" type="password" autocomplete="off"></v-text-field>
          </v-col>

          <v-col cols="12" class="text-end">
            <NuxtLink to="/recover-password" class="text-caption text-white text-decoration-none">{{
              $t('login.forgotPassword') }}</NuxtLink>
          </v-col>

          <v-col cols="12">
            <v-btn class="text-white" block variant="outlined" type="submit">{{ $t('login.title') }}</v-btn>
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
  title: `SOE Latam | ${t('login.title')}`
})

const { notify } = useSnackbar();
const { $ability } = useNuxtApp();
const email = ref('')
const password = ref('')

const logIn = async () => {
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