$(function() {
  $('#image').cropper({
      viewMode: 1,
      aspectRatio: 1
    });
});

function rotate_left(){
    $('#image').cropper("rotate", -90)
}
function rotate_right(){
    $('#image').cropper("rotate", 90)
}

function refresh(){
   $('#image').cropper("replace", $('#image')[0].src);
}

function save_photo(){
    $('#image').cropper('getCroppedCanvas').toBlob(function (blob) {
      var formData = new FormData();
      var file_name = $("#file-upload")[0].files[0].name;
      var fileOfBlob = new File([blob], file_name);
      formData.append('image', fileOfBlob);

      $.ajax('/api/upload/image', {
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            if (data.c == 0) {
                var index = parent.layer.getFrameIndex(window.name);
                var ret_val = parent.window.upload_photo_success(data.d[0].url);
                if (ret_val == true){
                    parent.layer.close(index);
                } else {
                    layer.msg('上传失败: ' + ret_val );
                }

            } else {
                layer.msg('上传失败: ' + data.m );
            }
        },
        error: function () {
          layer.msg('上传失败');
        }
      });
    });
}
function upload_img(fileDom){
    //显示选择文件的文件名
    var file_name = document.getElementById('file-upload').files[0].name ;
    $('#file_name_box').html(file_name);
    //判断是否支持FileReader
    if (window.FileReader) {
        var reader = new FileReader();
    } else {
        layer.msg("您的设备不支持图片预览功能，如需该功能请升级您的设备！");
    }

    //获取文件
    var file = fileDom.files[0];
    var imageType = /^image\//;
    //是否是图片
    if (!imageType.test(file.type)) {
        layer.msg("请选择图片！");
        return;
    }
    //读取完成
    reader.onload = function(e) {
        //获取图片dom
        var img = document.getElementById("image");
        //图片路径设置为读取的图片
        img.src = e.target.result;
        refresh();
    };
    reader.readAsDataURL(file);
}

function openFile(){
    $('#file-upload').click();
}