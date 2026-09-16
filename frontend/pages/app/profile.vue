<template>
  <v-container max-width="800">
    <h1 class="text-h6 mb-2">{{ $t('profile.title') }}</h1>

    <v-card class="mb-6 pa-6 d-flex align-center ga-4">
      <v-hover v-slot="{ isHovering, props }">
        <v-avatar v-bind="props" color="primary" size="72" class="position-relative cursor-pointer"
          @click="!hasPhoto ? triggerUpload() : null">
          <v-img v-if="hasPhoto" :src="`/api/files?path=${photoPath}`" cover>
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular indeterminate color="grey-lighten-5" size="20" />
              </v-row>
            </template>
          </v-img>
          <v-icon v-else icon="mdi-account" size="40" />

          <v-overlay :model-value="isHovering" contained scrim="black"
            content-class="w-100 h-100 d-flex align-center justify-center">
            <v-btn v-if="hasPhoto" class="d-flex align-center justify-center bg-error opacity-70" height="100%"
              width="100%" icon="mdi-trash-can" variant="text" color="white" @click.stop="deletePhoto" />
            <v-btn v-else class="d-flex align-center justify-center" icon="mdi-camera" height="100%" width="100%"
              variant="text" color="white" @click.stop="triggerUpload" />
          </v-overlay>
        </v-avatar>
      </v-hover>

      <input type="file" ref="fileInput" class="d-none" accept="image/*" @change="onFileSelected" />

      <div>
        <p class="text-h6">{{ fullName }}</p>
        <p class="text-caption text-grey">{{ email || username }}</p>
      </div>
    </v-card>

    <v-card class="mb-6">
      <v-card-title class="text-h6">{{ $t('profile.personalInfo') }}</v-card-title>

      <v-card-text>
        <v-form v-model="updateProfileModel" @submit.prevent="updateProfile">
          <v-row dense>
            <v-col cols="6">
              <v-text-field v-model="profile.fullName" hide-details="auto" :label="$t('profile.fullName')" counter="50"
                maxlength="50" :rules="[fullNameRequired]" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="profile.username" hide-details="auto" :label="$t('profile.username')" counter="50"
                maxlength="50" :rules="[usernameRequired]"
                @update:model-value="profile.username = $formatUsername($event)" :hint="$t('users.hints.username')" />
            </v-col>
            <v-col>
              <v-text-field v-model="profile.email" hide-details="auto" :label="$t('profile.email')" counter="50"
                maxlength="50" :rules="[emailRequired]" @update:model-value="form.email = $formatEmail($event)" />
            </v-col>
            <v-col>
              <v-select v-model="profile.language" item-title="title" item-value="value" hide-details="auto"
                :label="$t('profile.language')" :items="languages" />
            </v-col>
            <v-col cols="12" class="text-end">
              <v-btn type="submit" class="text bg-primary" :loading="loading">
                {{ $t('profile.update') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card class="mb-6">
      <v-card-title class="text-h6">{{ $t('profile.changePassword.title') }}</v-card-title>

      <v-card-text>
        <v-form ref="passwordForm" v-model="updatePasswordModel" @submit.prevent="updatePassword">
          <v-row dense>
            <v-text-field v-model="profile.username" type="text" autocomplete="username" hidden class="d-none" />
            <v-col cols="12">
              <v-text-field v-model="password.current" :label="$t('profile.changePassword.current')" hide-details="auto"
                :type="showCurrentPassword ? 'text' : 'password'" prepend-inner-icon="mdi-lock-outline"
                :append-inner-icon="showCurrentPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showCurrentPassword = !showCurrentPassword" :rules="[changePasswordRules[0]]" autocomplete="current-password">
                <template v-slot:message="{ message }">
                  {{ $t(message) }}
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="password.new" :label="$t('profile.changePassword.new')" hide-details="auto"
                :type="showNewPassword ? 'text' : 'password'" prepend-inner-icon="mdi-lock-plus-outline"
                :append-inner-icon="showNewPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showNewPassword = !showNewPassword" :rules="changePasswordRules" autocomplete="new-password">
                <template v-slot:message="{ message }">
                  {{ $t(message) }}
                </template>
              </v-text-field>

            </v-col>
            <v-col cols="12">
              <v-text-field v-model="password.confirm" :label="$t('profile.changePassword.confirm')" hide-details="auto"
                :type="showConfirmPassword ? 'text' : 'password'" prepend-inner-icon="mdi-lock-check-outline"
                :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showConfirmPassword = !showConfirmPassword" :rules="changePasswordRules" autocomplete="new-password">
                <template v-slot:message="{ message }">
                  {{ $t(message) }}
                </template></v-text-field>
            </v-col>

            <v-col cols="12" class="text-end">
              <v-btn type="submit" class="text bg-primary" :loading="loading">
                {{ $t('profile.update') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'

const { notify } = useSnackbar();
const { t, setLocale } = useI18n();
const { setPhotoPath } = useProfile();
const { $formatEmail, $formatUsername } = useNuxtApp();

definePageMeta({
  layout: 'app',
  middleware: ['private']
})

useHead({
  title: `SOE Latam | ${t('equipments.title', 2)}`
})

const languages = computed(() => [
  { title: 'Español', value: 'es' },
  { title: 'English', value: 'en' }
])

const fullName = ref('');
const email = ref('');
const username = ref('');

const photoPath = ref(null)
const hasPhoto = computed(() => !!photoPath.value)
const fileInput = ref(null)

const passwordForm = ref(null)
const updateProfileModel = ref(false);
const updatePasswordModel = ref(false);
const loading = ref(false)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const profile = ref({
  fullName: '',
  username: '',
  email: '',
  language: 'en',
})
const password = ref({
  current: '',
  new: '',
  confirm: ''
})

onBeforeMount(async () => {
  await getProfile();
})

const getProfile = async () => {
  try {
    const data = await $api('/api/users/profile');
    profile.value = data;
    fullName.value = data.fullName;
    email.value = data.email;
    username.value = data.username;
    photoPath.value = data.photoPath;
    await setLocale(data.language);
    setPhotoPath(data.photoPath);
  } catch (err) {
    notify(err, 'error');
  }
}

const updateProfile = async () => {
  try {
    if (!updateProfileModel.value) return;
    const { message } = await $api('/api/users/profile', {
      method: 'PATCH',
      body: profile.value
    })
    await getProfile();
    notify(message, 'success');
  } catch (err) {
    notify(err, 'error');
  }
}

const updatePassword = async () => {
  try {
    loading.value = true;
    if (!updatePasswordModel.value) return;
    const { message } = await $api('/api/users/password', {
      method: 'PUT',
      body: {
        current: password.value.current,
        new: password.value.new
      }
    })
    notify(message, 'success');
    passwordForm.value.reset();
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

const triggerUpload = () => fileInput.value.click();
const onFileSelected = async (event) => {
  try {
    loading.value = true;
    const file = event.target.files[0]
    if (file) {
      const formData = new FormData();
      formData.append('photo', file);
      const { message } = await $api('/api/users/photo', {
        method: 'POST',
        body: formData
      })
      notify(message, 'success');
      await getProfile();
    }
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
    event.target.value = ''
  }
}

const deletePhoto = async () => {
  try {
    loading.value = true;
    const { message } = await $api('/api/users/photo', { method: 'DELETE' })
    notify(message, 'success');
    await getProfile();
  } catch (err) {
    notify(err, 'error');
  } finally {
    loading.value = false;
  }
}

// Rules
const changePasswordRules = [
  v => !!v || 'passwordRules.required',
  v => /[A-Z]/.test(v) || 'passwordRules.requiredUpper',
  v => /[a-z]/.test(v) || 'passwordRules.requiredLower',
  v => /[^a-zA-Z\d]/.test(v) || 'passwordRules.requiredSpecial',
  v => /\d/.test(v) || 'passwordRules.requiredNumber',
  v => (v && v.length >= 10) || 'passwordRules.minLength10',
  v => (v && v.length <= 24) || 'passwordRules.maxLength24',
  v => (v === password.value.new) || 'passwordRules.dontMatch'
]
const fullNameRequired = (v) => !!v || t('users.rules.fullNameRequired');
const usernameRequired = (v) => !!v || t('users.rules.usernameRequired');
const emailRequired = (v) => !!v || t('users.rules.emailRequired');

</script>
