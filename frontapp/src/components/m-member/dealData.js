import fetch from '../../config/fetch.js'

/**
 *从群组中删除多个用户
 **/
export const contactGroupUserDel = (group_id,delete_users) => fetch('/api/contacts/group/user/delete',{
  group_id:group_id,
  delete_users:delete_users //格式：1,1,1;2,2,2;3,3,3;
},'POST');


/**
 *某群组尚可邀请的用户（新）
 **/
export const contactGroupInviteAgain = (group_id) => fetch('/api/v2/contacts/group/user/invite/available',{
  group_id:group_id
},'GET');


/**
 *邀请用户加入群组
 **/
export const contactGroupUserInvite = (group_id,invite_users) => fetch('/api/contacts/group/user/invite',{
  group_id:group_id,
  invite_users:invite_users,
},'POST');


/**
 *获取某班级现有用户列表(包含自己)
 **/
export const contactClassUserList = (class_id) => fetch('/api/contacts/class/user/list',{
  class_id:class_id
},'POST');
