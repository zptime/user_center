import nativeImage from "./nativeImage";
import weixinImage from "./weixinImage";

export function createImageMgr(context, option) {
    //alert("process=" + context.$store.state.env.process);
    if (context.$store.state.env.process == 'weixin') {
      return new weixinImage(context,option);
    }

    if (context.$store.state.env.process == 'hxApp') {
      return new nativeImage(option);
    }

    //return new weixinImage(context,option);
    return new nativeImage(option);
}
