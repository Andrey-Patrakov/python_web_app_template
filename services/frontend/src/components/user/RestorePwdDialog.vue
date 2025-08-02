<template>
  <v-card
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
                v-model="confirmForm.password"
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
                :rules="[$rules.requred, $rules.passwordRepeat(confirmForm.password || '')]"
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
</template>

<script lang="ts" setup>
import rules from '@/rules';
import { useMessagesStore } from '@/stores/messages';
import { useUsers, type UserConfirmForm } from '@/stores/user';

const $rules = rules();
const user = useUsers();
const router = useRouter();
const messages = useMessagesStore();

const token = defineModel<string>({ required: true });
const isValid = ref<boolean>(false);
const loading = ref(false);

const confirmForm = ref<UserConfirmForm>({ token: token.value, password: '' });
const password2 = ref('');
const changePassword = async () => {
  if (isValid.value) {
    loading.value = true;
    try {
      await user.confirm(confirmForm.value);
      messages.info('Пароль изменен успешно!');
      router.replace('/user/login');
    }
    finally {
      loading.value = false;
    }
  }
}
</script>
