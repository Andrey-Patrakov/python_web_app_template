<template>
  <v-list-group
    v-if="params.data.children && params.data.children.length"
    :value="params.data.title"
  >
    <template #activator="{ props }">
      <v-list-item
        v-bind="props"
        :prepend-icon="params.data.icon"
        :title="params.data.title"
      />
      <v-divider class="border-opacity-50" />
    </template>

    <link-list-node
      v-for="row in params.data.children"
      :key="row.title"
      :data="row"
    />
  </v-list-group>

  <template v-else>
    <v-list-item
      v-if="params.data.click"
      :prepend-icon="params.data.icon"
      :to="params.data.link"
      :title="params.data.title"
      @click="params.data.click()"
    />
    <v-list-item
      v-else
      :prepend-icon="params.data.icon"
      :to="params.data.link"
      :title="params.data.title"
    />
    <v-divider class="border-opacity-50" />
  </template>
</template>

<script lang="ts" setup>
import LinkListNode from './LinkListNode.vue';
import type ListNodeInteface from './listNodeInterface';
const params = defineProps<{
  data: ListNodeInteface,
}>();
</script>
