<template>
  <nav>
    <RouterLink to="/">홈</RouterLink>
    <RouterLink to="/movies">영화목록</RouterLink>
    <RouterLink to="/review-search">리뷰검색</RouterLink>
    <RouterLink to="/recommended">영화추천</RouterLink>
  </nav>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
nav {
  padding: 16px;
  display: flex;
  gap: 20px;
  background-color: #1a1a2e;
}
nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}
nav a:hover {
  color: #e94560;
}
</style>
