/**
 * Created by Xi Chen on 3/27/2017.
 */

var vm= new Vue({
    el: '#content',
    data: {
        textbook: {
/*            grade_name: "一年级",
            grade_num: "1",
            id: "1",
            subject_name: "语文",
            textbook_name: "人教语文"*/
        }
    },
    computed: {

    },
    methods: {

    }
});

$(document).ready(function(){
    get_textbook(); //获取教材对象
    initZtree(); //初始化ztree
});

//获取教材对象
function get_textbook(){
    myajax({
        url: '/api/admin_detail/textbook',
        data: {
            textbook_id: $.trim($('#textbook_id').val())
        }
    },function(data){
        if (data.c==0){
            vm.textbook = data.d[0];
        }
    });
}

//获取章节列表
function get_chapter_list(){
    var res = [];
    myajax({
        url: '/api/admin_list/chapter',
        data: {
            textbook_id:  $.trim($('#textbook_id').val())
        },
        async: false
    }, function (data) {
        if (data.c == 0){
            res = data.d ;
            for(var i=0; i<res.length; i++){
                res[i]['open'] = true;
            }
        }
    })
    return res;
}

//初始化ztree
function initZtree(){
    var setting={
            view:{
                addHoverDom:addHoverDom,
                removeHoverDom:removeHoverDom,
                selectedMulti:false,
                showLine:false,
                showIcon:false
            },
            edit: {
                enable: true,
                editNameSelectAll:true,
                removeTitle:'删除',
                renameTitle:'编辑',
                drag:{
                    isCopy:false,
                    isMove:false
                }
            },
            data: {
                simpleData: {
                    enable: true
                }
            },
            callback:{
                    beforeRemove:beforeRemove,//点击删除时触发，用来提示用户是否确定删除
                    beforeEditName: beforeEditName,//点击编辑时触发，用来判断该节点是否能编辑
                    //beforeRename:beforeRename,//编辑结束时触发，用来验证输入的数据是否符合要求
                    onRemove:onRemove,//删除节点后触发，用户后台操作
                    //onRename:onRename,//编辑后触发，用于操作后台
                    //beforeDrag:beforeDrag,//用户禁止拖动节点
                    //onClick:clickNode,//点击节点触发的事件
                    //beforeDrop:zTreeBeforeDrop
                    //onComplete: onComplete //ztree渲染完成触发的事件
            }
    };
    /*var zNodes =[
        { id:1, pId:0, name:"父节点 1", open:true, sn:1},
        { id:11, pId:1, name:"heiheihei", sn:1},
        { id:12, pId:1, name:"叶子节点 1-2", sn:2},
        { id:13, pId:1, name:"叶子节点 1-3", sn:3},
        { id:2, pId:0, name:"父节点 2", open:true,sn:2},
    ];*/
    var zNodes = get_chapter_list();
    zTree = $.fn.zTree.init($("#zTree"), setting, zNodes);
    if (zTree.getNodes().length <= 0){
        var nodes = zTree.addNodes(null, {id: 0, pId: 0, name: "" , sn:1, newNode: 1});
        zTree.editName(nodes[0]);
    }
}

//刷新树
function reloadZtree(){
    zTree.destroy();
    initZtree();
}

//删除
function beforeRemove(e,treeNode){
    var childNodes = [];
    if (treeNode.children){
        childNodes = treeNode.children;
    }
    var paramsArray = new Array();
    for(var i = 0; i < childNodes.length; i++){
        paramsArray.push(childNodes[i].name);
    }
    return confirm("你确定要删除节点 [ "+treeNode.name+" ] 吗？"+ (childNodes.length>0?"\r\n他的孩子节点有：[ "+paramsArray.join(",")+" ]":""))
}

function onRemove(e,treeId,treeNode){
    myajax({
        url: '/api/admin_delete/chapter',
        data: {
            'chapter_id': treeNode.id
        },
    },function(data){
        reloadZtree();
    })
}

//编辑
function beforeEditName(treeId,treeNode){
    return true;
}

/*function beforeRename(treeId,treeNode,newName,isCancel){
    if(newName.length < 1){
        layer.alert("名称不能少于1个字符！");
        return false;
    }
    return true;
}
function onRename(e,treeId,treeNode,isCancel){
    layer.alert("修改节点的id为："+treeNode.id+"\n修改后的名称为："+treeNode.name);
    //TODO 编辑
    myajax({

    },function(){

    });
}*/

/*
//拖曳前调用
var dragId;
function beforeDrag(treeId,treeNodes){
    for(var i=0,l=treeNodes.length;i<l;i++) {
          dragId = treeNodes[i].pid;
    }
    return true;
}
//拖曳完成
function zTreeBeforeDrop(treeId, treeNodes, targetNode, moveType) {
    var oldPid = treeNodes[0].pId;
    var targetPid = targetNode.pId;
    if (oldPid != targetPid) {
        layer.alert("只能在同一知识点下面移动位置");
        return false;
    }
    if (oldPid == "root" || targetPid == "root") {
        layer.alert("只能移动子知识的节点。");
        return false;
    }
}
*/

