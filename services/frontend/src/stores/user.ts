// Utilities
import { defineStore } from 'pinia'
import axios from 'axios';

interface UserState {
  email: string | null;
  username: string | null;
  description: string | null;
  created_at: Date | null;
  isAuthenticated:  boolean;
}

export interface UpdateInfoInterface {
  email: string | null;
  username: string | null;
  description: string | null;
}

export const userStore = defineStore('user', {
  state: (): UserState => ({
    email: null,
    username: null,
    description: null,
    created_at: null,
    isAuthenticated: false,
  }),

  actions: {
    async register(user: object) {
      await axios.post('/auth/register', user);
      return user;
    },

    async login(user: object) {
      await axios.post('/auth/login', user).then(async () => {
        await this.viewMe();
      });
      return user;
    },

    async logout() {
      await axios.post('/auth/logout');
      this.clear();
      return null;
    },

    async viewMe() {
      try {
        await axios.get('/auth/me').then((res) => {
          this.email = res.data.email;
          this.username = res.data.username;
          this.description = res.data.description || '';
          this.isAuthenticated = true;
          this.created_at = new Date(res.data.created_at);
        });
        return null;
      } catch(error) {
        this.clear();
        throw error;
      }
    },

    async updateInfo(user: UpdateInfoInterface) {
      await axios.post('/auth/upd_info', user).then(async () => {
        await this.viewMe();
      });
    },

    clear() {
      this.$reset();
    },
  },
})
