<template>
  <Picture mysrc="/assets/logo.png"></Picture>
</template>

<script>
import Picture from './components/SinglePicture.vue'

export default {
  name: 'App',
  components: {
    Picture
  }
}
</script>

<style scoped lang="less">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
