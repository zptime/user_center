export const queryPermission = (os, process, capbility) => {
   return PERMISSION_TABLE[os][process][capbility];
}

export const PERMISSION_IMAGE = 'enable_image';
export const PERMISSION_VOICE = 'enable_voice';
export const PERMISSION_SHOW_FILE = 'enable_show_file';
export const PERMISSION_FILE = 'enable_file';
export const PERMISSION_VIDEO = 'enable_video';
export const PERMISSION_LOCATION = 'enable_location';
export const PERMISSION_SHARE = 'enable_share';

export const PERMISSION_TABLE = {
  ios :{
    weixin :{
      enable_image : true,
      enable_voice : true,
      enable_show_file : false,
      enable_file : true,
      enable_video : false,
      enable_location : false,
      enable_share : false,
    },
    hxApp: {
      enable_image : true,
      enable_voice : true,
      enable_show_file : true,
      enable_file : true,
      enable_video : true,
      enable_location : true,
      enable_share : true,
    },
  },
  android: {
    weixin :{
      enable_image : true,
      enable_voice : true,
      enable_show_file : false,
      enable_file : true,
      enable_video : true,
      enable_location : false,
      enable_share : false,
    },
    hxApp: {
      enable_image : true,
      enable_voice : true,
      enable_show_file : true,
      enable_file : true,
      enable_video : true,
      enable_location : true,
      enable_share : true,
    },
  },
}
