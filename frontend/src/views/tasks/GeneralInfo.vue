<template>
  <el-form-item label="Job ID" prop="job_id">
    <el-input v-model="selectedItem!.job_id"></el-input>
  </el-form-item>
  <!-- <el-form-item label="名称" prop="name">
      <el-input v-model="selectedItem!.name" disabled></el-input>
  </el-form-item> -->
  <el-form-item label="请求" prop="request_url">
    <el-input v-model="selectedItem!.request_url"></el-input>
  </el-form-item>
  <el-form-item label="下一次运行时间" prop="next_run_time">
    <el-input v-model="selectedItem!.next_run_time" disabled></el-input>
  </el-form-item>
</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia';

import { useShareStatesStore } from '@/stores/UseShareStatesStore'

const { selectedItem } = storeToRefs(useShareStatesStore())
</script>

<style lang="less" scoped>
.input-3 {
    width: calc(100%/3);
    padding-right: 10px;

}
.last-input {
    padding-right: 0px;
}

</style>