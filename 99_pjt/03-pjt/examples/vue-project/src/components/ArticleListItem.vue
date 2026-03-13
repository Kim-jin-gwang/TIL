<template>
  <div>
    <h4>{{ article.title }}</h4>
    <p>{{ article.content }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})
</script>
