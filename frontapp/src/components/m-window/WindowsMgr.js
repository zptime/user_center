import weixinWindows from "./weixinWindows.js";
import nativeWindows from "./nativeWindows.js";

export function createWindowsMgr(context, option) {

  if (context.$store.state.env.process == 'weixin') {
    return new weixinWindows(context,option);
  }

  if (context.$store.state.env.process == 'hxApp') {
    return new nativeWindows(option);
  }

  return new nativeWindows(option);
}
