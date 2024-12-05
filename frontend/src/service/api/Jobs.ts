import { httpSingle } from '@/lib/axios'

// 定义不同类型任务的数据结构
export interface DateJobData {
  year: number
  month: number
  day: number
  hour: number
  minute: number
  second: number
}

export interface CronJobData {
  year: string | number
  month: string | number
  day: string | number
  week?: string
  day_of_week: string
  hour: string | number
  minute: string | number
  second: string | number
}

export interface IntervalJobData {
  hour: number
  minute: number
  second: number
}

// 主接口定义
export interface IJob {
  job_id: string
  name: string
  type: 'date' | 'cron' | 'interval'
  request_url: string
  next_run_time: string
  status: string
  data: DateJobData | CronJobData | IntervalJobData
}

// API 请求参数接口定义
export interface DJob {
  job_id?: string
  url?: string
  year: number
  month: number
  day: number
  hour: number
  minute: number
  second: number
}

export interface CJob {
  job_id?: string
  url?: string
  day_of_week: string
  month: string
  day: string
  hour: string
  minute: string
  second: string
}

export interface TJob {
  job_id?: string
  url?: string
  hours: number
  minutes: number
  seconds: number
}

/**
 * 指定【 baseUrl 】新增 date定时任务
 * @param mockUrl
 * @param params
 * @returns {*}
 */
export const C_DateJob = (baseUrl: string, params: DJob) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/date/add_job`,
    method: 'post',
    data: params
  })
}

/**
 * 指定【 baseUrl 】新增 cron定时任务
 * @param baseUrl
 * @param params
 * @returns {*}
 */
export const C_CronJob = (baseUrl: string, params: CJob) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/cron/add_job`,
    method: 'post',
    data: params
  })
}

/**
 * 指定【 baseUrl 】新增 interval定时任务
 * @param baseUrl
 * @param params
 * @returns {*}
 */
export const C_IntervalJob = (baseUrl: string, params: TJob) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/interval/add_job`,
    method: 'post',
    data: params
  })
}

/**
 * 查询指定【 baseUrl 】jobs 列表数据
 * @param baseUrl
 * @returns {*}
 */
export const R_Jobs = (baseUrl: string) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/get_jobs`,
    method: 'get'
  })
}

/**
 * 查询指定【 baseUrl 】中，指定【 jobID 】的 mapping 信息
 * @param baseUrl
 * @param jobID
 * @returns {*}
 */
export const R_Job = (baseUrl: string, jobID: string) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/get_jobs?job_id=${jobID}`,
    method: 'get'
  })
}

/**
 * 删除指定【 baseUrl 】中，指定【 jobID 】的 mapping 信息
 * @param baseUrl
 * @param jobID
 * @returns {*}
 */
export const D_Job = (baseUrl: string, jobID: string) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/remove_job?job_id=${jobID}`,
    method: 'delete'
  })
}

/**
 * 暂停指定【 baseUrl 】中，指定【 jobID 】的 mapping 信息
 * @param baseUrl
 * @param jobID
 * @returns {*}
 */
export const Pause_Job = (baseUrl: string, jobID: string) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/pause_job?job_id=${jobID}`,
    method: 'put'
  })
}

/**
 * 回复指定【 baseUrl 】中，指定【 jobID 】的 mapping 信息
 * @param baseUrl
 * @param jobID
 * @returns {*}
 */
export const Resume_Job = (baseUrl: string, jobID: string) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/resume_job?job_id=${jobID}`,
    method: 'put'
  })
}
