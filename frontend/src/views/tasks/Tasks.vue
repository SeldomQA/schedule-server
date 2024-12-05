<template>
  <div class="stubs-list">
    <div>
      <!-- <tool-bar></tool-bar> -->
      <!-- 顶部工具栏 -->
      <el-row class="top-tools" justify="start">
        <el-form :inline="true" class="form-inline" size="small">
          <el-form-item>
            <el-input
              class="tools-filter"
              placeholder="根据 job ID 查询"
              clearable
              v-model="jobID"
              @clear="refreshListData"
              @keydown.enter.prevent
            >
              <template #append>
                <el-button :icon="Search" @click="getJobByID"></el-button>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button :icon="Plus" type="primary" @click="addJob">添加</el-button>
          </el-form-item>
          <el-form-item>
            <el-button :icon="Refresh" type="warning" @click="refreshListData">刷新</el-button>
          </el-form-item>
        </el-form>
      </el-row>

      <!-- 内容显示区 -->
      <!-- 无内容时显示 -->
      <div class="empty-data" v-if="!tableData.length">暂无数据，请先添加</div>
      <!-- 有内容时显示 -->
      <div v-else>
        <el-row>
          <!-- 左侧 Tasks 列表 -->
          <el-col :span="5" class="left-list">
            <!-- 分页信息及翻页功能 -->
            <el-row class="list-pagination" align="middle" justify="space-between">
              <div class="filter-options">
                <el-input
                  placeholder="当前数据中检索"
                  clearable
                  v-model="listFilter"
                  size="small"
                />
              </div>
            </el-row>
            <!-- 列表 -->
            <el-scrollbar class="list-content">
              <ul>
                <li
                  v-for="(item, index) in tableData"
                  :key="item.job_id || index"
                  @click="onClickListItem(item, index)"
                >
                  <div
                    :class="selectedIndex === index ? 'content-item select' : 'content-item'"
                    v-if="localSearch(item)"
                  >
                    <label class="first-line">
                      <span>{{ item.job_id }}</span>
                      <div class="status-flag">
                        <span v-if="isUnsave(item)" class="unsave-flag">
                          <el-icon><Edit /></el-icon>
                        </span>
                      </div>
                    </label>
                    <label class="second-line">
                      <el-tag size="small" :type="jobDataStyle('type')">
                        {{ item.type }}
                      </el-tag>
                    </label>
                  </div>
                </li>
              </ul>
            </el-scrollbar>
          </el-col>
          <!-- 右侧 job 详情 -->
          <el-col :span="19" class="right-detail" v-if="selectedItem">
            <!-- 操作栏 -->
            <div class="detail-tools">
              <!-- 操作按钮 -->
              <div class="switch-edit-view">
                <span
                  :class="isShowFormEdit ? 'switch-button is-active' : 'switch-button'"
                  @click="isShowFormEdit = true"
                  >编辑</span
                >
                <span
                  :class="!isShowFormEdit ? 'switch-button is-active' : 'switch-button'"
                  @click="isShowFormEdit = false"
                  >预览</span
                >
              </div>
              <el-form size="small" v-show="isShowFormEdit">
                <el-button
                  :icon="Finished"
                  type="primary"
                  @click="saveStubMapping"
                  v-if="isUnsave(selectedItem)"
                  >保存</el-button
                >
                <template v-if="JSON.stringify(selectedItem) !== JSON.stringify(resetItem)">
                  <el-popconfirm title="确定重置吗？" @confirm="resetStubMapping" width="150">
                    <template #reference>
                      <el-button :icon="RefreshLeft" type="warning">重置</el-button>
                    </template>
                  </el-popconfirm>
                </template>
                <el-popconfirm 
                  title="确定删除吗？" 
                  @confirm="deleteStubMappingByID" 
                  width="150"
                  v-if="!isNewJob"
                >
                  <template #reference>
                    <el-button :icon="Delete" type="danger">删除</el-button>
                  </template>
                </el-popconfirm>
              </el-form>
            </div>
            <!-- Form Edit/JSON View 切换 -->
            <el-scrollbar class="detail-tab">
              <!-- Form Edit -->
              <el-form
                class="detail-info"
                :model="selectedItem"
                ref="selectedItemRef"
                label-width="120px"
                label-position="left"
                v-show="isShowFormEdit"
                size="default"
              >
                <el-collapse v-model="activeCollapseNames">
                  <!-- 基本信息：名称、优先级、场景、启用禁用、元数据 -->
                  <el-collapse-item name="General">
                    <template #title>
                      <b>基本信息</b>
                    </template>
                    <general-info 
                      :is-new-job="isNewJob"
                      :key="String(isNewJob)"
                    ></general-info>
                  </el-collapse-item>
                  <!-- timed -->
                  <el-collapse-item name="Timed">
                    <template #title>
                      <b>定时信息</b>
                    </template>
                    <timed-data :is-new-job="isNewJob" :create-empty-job="createEmptyJob"></timed-data>
                  </el-collapse-item>
                </el-collapse>
              </el-form>
              <!-- JSON View -->
              <div class="detail-preview" v-show="!isShowFormEdit">
                <json-viewer
                  :value="selectedItemView"
                  :copyable="{ copyText: '复制', copiedText: '已复制' }"
                  :expand-depth="10"
                ></json-viewer>
              </div>
            </el-scrollbar>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import baseUrl from '@/config/base-url'

