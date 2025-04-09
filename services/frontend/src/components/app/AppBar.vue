<template>
  <v-app-bar
    app
    color="app-primary"
    height="65"
  >
    <v-card
      id="user-menu-activator"
      max-width="350"
      class="d-flex align-center justify-center ml-auto mr-3 px-3 py-2 text-body-2"
    >
      <div class="text-body-1 font-weight-medium pa-1 mr-3">
        {{ username }}
      </div>
      <v-avatar color="app-primary">
        <img
          v-if="avatar"
          :src="avatar"
          alt=""
        >
        <v-icon
          v-else
          icon="mdi-account"
          size="large"
          color="white"
        />
      </v-avatar>
    </v-card>

    <v-menu
      activator="#user-menu-activator"
      transition="slide-x-transition"
      offset="15px"
    >
      <link-list
        :data="menu"
        width="350px"
      />
    </v-menu>
  </v-app-bar>
</template>

<script lang="ts" setup>
import router from '@/router';
import { userStore } from '@/stores/user';
import LinkList from '@/components/LinkList/LinkList.vue';
import type ListNodeInteface from '../LinkList/listNodeInterface';

const avatar = '';
const username = computed(() => {
  return user.username ? user.username : 'Гость';
});

const logout = async () => {
  user.logout();
  router.push('/user/login');
}

const menu = computed(() => {
  if (user.isAuthenticated) {
    return <ListNodeInteface[]>[
      {icon: 'mdi-home', title: 'Домой', link: '/'},
      {icon: 'mdi-account-edit', title: user.username, link: '/user'},
      {icon: 'mdi-view-dashboard', title: 'Панель инструментов', link: '/dashboard'},
      {icon: 'mdi-logout', title: 'Выход', click: logout},
    ];
  }
  return <ListNodeInteface[]>[
    {icon: 'mdi-home', title: 'Домой', link: '/'},
    {icon: 'mdi-login', title: 'Вход', link: '/user/login'},
    {icon: 'mdi-account-plus', title: 'Регистрация', link: '/user/register'},
  ];
});

onMounted(() => {
  user.viewMe();
});

const user = userStore();
</script>
