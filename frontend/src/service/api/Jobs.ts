import { httpSingle } from '@/lib/axios';


export interface IJob {
  job_id?: string,               // job ID
  name?: string,                 //job 名称
  next_run_time?: string,         // 下一次运行的时间
  request_url?: string,          // 请求的 URL 地址
  type: string,                  // 定时任务类型
  data: {
    day?: [string, number],
    day_of_week?: [string, number],
    hour?: [string, number],
    minute?: [string, number],
    month?: [string, number],
    second?: [string, number],
    week?: [string, number],
    year?: [string, number]
  }
}

export interface DJob {
  job_id?: string,            // job ID
  url?: string,               // 请求的 URL 地址
  year?: [string, number],
  month?: [string, number],
  day?: [string, number],
  hour?: [string, number],
  minute?: [string, number],
  second?: [string, number]
}

export interface CJob {
  job_id?: string,            // job ID
  url?: string,               // 请求的 URL 地址
  day_of_week?: [string, number],
  month?: [string, number],
  day?: [string, number],
  hour?: [string, number],
  minute?: [string, number],
  second?: [string, number]
}

export interface TJob {
  job_id?: string,            // job ID
  url?: string,               // 请求的 URL 地址
  hours?: [string, number],
  minutes?: [string, number],
  seconds?: [string, number]
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
  });
};

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
  });
};

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
  });
};

/**
 * 查询指定【 baseUrl 】jobs 列表数据
 * @param baseUrl
 * @returns {*}
 */
export const R_Jobs = (baseUrl: string) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/get_jobs`,
    method: 'get'
  });
};

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
  });
};

/**
 * 删除指定【 mockUrl 】中，指定【 jobID 】的 mapping 信息
 * @param baseUrl
 * @param jobID
 * @returns {*}
 */
export const D_Job = (baseUrl: string, jobID: string) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/remove_job?job_id=${jobID}`,
    method: 'delete'
  }); 
};
