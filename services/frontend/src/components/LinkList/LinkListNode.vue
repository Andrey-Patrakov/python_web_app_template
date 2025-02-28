<template>
  <v-list-group
    v-if="props.data.children && props.data.children.length"
    :value="props.data.title"
  >
    <template #activator>
      <v-list-item
        :prepend-icon="props.data.icon"
        :title="props.data.title"
      />
      <v-divider class="border-opacity-50" />
    </template>

    <link-list-node
      v-for="row in props.data.children"
      :key="row.title"
      :data="row"
    />
  </v-list-group>

  <template v-else>
    <v-list-item
      v-if="props.data.click"
      :prepend-icon="props.data.icon"
      :to="props.data.link"
      :title="props.data.title"
      @click="props.data.click()"
    />
    <v-list-item
      v-else
      :prepend-icon="props.data.icon"
      :to="props.data.link"
      :title="props.data.title"
    />
    <v-divider class="border-opacity-50" />
  </template>
</template>

<script lang="ts" setup>
import LinkListNode from './LinkListNode.vue';
import type ListNodeInteface from './listNodeInterface';
const props = defineProps<{
  data: ListNodeInteface,
}>();
</script>
