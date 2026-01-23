<template>
  <div>
    <h1 class="title">{{ singerList }}</h1>
    <SingerDetail />
  </div>
</template>

<script setup>
  import SingerDetail from './singers/SingerDetail.vue';
  import { ref } from 'vue'

  const singerList = ref('가수 목록')
</script>

<style scoped>
  .title{
    text-align: center;
  }
</style>