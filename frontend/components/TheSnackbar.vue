<template>
  <v-snackbar v-model="snackbar.visible" absolute :color="snackbar.color">
    {{ snackbar.message }}

    <template v-slot:actions>
      <v-btn color="white" icon="mdi-close" size="x-small" variant="text" @click="snackbar.visible = false"></v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
const { snackbar } = useSnackbar();
</script>
