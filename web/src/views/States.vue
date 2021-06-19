<template>
  <div class="container">
    <h2 class="text-center">States</h2>
    <br>
    <div v-if="states.length != 0" class="row">
        <StateBlock v-for="state in states" v-bind:key="state._id" v-bind:state="state" />
    </div>
    <div v-else>
        <p>No Data</p>
    </div>
    </div>
</template>

<script>

import axios from "axios";
import StateBlock from '@/components/StateBlock.vue'

export default {
  name: 'States',
  components: {
    StateBlock
  },
  data() {
    return {
      states: []
    };
  },
  async created() {
    this.states = await this.getStates();
    console.log(this.states);
  },
  methods: {
    async getStates() {
      const response = await axios.get("/api/state/");
      return response.data || [];
    }
  }
}
</script>