import { storeToRefs } from 'pinia'
import { onBeforeMount, onMounted, ref, watch, nextTick } from 'vue'
import { computed } from 'vue'
import {
  Search,
  Plus,
  Refresh,
  RefreshLeft,
  Finished,
  Delete,
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type Action } from 'element-plus'

import { isEmpty, cloneJson } from '@/lib/helper'
import { ErrorHandler } from '@/lib/axios'
import { useShareStatesStore } from '@/stores/UseShareStatesStore'
import {
  R_Job,
  C_DateJob,
  C_CronJob,
  C_IntervalJob,
  D_Job,
  R_Jobs
} from '@/service/api/Jobs'
import type { IJob, DJob, CJob, TJob } from '@/service/api/Jobs'
import type {
  DateJobData,
  CronJobData,
  IntervalJobData
} from '@/service/api/Jobs'

import { jobDataStyle } from '@/service/render/style'

import GeneralInfo from './GeneralInfo.vue'
import TimedData from './TimedData.vue'

const { currentMockUrl, selectedItem, selectedIndex, resetItem } =
  storeToRefs(useShareStatesStore())
const tableData = ref<IJob[]>([])
const pageNum = ref(1)
const pageSize = ref(10)

onMounted(() => {
  console.log('--->', selectedItem)
})

// 创建不同类型的空 Job
const createEmptyJob = (type: 'interval' | 'date' | 'cron' = 'interval'): IJob => {
  const timestamp = Date.parse(new Date().toString())
  const baseJob = {
    job_id: 'job_' + timestamp,
    type: type,
    name: 'requests_url',
    request_url: 'https://httpbin.org/get?id=1',
    next_run_time: ''
  }

  // 根据类型设置不同的默认数据
  switch (type) {
    case 'interval':
      return {
        ...baseJob,
        data: {
          hour: 0,
          minute: 10,
          second: 0
        }
      }
    case 'cron':
      return {
        ...baseJob,
        data: {
          year: '*',
          month: '*',
          day: '*',
          week: '*',
          day_of_week: '*',
          hour: '*',
          minute: '*',
          second: '*'
        }
      }
    case 'date':
      const now = new Date()
      return {
        ...baseJob,
        data: {
          year: now.getFullYear(),
          month: now.getMonth() + 1,
          day: now.getDate(),
          hour: now.getHours(),
          minute: now.getMinutes(),
          second: now.getSeconds()
        }
      }
  }
}

// 修改数据处理部分
const processJobData = (item: IJob) => {
  const baseItem = {
    job_id: item.job_id || '',
    type: item.type || 'date',
    name: item.name || '',
    request_url: item.request_url || '',
    next_run_time: item.next_run_time || ''
  }

  if (item.type === 'cron') {
    const cronData = item.data as CronJobData
    return {
      ...baseItem,
      data: {
        year: cronData.year || '*',
        month: cronData.month || '*',
        day: cronData.day || '*',
        week: cronData.week || '*',
        day_of_week: cronData.day_of_week || '*',
        hour: cronData.hour || '*',
        minute: cronData.minute || '*',
        second: cronData.second || '*'
      }
    }
  } else if (item.type === 'date') {
    const dateData = item.data as DateJobData
    return {
      ...baseItem,
      data: {
        year: Number(dateData.year) || 0,
        month: Number(dateData.month) || 0,
        day: Number(dateData.day) || 0,
        hour: Number(dateData.hour) || 0,
        minute: Number(dateData.minute) || 0,
        second: Number(dateData.second) || 0
      }
    }
  } else {
    const intervalData = item.data as IntervalJobData
    return {
      ...baseItem,
      data: {
        hour: Number(intervalData.hour) || 0,
        minute: Number(intervalData.minute) || 0,
        second: Number(intervalData.second) || 0
      }
    }
  }
}

