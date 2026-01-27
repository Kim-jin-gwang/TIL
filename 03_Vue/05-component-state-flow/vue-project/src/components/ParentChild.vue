<template>
  <div>
    <h2>Child</h2>
    <!-- <button @click="$emit('someEvent')">클릭!</button> -->
    <button @click="buttonClick">클릭!</button>
    <button @click="onEmitArgs">추가 인자 전달</button>
    <input type="text">
    <button @click="onChangeName">데이터 전송</button>
    <p>{{ myMsg }}</p>
    <ParentGrandChild
      :my-msg="myMsg"
      />
  </div>
</template>

<script setup>
import ParentGrandChild from '@/components/ParentGrandChild.vue'
import {ref} from 'vue'

const props = defineProps({
  myMsg: String // 다른 데이터 타입 들어와도 경고만 뜸
})

const emit = defineEmits(['someEvent','emitArgs'])

const buttonClick = function() {
  emit('someEvent')
}

const onEmitArgs = function() {
  emit('emitArgs', 1, 2, 3)
}

const name = ref('')
const onChangeName = function(){
  emit('updateName',name.value)
}

console.log('myMsg:', props.myMsg)
</script>

<style scoped>

</style>