<template>
  <v-container
    max-width="500px"
    class="my-5 mx-auto"
  >
    <v-card
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
                  v-model="restorePasswordForm.email"
                  label="E-mail"
                  :rules="[rules.requred, rules.email]"
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
import { useRules } from '@/stores/rules';
import { useMessagesStore } from '@/stores/messages';
import { useUsers, type UserRestorePasswordForm } from '@/stores/user';

const rules = useRules();
const user = useUsers();
const router = useRouter();
const messages = useMessagesStore();

const isValid = ref(false);
const loading = ref(false);

const restorePasswordForm = ref<UserRestorePasswordForm>({ email: '' });
const sendMessage = async () => {
  if (isValid.value) {
    loading.value = true;
    try {
      await user.restorePassword(restorePasswordForm.value);
      messages.info('Письмо отправлено на указанный адрес электронной почты!');
      router.replace('/user/login');
    }
    finally {
      loading.value = false;
    }
  }
}
</script>
