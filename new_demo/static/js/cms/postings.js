/**
 * Created by zhuzhengyang on 2018/6/18.
 */
$(function () {
    var ue = UE.getEditor('editor',{'serverUrl':'/ueditor/upload/'});
    $('button.postings').click(function (e) {
        e.preventDefault();
        var title_e = $('input[name="title"]');
        var board_id_e = $('select[name="board_id"]');
        var csrf_token = $("meta[name=csrf-token]").attr('content');

        var title = $.trim(title_e.val());
        if (title.length >20){
            swal("你的标题不能超过20字符");
            return;
        }
        var board_id = board_id_e.val();
        var content = $.trim(ue.getContent());
        $.post({
            'url':'/cms/postings',
            'data':{
                'title':title,
                'board_id':board_id,
                'content':content,
                'csrf_token':csrf_token
            },
            'success':function (data) {
                if(data.code == 200){
                    swal({
                        title:"发送成功",
                        icon:'success',
                        buttons:['再发一篇','返回首页']
                    }).then(function (ok) {
                        if(ok){
                            window.location='/';
                        }else{
                            title_e.val("");
                            ue.setContent("");
                            title_e.focus();
                        }
                    });
                }else{
                     swal("错误", data.message, "error");
                }
            },
            'fail':function () {
                swal("错误", "服务器繁忙,请稍后再试", "error")
            }
            
        });
    });
});

