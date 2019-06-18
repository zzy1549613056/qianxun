/**
 * Created by zhuzhengyang on 2019/6/6.
 */
$(function () {
    var csrf_token = $("input[name='csrf_token']").val();
    $('#message-submit').click(function (e) {
        e.preventDefault();
        var name = $.trim($("input[name='name']").val());
        var tel = $.trim($("input[name='tel']").val());
        var email = $.trim($("input[name='email']").val());
        var kind = $("select[name='kind']").val();
        var question = $("textarea[name='question']").val();
        $.post({
            'url':'/about',
            'data':{
                'name':name,
                'csrf_token':csrf_token,
                'tel':tel,
                'email':email,
                'kind':kind,
                'question':question
            },
            'success':function (data) {
                if(data.code==200){
                    swal("成功", '你的问题已经提交成功', "success");
                }else{
                    swal("提示", data.message, "warning");
                }
            },
            'fail':function (error) {
                swal("错误", '请稍后再试', "error");
            }
        });
    });

});

function cal() {
    var length = $("textarea[name='question']").val().length;
    $("span.len").text(length+'/200');

}