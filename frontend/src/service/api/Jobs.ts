import { httpSingle } from '@/lib/axios';

// <predicate> 可选值：
// 1. equalTo           相等
//    [case1] { "equalTo": "WireMock" }                                       //默认区分大小写
//    [case2] { "equalTo": "application/json", "caseInsensitive": true }      //不区分大小写
// 
// 2. binaryEqualTo     二进制相等（转换为 Base64 比较），用于匹配非纯文本，比如字节流、对象、文件
//    [case1] { "binaryEqualTo" : "AQID" }                                    //new byte[] { 1, 2, 3 }
// 
// 3. contains          包含
//    [case1] { "contains": "johnsmith@example.com" }
// 
// 4. doesNotContain    不包含
//    [case1] { "doesNotContain": "johnsmith@example.com" }
// 
// 5. matches           正则匹配
//    [case1] { "matches": ".*12345.*" }
// 
// 6. doesNotMatch      反向正则匹配，当值不匹配正则表达式时匹配成功
//    [case1] { "doesNotMatch" : "^(.*)wiremock([A-Za-z]+)$" }
// 
// 7. equalToJson       相等（JSON）
//    [case1] { "equalToJson": { "total_results": 4 } }       //JSONObject 形式
//    [case2] { "equalToJson": "{ \"total_results\": 4 }" }   //JSON 字面量形式
//    [case3] { "equalToJson": "{ \"total_results\": 4  }", "ignoreArrayOrder": true, "ignoreExtraElements": true }   //额外控制选项，选项默认都是 false
//    [case4] { "equalToJson": { "id": "${json-unit.any-string}" } }    //JSON Unit 占位符，{ "id": "abc123" } 匹配成功
// 
// 8. matchesJsonPath   JSON Path
//    ### Direct JSONPath ###
//    [case1] { "matchesJsonPath": "$.name" }
//            匹配成功：{ "name": "Wiremock" }
//            匹配失败：{ "price": 15 } 
//    [case2] { "matchesJsonPath" : "$.things[?(@.name == 'RequiredThing')]" }  
//            匹配成功：{ "things": { "name": "RequiredThing" } }
//                     { "things": [ { "name": "RequiredThing" }, { "name": "Wiremock" } ] } 
//            匹配失败：{ "price": 15 }
//                     { "things": { "name": "Wiremock" } } 
//    [case3] { "matchesJsonPath" : "$.things[?(@.name =~ /Required.*/i)]" }
//            匹配成功：{ "things": { "name": "RequiredThing" } }
//                     { "things": [ { "name": "Required" }, { "name": "Wiremock" } ] } 
//            匹配失败：{ "price": 15 }
//                     { "things": { "name": "Wiremock" } }
//                     { "things": [ { "name": "Thing" }, { "name": "Wiremock" } ] } 
//    [case4] { "matchesJsonPath" : "$[?(@.things.size() == 2)]" }
//            匹配成功：{ "things": [ { "name": "RequiredThing" }, { "name": "Wiremock" } ] }
//            匹配失败：{ "things": [ { "name": "RequiredThing" } ] } 
//    ### Nested Match ###
//    [case5]   contains
//              { "matchesJsonPath": { "expression": "$..todoItem", "contains": "wash" } }
//    [case6]   equalToJson
//              { "matchesJsonPath": { "expression": "$.outer", "equalToJson": "{ \"inner\": 42 }"} }
//    [case7]   equalTo
//              {expression: "$.data.id", equalTo: "xxxyyy"}}
//    [case8]   contains
//              {expression: "$.data.id", contains: "xx"}}
//    [case9]   matches          
//              {expression: "$.data.id", matches: "/x{3}/"}}
//    [case10]  doesNotMatch     
//              {expression: "ee", doesNotMatch: "/x{4}/"}}
//    [case11]  absent           
//              {expression: "ee", absent: true}
//    [case12] after
//            {
//              "matchesJsonPath": {
//                "expression": "$.completedDate",
//                "after": "now +15 days",
//                "truncateExpected": "first day of month"
//              }
//            }
//    [case13] equalToDateTime
//            {
//              "matchesJsonPath": {
//                  "expression": "$.completedDate",
//                  "equalToDateTime": "2020-03-01T00:00:00Z",
//                  "truncateActual": "first day of month"
//              }
//            }
//    [case14] and
//           {
//             "matchesJsonPath": {
//                 "expression": "$.date",
//                 "and": [
//                     { "before": "2022-01-01T00:00:00" },
//                     { "after": "2020-01-01T00:00:00" }
//                 ]
//             }
//           }
// 
// 9. equalToXml       相等（XML）
//    [case1] { "equalToXml": "<thing>Hello</thing>" }
//    [case2] { "equalToXml": "<message><id>${xmlunit.ignore}</id><content>Hello</content></message>", "enablePlaceholders": true }  //XMLUnit 占位符
//            匹配成功：<message><id>123456</id><content>Hello</content></message>
//    [case3] { "equalToXml": "<message><id>[[xmlunit.ignore]]</id><content>Hello</content></message>", "enablePlaceholders": true, 
//            "placeholderOpeningDelimiterRegex": "\\[\\[", "placeholderClosingDelimiterRegex": "]]" }                               //使用自定义 delimiters
//    [case4] { "equalToXml": "<thing>Hello</thing>", "exemptedComparisons": ["NAMESPACE_URI", "ELEMENT_TAG_NAME"] }                 //忽视指定的比较类型
//            完整的类型列表如下：
//            ELEMENT_TAG_NAME SCHEMA_LOCATION NO_NAMESPACE_SCHEMA_LOCATION NODE_TYPE NAMESPACE_URI TEXT_VALUE PROCESSING_INSTRUCTION_TARGET
//            PROCESSING_INSTRUCTION_DATA ELEMENT_NUM_ATTRIBUTES ATTR_VALUE CHILD_NODELIST_LENGTH CHILD_LOOKUP ATTR_NAME_LOOKUP
// 
// 10. matchesXPath      XPath
//    ### Direct XPath ###
//    [case1] { "matchesXPath": "/todo-list[count(todo-item) = 3]" }
//    [case2] //基于 namespace
//            {
//              "matchesXPath" : "/stuff:outer/more:inner[.=111]",
//              "xPathNamespaces" : {
//                "stuff" : "http://stuff.example.com",
//                "more"  : "http://more.example.com"
//              }
//            }
//    ### Nested Match ###
//    [case3] contains
//           {
//             "matchesXPath" : {
//               "expression": "//todo-item/text()",
//               "contains": "wash"
//             }
//           }
//    [case4] equalToXml
//           {
//             "matchesXPath" : {
//                "expression": "//todo-item",
//                "equalToXml": "<todo-item>Do the washing</todo-item>"
//             }
//           }
// 
// 11. absent        缺失该属性
//    [case1] { "absent": true }
// 
// 12. before       在某个时间之前
//    [case1] { "before": "now +3 days" }
//    [case2] {
//                // This is equivalent to "now +2 months"
//                "before": "now",
//                "expectedOffset": 2,
//                "expectedOffsetUnit": "months"
//            }
// 
// 
// 13. after        在某个时间之后
//    [case1] { "after": "2021-05-01T00:00:00Z" }
//    [case2] { "after": "now +15 days", "truncateExpected": "first day of month" }
// 
// 
// 14. equalToDateTime
//    [case1] { "equalToDateTime": "2021-06-24T00:00:00", "actualFormat": "dd/MM/yyyy" }
//    [case2] { "equalToDateTime": "2020-03-01T00:00:00Z", "truncateActual": "first day of month" }
//    [truncateActual - full list] first minute of hour
//                first hour of day
//                first day of month
//                first day of next month
//                last day of month
//                first day of year
//                first day of next year
//                last day of year
// 
// 15. and
//      [case1] {
//                 "and": [
//                     { "matches": "[a-z]+" },
//                     { "contains": "magicvalue" }
//                 ]
//               }
//      [case2] {
//                 "and": [
//                     { "before": "2022-01-01T00:00:00" },
//                     { "after": "2020-01-01T00:00:00" }
//                 ]
//              }
// 
// 
// 16. or
//      [case1] {
//                "or": [
//                    { "matches": "[a-z]+" },
//                    { "absent": true }
//                ]
//              }
// 
// 
// 17. hasExactly（queryParameters/headers） 多值参数，准确匹配预定规则且不包含其他值，顺序不影响
//    [case1] ?id=1&id=2&id=3 或者 ?id=2&id=3&id=1 或者 多个 id Header
//            了解多值 Param 和多值 Header：https://www.cnblogs.com/hochan100/p/14924316.html
//            {
//              "hasExactly": [
//                { "equalTo": "1" },
//                { "equalTo": "2" },
//                { "equalTo": "3" }
//              ]
//            }
//    [case2] ?id=1&id=xx2yy&id=12456
//            {
//              "hasExactly": [
//                { "equalTo": "1" },
//                { "contains": "2" },
//                { "doesNotContain": "3" }
//              ]
//            }
// 
// 18. includes（queryParameters/headers） 多值参数，包含匹配预定规则，可以包含其他值，顺序不影响
//      [case1] ?id=1&id=2&id=3&id=4&id=5
//             {
//               "includes": [
//                 { "equalTo": "1" },
//                 { "equalTo": "2" },
//                 { "equalTo": "3" }
//               ]
//             }
//      [case2] ?id=1&id=223&id=abc&id=000
//             {
//               "includes": [
//                 { "equalTo": "1" },
//                 { "contains": "2" },
//                 { "doesNotContain": "3" }
//               ]
//             }


