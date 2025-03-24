import { defineStore } from 'pinia'
import axios from 'axios';

export interface File {
  id: string,
  filename: string,
  size: number,
  sizeString: string,
}

const fileSizeToString = (size: number) => {
  if (!size) {
    return '';
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

export const storageStore = defineStore('storage', {

  getters: {
    async getUserFiles() {
      const files_list: File[] = [];
      await axios.get('storage/list').then(response => {
        for (let i = 0; i < response.data.length; i++) {
          files_list.push(<File>{
            id: response.data[i].storage_id,
            filename: response.data[i].filename,
            size: response.data[i].size,
            sizeString: fileSizeToString(response.data[i].size),
          });
        }
      });
      return files_list;
    },
  },

  actions: {
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
    },

    async getLink(file: File, on_progress: null | ((progress: number) => void) = null) {
      let url = '';
      await axios.get(`storage/download/${file.id}`, {
        responseType: 'blob',
        onDownloadProgress: (itemDownload) => {
          if (on_progress && file.size > 0) {
            let progress = (itemDownload.loaded / file.size);
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
    },
  },
})
