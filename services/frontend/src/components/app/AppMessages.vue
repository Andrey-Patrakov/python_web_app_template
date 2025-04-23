<template>
  <v-snackbar-queue
    v-model="messages.queue"
    location="bottom right"
  />
</template>

<script lang="ts" setup>
import { useMessagesStore } from '@/stores/messages';

const messages = useMessagesStore();
</script>