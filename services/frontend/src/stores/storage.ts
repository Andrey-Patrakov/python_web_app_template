import axios from 'axios';

export const getFileLink = async (
    storage_id: string,
    file_size: number = 0,
    on_progress: null | ((progress: number) => void) = null) => {

  let url = '';
  await axios.get(`api/download/${storage_id}`, {
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
