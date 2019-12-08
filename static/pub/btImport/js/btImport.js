/**
 * Created by jie on 2017/4/11.
 */

(function ($) {
    $.extend({
        btImport : function (options) {
            // default plugin settings
            var defaults = {
                templateURL: '',
                url: '',
                fileDesc: '',
                success: null,
                successInfo: ''
            };
            var opts = $.extend(defaults, options);
            /*校验excel文件*/
            var checkExcel = function (){
                var filePath = $("#modal-import input[type=file]").val();
                if (!(filePath.substring(filePath.length-5) == ".xlsx" || filePath.substring(filePath.length-4) == ".xls")) {
                    $("label.file-error-box[for=file-error]").text("请选择EXCEL文件");
                    $("label.file-error-box[for=file-error]").removeClass("hidden");
                    return false;
                } else{
                    $("label.file-error-box[for=file-error]").text("");
                    $("label.file-error-box[for=file-error]").addClass("hidden");
                    return true;
                }
            }
            /**上传**/
            var uploadExcelData = function (){
                var formData = new FormData($("#modal-import form")[0]);
                $.ajax({
                    url: opts.url,
                    data: formData,
                    dataType: 'json',
                    type: 'POST',
                    cache: false,
                    contentType: false,
                    processData: false,
                    //timeout: 60*1000,
                    success: function (data) {
                        if (data.c != 0) {
                            $('#modal-import .step-2 .error-box .error-msg').html( data.m );
                            var msg = (typeof data.d == 'undefined') ? '' : data.d.join('<br>');
                            $('#modal-import .step-2 .error-box .error-data .e-box').html(msg).mCustomScrollbar();
                            $('#modal-import .step-2 .waiting-box').addClass('hidden');
                            $('#modal-import .step-2 .error-box').removeClass('hidden');
                            $('#modal-import .step-2 .btn-reupload').removeClass('hidden');
                        } else {
                            //跳入第三步
                            if(data.m){
                                $('#modal-import .mod-step-content .step-3 .successInfo').html(data.m);
                            }
                            $('#modal-import .mod-guide-container .mod-sub-list3').addClass('list3-active');
                            $('#modal-import .mod-guide-container .mod-sub-list2').removeClass('list2-active');
                            $('#modal-import .mod-step-content .step-3').css('display','block');
                            $('#modal-import .mod-step-content .step-2').css('display','none');
                        }
                    },
                    error: function () {
                        $('#modal-import .error-box .error-data').html('请求超时');
                    }
                });
            }
            /*上传成功*/
            var upload_success = function (layerObj){
                if (layerObj){
                    layer.close(layerObj);
                }else{
                    layer.closeAll();
                }
            }


            $(function () {
                var content = '';
                layer.open({
                    title: '批量导入',
                    area: ['880px', '480px'], //宽高
                    //content: $('#modal-import'),
                    content: '<div id="modal-import">' +
                    '<div class="modal-import-box">' +
                    '<div class="mod-guide-container">' +
                    '<div class="modal-guide">' +
                    '<ul class="mod-sub-nav">' +
                    '<li class="mod-sub-list1 list1-active">下载模板</li>' +
                    '<li class="mod-sub-list2">验证导入信息</li>' +
                    '<li class="mod-sub-list3">导入完成</li>' +
                    '</ul>' +
                    '</div>' +
                    '</div>' +
                    '<div class="mod-step-content">' +
                    '<div class="step-1" style="display: block;">' +
                    '<form>' +
                    '<div class="hx-margin20-tb">' +
                    '<p class="download-box">' +
                    '<a class="download">下载Excel模板</a>' +
                    '</p>' +
                    '<p class="file-box">' +
                    '<input name="file" type="file" class="hidden" accept=".xls,.xlsx">' +
                    '<button type="button" class="choosefile-btn">上传文件</button>' +
                    '<span class="hx-margin20-l tips file-desc">' +
                    opts.fileDesc +
                    '</span>' +
                    '<label class="file-name-box" for="file"></label>' +
                    '<label class="file-error-box hidden" for="file-error"></label>' +
                    '</p>' +
                    '</div>' +
                    '<div class="bottom-btn-box">' +
                    '<button type="button" class="next-btn">下一步</button>' +
                    '</div>' +
                    '</form>' +
                    '</div>' +
                    '<div class="step-2" style="display: none;">' +
                    '<div class="error-box hidden">' +
                    '<p class="error-msg">' +
                    'N条数据导入错误,未导入' +
                    '</p>' +
                    '<div class="error-data">' +
                        '<div class="e-box">' +
                        '</div>' +
                    '</div>' +
                    '</div>' +
                    '<div class="waiting-box">' +
                    '数据校验中，请等待...' +
                    '<em class="gif-box">' +
                    '<img src="/static/resources/images/icon/loading-cricle.gif">' +
                    '</em>' +
                    '</div>' +
                    '<div class="bottom-btn-box">' +
                    '<button type="button" class="btn-120 btn-reupload hidden">重新上传文件</button>' +
                    '</div>' +
                    '</div>' +
                    '<div class="step-3" style="display: none;">' +
                    '<div class="import-success">' +
                    '<img src="/static/resources/images/guide/icon-success.png" class="icon-success">' +
                        '<span class="successInfo">'+opts.successInfo+'</span>' +
                    '</div>' +
                    '<div class="bottom-btn-box">' +
                    '<button type="button" class="success-btn">完成</button>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>',
                    move: false,
                    btn: false
                });
                /**下载Excel模板**/
                $('#modal-import .download').on('click', function () {
                    var element_iframe = document.createElement("iframe");
                    element_iframe.src = opts.templateURL;
                    element_iframe.style.display = "none";
                    document.body.appendChild(element_iframe);
                });
                /**上传文件按钮**/
                $('#modal-import .choosefile-btn').on('click', function () {
                    $(this).parent().children('input[type=file]').click();
                });
                /**上传文件元素**/
                $('#modal-import input[type=file]').on('change', function () {
                    checkExcel();
                    $(this).parent().children('label[for=file]').html($(this).val());
                });
                /*下一步*/
                $('#modal-import .next-btn').on('click', function () {
                    if (!checkExcel()) {
                        return
                    }
                    ;
                    $('#modal-import .mod-guide-container .mod-sub-list1').removeClass('list1-active');
                    $('#modal-import .mod-guide-container .mod-sub-list2').addClass('list2-active');
                    $('#modal-import .mod-step-content .step-1').css('display', 'none');
                    $('#modal-import .mod-step-content .step-2').css('display', 'block');
                    uploadExcelData();
                });
                /*重新上传文件*/
                $('#modal-import .btn-reupload').on('click', function () {
                    $('#modal-import .mod-guide-container .mod-sub-list1').addClass('list1-active');
                    $('#modal-import .mod-guide-container .mod-sub-list2').removeClass('list2-active');
                    $('#modal-import .mod-step-content .step-1').css('display', 'block');
                    $('#modal-import .mod-step-content .step-2').css('display', 'none');
                    //清空 step-2 的error-msg   error-data
                    $('#modal-import .step-2 .error-box .error-msg').empty();
                    $('#modal-import .step-2 .error-box .error-data').html('<div class="e-box"></div>');
                    $('#modal-import .step-2 .error-box').addClass('hidden');
                    $('#modal-import .step-2 .btn-reupload').addClass('hidden');
                    $('#modal-import .step-2 .waiting-box').removeClass('hidden');
                });
                /*完成*/
                $('#modal-import .success-btn').on('click', function () {
                    upload_success();
                    if ($.isFunction(opts.success)) {
                        opts.success.apply(this);
                    }
                });
            });
        }
    });
})(jQuery);

