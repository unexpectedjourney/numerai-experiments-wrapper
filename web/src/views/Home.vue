<template>
  <div class="container center">
    <p>Hello, this is a numerai wrapper to provide easy interface for numerai competition pipeline. You can see you several models here and get their results.</p>
    <p>To work properly with this pipeline, please download numerai data, and after submission or prediction, please, wait a while to get state file.</p>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld
  }
}
</script>
