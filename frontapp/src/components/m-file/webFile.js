/**
 * Created by jie on 2018/3/15.
 * 说明： 本文件为nativeImage
 */
import EventTarget from './observer.js'

var webFile = new EventTarget();
var _onProgress = function(data){
  data.options.target.progress( data.params )
}
var _onComplete = function(data){
  data.options.target.complete( data.params )
}
var _onGetPhoneFileResult = function(data){
  data.options.target.getPhoneFileResult( data.params )
}
var _onDownloadFileResult = function(data){
  data.options.target.downloadFileResult( data.params )
}
webFile.addEvent("onProgress", _onProgress)
webFile.addEvent("onComplete", _onComplete)
webFile.addEvent("onGetPhoneFileResult", _onGetPhoneFileResult)
webFile.addEvent("onDownloadFileResult",_onDownloadFileResult)

export default webFile = webFile
