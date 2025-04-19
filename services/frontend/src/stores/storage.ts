import { defineStore } from 'pinia'
import axios from 'axios';

interface StorageState {
  used: number,
  available: number,
  usedString: string,
  availableString: string,
}

export interface File {
  id: string,
  filename: string,
  size: number,
  sizeString: string,
  isImage: boolean,
  url: string,
}

const fileSizeToString = (size: number) => {
  if (!size) {
    return '0KB';
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

const fileIsImage = (filename: string) => {
  const imageExtensions = [".jpg", ".png", ".gif", ".jpeg"];
  const lastDot = filename.lastIndexOf(".");
  const extension = filename.substring(lastDot);
  return imageExtensions.includes(extension.toLowerCase());
}

export const getFileLink = async (
    storage_id: string,
    file_size: number = 0,
    on_progress: null | ((progress: number) => void) = null) => {

  let url = '';
  await axios.get(`storage/download/${storage_id}`, {
    responseType: 'blob',
    onDownloadProgress: (itemDownload) => {
      if (on_progress && file_size > 0) {
        let progress = (itemDownload.loaded / file_size);
        progress = Math.round(progress * 100);
        on_progress(progress);
      }
    },
  }).then(response => {
    url = window.URL.createObjectURL(response.data);
  });

  if (on_progress) {
    on_progress(0);
  }
  return url;
}

export const storageStore = defineStore('storage', {

  state: (): StorageState => ({
    used: 0,
    available: 0,
    usedString: '',
    availableString: '',
  }),

  getters: {
    async getUserFiles() {
      const files_list: File[] = [];
      await axios.get('storage/list').then(response => {
        for (let i = 0; i < response.data.length; i++) {
          const file = <File>{
            id: response.data[i].storage_id,
            filename: response.data[i].filename,
            size: response.data[i].size,
            sizeString: fileSizeToString(response.data[i].size),
            isImage: fileIsImage(response.data[i].filename),
            url: '',
          }

          files_list.push(file);
        }
      });
      return files_list;
    },
  },

  actions: {
    async status() {
      await axios.get('storage/status').then(response => {
        this.used = response.data.used_space;
        this.available = response.data.available_space;
        this.usedString = fileSizeToString(this.used * 1024 * 1024);
        this.availableString = fileSizeToString(this.available * 1024 * 1024);
      });
      return <StorageState>{
        used: this.used,
        available: this.available,
        usedString: this.usedString,
        availableString: this.availableString,
      }
    },

    async upload(files:never[], on_progress: null | ((progress: number) => void) = null) {
      for (let i = 0; i < files.length; i++) {
        const form = new FormData();
        form.append('file', files[i]);

        await axios.post('storage/upload', form, {
          onUploadProgress: (itemUpload) => {
            if (on_progress && itemUpload.total) {
              let progress = (i / files.length);
              progress += (itemUpload.loaded / itemUpload.total) / files.length;
              progress = Math.round(progress * 100);
              on_progress(progress);
            }
          }
        })
        .catch(error => {
          console.log(error);
        });
      }

      if (on_progress) {
        on_progress(0);
      }
      await this.status();
    },

    async getLink(file: File, on_progress: null | ((progress: number) => void) = null) {
      return await getFileLink(file.id, file.size, on_progress);
    },

    async download(file: File, on_progress: null | ((progress: number) => void) = null) {
      const url = await this.getLink(file, on_progress);
      if (url) {
        const a = document.createElement('a');
        a.href = url;
        a.download = file.filename;
        a.click();
        setTimeout(() => window.URL.revokeObjectURL(url), 0);
      }
    },

    async delete(file: File) {
      await axios.delete(`storage/${file.id}`);
      await this.status();
    },
  },
})
