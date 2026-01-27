<template>
  <header class="header">
    <h2>보유 명함 목록</h2>
  </header>

  <section class="card-section">
    <div class="card-grid">
      <BusinessDetail
        v-for="card in Cards"
        :key="card.name"
        :card="card"
      />
    </div>
  </section>
</template>

<script setup>
  import BusinessDetail from './BusinessDetail.vue';
  

  const Cards = [
    {name:'일론 머스크',title: '테슬라 테크노킹'},
    {name:'래리 엘리슨',title: '오라클 창업주'},
    {name:'빌 게이츠',title: '마이크로소프트 공동창업주'},
    {name:'래리 페이지',title: '구글 공동창업주'},
    {name:'세르게이 브린',title: '구글 공동창업주'}
  ]

</script>

<style scoped>
.header{
  text-align: center;
}

.card-section{
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px 20px;
}

.card-grid{
  display: grid;
  grid-template-columns: repeat(2,1fr);
  gap: 40px 50px;
  justify-items: center;
}

.card-grid > :last-child{
  grid-column: 1 / -1;
  justify-self: center;
  
}

</style>