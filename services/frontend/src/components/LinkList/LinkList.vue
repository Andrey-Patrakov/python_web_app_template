<template>
    <v-list class="py-0">
        <link-list-node :data="row" v-for="row in data"></link-list-node>
    </v-list>
</template>

<script lang="ts" setup>
</script>

<script lang="ts">
    import LinkListNode from './LinkListNode.vue';
    export default {
        props: {
            data: { type: Object, required: true },
        },
        components: {
            LinkListNode,
        },
    }
</script>