<template>
  <div>
    <h3>Grandchild</h3>
    <p>{{ myMsg }}</p>
  </div>
</template>

<script setup>
defineProps({
  myMsg:String
})

</script>

<style scoped>

</style>