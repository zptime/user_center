import {createWindowsMgr} from "../m-window/WindowsMgr";

export const hasActionBar = (context) => {
  return context.$store.state.env.process == 'weixin';
}

export const closeWindows = (context) => {
  let windowsMgr = createWindowsMgr(context,null);
  windowsMgr.closeWindows();
}
