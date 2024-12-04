import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { IStubMapping } from '@/service/api/StubMappings'
import type { IJob } from '@/service/api/Jobs'

export const useShareStatesStore = defineStore('shareStatesStore', () => {
  // 切换项目管理页
  const isShowProjects = ref(false) //展示项目管理页，默认不展示

  // 当前项目信息
  const currentProjectId = ref('') //当前选中的项目 ID
  const currentMockUrl = ref('') //当前选中的项目 URL

  //  当前 job
  const selectedItem = ref<IJob>() //当前选中 job
  const selectedIndex = ref(0) //当前选中 job 的列表索引
  const currentJobID = ref('') //当前选中的 job ID
  const resetItem = ref<IJob>() //重置数据，即一开始加载的数据

  return {
    isShowProjects,
    currentProjectId,
    currentMockUrl,
    selectedItem,
    selectedIndex,
    currentJobID,
    resetItem
  }
})
