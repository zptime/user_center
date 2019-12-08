import fetch from '../../config/fetch'

/**
 *测试登录
 **/
export const testLogin = (username,password) => fetch('/user_center/api/login',{
  username: username,
  password: password,
},'POST');

///api/list/send_target'
//获取可发送对象
export const getSendTarget = () => fetch('/api/list/send_target',{

},'POST');
