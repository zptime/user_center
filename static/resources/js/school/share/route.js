/**
 * Created by jie on 2016/10/20.
 */
//清理缓存
if ($('#recache').val()){
    HX_CACHE.refresh();
}
Vue.config.delimiters = ["{$", "$}"];

$(document).ready(function(){
    render_nav();
    //切换导航栏
    $('.main-nav li').on('click',function(){
        var a = this;
        url_go( '/index?nav='+ a.id );
    })
    //切换左侧视图
    $('.left-view li').on('click',function(){
        var b = this;
        url_go( '/index?nav='+$('#nav_val').val()+'&view='+ b.id);
    })
})

/**渲染nav栏*/
function render_nav(){
    if ($('#view_val').val()){
        view_val = $('#view_val').val();
        $('#'+view_val).prepend('<el class="li-active-tag"></el>');
        $('#'+view_val).children('a').addClass('active');
    }
}

