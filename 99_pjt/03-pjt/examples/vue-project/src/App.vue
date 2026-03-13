<template>
  <header>
    <nav>
      <RouterLink v-bind:to = "{name: 'ArticleView'}">Article</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink} from 'vue-router'
</script>

<style scoped>
</style>
