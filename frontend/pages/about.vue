<template>
    <v-container fluid class="fill-height justify-center pa-0 position-relative">
        <v-img width="100%" height="100%" cover class="position-absolute" src="/snapon_wallpaper.jpg"></v-img>
        <v-card max-width="800" class="my-6 pa-5 bg-transparent" style="backdrop-filter: blur(12px);">
            <v-card-title class="text-h4 text-white text-center">{{ $t('aboutUs.title') }}</v-card-title>
            <v-card-text class="text-white">
                <!-- 🛠️ About SOE Latam -->
                <p class="text-h6">{{ $t('aboutUs.part1.title') }}</p>
                <p class="mt-2">
                    {{ $t('aboutUs.part1.paragraph1') }}
                    <br /><br />
                    {{ $t('aboutUs.part1.paragraph2') }}
                    <br /><br />
                    {{ $t('aboutUs.part1.paragraph3') }}
                    <br /><br />
                </p>
                
                <!-- 🌍 Vision & Mission -->
                <p class="font-weight-bold text-h6 mt-4">{{ $t('aboutUs.part2.title') }}</p>

                <!-- Vision -->
                <p class="font-weight-bold mt-2">{{ $t('aboutUs.part2.vision.title') }}</p>
                <p>{{ $t('aboutUs.part2.vision.description') }}</p>
                
                <!-- Mission -->
                <p class="font-weight-bold mt-4">{{ $t('aboutUs.part2.mission.title') }}</p>
                <p>{{ $t('aboutUs.part2.mission.description') }}</p>

                <!-- 💡 Why Choose SOE Latam? -->
                <p class="text-h6 mt-4">{{ $t('aboutUs.part3.title') }}</p>
                <ul class="mt-2 ps-6">
                    <li class="py-2">
                        <p class="font-weight-bold">{{ $t('aboutUs.part3.bullet1.title') }}</p>
                        <p>{{ $t('aboutUs.part3.bullet1.description') }}</p>
                    </li>

                    <li class="py-2">
                        <p class="font-weight-bold">{{ $t('aboutUs.part3.bullet2.title') }}</p>
                        <p>{{ $t('aboutUs.part3.bullet2.description') }}</p>
                    </li>

                    <li class="py-2">
                        <p class="font-weight-bold">{{ $t('aboutUs.part3.bullet3.title') }}</p>
                        <p>{{ $t('aboutUs.part3.bullet3.description') }}</p>
                    </li>

                    <li class="py-2">
                        <p class="font-weight-bold">{{ $t('aboutUs.part3.bullet4.title') }}</p>
                        <p>{{ $t('aboutUs.part3.bullet4.description') }}</p>
                    </li>

                    <li class="py-2">
                        <p class="font-weight-bold">{{ $t('aboutUs.part3.bullet5.title') }}</p>
                        <p>{{ $t('aboutUs.part3.bullet5.description') }}</p>
                    </li>
                </ul>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>

</script>
