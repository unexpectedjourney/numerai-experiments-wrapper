<template>
    <div class="media">
        <div class="media-body">
            <h3 class="text-center image-link-text">{{state._id}}</h3>
            <h4 class="text-center image-link-text">{{state.created_at}}</h4>
        </div>

    </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'State',
  components: {
  },
  data() {
    return {
      state: {}
    };
  },
  async created() {
    this.state = await this.getState();
  },
  methods: {
    async getState() {
      const response = await axios.get(`/api/state/${this.$route.params.id}/`);
      return response.data || {};
    },
  }
}
</script>

<style scoped>
button {
    margin-left: 10px;
}
</style>
