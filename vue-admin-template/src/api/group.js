import request from '@/utils/request'

// 获取组列表
export function getGroupList (params) {
  return request({
    url: '/api/groups/',
    method: 'get',
    params
  })
}

// 创建组
export function addGroup (data) {
  return request({
    url: '/api/groups/',
    method: 'post',
    data
  })
}

// 更新组
export function modifyGroup (id, data) {
  return request({
    url: `/api/groups/${id}/`,
    method: 'patch',
    data
  })
}

// 修改指定用户的角色(组)
export function updateUserGroups (uid, data) {
  return request({
    url: `/api/userGroups/${uid}/`,
    method: 'patch',
    data
  })
}

// 获取指定用户的所有组
export function getUserGroupList (uid, params) {
  return request({
    url: `/api/userGroups/${uid}/`,
    method: 'get',
    params
  })
}

// 获取指定用户组下的成员列表
export function getGroupMemberList (gid, params) {
  return request({
    url: `/api/groupMembers/${gid}/`,
    method: 'get',
    params
  })
}

// 从用户组中移除指定用户
export function removeGroupMember (gid, data) {
  return request({
    url: `/api/groupMembers/${gid}/`,
    method: 'delete',
    data
  })
}
