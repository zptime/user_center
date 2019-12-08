import weixinFile from "./weixinFile";
import nativeFile from "./nativeFile";

export function createFileMgr(context, option) {

  if (context.$store.state.env.process == 'weixin') {
    return new weixinFile(context, option);
  }

  if (context.$store.state.env.process == 'hxApp') {
    return new nativeFile(option);
  }

  //return new weixinFile(option);
  return new nativeFile(option);
}
