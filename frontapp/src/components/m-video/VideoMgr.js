import weixinVideo from "./weixinVideo";
import nativeVideo from "./nativeVideo";

export function createVideoMgr(context, option) {

  if (context.$store.state.env.process == 'weixin') {
    return new weixinVideo(context,option);
  }

  if (context.$store.state.env.process == 'hxApp') {
    return new nativeVideo(option);
  }

  //return new weixinFile(option);
  return new nativeVideo(option);
}
