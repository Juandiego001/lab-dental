<template>
  <v-dialog v-model="sliderDialog" max-width="800" persistent :fullscreen="$vuetify.display.smAndDown">
    <v-card class="bg-grey-darken-4">
      <v-card-title class="bg-primary">
        <v-row no-gutters align="center">
          {{ $t('equipments.files.title') }}
          <v-spacer />
          <v-btn class="bg-primary" size="small" icon="mdi-close" @click="sliderDialog = false" />
        </v-row>
      </v-card-title>
      <v-card-text class="pa-0 d-flex justify-center align-center">
        <v-carousel>
          <v-carousel-item v-for="file of items">
            <v-img v-if="file.extension !== '.mp4'" width="100%" height="100%" contain
              :src="`/api/files?path=${file.path}`">
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="white" size="40" />
                </v-row>
              </template>
            </v-img>
            <video controls preload="metadata" style="width: 100%; height: calc(100% - 50px); object-fit: contain;">
              <source :src="`/api/files?path=${file.path}`" type="video/mp4" />
              {{ $t('equipments.files.videoNotSupported') }}
            </video>
          </v-carousel-item>
        </v-carousel>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
const { items, sliderDialog } = useEquipmentFiles();
</script>