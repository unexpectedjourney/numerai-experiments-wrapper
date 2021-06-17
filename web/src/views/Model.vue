<template>
    <div class="media">
        <div class="media-body">
            <h3 class="text-center image-link-text">{{model.model_name}}</h3>
            <button type="button" v-on:click="trainModel()" class="btn btn-outline-primary">Train</button>
            <button type="button" v-on:click="tuneModel()" class="btn btn-outline-secondary">Tune Params</button>
            <button type="button" v-on:click="testModel()" class="btn btn-outline-success">Predict and Score</button>
            <button type="button" v-on:click="submitModel()" class="btn btn-outline-warning">Submit</button>
        </div>

    </div>
</template>

<script>
import axios from "axios";
import ModelBlock from '@/components/ModelBlock.vue'

export default {
  name: 'Model',
  components: {
    ModelBlock
  },
  data() {
    return {
      model: []
    };
  },
  async created() {
    this.model = await this.getModel();
    console.log(this.model);
  },
  methods: {
    async getModel() {
      const response = await axios.get("/api/model/");
      let data = response.data || [];
      data = data.filter((element) => {return element.id == this.$route.params.id});
      if (data.length != 0) {
        return data[0]
      } else {
        return {}
      }
    },
    async trainModel() {
      let data = {
        "model_id": this.$route.params.id,
        "action": 1,
        "model_params": {}
      }
      const response = await axios.post(`/api/model/`, data);
      this.$router.push({name:'Models'});
    },
    async tuneModel() {
      let data = {
        "model_id": this.$route.params.id,
        "action": 2,
        "model_params": {}
      }
      const response = await axios.post(`/api/model/`, data);
      this.$router.push({name:'Models'});
    },
    async testModel() {
      let data = {
        "model_id": this.$route.params.id,
        "action": 3,
        "model_params": {}
      }
      const response = await axios.post(`/api/model/`, data);
      this.$router.push({name:'Models'});
    },
    async submitModel() {
      let data = {
        "model_id": this.$route.params.id,
        "action": 4,
        "model_params": {}
      }
      const response = await axios.post(`/api/model/`, data);
      this.$router.push({name:'Models'});
    },

  }
}
</script>

<style scoped>
button {
    margin-left: 10px;
}
</style>
