<template>
  <div class="text-center pa-4">
    <v-dialog
      v-model="messages.showYesNo"
      max-width="450px"
      persistent
    >
      <v-card>
        <v-card-title>
          Подтвердите действие
        </v-card-title>
        <v-card-text>
          {{ messages.yesNoMessage }}
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="messages.resolveNo()">
            Нет
          </v-btn>
          <v-btn @click="messages.resolveYes()">
            Да
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup>
import { useMessagesStore } from '@/stores/messages';
const messages = useMessagesStore();
</script>