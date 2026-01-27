<template>
  <div>
    <h3>자식 페이지입니다.</h3>
    <p>이름 : {{ item.name }}</p>
    <p>나이 : {{ item.age }}</p>
  </div>
</template>

<script setup>
defineProps({
  item:Object
})

</script>

<style scoped>
div{
  border: 1px solid black;
  margin: 20px;
  padding: 15px;
}

</style>