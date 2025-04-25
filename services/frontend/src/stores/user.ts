// Utilities
import { defineStore } from 'pinia'
import axios from 'axios';
import { getFileLink } from '@/stores/storage';
import { showApiErrorMessage } from './messages';

export interface UserState {
  email: string | null,
  username: string | null,
  description: string | null,
  created_at: Date | null,
  is_verified: boolean,
  isAuthenticated: boolean,
  avatar: string | null,
}

export interface RegisterInterface {
  email: string,
  username: string,
  password: string,
}

export interface LoginInterface {
  email: string,
  password: string,
}

export interface UpdateInfoInterface {
  email: string | null,
  username: string | null,
  description: string | null,
}

export interface PwdChangeInterface {
  old_password: string,
  new_password: string,
}

export const useUserStore = defineStore('user', {
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
    async register(registerForm: RegisterInterface) {
      await axios.post('/user/register', registerForm);
    },

    async login(loginForm: LoginInterface) {
      await axios.post('/user/login', loginForm).then(async () => {
        await this.viewMe();
      });
    },

    async logout() {
      await axios.post('/user/logout');
      this.clear();
    },

    async changePassword(pwdForm: PwdChangeInterface) {
      await axios.post('/user/change_pwd', pwdForm);
    },

    async viewMe() {
      const api = axios.create(); // to ignore interceptors
      await api.get('/user/me').then (async (res) => {
        this.email = res.data.email;
        this.username = res.data.username;
        this.description = res.data.description || '';
        this.is_verified = res.data.is_verified;
        this.isAuthenticated = true;
        this.created_at = new Date(res.data.created_at);
        this.avatar = res.data.avatar ? await getFileLink(res.data.avatar) : null;
      }).catch((error) => {
        if (error.status != 401) {
          showApiErrorMessage(error);
        }
        this.clear();
      });
    },

    async updateInfo(user: UpdateInfoInterface) {
      await axios.post('/user/upd_info', user).then(async () => {
        await this.viewMe();
      });
    },

    async sendMessage() {
      let message = '';
      await axios.post('/user/send_message').then((res) => {
        message = res.data.message;
      });
      return message;
    },

    async verifyEmail(token: string) {
      let message = '';
      await axios.post('/user/verify_email', {token}).then((res) => {
        message = res.data.message;
      });
      return message;
    },

    async uploadAvatar(file:File | File[]) {
      const form = new FormData();
      if (file instanceof File) {
        form.append('file', file);
      } else {
        form.append('file', file[0]);
      }
      await axios.post('user/change_avatar', form);
      this.viewMe();
    },

    clear() {
      this.$reset();
    },
  },
})
