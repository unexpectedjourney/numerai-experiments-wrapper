<template>
  <div class="container">
    <h2 class="text-center">Models</h2>
    <br>
    <div v-if="models.length != 0" class="row">
        <ModelBlock v-for="model in models" v-bind:key="model.id" v-bind:model="model" />
    </div>
    <div v-else>
        <p>No Data</p>
    </div>
    </div>
</template>

<script>

import axios from "axios";
import ModelBlock from '@/components/ModelBlock.vue'

export default {
  name: 'Models',
  components: {
    ModelBlock
  },
  data() {
    return {
      models: []
    };
  },
  async created() {
    this.models = await this.getModels();
    console.log(this.models);
  },
  methods: {
    async getModels() {
      const response = await axios.get("/api/model/");
      return response.data || [];
    }
  }
}
</script>