// fault 可选值：
// EMPTY_RESPONSE               不发送响应数据，直接关闭 socket 连接。
//                              Postman 错误信息：socket hang up
// RANDOM_DATA_THEN_CLOSE       发送非法响应数据，然后关闭 socket 连接。
//                              Postman 错误信息：Parse Error: Expected HTTP/
// MALFORMED_RESPONSE_CHUNK     发送 200 状态码和非法响应数据，然后关闭 socket 连接。
//                              Postman 错误信息：Parse Error: Invalid character in chunk size
// CONNECTION_RESET_BY_PEER     Peer connection reset
//                              Postman 错误信息：read ECONNRESET

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

/**
 * 指定【 mockUrl 】新增 mapping
 * @param mockUrl
 * @param params
 * @returns {*}
 */
export const C_Mapping = (mockUrl: string, params: IJob) => {
  return httpSingle({
    url: `${mockUrl}/__admin/mappings`,
    method: 'post',
    data: params
  });
};

/**
 * 修改指定【 mockUrl 】中，指定【 mappingUUID 】的 mapping 信息
 * @param mockUrl
 * @param mappingUUID
 * @param params
 * @returns {*}
 */
export const U_Mapping = (mockUrl: string, mappingUUID: string, params: IJob) => {
  return httpSingle({
    url: `${mockUrl}/__admin/mappings/${mappingUUID}`,
    method: 'put',
    data: params
  });
};

