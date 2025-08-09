<template>
  <v-container
    class="my-5 mx-auto"
    max-width="500px"
  >
    <v-row>
      <v-col>
        <v-form
          v-model="isValid"
          @submit.prevent="submit"
        >
          <v-card>
            <v-container>
              <v-card-title class="text-h5">
                Регистрация
              </v-card-title>
    
              <v-card-text>
                <v-row>
                  <v-col>
                    <v-text-field
                      v-model="userForm.username"
                      label="Имя пользователя"
                      :rules="[rules.requred, rules.username]"
                    />
                  </v-col>
                </v-row>
        
                <v-row>
                  <v-col>
                    <v-text-field
                      v-model="userForm.email"
                      label="E-mail"
                      :rules="[rules.requred, rules.email]"
                    />
                  </v-col>
                </v-row>
                
                <v-row>
                  <v-col>
                    <v-text-field
                      v-model="userForm.password"
                      label="Пароль"
                      :rules="[rules.requred, rules.password]"
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
                      :rules="[rules.requred, rules.passwordRepeat(userForm.password)]"
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
    
                <v-row>
                  <v-col>
                    <v-btn
                      type="submit"
                      variant="elevated"
                      size="large"
                      color="app-primary"
                      width="100%"
                    >
                      Регистрация
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-container>
          </v-card>
        </v-form>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card>
          <v-card-text class="text-center">
            Уже зарегистрированы?
            <v-btn
              color="blue"
              variant="plain"
              class="text-body-2 pa-0"
              @click="router.push('/user/login')"
            >
              Войдите
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import router from '@/router';
import { useUsers, type UserRegisterForm } from '@/stores/user';
import { useRules } from '@/stores/rules';

const user = useUsers();
const rules = useRules();

const isValid = ref<boolean>(false);
const errorMessage = ref<string>('');
const password2 = ref<string>('');

const userForm = ref<UserRegisterForm>({
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
</script>
