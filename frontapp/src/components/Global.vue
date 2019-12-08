<script type="es6">
  const colorList = {
    c_blue: '#4685ff',//蓝色
    c_light_blue: '#afc8f9',//浅蓝色

    c_green: '#4dc647',//绿色
    c_light_green: '#b2e2af',//浅绿色

    c_gray: '#a9a9a9',//灰色
    c_light_gray: '#d2d2d2',//浅灰色

    c_gray_blue: '#a2b9cb',//蓝灰色
    c_light_gray_blue: '#d4dde4',//浅蓝灰色

    c_orange: '#ffab00',//黄橙色
    c_light_orange: '#ffdb9b',//浅黄橙色

    c_red: '#fd5555',//红色
    c_light_red: '#de8169',//浅红色

    c_red_orange: '#fb8c00',//红橙色
    c_light_red_orange:'#c2c975',//浅红橙色

    c_title_gray:'#888', //小标题字体-灰色（如：已选择3人，24px）
    c_title_orange:'#ff9e35', //小标题字体-橙色（如：批量编辑，24px）
    c_content_gray:'#aaa',//内容-灰色（如：数学，24px）
    c_content_black:'#444',//内容字体-黑色（如：李明，32px）
    c_btn_blue:'#4685ff',//按钮字体-蓝色（如：添加小组成员，30px）
    c_btn_red:'#fd5555',//按钮字体-红色（如：移除，24px）
    c_btn_green:'#23d42e',//按钮字体-绿色（如：全选，24px）
    c_border_gray:'#eee',//边框颜色-灰色（如：成员下面的下划线）
  }

  const showHead = true;//是否显示头部

  const regShowHead = false;//注册-相关页面-是否显示头部

  const checkStatus = {
    check_all:true,//全选
    deselect_all:false,//取消全选
    partial_select:'partial',//部分选择
  };

  export default
  {
    colorList,
    checkStatus,
    showHead,
    setHeadVal(newVal){
      this.showHead = newVal;
    },
    regShowHead,
    setRegHeadVal(newVal){
      this.regShowHead = newVal;
    }
  }
</script>
