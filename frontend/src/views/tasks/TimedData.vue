<template>
  <div>
    <el-form-item label="定时类型">
      <el-radio-group 
        v-model="selectedItem!.type"
        :disabled="!isNewJob"
      >
        <el-radio-button label="interval">Interval</el-radio-button>
        <el-radio-button label="cron">Cron</el-radio-button>
        <el-radio-button label="date">Date</el-radio-button>
      </el-radio-group>
    </el-form-item>
    <div v-if="selectedItem!.type === 'interval'">
      <el-form-item label="Hours">
        <el-input-number v-model="selectedItem!.data.hour" :min="0" style="width: 150px" />
      </el-form-item>
      <el-form-item label="Minutes">
        <el-input-number v-model="selectedItem!.data.minute" :min="0" style="width: 150px" />
      </el-form-item>
      <el-form-item label="Seconds">
        <el-input-number v-model="selectedItem!.data.second" :min="0" style="width: 150px" />
      </el-form-item>
    </div>
    <div v-else-if="selectedItem!.type === 'cron'">
      <el-form-item label="Second">
        <el-input v-model="selectedItem!.data.second" style="width: 150px" />
      </el-form-item>
      <el-form-item label="Minute">
        <el-input v-model="selectedItem!.data.minute" style="width: 150px" />
      </el-form-item>
      <el-form-item label="Hour">
        <el-input v-model="selectedItem!.data.hour" style="width: 150px" />
      </el-form-item>
      <el-form-item label="Day">
        <el-input v-model="selectedItem!.data.day" style="width: 150px" />
      </el-form-item>
      <el-form-item label="Day of week">
        <el-input v-model="selectedItem!.data.day_of_week" style="width: 150px" />
      </el-form-item>
    </div>
    <div v-else-if="selectedItem!.type === 'date'">
      <el-form-item label="日期时间">
        <el-date-picker
          v-model="dateValue"
          type="datetime"
          placeholder="选择日期时间"
          format="YYYY-MM-DD HH:mm:ss"
          value-format="x"
          :shortcuts="shortcuts"
          style="width: 220px"
          @change="handleDateChange"
        />
      </el-form-item>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { watch, ref, onMounted } from 'vue'
import { useShareStatesStore } from '@/stores/UseShareStatesStore'

const { selectedItem } = storeToRefs(useShareStatesStore())
const dateValue = ref<number>()

// 添加 props 接收 isNewJob
const props = defineProps<{
  isNewJob: boolean
}>()

// 将日期对象转换为时间戳
const convertDateToTimestamp = (data: any) => {
  if (!data) return Date.now()
  
  const date = new Date(
    Number(data.year),
    Number(data.month) - 1, // 月份从0开始
    Number(data.day),
    Number(data.hour),
    Number(data.minute),
    Number(data.second)
  )
  return date.getTime()
}

// 监听 selectedItem 变化，更新日期选择器的值
watch(() => selectedItem.value, (newVal) => {
  if (newVal?.type === 'date' && newVal.data) {
    dateValue.value = convertDateToTimestamp(newVal.data)
  }
}, { immediate: true, deep: true })

// 处理日期变化
const handleDateChange = (val: number) => {
  if (!selectedItem.value || !val) return
  
  const date = new Date(val)
  selectedItem.value.data = {
    year: date.getFullYear(),
    month: date.getMonth() + 1,
    day: date.getDate(),
    hour: date.getHours(),
    minute: date.getMinutes(),
    second: date.getSeconds()
  }
}

// 快捷选项
const shortcuts = [
  {
    text: '今天',
    value: new Date()
  },
  {
    text: '明天',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() + 3600 * 1000 * 24)
      return date
    }
  },
  {
    text: '一周后',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() + 3600 * 1000 * 24 * 7)
      return date
    }
  }
]

// 监听类型变化
watch(() => selectedItem.value?.type, (newType) => {
  if (!selectedItem.value || !props.isNewJob) return
  
  if (newType === 'date') {
    const now = new Date()
    dateValue.value = now.getTime()
    selectedItem.value.data = {
      year: now.getFullYear(),
      month: now.getMonth() + 1,
      day: now.getDate(),
      hour: now.getHours(),
      minute: now.getMinutes(),
      second: now.getSeconds()
    }
  }
  // ... 其他类型的处理保持不变
})

// 组件挂载时初始化日期值
onMounted(() => {
  if (selectedItem.value?.type === 'date' && selectedItem.value.data) {
    dateValue.value = convertDateToTimestamp(selectedItem.value.data)
  }
})

</script>

<style lang="less" scoped>
.delay-input {
  width: 200px;
}

.not-last-input {
  padding-right: 10px;
}
</style>
