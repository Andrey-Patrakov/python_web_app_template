// Utilities
import { defineStore } from 'pinia'
import axios from 'axios';
import { getFileLink } from '@/stores/storage';
import { showApiErrorMessage } from './messages';

const USERS_API_PATH = '/api/users';

export interface UserState {
  email: string | null,
  username: string | null,
  description: string | null,
  created_at: Date | null,
  is_verified: boolean,
  isAuthenticated: boolean,
  avatar: string | null,
}

export interface UserRegisterForm {
  email: string,
  username: string,
  password: string,
}

export interface UserLoginForm {
  email: string,
  password: string,
}

export interface UserUpdateForm {
  email: string | null,
  username: string | null,
  description: string | null,
}

export interface UserChangePasswordForm {
  old_password: string,
  new_password: string,
}

export interface UserSendRestoreMessageForm {
  email: string,
}

export interface UserRestorePasswordForm {
  token: string,
  new_password: string,
}

export interface UserConfirmForm {
  token: string,
}

export const useUsers = defineStore('user', {
  state: (): UserState => ({
    email: null,
    username: null,
    description: null,
    created_at: null,
    is_verified: false,
    isAuthenticated: false,
    avatar: null,
  }),

  actions: {
    async get_current() {
      const api = axios.create(); // to ignore interceptors
      await api.get(USERS_API_PATH).then(async (res) => {
        this.email = res.data.email;
        this.username = res.data.username;
        this.description = res.data.description || '';
        this.is_verified = res.data.is_verified;
        this.isAuthenticated = true;
        this.created_at = new Date(res.data.created_at);
        this.avatar = null; // res.data.avatar ? await getFileLink(res.data.avatar) : null; // TODO
      }).catch((error) => {
        if (error.status != 401) {
          showApiErrorMessage(error);
        }
        this.clear();
      });
    },

    async updateCurrent(user: UserUpdateForm) {
      await axios.put(`${USERS_API_PATH}`, user).then(async () => {
        await this.get_current();
      });
    },

    async changePassword(pwdForm: UserChangePasswordForm) {
      await axios.put(`${USERS_API_PATH}/change-password`, pwdForm);
    },

    async register(registerForm: UserRegisterForm) {
      await axios.post(`${USERS_API_PATH}/register`, registerForm);
    },

    async login(loginForm: UserLoginForm) {
      await axios.post(`${USERS_API_PATH}/login`, loginForm).then(async () => {
        await this.get_current();
      });
    },

    async logout() {
      await axios.post(`${USERS_API_PATH}/logout`);
      this.clear();
    },

    async verifyEmail() {
      await axios.post(`${USERS_API_PATH}/verify-email`);
    },

    async confirm(confirm_form: UserConfirmForm) {
      await axios.post(`${USERS_API_PATH}/confirm`, confirm_form);
    },

    // async sendMessage() {
    //   let message = '';
    //   await axios.post('/user/send_message').then((res) => {
    //     message = res.data.message;
    //   });
    //   return message;
    // },

    // async uploadAvatar(file:File | File[]) {
    //   const form = new FormData();
    //   if (file instanceof File) {
    //     form.append('file', file);
    //   } else {
    //     form.append('file', file[0]);
    //   }
    //   await axios.post('user/change_avatar', form);
    //   this.get_current();
    // },

    // async sendRestoreMessage(send_message_form: SendRestoreMessageInterface) {
    //   let message = '';
    //   await axios.post('user/send_restore_message', send_message_form).then((res) => {
    //     message = res.data.message;
    //   });
    //   return message;
    // },

    // async restorePassword(form: RestorePasswordInterface) {
    //   let message = '';
    //   await axios.post('user/restore_password', form).then((res) => {
    //     message = res.data.message;
    //   });
    //   return message;
    // },

    clear() {
      this.$reset();
    },
  },
})
