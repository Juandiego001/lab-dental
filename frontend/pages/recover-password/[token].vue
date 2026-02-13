<template>
  <v-container fluid class="fill-height justify-center pa-0 position-relative">
    <v-img width="100%" height="100%" cover class="position-absolute" src="/public/login_bg.png"
      style="filter:brightness(40%);"></v-img>
    <v-card max-width="400" class="bg-transparent px-6 pb-6" elevation="12">
      <v-card-title class="text-center text-h6 text-white py-4">{{ $t('recoverPassword.title') }}</v-card-title>
      <v-form @submit.prevent="changePassword">
        <v-row>
          <v-col cols="12">
            <v-text-field class="text-white" v-model="newPassword" :label="$t('recoverPassword.newPassword')"
              hide-details="auto" :type="isVisibleNewPassword ? 'text' : 'password'" variant="outlined">
              <template #append-inner>
                <v-btn :icon="isVisibleNewPassword ? 'mdi-eye-off' : 'mdi-eye'" variant="text" size="small"
                  @click="isVisibleNewPassword = !isVisibleNewPassword" />
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field class="text-white" v-model="confirmPassword" :label="$t('recoverPassword.confirmPassword')"
              hide-details="auto" :type="isVisibleConfirmPassword ? 'text' : 'password'" variant="outlined">
              <template #append-inner>
                <v-btn :icon="isVisibleConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'" variant="text" size="small"
                  @click="isVisibleConfirmPassword = !isVisibleConfirmPassword" />
              </template>
            </v-text-field>
          </v-col>

          <v-col cols="12" class="text-end">
            <NuxtLink to="/login" class="text-caption text-white text-decoration-none">
              {{ $t('recoverPassword.backToLogin') }}
            </NuxtLink>
          </v-col>

          <v-col cols="12">
            <v-btn class="text-white" block variant="outlined" type="submit">{{ $t('confirm') }}</v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { onBeforeMount } from 'vue';
import { useI18n } from 'vue-i18n'

definePageMeta({
  layout: 'account'
})

const { t } = useI18n();
const { back } = useBack();
const { notify } = useSnackbar();
const route = useRoute();

useHead({
  title: `SOE Latam | ${t('recoverPassword.title')}`
})

const isVisibleNewPassword = ref(false);
const isVisibleConfirmPassword = ref(false);
const newPassword = ref('');
const confirmPassword = ref('');

// Verificar si el link todavía está activo
onBeforeMount(async () => {
  try {
    const response = await $api('/api/users/token', {
      query: {
        token: route.params.token
      }
    })
    notify(response.message, 'success');
  } catch (err) {
    notify(err, 'error');
    back('/login');
  }
})

const changePassword = async () => {
  try {
    if (!newPassword.value || !confirmPassword.value) {
      notify(t('recoverPassword.rules.passwordRequired'), 'error');
      return;
    }

    if (newPassword.value !== confirmPassword.value) {
      notify(t('recoverPassword.rules.passwordsDontMatch'), 'error');
      return;
    }


    const response = await $api('/api/users/password', {
      method: 'PATCH',
      body: {
        token: route.params.token,
        password: newPassword.value
      }
    })

    notify(response.message, 'success')
    navigateTo('/login');
  } catch (err) {
    notify(err, 'error');
  }
}
</script>