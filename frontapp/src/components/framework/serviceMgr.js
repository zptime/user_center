import {queryPermission} from './permissionMgr';

export const hasSystemPermission = (context, capbility) => {
  if (isInvalidateEnv(context) == true) {
    return false;
  }

  return queryPermission(context.$store.state.env.os, context.$store.state.env.process,capbility);
}


export const isInvalidateEnv = (context) => {
  if ((!context.$store.state.env.os)
    || (context.$store.state.env.os == '')) {
    return true;
  }

  if ((!context.$store.state.env.process)
    || (context.$store.state.env.process == '')) {
    return true;
  }

  return false;
}

export const initializeEnv = (context) => {
  initializeSystem(context);
  initializeSignUrl(context);
}

const initializeSystem = (context) => {
  let deviceInfo = queryDeviceInfo();
  if (deviceInfo == null) {
    return;
  }

  if (!deviceInfo.sid) {
    alert('微信缺少关联的学校信息');
  }

  context.$store.state.env
    = {os:deviceInfo.deviceType, process: (deviceInfo.from ? deviceInfo.from : 'hxApp'),sid:deviceInfo.sid ? deviceInfo.sid :''};
}

export const queryDeviceInfo = function() {
  var url = location.search; //
  var request = new Object();
  if (url.indexOf("?") == -1) {
    return null;
  }

  let strs = [];
  var str = url.substr(1);
  strs = str.split("&");
  for(var i = 0; i < strs.length; i ++) {
    request[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
  }

  if (!request.deviceType && request.from) {
      request['deviceType'] = tellDevice();
      return request;
  }

  if (!request.deviceType) {
    return null;
  }

  return request;
};

export const exitCurApp = (context)=>{
  if (context.$store.state.env.process == 'weixin') {
    context.$router.back();
  } else {
    context.backNative.init();
  }
}

const initializeSignUrl =(context) => {
  if (context.$store.state.env.process != 'weixin') {
    return;
  }

  if (context.$store.state.env.os != 'ios') {
    return;
  }

  if ((context.$store.state.env.signUrl == '') || !context.$store.state.env.signUrl) {
    //alert("settings url=" + location.href.split('#')[0]);
    context.$store.state.env.signUrl = location.href.split('#')[0];
    return;
  }
}

export const querySignUrl = (context) => {
  return (context.$store.state.env.os == 'ios')
          ? context.$store.state.env.signUrl : location.href.split('#')[0];
}

export const querySid = (context) => {
  return context.$store.state.env.sid;
}

const forceSetSignUrl = (context) => {
  if ((context.$store.state.env.signUrl == '') || !context.$store.state.env.signUrl) {
    context.$store.state.env.signUrl = location.href.split('#')[0];
    return;
  }
}

export const forceConfigSettings = (context) => {
  try {
    forceSetSignUrl(context);
    forceSetSid(context);
  }catch (error) {
    alert(error.message);
  }

}

const forceSetSid = (context) => {
  if (!context.$route.query.sid) {
    return;
  }

  /*if (context.$store.env.sid && (context.$store.env.sid != '')) {
    return;
  }*/

  context.$store.state.env.sid = context.$route.query.sid;
}

const tellDevice = () =>{
  let userAgent = navigator.userAgent;
  let isAndroid = userAgent.indexOf('Android') > -1 || userAgent.indexOf('Adr') > -1; //androidÖÕ¶Ë
  let isIOS = !!userAgent.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);

  if (isAndroid) {
    return 'android'
  }
  if (isIOS) {
    return 'ios'
  }

  return 'unknown'
}
