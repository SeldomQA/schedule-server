<script lang="ts" setup>
import { ref } from 'vue'

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<template>
  <div>
    <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    @select="handleSelect"
  >
    <el-menu-item index="0">
      <span style="font-size: 20px;font-weight: 500;">
        Schedule-Server
      </span>
    </el-menu-item>
    <div class="flex-grow" />
    <el-sub-menu index="2">
      <template #title>个人</template>
      <el-menu-item index="2-1">Setting</el-menu-item>
      <el-menu-item index="2-2">Logout</el-menu-item>
    </el-sub-menu>
  </el-menu>
  </div>
</template>

<style>
.el-emeu-demo {
  padding: 0 24px;
  box-shadow: var(--ct-box-shadow);
  min-height: 70px;
  left: 260px;
  right: 0;
  z-index: 1001;
}

.flex-grow {
  flex-grow: 1;
  
}
</style>
