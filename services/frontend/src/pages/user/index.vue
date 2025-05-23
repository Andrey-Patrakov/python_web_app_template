<template>
  <v-container>
    <v-card
      class="mt-5 mx-auto"
      max-width="700px"
      :loading="loading"
      :disabled="loading"
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
                  <v-btn
                    v-if="!user.is_verified && !isChanged"
                    color="info"
                    width="100%"
                    @click="verifyEmail"
                  >
                    Подтвердить E-mail
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>
            <v-col
              class="text-center align-content-center"
              order-md="2"
              order="1"
            >
              <v-hover>
                <template #default="{ isHovering, props }">
                  <label
                    for="f-input"
                    v-bind="props"
                  >
                    <v-avatar
                      color="app-primary"
                      size="160"
                    >
                      <v-icon
                        v-if="isHovering"
                        icon="mdi-upload-circle-outline"
                        size="160"
                        color="white"
                      />
                      <v-img
                        v-else-if="user.avatar"
                        :src="user.avatar"
                        alt="avatar image"
                      />
                      <v-icon
                        v-else
                        icon="mdi-account"
                        size="160"
                        color="white"
                      />
                    </v-avatar>
                  </label>
                </template>
              </v-hover>
              <div hidden>
                <v-file-input
                  id="f-input"
                  accept="image/*"
                  @update:model-value="user.uploadAvatar"
                />
              </div>
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
import changePwdDialog from '@/components/user/ChangePwdDialog.vue';

import { ref } from 'vue';
import { useUserStore, type UpdateInfoInterface } from '@/stores/user';
import rules from '@/rules';
import router from '@/router';
import { useMessagesStore } from '@/stores/messages';

const user = useUserStore();
const $rules = rules();
const isValid = ref<boolean>(false);
const showDialog = ref<boolean>(false);
const infoMessage = ref<string>('');
const messages = useMessagesStore();
const loading = ref(false);

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
  if (!isChanged.value) {
    return;
  }

  if (userForm.value.email.trim() != user.email && user.is_verified) {
    let message = ' При смене адреса электронной почты потребуется повторное подтверждение!';
    message += ' Вы уверены, что хотите продолжить?';
    if (!await messages.yesNo(message)) {
      return;
    }
  }

  loading.value = true;
  const info = <UpdateInfoInterface>{
    email: userForm.value.email,
    username: userForm.value.username,
    description: userForm.value.description
  };
  user.updateInfo(info);
  loading.value = false;

};

const verifyEmail = async () => {
  loading.value = true;
  infoMessage.value = await user.sendMessage();
  router.push('/user/verify');
  loading.value = false;
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
