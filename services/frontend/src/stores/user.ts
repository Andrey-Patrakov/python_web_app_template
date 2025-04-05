// Utilities
import { defineStore } from 'pinia'
import axios from 'axios';

export interface UserState {
  email: string | null,
  username: string | null,
  description: string | null,
  created_at: Date | null,
  is_verified: boolean,
  isAuthenticated: boolean,
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

export const userStore = defineStore('user', {
  state: (): UserState => ({
    email: null,
    username: null,
    description: null,
    created_at: null,
    is_verified: false,
    isAuthenticated: false,
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
      try {
        await axios.get('/user/me').then((res) => {
          this.email = res.data.email;
          this.username = res.data.username;
          this.description = res.data.description || '';
          this.is_verified = res.data.is_verified;
          this.isAuthenticated = true;
          this.created_at = new Date(res.data.created_at);
        });
      } catch(error) {
        this.clear();
        throw error;
      }
    },

    async updateInfo(user: UpdateInfoInterface) {
      await axios.post('/user/upd_info', user).then(async () => {
        await this.viewMe();
      });
    },

    async verifyEmail() {
      let message = '';
      await axios.post('/user/verify_email').then((res) => {
        message = res.data.message;
      });
      return message;
    },

    clear() {
      this.$reset();
    },
  },
})
