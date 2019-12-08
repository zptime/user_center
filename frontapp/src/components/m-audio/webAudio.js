/**
 * Created by jie on 2018/3/15.
 * 说明： 本文件为nativeImage
 */
import EventTarget from './observer.js'

var webAudio = new EventTarget();

var _onLoad= function(data){
    data.options.target.load( data.params )
}
var _onStart= function(data){
    data.options.target.start( data.params )
}
var _onStop= function(data){
    data.options.target.stop( data.params )
}
var _onComplete= function(data){
  data.options.target.complete( data.params )
}

var _onStopPlayAudio= function(data){
  data.options.target.stopPlayAudio(data.params )
}

webAudio.addEvent("onLoad", _onLoad)
webAudio.addEvent("onStart", _onStart)
webAudio.addEvent("onStop", _onStop)
webAudio.addEvent("onComplete", _onComplete)
webAudio.addEvent("onStopPlayAudio", _onStopPlayAudio)


export default webAudio = webAudio