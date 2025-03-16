<template>
  <v-container>
    <v-card>
      <v-card-title>Файловое хранилище</v-card-title>

      <v-card-subtitle>
        <v-progress-linear
          v-model="ailableSpace"
          height="50"
          color="blue"
          striped
        >
          Доступное место на диске
        </v-progress-linear>
      </v-card-subtitle>

      <v-container>
        <v-row>
          <v-col>
            <v-card>
              <v-card-text>
                <v-progress-linear
                  v-if="fileProgress > 0"
                  v-model="fileProgress"
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
          v-for="(download, index) in downloads"
          :key="download.id"
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
                      <v-container class="d-flex align-center text-body-2 py-1">
                        <v-icon icon="mdi mdi-file-document" />
                        <div class="ml-4 text">
                          {{ download.filename }} <br>
                          {{ getFileSize(download.size) }}
                        </div>
                      </v-container>
                    </v-card>
    
                    <v-btn
                      variant="outlined"
                      color="secondary"
                      height="50"
                      class="ml-1"
                    >
                      Скачать
                    </v-btn>
    
                    <v-btn
                      variant="outlined"
                      color="red-lighten-1"
                      class="ml-1"
                      height="50"
                      @click="deleteFile(index)"
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
import axios from 'axios';
import { ref } from 'vue';
import { VFileUpload } from 'vuetify/labs/VFileUpload'

interface FileItem {
  id: number,
  filename: string,
  size: number
}

const uploads = ref([]);
const downloads = ref<FileItem[]>([]);
const fileProgress = ref(0);
const ailableSpace = ref(50);

const getFileSize = (size: number) => {
  if (!size) {
    return ''
  }

  const items = ['KB', 'MB', 'GB'];
  for(let i = 0; i <= items.length; i++)
  {
    size = size / 1024;
    if (size < 1024) {
      return Math.round(size * 100) / 100 + items[i];
    }  
  }

  return Math.round(size * 100) / 100 + 'GB';
}

const refreshListOfFiles = async () => {
  downloads.value = []
  await axios.get('storage/list').then(response => {
    const files = response.data;
    for (let i = 0; i < files.length; i++) {
      const item = <FileItem>{
        id: files[i].storage_id,
        filename: files[i].filename,
        size: files[i].size,
      }
      downloads.value.push(item);
    }
  });
}

const uploadFiles = async () => {

  const items_count = uploads.value.length;
  for (let i = 0; i < items_count; i++) {
    const form = new FormData();
    form.append('file', uploads.value[i]);

    await axios.post('storage/upload', form, {
      onUploadProgress: (itemUpload) => {
        if (itemUpload.total) {
          let progress = (i / items_count);
          progress += (itemUpload.loaded / itemUpload.total) / items_count;
          progress = Math.round(progress * 100);
          fileProgress.value = progress;
        }
      }
    })
    .catch(error => {
      console.log(error);
    });
  }

  fileProgress.value = 0;
  uploads.value = [];
  refreshListOfFiles();
}

const deleteFile = async (index: number) => {
  await axios.delete('storage/'+downloads.value[index].id);
  refreshListOfFiles();
}

onMounted(() => {
  refreshListOfFiles();
});

</script>