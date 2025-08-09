<template>
  <v-container class="fill-height">
    <restore-pwd-dialog
      v-if="token && token_type==RESTORE_PASSWORD"
      v-model="token"
      class="mt-5 pa-5 mx-auto"
      width="500"
    />

    <v-card
      v-else
      class="mt-5 pa-5 mx-auto"
      width="600"
    >
      <v-container>
        <v-row>
          <v-col align="center">
            <v-progress-circular
              v-if="loading"
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
            <span v-if="loading">
              Выполняю подтверждение действия, ждите...
            </span>
            <span v-else-if="error">
              При выполнении операции возникла ошибка!<br>
              {{ errorMessage }}
            </span>
            <span v-else>
              Подтверждение прошло успешно, эту страницу можно закрыть.
            </span>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-container>
</template>

<script lang="ts" setup>
import { useUsers, type UserConfirmForm } from '@/stores/user';

const user = useUsers();
const query = useRoute().query;

const loading = ref(true);
const error = ref(false);
const errorMessage = ref('');

const token = ref('');
const token_type = ref('');

const RESTORE_PASSWORD = 'rpwd';

onMounted(async () => {
  if (query.token) {
    token.value = query.token.toString();
    token_type.value = query.type?.toString() || '';
    switch(token_type.value)
    {
      case RESTORE_PASSWORD: break;
      default: await confirm();
    }
  } else {
    errorMessage.value = 'Токен отсутствует!';
    error.value = true;
    loading.value = false;
  }
});

const confirm = async () => {
  loading.value = true;
  error.value = false;
  errorMessage.value = '';
  try {
    const confirm_form = <UserConfirmForm>{token: query.token};
    await user.confirm(confirm_form);
  } catch (e: any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    errorMessage.value = '';
    error.value = true;
    if (e.status == 404) {
      errorMessage.value = 'Токен не найден!';
    }
  }
  loading.value = false;
}

</script>