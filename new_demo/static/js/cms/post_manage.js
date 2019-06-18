/**
 * Created by zhuzhengyang on 2019/6/5.
 */
var url = window.location.href;
var page_match = url.match(/page=(\d+)/);
if (page_match){
    var page = Number(page_match[1]);
}else {
    var page = 1;
}

$(function () {
    $('td.index').text(function(a,b) {
    return a+(page-1)*5+1;
    });
    var csrf_token = $("meta[name=csrf-token]").attr('content');
    $('button.delete-post').click(function () {
        var tr = $(this).parent().parent();
        var id = tr.attr('data-id');
        var title = tr.attr('data-title');
        swal({
            title: '确定删除 '+ title +' 吗？',
            icon: 'warning',
            buttons: true,
        }).then(function (isdelete) {
            if(isdelete){
                $.post({
                    'url':'/cms/post_delete',
                    'data':{
                        'id':id,
                        'csrf_token':csrf_token
                    },
                    'success':function (data) {
                        if(data.code==200){
                            window.location.reload()
                        }else{
                            swal("错误", data.message, "error");
                        }

                    },
                    'fail':function (error) {
                        swal("错误", '请稍后再试', "error");
                    }

                });
            }
        });
    });
})