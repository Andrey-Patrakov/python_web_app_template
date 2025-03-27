<template>
  <v-card
    class="mt-5 mx-auto"
    width="700"
  >
    <v-card-title>
      Пользователь: {{ user.username }}
    </v-card-title>

    <v-divider />

    <v-form
      v-model="isValid"
      @submit.prevent="submit"
    >
      <v-card-text>
        <v-row>
          <v-col cols="8">
            <v-row>
              <v-col>
                <v-text-field
                  v-model="userForm.username"
                  variant="outlined"
                  label="Имя пользователя"
                  :rules="[$rules.requred, $rules.username]"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <v-text-field
                  v-model="userForm.email"
                  variant="outlined"
                  label="E-mail"
                  :rules="[$rules.requred, $rules.email]"
                />
              </v-col>
            </v-row>
          </v-col>
          <v-col class="text-center align-content-center">
            <v-avatar
              color="green"
              size="120"
            >
              <img
                v-if="avatar"
                width="120"
                aspect-ratio="1/1"
                :src="avatar"
                alt=""
              >
              <v-icon
                v-else
                icon="mdi-account"
                size="120"
                color="white"
              />
            </v-avatar>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="8">
            <v-text-field
              v-model="userForm.created_at"
              variant="outlined"
              label="Дата создания"
              disabled
            />
          </v-col>
          <v-col>
            <v-btn
              block
              variant="elevated"
              height="55"
              @click="showDialog = true"
            >
              Смена пароля
            </v-btn>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-textarea
              v-model="userForm.description"
              variant="outlined"
              label="Описание"
              maxlength="1000"
              counter="1000"
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
          type="submit"
          variant="elevated"
          size="large"
          class="ml-auto"
          :color="!isChanged || !isValid ? 'gray-lighten-1' : 'green-lighten-1'"
          :disabled="!isChanged || !isValid"
        >
          Сохранить
        </v-btn>
      </v-card-actions>
    </v-form>

    <change-pwd-dialog v-model="showDialog" />
  </v-card>
</template>

<script lang="ts" setup>
import changePwdDialog from './$dialogs/ChangePwdDialog.vue';

import { ref } from 'vue';
import { userStore, type UpdateInfoInterface } from '@/stores/user';
import rules from '@/rules';

const avatar = '';
const user = userStore();
const $rules = rules();
const isValid = ref<boolean>(false);
const showDialog = ref<boolean>(false);
const errorMessage = ref<string>('');

interface IUserForm {
  email: string,
  username: string,
  description: string,
  created_at: string,
}

const userForm = ref<IUserForm>({
  email: user.email || '',
  username: user.username || '',
  description: user.description || '',
  created_at: user.created_at?.toLocaleDateString() || '',
});

const submit = async () => {
  if (isChanged.value) {
    const info = <UpdateInfoInterface>{
      email: userForm.value.email,
      username: userForm.value.username,
      description: userForm.value.description
    };
    user.updateInfo(info);
  }
};

const isChanged = computed(() => {
  return (
    userForm.value.email.trim() != user.email ||
    userForm.value.username.trim() != user.username ||
    userForm.value.description.trim() != user.description
  );
})

</script>
