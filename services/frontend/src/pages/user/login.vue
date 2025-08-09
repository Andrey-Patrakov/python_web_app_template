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
                Вход
              </v-card-title>

              <v-card-text>
                <v-row>
                  <v-col>
                    <v-text-field
                      v-model="userForm.email"
                      label="E-mail или имя пользователя"
                      :rules="[rules.requred, rules.min_str_length(5)]"
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
                    />
                  </v-col>
                </v-row>

                <v-row>
                  <v-col>
                    <v-btn
                      color="blue"
                      variant="plain"
                      density="compact"
                      class="text-body-2 pa-0"
                      @click="router.push('/user/restore-pwd')"
                    >
                      Забыли пароль?
                    </v-btn>
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
                      width="100%"
                      color="app-primary"
                    >
                      Войти
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
            Ещё нет аккаунта?
            <v-btn
              color="blue"
              variant="plain"
              class="text-body-2 pa-0"
              @click="router.push('/user/register')"
            >
              Зарегистрируйтесь
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useUsers, type UserLoginForm } from '@/stores/user';
import router from '@/router';
import { useRules } from '@/stores/rules';

const user = useUsers();

const rules = useRules();
const isValid = ref<boolean>(false);
const errorMessage = ref<string>('');

const userForm = ref<UserLoginForm>({
  email: '',
  password: '',
});

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
      errorMessage.value = error.message;
    }
  }
}
</script>
