<template>
  <el-form-item label="响应类型">
    <el-radio-group v-model="selectedItem!.type">
      <el-radio-button label="interval">Interval</el-radio-button>
      <el-radio-button label="cron">Cron</el-radio-button>
      <el-radio-button label="data">Data</el-radio-button>
    </el-radio-group>
  </el-form-item>
  <template v-if="selectedItem!.type === 'interval'">
    <el-form-item label="Hour">
      <el-input v-model="selectedItem!.data.hour" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Minute">
      <el-input v-model="selectedItem!.data.minute" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Second">
      <el-input v-model="selectedItem!.data.second" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
  </template>
  <template v-if="selectedItem!.type === 'cron'">
    <el-form-item label="Second">
      <el-input v-model="selectedItem!.data.second" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Minute">
      <el-input v-model="selectedItem!.data.minute" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Hour">
      <el-input v-model="selectedItem!.data.hour" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Day">
      <el-input v-model="selectedItem!.data.day" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Day of week">
      <el-input v-model="selectedItem!.data.day_of_week" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Week">
      <el-input v-model="selectedItem!.data.week" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>    
    <el-form-item label="Month">
      <el-input v-model="selectedItem!.data.month" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Year">
      <el-input v-model="selectedItem!.data.year" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
  </template>
  <template v-if="selectedItem!.type === 'data'">
  <el-form-item label="Second">
    <el-input v-model="selectedItem!.data.second" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Minute">
      <el-input v-model="selectedItem!.data.minute" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Hour">
      <el-input v-model="selectedItem!.data.hour" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Day">
      <el-input v-model="selectedItem!.data.day" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>  
    <el-form-item label="Month">
      <el-input v-model="selectedItem!.data.month" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
    <el-form-item label="Year">
      <el-input v-model="selectedItem!.data.year" class="not-last-input" style="width: 150px;">
      </el-input>
    </el-form-item>
  </template>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { storeToRefs } from 'pinia';

import { useShareStatesStore } from '@/stores/UseShareStatesStore'


const { selectedItem } = storeToRefs(useShareStatesStore())

</script>

<style lang="less" scoped>
.delay-input {
    width: 200px
}

.not-last-input {
    padding-right: 10px;
}

</style>