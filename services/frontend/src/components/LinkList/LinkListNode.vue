<template>
  <v-list-group
    v-if="data.children && data.children.length"
    :value="data.name"
  >
    <template v-slot:activator="{ props }">
      <v-list-item
        v-bind="props"
        :prepend-icon="data.icon"
        :title="data.title"
      ></v-list-item>
      <v-divider class="border-opacity-50"></v-divider>
    </template>

    <link-list-node
      :data="row"
      v-for="row in data.children"
    ></link-list-node>
  </v-list-group>

  <template v-else>
    <v-list-item
      v-if="'click' in data"
      :prepend-icon="data.icon"
      :to="data.link"
      :title="data.title"
      @click="data.click()"
    ></v-list-item>
    <v-list-item
      v-else
      :prepend-icon="data.icon"
      :to="data.link"
      :title="data.title"
    ></v-list-item>
    <v-divider class="border-opacity-50"></v-divider>
  </template>
</template>

<script lang="ts" setup>
</script>

<script lang="ts">
export default {
  name: 'link-list-node',
  props: {
    data: { type: Object, required: true },
  },
}
</script>