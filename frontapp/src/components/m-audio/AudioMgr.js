import weixinAudio from "./weixinAudio";
import nativeAudio from "./nativeAudio";

export function createAudioMgr(context, option) {

  //alert(context.$store.state.env.process);
  if (context.$store.state.env.process == 'weixin') {
    return new weixinAudio(context,option);
  }

  if (context.$store.state.env.process == 'hxApp') {
    return new nativeAudio(option);
  }

  //return new weixinAudio(option);
  return new nativeAudio(option);
}
