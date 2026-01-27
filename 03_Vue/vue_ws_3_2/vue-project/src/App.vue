
<template>
  <header class="header">
    <h1 class="card-header">명함 관리 페이지</h1>
  </header>
  
  <main class="main">
    <p>명함을 관리하는 페이지입니다. 여기에 명함 목록이 표시됩니다.</p>
  </main>

  <article>
    <BusinessCard />
  </article>

  <footer class="footer">
    © 2023 My Business Cards
  </footer>

</template>


<script setup>
import BusinessCard from './components/BusinessCard.vue';



</script>





<style scoped>
  .main{
    text-align: center;
  }


  .header{
    display: flex;
    justify-content: center;
  }

  .card-header{
    width :300px;
    height:130px;
    color:white;
    background-color: rgb(28, 56, 214);

    display: flex;
    justify-content:center;
    align-items: center;

  }

  .footer{
    position: fixed;
    bottom:0;
    left:0;

    background-color: rgb(211, 210, 210);
    text-align: center;

    width:100%;
    height:50px;

    display:flex;
    justify-content: center;
    align-items: center;
  }

</style>