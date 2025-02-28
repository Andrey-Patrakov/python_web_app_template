<template>
  <v-list class="py-0">
    <link-list-node
      v-for="row in props.data"
      :key="row.title"
      :data="row"
    />
  </v-list>
</template>

<script lang="ts" setup>
import LinkListNode from './LinkListNode.vue';
import type ListNodeInteface from './listNodeInterface';
const props = defineProps<{
  data: ListNodeInteface[],
}>();
</script>
