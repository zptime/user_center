/**
 * Created by jie on 2016/10/20.
 */
//清理缓存
if ($('#recache').val()){
    HX_CACHE.refresh();
}
Vue.config.delimiters = ["{$", "$}"];

$(document).ready(function(){
    //切换导航栏
    $('.main-nav li').on('click',function(){
        var a = this;
        url_go( '/root/index?nav='+ a.id );
    })
})
