<template>
  <div>
    <p>{{ item.id }}</p>
    <p>{{ item.name }}</p>
  </div>
</template>

<script setup>
defineProps({
  item:Object
})
</script>

<style scoped>

</style>