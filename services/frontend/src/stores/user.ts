// Utilities
import { defineStore } from 'pinia'
import axios from 'axios';

interface UserState {
  email: string | null;
  username: string | null;
  isAuthenticated:  boolean;
}

export const userStore = defineStore('user', {
  state: (): UserState => ({
    email: null,
    username: null,
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
          this.isAuthenticated = true;
        });
        return null;
      } catch(error) {
        this.clear();
        throw error;
      }
    },

    clear() {
      this.$reset();
    },
  },
})
