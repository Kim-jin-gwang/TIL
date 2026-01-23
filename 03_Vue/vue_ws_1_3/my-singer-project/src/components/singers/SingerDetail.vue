<template>
  <div class="box">
    <h1 class="singerName">가수 이름</h1>
    <img src="@/assets/singer.jpg" class="singer">
    <p class="explain">가수 소개글</p>
  </div>
</template>

<script setup>

</script>

<style scoped>
  .box{
    text-align: center;
    border: 1px solid black;
  }

  .box img{
    width:30%;
    height: auto;
    border-radius: 50%;
  }
</style>