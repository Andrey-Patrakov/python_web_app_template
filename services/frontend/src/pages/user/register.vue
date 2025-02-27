<template>
<v-form v-model="isValid" @submit.prevent="submit">
  <v-card
    title="Регистрация"
    class="mt-5 mx-auto"
    width="450"
  >
    <v-card-text>
      <v-row>
        <v-col>
          <v-text-field
            v-model="userForm.username"
            label="Имя пользователя"
            :rules="[$rules.requred, $rules.username]"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-text-field
            v-model="userForm.email"
            label="E-mail"
            :rules="[$rules.requred, $rules.email]"
          ></v-text-field>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col>
          <v-text-field
            v-model="userForm.password"
            label="Пароль"
            :rules="[$rules.requred, $rules.password]"
            type="password"
            @input="password2=''"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-text-field
            v-model="password2"
            label="Повторите пароль"
            :rules="[$rules.requred, $rules.passwordRepeat(userForm.password)]"
            type="password"
          ></v-text-field>
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

    <v-divider></v-divider>
    <v-card-actions>
      <v-btn
        size="large"
        color="green-lighten-1"
        class="ml-auto"
        @click="clear"
      >Очистить</v-btn>
      <v-btn
        type="submit"
        variant="elevated"
        size="large"
        color="green-lighten-1"
      >Подтвердить</v-btn>
    </v-card-actions>

    </v-card>
  </v-form>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import router from '@/router';
import { userStore } from '@/stores/user';
import rules from '@/rules';

const $rules = rules();
const isValid = ref<boolean>(false);
const errorMessage = ref<string>('');
const password2 = ref<string>('');

interface IUserForm {
  email: string,
  username: string,
  password: string,
}

const userForm = ref<IUserForm>({
    email: '',
    username: '',
    password: '',
});

const submit = async () => {
  if (!isValid.value) {
    errorMessage.value = 'Поля заполнены некорректно';
  }
  else {
    try {
      await user.register(userForm.value);
      router.push('/user/login');
    } catch (error: any) {
      if (typeof error?.response?.data?.detail == 'string') {
        errorMessage.value = error.response.data.detail;
      } else {
        errorMessage.value = 'Ошибка создания пользователя, проверьте правильность заполнения полей.';
      }
    }
  }
};

const clear = () => {
  userForm.value.email = '';
  userForm.value.username = '';
  userForm.value.password = '';
  password2.value = '';
};

const user = userStore();
</script>
