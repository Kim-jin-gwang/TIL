<template>
  <div>
      <h3>자식 페이지입니다.</h3>
      <p>이름 : {{ child.name }}</p>
      <p>나이 : {{ child.age }}</p>
      <p>용돈 : {{ child.balance }}</p>
      <button @click="moreBalance">용돈 더 주세요</button>
  </div>
</template>

<script setup>

const props = defineProps({
  child:Object
})

const emit = defineEmits('changeBalance')

const moreBalance = () =>{
  emit('changeBalance',props.child)
}


</script> 

<style scoped>

</style>