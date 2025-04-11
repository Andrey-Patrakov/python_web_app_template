<template>
  <v-container class="fill-height">
    <v-card
      class="mt-5 pa-5 mx-auto"
      width="600"
    >
      <v-container>
        <v-row>
          <v-col align="center">
            <v-progress-circular
              v-if="!user.is_verified"
              size="160"
              width="17"
              color="app-primary"
              indeterminate
            />
            <v-icon
              v-else
              icon="mdi-check-circle-outline"
              size="185"
              color="app-primary"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col align="center">
            На указанный адрес электронной почты отправлено письмо со ссылкой для подтверждения.
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-container>
</template>

<script lang="ts" setup>
import router from '@/router';
import { userStore } from '@/stores/user';

const checkVerification = async () => {
  await user.viewMe();
  return user.is_verified;
}

let interval: number | undefined;

onMounted(async () => {  
  interval = setInterval(async () => {
    if (await checkVerification()) {
      clearInterval(interval);
      setTimeout(() => {
        router.back();
      }, 1500);
    }
  }, 5000);
});

onUnmounted(() => {
  if (interval) {
    clearInterval(interval);
  }
});

const user = userStore();
</script>
