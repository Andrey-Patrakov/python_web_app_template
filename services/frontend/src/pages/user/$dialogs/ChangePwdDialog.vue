<template>
  <v-dialog
    v-model="showDialog"
    width="auto"
    persistent
  >
    <v-form
      v-model="isValid"
      @submit.prevent="submit"
    >
      <v-card width="600">
        <v-card-title>
          <v-card-actions>
            Смена пароля            
            <v-btn
              variant="elevated"
              color="red-lighten-2"
              height="40"
              width="40"
              min-width="40"
              class="ml-auto px-0"
              @click="close"
            >
              <v-icon icon="mdi mdi-window-close" />
            </v-btn>
          </v-card-actions>
        </v-card-title>
        
        <v-card-text>
          <v-row>
            <v-col>
              <v-text-field
                v-model="pwdForm.old_password"
                label="Старый пароль"
                :rules="[$rules.requred, $rules.password]"
                type="password"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                v-model="pwdForm.new_password"
                label="Новый пароль"
                :rules="[$rules.requred, $rules.password, equalPasswords(pwdForm.old_password)]"
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
                :rules="[$rules.requred, $rules.passwordRepeat(pwdForm.new_password)]"
                type="password"
              />
            </v-col>
          </v-row>

          <v-row v-if="errorMessage">
            <v-col>
              <div class="text-red-darken-4 text-body-2">
                Ошибка: {{ errorMessage }}
              </div>
            </v-col>
          </v-row>
        </v-card-text>

        <v-divider />
        <v-card-actions>
          <v-btn
            size="large"
            color="green-lighten-1"
            class="ml-auto"
            @click="clear"
          >
            Очистить
          </v-btn>
          <v-btn
            type="submit"
            variant="elevated"
            size="large"
            color="green-lighten-1"
          >
            Подтвердить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script setup lang="ts">
import rules from '@/rules';
import { type PwdChangeInterface, userStore } from '@/stores/user';
const $rules = rules();

const showDialog = defineModel<boolean>();
const isValid = ref<boolean>(false);
const errorMessage = ref<string>('');
const password2 = ref<string>('');

const pwdForm = ref<PwdChangeInterface>({
  old_password: '',
  new_password: '',
});

const equalPasswords = (old_pwd: string) => {
  return (new_pwd: string): boolean | string => {
    return !old_pwd || !new_pwd || old_pwd != new_pwd || 'Новый пароль не должен совпадать со старым!';
  }
}

const clear = () => {
  pwdForm.value.old_password = '';
  pwdForm.value.new_password = '';
  password2.value = '';
  errorMessage.value = '';
};

const submit = async () => {
  if (!isValid.value) {
    errorMessage.value = 'Поля заполнены некорректно';
  }
  else {
    try {
      await user.changePassword(pwdForm.value);
      close();
    } catch (error: any) { // eslint-disable-line @typescript-eslint/no-explicit-any
      if (typeof error?.response?.data?.detail == 'string') {
        errorMessage.value = error.response.data.detail;
      } else {
        errorMessage.value = `${error.code}: ${error.message}`;
      }
    }
  }
};

const close = () => {
  showDialog.value = false;
  clear();
};

const user = userStore();
</script>
