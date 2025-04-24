<template>
  <v-container>
    <v-card :disabled="progress > 0">
      <v-card-title>Файловое хранилище</v-card-title>

      <v-card-subtitle>
        <v-progress-linear
          v-model="availableSpace"
          height="50"
          color="blue"
          striped
        >
          Занято места на диске
          ({{ storage.usedString }} / {{ storage.availableString }})
        </v-progress-linear>
      </v-card-subtitle>

      <v-container>
        <v-row>
          <v-col>
            <v-card>
              <v-card-text>
                <v-progress-linear
                  v-if="progress > 0"
                  v-model="progress"
                  height="35"
                  color="amber"
                  striped
                >
                  <template #default="{value}">
                    <strong>{{ Math.ceil(value) }}%</strong>
                  </template>
                </v-progress-linear>
              </v-card-text>
              
              <v-card-text>
                <v-file-upload
                  v-model="uploads"
                  title="Выберите файлы"
                  density="comfortable"
                  variant="comfortable"
                  multiple
                  clearable
                  show-size
                />
              </v-card-text>
          
              <v-card-actions>
                <v-btn
                  variant="outlined"
                  color="secondary"
                  height="50"
                  class="ml-auto"
                  :disabled="uploads.length == 0"
                  @click="uploadFiles"
                >
                  Загрузить
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <v-row
          v-for="file in files_list"
          :key="file.id"
        >
          <v-col>
            <v-row>
              <v-col>
                <v-card>
                  <v-card-actions>
                    <v-card
                      variant="outlined"
                      disabled
                      width="100%"
                    >
                      <v-container class="d-flex align-center text-body-2 py-2 px-3">
                        <v-avatar rounded="0">
                          <v-img
                            v-if="file.isImage && file.url"
                            :src="file.url"
                            cover
                          />
                          <v-icon
                            v-else
                            icon="mdi mdi-file-document"
                          />
                        </v-avatar>
                        <div class="ml-3 text">
                          {{ file.filename }} <br>
                          {{ file.sizeString }}
                        </div>
                      </v-container>
                    </v-card>

                    <v-btn
                      variant="outlined"
                      color="secondary"
                      height="56"
                      class="ml-1"
                      @click="downloadFile(file)"
                    >
                      Скачать
                    </v-btn>
    
                    <v-btn
                      variant="outlined"
                      color="red-lighten-1"
                      class="ml-1"
                      height="56"
                      @click="deleteFile(file)"
                    >
                      Удалить
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { VFileUpload } from 'vuetify/labs/VFileUpload'

import { type File, useStorageStore } from '@/stores/storage';

const storage = useStorageStore();

const progress = ref(0);
const uploads = ref([]);
const files_list = ref<File[]>([]);

const onProgress = (value: number) => {
  progress.value = value;
}

const refreshList = async () => {
  files_list.value = await storage.getUserFiles;
  files_list.value.forEach(file => {
    if (file.isImage) {
      storage.getLink(file);
    }
  });
}

const uploadFiles = async () => {
  await storage.upload(uploads.value, onProgress);
  uploads.value = [];
  await refreshList();
}

const deleteFile = async (file: File) => {
  await storage.delete(file);
  await refreshList();
}

const downloadFile = async (file: File) => {
  await storage.download(file, onProgress);
}

const availableSpace = computed(() => {
  return Math.ceil(storage.used / storage.available * 100);
});

onMounted(async () => {
  await refreshList();
  await storage.status();
});

</script>