const getTasksJobs = async (isUserAction: boolean) => {
  try {
    const res = await R_Jobs(baseUrl)
    const taskList = res?.data?.task_list || []
    
    tableData.value = taskList.map(processJobData)

    total.value = res?.data?.total || 0
    
    if (tableData.value.length > 0) {
      selectedItem.value = tableData.value[0]
      selectedIndex.value = 0
      resetItem.value = cloneJson(selectedItem.value)
    } else {
      selectedItem.value = createEmptyJob()
      selectedIndex.value = -1
      resetItem.value = createEmptyJob()
    }

    isShowFormEdit.value = true

    if (isUserAction) {
      ElMessage({
        type: 'success',
        message: '刷新成功'
      })
    }
  } catch (err) {
    tableData.value = [] // 错误时设置为空数组而不是 undefined
    total.value = 0
    selectedItem.value = createEmptyJob()
    selectedIndex.value = -1
    ErrorHandler.create(err).end()
  }
}

// ###### 页面加载和监 ######

onBeforeMount(() => {
  if (!isEmpty(currentMockUrl.value)) {
    getTasksJobs(false)
  }
})

onMounted(() => {
  getTasksJobs(true)
})

watch(currentMockUrl, (newValue, oldValue) => {
  if (currentMockUrl.value) {
    getTasksJobs(false)
  } else {
    tableData.value = []
  }
})

// ###### 1. 顶部工具栏 ######
const dialogRecordFormVisible = ref(false)
const jobID = ref('')
const total = ref(0)

/**
 * 当每页条数改变或点击刷新按钮时重新查询
 */
const refreshListData = () => {
  pageNum.value = 1
  saveItemBeforeNextAction().then(async (action: Action) => {
    if (action === 'confirm' || action === 'cancel') {
      if (jobID.value) {
        getJobByID()
      } else {
        await getTasksJobs(true)
        if (tableData.value.length) switchSelectedItem(0)
      }
    }
  })
}

/**
 * 根据 job ID 查询
 */
const getJobByID = async () => {
  if (isEmpty(jobID.value)) {
    ElMessage({ type: 'warning', message: '请输入 Job 的 ID' })
    return
  }

  try {
    const res = await R_Job(baseUrl, jobID.value)
    const taskList = res?.data?.task_list || []
    
    tableData.value = taskList.map(processJobData)

    total.value = res?.data?.total || 0
    
    if (tableData.value.length > 0) {
      selectedItem.value = tableData.value[0]
      selectedIndex.value = 0
      resetItem.value = cloneJson(selectedItem.value)
    } else {
      selectedItem.value = createEmptyJob()
      selectedIndex.value = -1
      resetItem.value = createEmptyJob()
    }

    isShowFormEdit.value = true
    
    ElMessage({
      type: 'success',
      message: '刷新成功'
    })
  } catch (err) {
    tableData.value = [] // 错误时设置为空数组而不是 undefined
    total.value = 0
    selectedItem.value = createEmptyJob()
    selectedIndex.value = -1
    
    ErrorHandler.create(err)
      .handle(err => {
        if (err.response && err.response.status === 404) {
          ElMessage({ type: 'warning', message: '不存在该 job ID ' })
          return true
        }
        return false
      })
      .end()
  }
}

/**
 * 添加一个默认 job 到列表（未保存）
 */
const addJob = () => {
  if (tableData.value.length && !tableData.value[0].job_id) return
  
  // 创建一个 interval 类型的新 job
  const item = createEmptyJob('interval')
  
  isNewJob.value = true
  tableData.value.unshift(item)
  switchSelectedItem(0)
  nextTick(() => {
    isNewJob.value = true
  })
}

// ###### 2. 左侧列表 ######

/**
 * 判断当前选中项是否有修改未保存
 * @param item 当前选中项
 */
const isUnsave = computed(() => (item: IJob) => {
  // 如果是新增的 job，只有当前选中的 item 才显示保存按钮
  if (isNewJob.value) {
    return selectedItem.value === item
  }
  
  // 对于已有的 job，只有当内容发生变化时才显示保存按钮
  return (
    (selectedItem.value === item &&
      JSON.stringify(selectedItem.value) !== JSON.stringify(resetItem.value))
  )
})

