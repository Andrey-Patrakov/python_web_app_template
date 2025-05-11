import { defineStore } from "pinia";

interface MessagesState {
  queue: object[]
  showYesNo: boolean
  yesNoMessage: string
  resolve: (value: boolean) => void; 
}

export const useMessagesStore = defineStore('messages', {
  state: (): MessagesState => ({
    queue: [],
    showYesNo: false,
    yesNoMessage: '',
    resolve: (value: boolean) => { return value }
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

    async yesNo(message: string) {
      this.yesNoMessage = message;
      this.showYesNo = true;
      return new Promise((resolve) => {
        this.resolve = resolve;
      })
    },

    resolveYes() {
      this.resolve(true);
      this.showYesNo = false;
      this.yesNoMessage = '';
    },

    resolveNo() {
      this.resolve(false);
      this.showYesNo = false;
      this.yesNoMessage = '';
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
