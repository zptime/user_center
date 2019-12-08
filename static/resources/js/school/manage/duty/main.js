/**
 * Created by jie on 2017/3/27.
 */

var vm= new Vue({
    el: '#content',
    data: {
        multiple: false,
    },
    computed: {

    },
    methods: {

    }
});

$(document).ready(function(){
    //加载grid表格
    myjqGrid( $('#grid') ,{
        url: '/api/list/title',
        colNames:['id','职务名称','职务类型','人数','操作'],
        colModel:[
            {name:'id',index:'id', hidden:true},
            {name:'name',index:'name', width:100, align:"center", sorttype:"string"},
            {name:'comments',index:'comments', width:300, align:"center", sorttype:"string"},
            {name:'teacher_amount',index:'teacher_amount', width:100,  align:"center", sorttype:"string"},
            {name:'oper',index:'oper', formatter: fmt_oper, width:100, align:"center"}
        ],
        multiselect: false,
        choosed: function(multiple){
            vm.multiple = multiple;
        },
        //ispaged: true
    },function(){});
    function fmt_oper(cellvalue, options, rowObject){
        var id= rowObject.id;
        return  '<span class="mytooltip">...<span class="mytooltiptext"><li  onclick="edit('+id+')">编辑</li><li  onclick="del('+id+')">删除</li></span></span>'
    };
});

/**刷新gird**/
function reloadGrid(){
    var data = {
    };
    $("#grid").jqGrid('setGridParam', {
        url: '/api/list/title',
        datatype: "json",
        mtype: "POST",
        postData: data,
        page: 1
    }).trigger("reloadGrid"); //重新载入
}

function add(){
    $('#duty-name').val("");
    layer.open({
        type: 1,
        title: '添加职务',
        area: ['550px','330px'],
        content : $('#modal-add-duty'),
        btn:['确定','取消'],
        btn1: function(index){
            var data = {
                "name": $("#duty-name").val()
            };
            myajax({
                aysnc: false,
                url: '/api/add/title',
                data:  data
            },function(data){
                if(data.c == 0){
                    reloadGrid();
                    layer.close(index);
                    layer.msg('操作成功');
                }
            })
        },
        cancel: function(index){
            layer.close(index);
        }
    });

}

//修改
function edit(id){
    $('#duty-name').val("");
    layer.open({
        type: 1,
        title: '编辑职务',
        area: ['550px','330px'],
        content : $('#modal-add-duty'),
        btn:['确定','取消'],
        btn1: function(index){
            var data = {
                "tile_id": id,
                "name": $("#duty-name").val()
            };
            myajax({
                aysnc: false,
                url: '/api/update/title',
                data:  data
            },function(data){
                if(data.c == 0){
                    reloadGrid();
                    layer.close(index);
                    layer.msg('操作成功');
                }
            })
        },
        cancel: function(index){
            layer.close(index);
        }
    });

}

//删除
function del(id){
    var ids = [id];
    layer.confirm('确认删除选中记录吗?', {
           icon: 3,
           title: '提示',
           btn:['确定','取消'],
           btn1: function (index) {
                myajax({
                    aysnc: false,
                    url: '/api/delete/title',
                    data: {
                        id_list: JSON.stringify(ids)
                    }
                },function(data){
                    reloadGrid();
                    if(data.c == 0){
                        layer.msg('删除成功');
                    }
                });
                layer.close(index);
           },
           cancel: function(index){
               layer.close(index);
           }
    });
};
