<template>
  <div class="card">
    <h4>이름 : {{ card.name }}</h4>
    <p>직함 : {{ card.title }}</p>
  </div>
</template>

<script setup>
defineProps({
  card:Object
})

</script>

<style scoped>
.card{
  width:100%;
  max-width: 420px;
  border: 1px solid #cfcfcf;
  background-color: rgb(245, 244, 244);
  text-align: center;
  padding: 26px 18px;

}


</style>