/**
 * 查询指定【 mockUrl 】mapping 列表数据
 * 
 * 查询结果为 [offset, offset + limit -1]
 * 
 * @param mockUrl
 * @param params
 * @returns {*}
 */
interface ISearchOptions {
  offset: number,         //开始索引，从 0 开始，包括 0
  limit: number           //查询数量
}
export const R_Mappings = (mockUrl: string, params: ISearchOptions) => {
  return httpSingle({
    url: `${mockUrl}/__admin/mappings`,
    method: 'get',
    params: params
  });
};

/**
 * 查询指定【 baseUrl 】jobs 列表数据
 * 
 * 
 * @param baseUrl
 * @returns {*}
 */
export const GetJobs = (baseUrl: string) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/get_jobs`,
    method: 'get'
  });
};


/**
 * 查询指定【 mockUrl 】中，指定【 mappingUUID 】的 mapping 信息
 * @param mockUrl
 * @param jobID
 * @returns {*}
 */
export const R_Mapping = (baseUrl: string, jobID: string) => {
  return httpSingle({
    url: `${baseUrl}/scheduler/get_jobs?job_id=${jobID}`,
    method: 'get'
  });
};

/**
 * 删除指定【 mockUrl 】中，指定【 mappingUUID 】的 mapping 信息
 * @param mockUrl
 * @param mappingUUID
 * @returns {*}
 */
export const D_Mapping = (mockUrl: string, mappingUUID: string) => {
  return httpSingle({
    url: `${mockUrl}/__admin/mappings/${mappingUUID}`,
    method: 'delete'
  });
};


