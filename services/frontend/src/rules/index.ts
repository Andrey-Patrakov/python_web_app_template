import type { App } from 'vue'
import { inject } from 'vue'

interface Rules {
  requred: Function,
  username: Function,
  email: Function,
  password: Function,
  passwordRepeat: Function,
}

const rules = <Rules>{
  requred: (value: string) => !!value || 'Поле обязательно для заполнения',

  min_str_length: (len: number) => {
    return (value: string) => {
      return value.trim().length >= len || `Минимальный размер поля ${len} символов`;
    };
  },

  username: (value: string) => {
    const regex = /^[a-zа-я0-9!#$%&'*+/=?^_`{|}~-]+/i;
    value = value.trim();
    if (value.length < 5) {
      return 'Имя пользователя должно содержать минимум 5 символов';
    }

    return regex.test(value) || 'Допускаются цифры буквы и символы (!#$%&*+/=?^_`{|}~-)';
  },

  email: (value: string) => {
    const regex = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/i
    return regex.test(value.trim()) || 'Невалидный e-mail адрес';
  },

  password: (value: string) => {
    // const regex = /^(?=(.*[a-zа-я]){1,})(?=(.*[A-ZА-Я]){1,})(?=(.*[0-9]){1,})(?=(.*[!@#$%^&*()\-__+.]){1,}).{8,}$/
    const regex = /^(?=(.*[a-zа-я]){1,})(?=(.*[A-ZА-Я]){1,})(?=(.*[0-9]){1,}).{8,}$/
    return regex.test(value.trim()) || 'Пароль должен содержать минимум 8 символов и состоять из букв в верхнем и нижнем регистре и цифр';
  },

  passwordRepeat: (password: string) => {
    return (value: string) => value == password || 'Пароли не совпадают'
  },
};

export const installRules = {
  install: (app: App) => {
    app.provide('$rules', rules);
  }
}

export default function (): any {
  return inject('$rules');
}
