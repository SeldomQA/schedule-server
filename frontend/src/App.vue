<template>
  <el-container>
    <HomeHeader />
  </el-container>
  <el-container>
    <HomeMain />
  </el-container>
</template>

<script setup lang="ts">
import HomeHeader from './views/HomeHeader.vue';
import HomeMain from './views/HomeMain.vue';

</script>

<style lang="less">
body {
  margin: 0;
  overflow: hidden;   //解决切换路由时页面抖动：竖向滚动条闪烁
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
}
</style>
