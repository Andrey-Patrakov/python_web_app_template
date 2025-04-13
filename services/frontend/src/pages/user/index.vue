<template>
  <v-container>
    <v-card
      class="mt-5 mx-auto"
      max-width="700px"
    >
      <v-card-title>
        Пользователь: {{ user.username }}
        <v-card-subtitle
          v-if="!user.is_verified"
          class="text-red pl-0"
        >
          Внимание: E-mail пользователя не подтвержден!
        </v-card-subtitle>
      </v-card-title>
  
      <v-divider />
  
      <v-form
        v-model="isValid"
        @submit.prevent="submit"
      >
        <v-card-text>
          <v-row>
            <v-col
              md="8"
              order-md="1"
              cols="12"
              order="2"
            >
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
                    :prepend-inner-icon="user.is_verified ? 'mdi-check-circle-outline' : 'mdi-close-circle-outline'"
                    :append-inner-icon="user.is_verified || isChanged ? '' : 'mdi-send'"
                    :rules="[$rules.requred, $rules.email]"
                    @click:append-inner="verifyEmail"
                  />
                </v-col>
              </v-row>
            </v-col>
            <v-col
              class="text-center align-content-center"
              order-md="2"
              order="1"
            >
              <v-avatar
                color="app-primary"
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
            <v-col
              md="8"
              cols="12"
            >
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
            :color="!isChanged || !isValid ? 'gray-lighten-1' : 'app-primary'"
            :disabled="!isChanged || !isValid"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-form>
  
      <change-pwd-dialog v-model="showDialog" />
    </v-card>
  </v-container>
</template>

<script lang="ts" setup>
import changePwdDialog from './$dialogs/ChangePwdDialog.vue';

import { ref } from 'vue';
import { userStore, type UpdateInfoInterface } from '@/stores/user';
import rules from '@/rules';
import router from '@/router';

const avatar = '';
const user = userStore();
const $rules = rules();
const isValid = ref<boolean>(false);
const showDialog = ref<boolean>(false);
const errorMessage = ref<string>('');
const infoMessage = ref<string>('');

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

const verifyEmail = async () => {
  infoMessage.value = await user.sendMessage();
  router.push('/user/verify');
}

const isChanged = computed(() => {
  return (
    userForm.value.email.trim() != user.email ||
    userForm.value.username.trim() != user.username ||
    userForm.value.description.trim() != user.description
  );
})

onMounted(async() => {
  await user.viewMe();
})

</script>
