<template>
    <div class="media">
        <div class="media-body">
        <router-link :to="{name: 'State', params: { id: state._id, name: state._id }}"
                     class="d-block mb-6 image-link">
            <h3 class="text-center image-link-text">{{state._id}}</h3>
        </router-link>
        </div>
    </div>
</template>

<script>
    export default {
        name: "StateBlock",
        props: ['state'],
    }
</script>

<style scoped>
</style>
