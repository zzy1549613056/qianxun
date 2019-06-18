/**
 * Created by zhuzhengyang on 2018/6/16.
 */
$(function () {
    var dialog = $("#banner-dialog");
    var csrf_token = $("meta[name=csrf-token]").attr('content');
    $('button#add-board').click(function () {
        swal({
            text:'输入版块',
            content:'input',
            buttons:['取消','提交']
        })
        .then(function (data) {
            if($.trim(data)){
                $.post({
                    'url':'/cms/boards_add',
                    'data':{
                        'name':data,
                        'csrf_token':csrf_token
                    },
                    'success':function (data) {
                        if(data.code == 200){
                            window.location.reload()
                        }else{
                            swal("错误", data.message, "error");
                        }
                    },
                    'fail':function (error) {
                        swal("错误", "请稍后再试!", "error");
                    }
                });
            }
        });
    });
    $('button.edit-board').click(function (){
        var tr = $(this).parent().parent();
        var id = tr.attr('data-id');
        var name = tr.attr('data-name');
        swal({
            text:'修改版块名',
            content: {
                element: "input",
                attributes: {
                value: name
                },
            },
            buttons:['取消','修改']
        })
        .then(function (data) {
            if($.trim(data)){
                $.post({
                    'url':'/cms/boards_update',
                    'data':{
                        'name':data,
                        'id':id,
                        'csrf_token':csrf_token
                    },
                    'success':function (data) {
                        if(data.code == 200){
                            window.location.reload()
                        }else{
                            swal("错误", data.message, "error");
                        }
                    },
                    'fail':function (error) {
                        swal("错误", "请稍后再试!", "error");
                    }
                });
            }

        });
    });
    $('button.delete-board').click(function (){
        var tr = $(this).parent().parent();
        var id = tr.attr('data-id');
        var name = tr.attr('data-name');
        swal({
            title: '确定删除 '+ name +' 版块吗？',
            icon: 'warning',
            buttons: true,
        }).then(function (isdelete) {
            if(isdelete){
                $.post({
                    'url':'/cms/boards_delete',
                    'data':{
                        'id':id,
                        'csrf_token':csrf_token
                    },
                    'success':function (data) {
                        if(data.code == 200){
                            window.location.reload()
                        }else{
                            swal("错误", data.message, "error");
                        }
                    },
                    'fail':function (error) {
                        swal("错误", "请稍后再试!", "error");
                    }
                });
            }
        });
    });
});