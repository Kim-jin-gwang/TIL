import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


const API_URL = 'http://127.0.0.1:8000/api/v1/articles'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])

  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/`,
    })
    .then((response) => {
      // console.log(response.data)
      articles.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }

  return { 
    articles,
    getArticles
  }
}, { persist: true })
