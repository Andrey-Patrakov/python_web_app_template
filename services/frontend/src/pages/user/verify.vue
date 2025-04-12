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
              v-if="!user.is_verified && !error"
              size="160"
              width="17"
              color="app-primary"
              indeterminate
            />
            <v-icon
              v-else-if="error"
              icon="mdi-close-circle-outline"
              size="185"
              color="error"
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
            <span v-if="verification">
              {{ message }}
            </span>
            <span v-else>
              На указанный адрес электронной почты отправлено письмо со ссылкой для подтверждения.
            </span>
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

const verification = ref(false);
const error = ref(false);
const message = ref('');

let interval: number | undefined;

onMounted(async () => {
  const query = useRoute().query;
  if (query.token) {
    verification.value = true;
    message.value = 'Выполняю подтверждение адреса электронной почты, ждите!';
    try {
      message.value = await user.verifyEmail(query.token.toString());
      if (await checkVerification()) {
        message.value += ' Эту страницу можно закрыть.';
      }
    } catch {
      error.value = true;
      message.value = 'При выполнении операции возникла ошибка!'
    }
  } else {
    verification.value = false;
    interval = setInterval(async () => {
      if (await checkVerification()) {
        clearInterval(interval);
        setTimeout(() => {
          router.back();
        }, 1500);
      }
    }, 5000);
  }
});

onUnmounted(() => {
  if (interval) {
    clearInterval(interval);
  }
});

const user = userStore();
</script>
