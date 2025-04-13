<template>
  <v-container>
    <v-form
      v-model="isValid"
      @submit.prevent="submit"
    >
      <v-card
        title="Вход"
        class="mt-5 mx-auto"
        max-width="450px"
      >
        <v-card-text>
          <v-row>
            <v-col>
              <v-text-field
                v-model="userForm.email"
                label="E-mail или имя пользователя"
                :rules="[$rules.requred, $rules.min_str_length(5)]"
              />
            </v-col>
          </v-row>
          
          <v-row>
            <v-col>
              <v-text-field
                v-model="userForm.password"
                label="Пароль"
                :rules="[$rules.requred, $rules.password]"
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
            color="app-primary"
            class="ml-auto"
            @click="clear"
          >
            Очистить
          </v-btn>
          <v-btn
            type="submit"
            variant="elevated"
            size="large"
            color="app-primary"
          >
            Подтвердить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { userStore, type LoginInterface } from '@/stores/user';
import router from '@/router';
import rules from '@/rules';

const $rules = rules();
const isValid = ref<boolean>(false);
const errorMessage = ref<string>('');

const userForm = ref<LoginInterface>({
  email: '',
  password: '',
});

const clear = () => {
  userForm.value.email = '';
  userForm.value.password = '';
}

const submit = async () => {
  if (!isValid.value) {
    errorMessage.value = 'Поля заполнены некорректно';
  } else {
    errorMessage.value = '';
    try {
      await user.login(userForm.value);
      router.replace('/user');
      return 0;
    } catch (error: any) { // eslint-disable-line @typescript-eslint/no-explicit-any
      if (typeof error?.response?.data?.detail == 'string') {
        errorMessage.value = error.response.data.detail;
      } else {
        errorMessage.value = `${error.code}: ${error.message}`;
      }
    }
  }
}

const user = userStore();
</script>