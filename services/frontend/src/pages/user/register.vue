<template>
  <v-container>
    <v-form
      v-model="isValid"
      @submit.prevent="submit"
    >
      <v-card
        title="Регистрация"
        class="mt-5 mx-auto"
        max-width="450px"
      >
        <v-card-text>
          <v-row>
            <v-col>
              <v-text-field
                v-model="userForm.username"
                label="Имя пользователя"
                :rules="[$rules.requred, $rules.username]"
              />
            </v-col>
          </v-row>
  
          <v-row>
            <v-col>
              <v-text-field
                v-model="userForm.email"
                label="E-mail"
                :rules="[$rules.requred, $rules.email]"
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
                @input="password2=''"
              />
            </v-col>
          </v-row>
  
          <v-row>
            <v-col>
              <v-text-field
                v-model="password2"
                label="Повторите пароль"
                :rules="[$rules.requred, $rules.passwordRepeat(userForm.password)]"
                type="password"
              />
            </v-col>
          </v-row>
  
          <v-row v-if="errorMessage">
            <v-col>
              <div class="text-red-darken-4 text-body-2">
                {{ errorMessage }}
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
import router from '@/router';
import { useUserStore, type RegisterInterface } from '@/stores/user';
import rules from '@/rules';

const user = useUserStore();
const $rules = rules();

const isValid = ref<boolean>(false);
const errorMessage = ref<string>('');
const password2 = ref<string>('');

const userForm = ref<RegisterInterface>({
  email: '',
  username: '',
  password: '',
});

const submit = async () => {
  if (!isValid.value) {
    errorMessage.value = 'Ошибка: Поля заполнены некорректно';
  }
  else {
    try {
      await user.register(userForm.value);
      router.replace('/user/login');
    } catch (error: any) { // eslint-disable-line @typescript-eslint/no-explicit-any
      errorMessage.value = error.message;
    }
  }
};

const clear = () => {
  userForm.value.email = '';
  userForm.value.username = '';
  userForm.value.password = '';
  password2.value = '';
};

</script>
