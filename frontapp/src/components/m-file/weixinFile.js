/**
 * Created by yulu on 2018/6/19.
 */

import {uploadFile} from '../../service/getData.js'
import {showTextToast,showTextLoading,hideTextLoading} from "../framework/toastViewMgr.js";

function weixinFile (target, opt){
  var _self = this;
  this.target = target;
  this.options  = opt || {}
  this.init = function (obj) {
  },
    //预览文件
    //obj格式
    ////{
    //"file_id": "string",
    //"file_url": "string", //andirod主要是这个字段
    //"file_size": "string",
    //"file_name": "string"  //iOS主要是这个字段
    //"downloadState":""// -1 查看 0 下载 1 下载中
    //}
    this.filePreView = function (obj) {
      if((typeof callNativeFilePreViewFuc) != 'undefined') {
        callNativeFilePreViewFuc(JSON.stringify(obj));
      }
    },
    /*
    native在拿到文件对象后，调用 _win_nativeFile.progress()方法,参数传序列化的json对象
    每上传成功一个文件，就被触发一次
    */
    this.progress = function (data) {
      var fileObj = {}
      if (data){
        try {
          if (typeof data == 'string'){
            fileObj = JSON.parse(data)
          }else if(typeof data == 'object'){
            fileObj = data
          }
          _self.options.webFile.fireEvent({
            type: "onProgress",
            params: fileObj,
            options: _self.options
          })
        }catch(e){
          setTimeout(function () {
            alert(e)
          },500);
        }
      }
    },
    /*
    native在所有文件处理完之后，调用 _win_nativeFile.complete()方法,参数传序列化的json对象例如："{"flag":true}"
    */
    this.complete = function (data) {
      var flagObj = {}
      if (data){
        try {
          if (typeof data == 'string'){
            flagObj = JSON.parse(data)
          }else if(typeof data == 'object'){
            flagObj = data
          }
          _self.options.webFile.fireEvent({
            type: "onComplete",
            params: flagObj,
            options: _self.options
          })
        }catch(e){
          setTimeout(function () {
            alert(e)
          },500);
        }
      }
    },
    //获取手机所有的文件，用于判断展示文件列表的文件的状态
    //obj是数据数组，给app判断，并赋值downloadState字段
    //获取手机所有的文件，用于判断展示文件列表的文件的状态
    //发送的数组中的结构
    /*
     {
     *"file_id": "string",
     "file_url": "string",
     "file_size": "string",
     "file_name": "string"
     "downloadState":""// -1 查看 0 下载 1 下载中
     }
     *
     */
    //获取成功后，回调_win_nativeFile.getPhoneFileResult(Array)
    this.getPhoneFile = function (obj) {
      window._win_nativeFile = _self;
      if((typeof callNativePhoneFile) != 'undefined') {
        callNativePhoneFile(JSON.stringify(obj));
      }
    },
    //data是数组
    //{
    //*"file_id": "string",
    //"file_url": "string",
    //"file_size": "string",
    //"file_name": "string"
    //"downloadState":""// -1 查看 0 下载 1 下载中
    //}
    //}
    //显示文件列表的数据
    //原生APP来判断文件在本地是否保存，并且修改downloadState字段
    this.getPhoneFileResult = function (data) {
      var fileResultObj = {}
      if (data){
        try {
          if (typeof data == 'string'){
            fileResultObj = JSON.parse(data)
          }else if(typeof data == 'object'){
            fileResultObj = data
          }
          _self.options.webFile.fireEvent({
            type: "onGetPhoneFileResult",
            params: fileResultObj,
            options: _self.options
          })
        }catch(e){
          setTimeout(function () {
            alert(e)
          },500);
        }
      }
    },

    //下载文件
    //obj格式
    ////{
    //"file_id": "string",
    //"file_url": "string", // 主要使用这个字段
    //"file_size": "string",
    //"file_name": "string"
    //"downloadState":""// -1 查看 0 下载 1 下载中
    //}
    //下载完成的回调_win_nativeFile.downloadFileResult()
    this.downloadFile = function (item) {
      window._win_nativeFile = _self;
      if((typeof callNativeDownloadFile) != 'undefined') {
        callNativeDownloadFile(JSON.stringify(item));
      }
    },

    //手机下载文件的回调
    // 传递给js的参数，JSON字符串  @{@"flag":@"1",@"file_url":filePath};
    //flag ： 文件是否下载成功
    //file_url： 下载文件的url（用于安卓的预览）
    this.downloadFileResult =function (data) {
      var downLoadFlag = {}
      if (data){
        try {
          if (typeof data == 'string'){
            downLoadFlag = JSON.parse(data)
          }else if(typeof data == 'object'){
            downLoadFlag = data
          }
          _self.options.webFile.fireEvent({
            type: "onDownloadFileResult",
            params: downLoadFlag,
            options: _self.options
          })
        }catch(e){
          setTimeout(function () {
            alert(e)
          },500);
        }
      }
    },

    //取消文件下载
    //data可能有值 用于取消特定的文件下载 暂未开发
    this.cancelFileDownload = function (data) {
      if((typeof callNativeDownloadFileCancle) != 'undefined') {
        callNativeDownloadFileCancle(JSON.stringify(data));
      }
    }

    this.asyncUploadFile = function() {
      asyncUpload(this);
    }

  // 在原生应用显示
  this.showInNativeApp = function () {
    return false;
  }
}

let asyncUpload = async (fileMgrSelf)=> {
  showTextLoading(fileMgrSelf.target,'上传中');
  let res = await uploadFile(fileMgrSelf.target.$refs.uFile.files[0]);
  if (res.c == 0 ) {
    hideTextLoading(fileMgrSelf.target)
    showTextToast(fileMgrSelf.target,res.m);
    //alert(res.d.file_url);
    //oa系统返回的是数组，需要判断处理
    let resultD = undefined;
    let obj = Object.prototype.toString.call(res.d);
    if (obj == '[object Array]'){
        resultD = res.d[0];
    }else{
      resultD = res.d;
    }
    // alert(res.d);
    // alert(resultD.name);
    fileMgrSelf.progress(resultD);
    fileMgrSelf.complete({flag:true});
    return;
  }
  showTextToast(fileMgrSelf.target,res.m);
  fileMgrSelf.complete({flag:false});
  alert('文件上传失败');
}

export default weixinFile = weixinFile