/**
 * 本地搜索，筛选列表中符合查询条件的列表项。
 *
 * 如果参数符合查条件，则返回 true。
 *
 * @param item 当前列表项数据
 */
const listFilter = ref('')
const localSearch = (item: any) => {
  // TODO 语法搜索，如 title:客服介入 && urL:/abc/dwew
  return (
    !listFilter.value ||
    (item.name || '').indexOf(listFilter.value) !== -1 ||
    (item.url || '').indexOf(listFilter.value) !== -1
  )
}

/**
 * 点击列表项
 * @param item 被选中的列表项
 * @param index 被选中的列表项索引
 */
const onClickListItem = (item: IJob, index: number) => {
  console.log('switch', item)
  if (selectedItem && selectedItem.value === tableData.value[index]) {
    return
  }

  let removeFirst = false
  if (!tableData.value[0].job_id) {
    console.log('removeFirst==true')
    removeFirst = true
  }
  saveItemBeforeNextAction().then((action: Action) => {
    console.log("action", action)
    if (action === 'confirm' || action === 'cancel') {
      switchSelectedItem(removeFirst && action === 'cancel' ? --index : index)
    }
  })
}

// ###### 3. 右侧详情页 ######
const isShowFormEdit = ref(true)

// 3.1 表单编辑
const activeCollapseNames = ref(['General', 'Timed'])

// 修改类型定义部分
interface JobData {
  year?: number
  month?: number
  day?: number
  hour?: number
  minute?: number
  second?: number
  day_of_week?: string
}

/**
 * 保存按钮：创建或更新 StubMapping
 */
const saveStubMapping = () => {
  if (!selectedItem.value) {
    return
  }
  console.log('ss')

  if (selectedItem.value.job_id) {
    if (selectedItem.value.type === 'date') {
      const data = selectedItem.value.data as JobData
      const myJob: DJob = {
        job_id: selectedItem.value.job_id ?? '',
        url: selectedItem.value.request_url ?? '',
        year: Number(data.year) || 0,
        month: Number(data.month) || 0,
        day: Number(data.day) || 0,
        hour: Number(data.hour) || 0,
        minute: Number(data.minute) || 0,
        second: Number(data.second) || 0
      }

      C_DateJob(baseUrl, myJob)
        .then((res: any) => {
          getTasksJobs(false)
        })
        .catch(err => {
          ErrorHandler.create(err).end()
        })
    } else if (selectedItem.value.type === 'cron') {
      const data = selectedItem.value.data as JobData
      const myJob: CJob = {
        job_id: selectedItem.value.job_id ?? '',
        url: selectedItem.value.request_url ?? '',
        day_of_week: String(data.day_of_week) || '*',
        month: String(data.month) || '*',
        day: String(data.day) || '*',
        hour: String(data.hour) || '*',
        minute: String(data.minute) || '*',
        second: String(data.second) || '*'
      }

      C_CronJob(baseUrl, myJob)
        .then((res: any) => {
          getTasksJobs(false)
        })
        .catch(err => {
          ErrorHandler.create(err).end()
        })
    } else if (selectedItem.value.type === 'interval') {
      const data = selectedItem.value.data as JobData
      const myJob: TJob = {
        job_id: selectedItem.value.job_id ?? '',
        url: selectedItem.value.request_url ?? '',
        hours: Number(data.hour) || 0,
        minutes: Number(data.minute) || 0,
        seconds: Number(data.second) || 0
      }

      C_IntervalJob(baseUrl, myJob)
        .then((res: any) => {
          getTasksJobs(false)
        })
        .catch(err => {
          ErrorHandler.create(err).end()
        })
    }
    return
  }
}

/**
 * 重置当前选中项，数据回滚到编辑前的数据
 */
const resetStubMapping = () => {
  if (JSON.stringify(selectedItem.value) === JSON.stringify(resetItem.value)) {
    ElMessage({ type: 'success', message: '数据未变更，无需重置' })
    return
  }
  tableData.value[selectedIndex.value] = cloneJson(resetItem.value)
  switchSelectedItem(selectedIndex.value)
}

/**
 * 删除当前选中的 StubMapping。
 *
 * 如果是草稿项，直接移除；否则根据 ID 删除。
 */