var newCount = 1;
function addHoverDom(treeId,treeNode){
    var sObj = $("#" + treeNode.tId + "_span");
    var pObj = $(sObj).parent();
    if ( zTree.getSelectedNodes != undefined ){
        var selectNodes = zTree.getSelectedNodes();  //选中的节点
        if (selectNodes.length > 0 && selectNodes[0] != treeNode ){
            return;
        }
    }
    var edit_flag = false; //编辑模式  zTree_1_edit
    var noeditBtn_display = 'display:inline-block';
    var editBtn_display = 'display:none';
    if ( $("#"+treeNode.tId+'_edit').length<=0 ){
        edit_flag = true;
        noeditBtn_display = 'display:none';
        editBtn_display = 'display:inline-block';
    }

    if (treeNode.level == 0){
        //添加子节点
        var addStr = "<span class='button addChild' id='addchildBtn_" + treeNode.tId
            + "' title='添加下级节点' style='"+noeditBtn_display+"' onfocus='this.blur();'>添加下级章节</span>";
        if ( $(pObj).children('#addchildBtn_'+treeNode.tId).length <= 0 ) {
            pObj.append(addStr);
            var btn = $("#addchildBtn_" + treeNode.tId);
            if (btn) btn.bind("click", function () {
                //在这里向后台发送请求保存一个新建的叶子节点，父id为treeNode.id,让后将下面的100+newCount换成返回的id
                var sn = treeNode.children? (treeNode.children.length + 1): 1;
                var nodes = zTree.addNodes(treeNode, {id: (20000 + newCount), pId: treeNode.id, name: "新建下级节点" + (newCount++), sn:sn, newNode: 1});
                zTree.editName(nodes[0]);
                return false;
            });
        }
    }

    //添加兄弟节点
    var brotherStr = "<span class='button addBrother' id='addBrotherBtn_" + treeNode.tId
        + "' title='添加同级节点' style='"+noeditBtn_display+"'  onfocus='this.blur();'>添加同级章节</span>";
    if ( $(pObj).children('#addBrotherBtn_'+treeNode.tId).length <= 0 ){
        pObj.append(brotherStr);
        var brotherBtn = $("#addBrotherBtn_"+treeNode.tId);
        if (brotherBtn) brotherBtn.bind("click", function(){
            /*if(!treeNode.isParent){
                layer.msg('叶子节点不能建立同级节点');
            }*/
            var parentNode = treeNode.getParentNode();
            var pId = 0;
            if(parentNode != null){
                pId = parentNode.id;
            }
            var sn = zTree.getNodeIndex(treeNode);
            var nodes = zTree.addNodes(parentNode, sn+1, {'id':(10000+newCount),'pId':pId,'name':'新建同级节点'+ (newCount++),'sn':sn+2 ,newNode: 1});
            zTree.editName(nodes[0]);
            return false;
        });
    }

    //添加保存按钮
    var saveBtn = "<span class='button save' id='addSaveBtn_" + treeNode.tId
    + "' title='保存' style='"+editBtn_display+"' onfocus='this.blur();'>保存</span>";
    if ( $(pObj).children('#addSaveBtn_'+treeNode.tId).length <= 0 ) {
        pObj.append(saveBtn);
        var saveBtn = $("#addSaveBtn_" + treeNode.tId);
        if (saveBtn) saveBtn.bind("click", function () {
            var inputVal = $.trim($('#' + treeNode.tId + '_input').val());
            if(inputVal.length <= 0){
                layer.alert("名称不能为空！");
                return;
            }
            if (treeNode.newNode ) {
                //来源于新增
                var parentNode = treeNode.getParentNode();
                var parent_id = 0;
                if(parentNode != null){
                    parent_id = parentNode.id;
                }
                myajax({
                    url: '/api/admin_add/chapter',
                    data: {
                        textbook_id: $.trim($('#textbook_id').val()),
                        chapter_name: inputVal,
                        parent_id: parent_id,
                        sn: treeNode.sn
                    }
                }, function (data) {
                    reloadZtree();
                })
            }else{
                //来源已编辑
                myajax({
                    url: '/api/admin_edit/chapter',
                    data: {
                        chapter_id: treeNode.id,
                        chapter_name: inputVal
                    }
                }, function (data) {
                    reloadZtree();
                })
            }
        });
    }

    //添加取消按钮
    var cancelBtn = "<span class='button cancel' id='addCancelBtn_" + treeNode.tId
    + "' title='取消'  style='"+editBtn_display+"' onfocus='this.blur();'>取消</span>";
    if ( $(pObj).children('#addCancelBtn_'+treeNode.tId).length <= 0 ) {
        pObj.append(cancelBtn);
        var cancelBtn = $("#addCancelBtn_" + treeNode.tId);
        if (cancelBtn) cancelBtn.bind("click", function () {
            reloadZtree();
            return false;
        });
    }
}
function removeHoverDom(treeId,treeNode){
    if (treeNode.level == 0){
        $("#addchildBtn_"+treeNode.tId).unbind().remove();
    }
    $("#addBrotherBtn_"+treeNode.tId).unbind().remove();
    $("#addSaveBtn_"+treeNode.tId).unbind().remove();
    $("#addCancelBtn_"+treeNode.tId).unbind().remove();
}
