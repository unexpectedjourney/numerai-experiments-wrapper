<template>
    <div class="media">
        <div class="media-body">
        <router-link :to="{name: 'Model', params: { id: model.id, name: model.model_name }}"
                     class="d-block mb-6 image-link">
            <h3 class="text-center image-link-text">{{model.model_name}}</h3>
        </router-link>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ModelBlock",
        props: ['model'],
    }
</script>

<style scoped>
</style>
