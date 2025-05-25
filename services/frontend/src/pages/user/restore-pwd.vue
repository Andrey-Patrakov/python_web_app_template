<template>
  <v-container
    max-width="500px"
    class="my-5 mx-auto"
  >
    <v-card
      v-if="showPwdDialog"
      :disabled="loading"
      :loading="loading"
    >
      <v-form
        v-model="isValid"
        @submit.prevent="changePassword"
      >
        <v-container>
          <v-card-title>
            Смена пароля
          </v-card-title>

          <v-card-text>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="restoreForm.new_password"
                  label="Новый пароль"
                  :rules="[$rules.requred, $rules.password]"
                  type="password"
                  @input="password2=''"
                />
              </v-col>
            </v-row>
  
            <v-row>
              <v-col>
                <v-text-field
                  v-model="password2"
                  label="Повторите пароль"
                  :rules="[$rules.requred, $rules.passwordRepeat(restoreForm.new_password)]"
                  type="password"
                />
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-actions>
            <v-btn
              type="submit"
              variant="elevated"
              color="app-primary"
              width="100%"
            >
              Подтвердить
            </v-btn>
          </v-card-actions>
        </v-container>
      </v-form>
    </v-card>

    <v-card
      v-else
      :disabled="loading"
      :loading="loading"
    >
      <v-form
        v-model="isValid"
        @submit.prevent="sendMessage"
      >
        <v-container>
          <v-card-title>
            Восстановление пароля
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col>
                На указанный адрес электронной почты будет отправлено письмо со ссылкой на страницу восстановления пароля.
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <v-text-field
                  v-model="sendMessageForm.email"
                  label="E-mail"
                  :rules="[$rules.requred, $rules.email]"
                />
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="app-primary"
              variant="elevated"
              width="100%"
              @click="sendMessage"
            >
              Отправить письмо
            </v-btn>
          </v-card-actions>
        </v-container>
      </v-form>
    </v-card>
  </v-container>
</template>

<script lang="ts" setup>
import rules from '@/rules';
import { useMessagesStore } from '@/stores/messages';
import { useUserStore, type SendRestoreMessageInterface, type RestorePasswordInterface } from '@/stores/user';

const $rules = rules();
const user = useUserStore();
const router = useRouter();
const messages = useMessagesStore();

const isValid = ref(false);
const loading = ref(false);

const showPwdDialog = ref(false);

const restoreForm = ref<RestorePasswordInterface>({ token: '', new_password: '' });
const password2 = ref('');
const changePassword = async () => {
  if (isValid.value) {
    loading.value = true;
    try {
      await user.restorePassword(restoreForm.value);
      messages.info('Пароль изменен успешно!');
      router.replace('/user/login');
    }
    finally {
      loading.value = false;
    }
  }
}

const sendMessageForm = ref<SendRestoreMessageInterface>({ email: '' });
const sendMessage = async () => {
  if (isValid.value) {
    loading.value = true;
    try {
      await user.sendRestoreMessage(sendMessageForm.value);
      messages.info('Письмо отправлено на указанный адрес электронной почты!');
      router.replace('/user/login');
    }
    finally {
      loading.value = false;
    }
  }
}

onMounted(async () => {
  const query = useRoute().query;
  if (query.token) {
    restoreForm.value.token = query.token.toString();
    showPwdDialog.value = true;
  } else {
    showPwdDialog.value = false;
  }
});

</script>