/**
 * Created by zhuzhengyang on 2018/6/14.
 */
$(function () {
    var dialog = $("#banner-dialog");
    var name_e = $("input#name");
    var img_url_e = $("input#img-url");
    var link_url_e = $("input#link-url");
    var weight_e = $("input#weight");
    var csrf_token = $("meta[name=csrf-token]").attr('content');
    dialog.on('hide.bs.modal',function (e) {
        $('span#ossfile').text('');
        $('span.progress-bar').css('width','0%');
        name_e.val('');
        img_url_e.val('');
        link_url_e.val('');
        weight_e.val('');
    })
    $("#add-banner").click(function () {
        var name = $.trim(name_e.val());
        var img_url = $.trim(img_url_e.val());
        var link_url = $.trim(link_url_e.val());
        var weight = $.trim(weight_e.val());
        var type = $(this).attr('data-type');
        var id = $(this).attr('banner-id');
        var url = '/cms/banner_add';
        if (type == 'update') {
            url = '/cms/banner_update'
        }

        if ($('span.progress-bar').css('width') != $('div.progress').css('width')&&!id){
            sweetAlert("提示", "图片未上传成功", "warning");
            return;
        }
        // if (!name||!img_url||!link_url||!weight){
        //     sweetAlert("提示", "请输入完整信息", "warning");
        //     return;
        // }
        if (isNaN(weight)){
            sweetAlert("提示", "优先级请输入整数", "warning");
            return;
        }
        $.post({
            'url':url,
            'data':{
                'name':name,
                'img_url':img_url,
                'link_url':link_url,
                'weight':weight,
                'id':id,
                'csrf_token':csrf_token
            },
            'success':function (data) {
                if(data.code==200){
                    window.location.reload();
                    dialog.modal('hide');
                }else{
                    sweetAlert("提示", data.message, "warning");
                }
            },
            'fail':function (error) {
                sweetAlert("错误", "请稍后再试", "error");
            }
        });
    });
    $(".edit-banner").click(function () {
        dialog.modal('show');
        var tr = $(this).parent().parent();
        id = tr.attr('data-id');
        name = tr.attr('data-name');
        img = tr.attr('data-img');
        link = tr.attr('data-link');
        weight = tr.attr('data-weight');
        name_e.val(name);
        img_url_e.val(img);
        link_url_e.val(link);
        weight_e.val(weight);
        $("#add-banner").attr({
            'data-type':'update',
            'banner-id':id
        });
    });
    $(".delete-banner").click(function () {
        var id = $(this).parent().parent().attr('data-id');
        var name = $(this).parent().parent().attr('data-name');
        swal({
            title: '确定删除名称为'+ name +'的图片吗？',
            icon: 'warning',
            buttons: true,
        }).then(function (willDelete) {
            if (willDelete) {
                $.post({
                    'url':'/cms/banner_delete',
                    'data':{
                        'id':id,
                        'csrf_token':csrf_token
                    },
                    'success':function (data) {
                        if(data.code == 200){
                            window.location.reload();
                            dialog.modal('hide');
                        }else{
                            swal("错误", data.message, "error");
                        }
                    },
                    'fail':function () {
                        swal("错误", "请稍后再试!", "error");
                    }
                })
            }
        });
    });
    $(".add-banner").click(function () {
        $("#add-banner").removeAttr('data-type');
        $("#add-banner").removeAttr('banner-id');
    });
});