const deleteStubMappingByID = () => {
  if (!selectedItem.value) {
    return
  }

  if (!selectedItem.value.job_id) {
    tableData.value.shift()
    switchSelectedItem(0)
  } else {
    D_Job(baseUrl, selectedItem.value.job_id)
      .then(() => {
        ElMessage({ type: 'success', message: '删除成功' })
        getTasksJobs(false)
      })
      .catch(err => {
        ErrorHandler.create(err).end()
      })
  }
}


// 3.2 JSON 预览
const selectedItemView = computed(() => {
  // const clonedItem = JSON.parse(JSON.stringify(selectedItem.value))
  // return renderDataToApiData(clonedItem)
})

// ###### 辅助方法 ######

const saveItemBeforeNextAction = async (): Promise<Action> => {
  if (
    !tableData.value.length ||
    (tableData.value[0].job_id &&
      JSON.stringify(selectedItem.value) === JSON.stringify(resetItem.value))
  ) {
    return 'confirm' as Action
  }

  let userAction!: Action
  await ElMessageBox.confirm('您有 Job 未保存，是否先保存？', '提示', {
    confirmButtonText: '保存',
    cancelButtonText: '放弃',
    type: 'warning',
    distinguishCancelAndClose: true
  })
    .then(async () => {
      // 保存修改
      userAction = 'confirm' as Action

      if (!selectedItem.value) {
        return
      }

      // 如果是添加未保存的数据
      if (selectedItem.value.job_id) {
        console.log('s', selectedItem.value.job_id)
        console.log('s', selectedItem.value.type)
        if (selectedItem.value.type === 'date') {
          const data = selectedItem.value.data as JobData
          const myJob: DJob = {
            job_id: selectedItem.value.job_id ?? '',
            url: selectedItem.value.request_url ?? '',
            year: Number(data.year) || 0,
            month: Number(data.month) || 0,
            day: Number(data.day) || 0,
            hour: Number(data.hour) || 0,
            minute: Number(data.minute) || 0,
            second: Number(data.second) || 0
          }
          await C_DateJob(baseUrl, myJob).catch((err: Error) => {
            ErrorHandler.create(err).end()
          })
        } else if (selectedItem.value.type === 'cron') {
          const data = selectedItem.value.data as JobData
          const myJob: CJob = {
            job_id: selectedItem.value.job_id ?? '',
            url: selectedItem.value.request_url ?? '',
            day_of_week: String(data.day_of_week) || '*',
            month: String(data.month) || '*',
            day: String(data.day) || '*',
            hour: String(data.hour) || '*',
            minute: String(data.minute) || '*',
            second: String(data.second) || '*'
          }
          await C_CronJob(baseUrl, myJob).catch((err: Error) => {
            ErrorHandler.create(err).end()
          })
        } else if (selectedItem.value.type === 'interval') {
          const data = selectedItem.value.data as JobData
          const myJob: TJob = {
            job_id: selectedItem.value.job_id ?? '',
            url: selectedItem.value.request_url ?? '',
            hours: Number(data.hour) || 0,
            minutes: Number(data.minute) || 0,
            seconds: Number(data.second) || 0
          }
          await C_IntervalJob(baseUrl, myJob).catch((err: Error) => {
            ErrorHandler.create(err).end()
          })
        }
        await getTasksJobs(false)
        return
      }

      // 如果是修改未保存的数据
      if (JSON.stringify(selectedItem.value) !== JSON.stringify(resetItem.value)) {
        // 根据任务类型调用相应的更新接口
        // 注意: 这里需要根据实际的 API 接口实现更新逻辑
        await getTasksJobs(false)
        return
      }
    })
    .catch((action: Action) => {
      // 放弃修改或关闭弹
      userAction = action
      if (action === 'cancel') {
        if (!tableData.value[0].job_id) {
          tableData.value.shift()
        } else {
          tableData.value[selectedIndex.value] = cloneJson(resetItem.value)
        }
      }
    })
  return Promise.resolve(userAction)
}

// 切换选中项
const switchSelectedItem = (nextIndex: number) => {
  // 如果不是切换到新增的 job，就重置 isNewJob
  if (tableData.value[nextIndex]?.job_id !== tableData.value[0]?.job_id || !isNewJob.value) {
    isNewJob.value = false
  }
  selectedItem.value = tableData.value[nextIndex]
  selectedIndex.value = nextIndex
  resetItem.value = cloneJson(selectedItem.value)
}

// 添加一个 ref 来标识是否是增的 job
const isNewJob = ref(false)
</script>

