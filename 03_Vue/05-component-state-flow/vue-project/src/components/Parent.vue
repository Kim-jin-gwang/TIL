<template>
  <div>
    <h1>Parent</h1>
    <!-- html에서는 대소문자 구분이 되지 않아 케밥 케이스로 쓰고,  스크립트 영역으로 넘어가면 자동으로 카멜케이스로 변경됨-->
    <Child 
      my-msg="message"
      @some-event="someCallBack"
      @emit-args="getNumbers"
    />
    <ParentItem
      v-for="item in items"
      :key="item.id"
      :item="item"
    />
  </div>
</template>

<script setup>
import Child from '@/components/ParentChild.vue'
import ParentItem from '@/components/ParentItem.vue'
import {ref} from 'vue'

const items=ref([
  {id:1, name: 'Item1'},
  {id:2, name: 'Item2'},
  {id:3, name: 'Item3'},
])


const someCallBack = function() {
  console.log('someEvent 발생!')
}

const getNumbers = function(...args) {
  console.log('ParentChild로부터 전달받은 배열: ',args)
}

</script>

<style scoped>

</style>