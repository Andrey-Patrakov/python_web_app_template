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

});

export const showApiErrorMessage = (error: any) => {// eslint-disable-line @typescript-eslint/no-explicit-any
  const messages = useMessagesStore();

  let message = error.message;
  if (typeof error?.response?.data?.detail == 'string') {
    message = error.response.data.detail;
  }
  const errorMessage = `Ошибка ${error.status}: ${message}`;
  messages.error(errorMessage);
  return errorMessage;
}
