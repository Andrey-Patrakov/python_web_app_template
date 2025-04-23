import { defineStore } from "pinia";

interface MessagesState {
  queue: object[]
}

export const useMessagesStore = defineStore('messages', {
  state: (): MessagesState => ({
    queue: [],
  }),

  actions: {
    warning(message: string) {
      this.queue.push({text: message, color: 'warning'});
    },

    info(message: string) {
      this.queue.push({text: message, color: 'info'});
    },

    error(message: string) {
      this.queue.push({text: message, color: 'error'});
    },

  },

})