<style lang="less" scoped>
:deep(.el-scrollbar__bar) {
  height: 0 !important;
  width: 0 !important;
}

//改变默认输入框样式
.filter-options {
  :deep(:focus-visible) {
    outline: -webkit-focus-ring-color auto 0px;
  }

  :deep(.el-input__wrapper) {
    // background-color: #2c3e50;
    box-shadow: none;
  }

  :deep(.el-select:hover:not(.el-select--disabled) .el-input__wrapper) {
    box-shadow: none;
  }

  :deep(.el-input__inner) {
    color: black;
  }
}

// 顶部工具栏
.top-tools {
  padding: 8px 20px;
  text-align: left;

  .total-num {
    color: #0fb2ef;
    font-weight: bold;
  }

  .tools-filter {
    width: 300px;
    margin-right: 8px;
  }

  .form-inline {
    .el-form-item {
      margin-bottom: 0;
      margin-right: 15px;
    }
  }
}

// 左侧列表
.left-list {
  text-align: left;
  margin: 0px;
  padding: 0px;
  padding-left: 10px;

  // 分页
  .list-pagination {
    display: flex;
    // margin-bottom: 8px;
    // height: 20px;

    .pagination {
      display: flex;
      justify-content: end;
    }

    .pagination-tip {
      // float: left;
      font-size: 12px;
      line-height: 24px;
      color: gray;
      padding-left: 2px;
    }
  }

  // 列表内容
  .list-content {
    height: calc(100vh - 110px);
    width: 100%;
    padding: 0;
    margin: 0;
    border: 1px solid #dfdfdf;
    font-size: 0;
    float: left;

    ul {
      padding-left: 0px;
    }

    .status-flag {
      padding-left: 10px;
      text-align: center;

      .disable-flag {
        color: gray;
        padding-left: 3px;
      }

      .unsave-flag {
        padding-left: 3px;
        color: rgb(235, 101, 101);
        height: 20px;
        display: inline-block;
        vertical-align: middle;
        text-align: center;
        line-height: 26px;
        font-size: 20px;
      }
    }

    .content-item {
      list-style-type: none;
      padding: 0 20px;
      border-bottom: 1px solid #dfdfdf;

      cursor: pointer;

      label {
        display: block;
        font-size: 14px;
        word-break: break-all;
        word-wrap: break-word;
        cursor: pointer;
      }

      .first-line {
        font-weight: bold;
        color: #2c3e50d9;
        padding-top: 8px;
        display: flex;
        justify-content: space-between;
      }

      .second-line {
        padding: 10px 0;

        .item-url {
          padding: 0 10px;
          color: #2c3e50d9;
        }
      }

      .third-line {
        padding-bottom: 8px;
      }
    }

    .content-item:hover {
      background: #d0d0d040;
    }
  }

  .select {
    border-left: 2px solid #0fb2ef;
    // margin-left: 1px;
  }
}

// 右侧选中item详细信息
.right-detail {
  padding: 0 20px;

  // 功能栏
  .detail-tools {
    display: flex;
    justify-content: space-between;
    height: 30px;

    .switch-edit-view {
      margin-left: 20px;
      display: flex;
      align-items: flex-end;

      .switch-button {
        cursor: pointer;
        display: inline;
        vertical-align: bottom;
        margin-right: 5px;
        height: 24px;
        color: #0fb2ef;
        font-size: 14px;
      }

      .switch-button.is-active {
        height: 22px;
        color: #f59121;
        border-bottom: 2px solid #f59121;
      }
    }
  }

  .el-scrollbar {
    height: calc(100vh - 117px);
    width: 100%;
  }

  // 切换tab
  .detail-tab {
    .detail-info {
      padding-left: 20px;
    }
  }

  .jv-code {
    max-height: none !important;
  }

  .json-detail {
    overflow: scroll;
    height: 72vh;
    padding: 15px;
    margin: 0;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    border: 1px solid #dcdfe6;
    -webkit-box-shadow:
      0 2px 4px 0 rgba(0, 0, 0, 0.12),
      0 0 6px 0 rgba(0, 0, 0, 0.04);
    box-shadow:
      0 2px 4px 0 rgba(0, 0, 0, 0.12),
      0 0 6px 0 rgba(0, 0, 0, 0.04);

    .jv-more {
      display: none;
    }
  }
}

.empty-data {
  color: grey;
  display: flex;
  justify-content: center;
  margin-top: 40px;
  height: 89vh;
}
</style>
