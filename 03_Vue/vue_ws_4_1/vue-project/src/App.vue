<template>
  <div>
    <nav class="top-nav">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/products">Products</RouterLink>
      <RouterLink to="/favorite">Favorite</RouterLink>
    </nav>
    
  </div>
  <RouterView />
</template>

<script setup>
import { RouterLink,RouterView } from 'vue-router';
</script>

<style scoped>
.top-nav{
  color:white;
  background-color: rgb(85, 85, 85);
  font-size: 20px;

  display: flex;
  justify-content: center;
  align-items: center;
  gap:30px;
  height: 50px;
  
}

nav a{
  color:white;
  text-decoration: none;
}

</style>