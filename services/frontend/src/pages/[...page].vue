<template>
  <v-container
    class="my-5 mx-auto text-center"
    max-width="600px"
  >
    <v-row>
      <v-col class="text-h2 text-md-h1">
        Ошибка
        <span class="font-weight-bold text-primary">
          404
        </span>
      </v-col>
    </v-row>

    <v-row>
      <v-col class="text-h4">
        Страница не найдена!
      </v-col>
    </v-row>

    <v-row class="text-body-1">
      <v-col>
        Извините, но страницы на которую вы хотели попасть, не существует.
        Возможно, она была перемещена, удалена или переименована.
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-btn
          width="100%"
          prepend-icon="mdi-arrow-u-left-top-bold"
          @click="router.back()"
        >
          Вернуться назад
        </v-btn>
      </v-col>
      <v-col>
        <v-btn
          width="100%"
          color="app-primary"
          append-icon="mdi-arrow-right-thick"
          @click="router.replace('/')"
        >
          Перейти на главную
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import router from '@/router';
</script>