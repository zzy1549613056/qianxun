/**
* Created by zhuzhengyang on 2018/6/19.
*/
$(function () {
    var url = window.location.href;
    if(url.match(/\/\?(?!page=)/)){
        url = url.replace(/&page=\S+/,'')+'&';
    }else{
        url = url.match(/http:\/\/.*?(\/.*\/)/)[1]='?';
    }
    var nav = $('nav#navigation');
    var pages = parseFloat(nav.attr('data-pages'));
    var last = parseFloat(nav.attr('data-last'));
    var page = parseInt(nav.attr('data-page'));
    var next = $('a#next');
    var pre = $('a#pre');
    if (page < pages && page >1){
        for (var i=1;i<=5;i++) {
        $('ul.pagination li a:eq(' + i + ')').attr('href', url+'page=' + (i + page * 5 -5));
        $('ul.pagination li a:eq(' + i + ')').text(i + page * 5 -5);
        }
    }
    if(page==1){
        pre.text("到头");
        pre.attr('disabled',true);
        for (var i=1;i<=5;i++) {
        $('ul.pagination li a:eq(' + i + ')').attr('href', url+'page=' + (i + page * 5 -5));
        $('ul.pagination li a:eq(' + i + ')').text(i + page * 5 -5);
        }
    }
    if(page > pages){
        next.text("到底");
        next.attr('disabled',true);
        for (var i=1;i<=5;i++) {
            $('ul.pagination li a:eq(' + i + ')').attr('href','javascript:void(0);');
            $('ul.pagination li a:eq(' + i + ')').text('');
        }
        for (var i=1;i<=last;i++) {
            $('ul.pagination li a:eq(' + i + ')').attr('href', url+'page=' + (i + page * 5-5));
            $('ul.pagination li a:eq(' + i + ')').text(i + page * 5-5);
        }
    }
    if(page == pages) {
        next.text("到底");
        next.attr('disabled', true);
        for (var i = 1; i <= 5; i++) {
            $('ul.pagination li a:eq(' + i + ')').attr('href', url + 'page=' + (i + page * 5 - 5));
            $('ul.pagination li a:eq(' + i + ')').text(i + page * 5 - 5);
        }
    }



    next.click(function (e) {
        e.preventDefault();
        if ($(this).attr('disabled')){
            return;
        }
        var page = parseInt(nav.attr('data-page'));
        nav.attr('data-page',page+1);
        pre.html('<span aria-hidden="true">&laquo;</span>');
        $('a#pre').attr('disabled',false);
        for (var i=1;i<=5;i++) {
            $('ul.pagination li a:eq(' + i + ')').attr('href', url+'page=' + (i + page * 5));
            $('ul.pagination li a:eq(' + i + ')').text(i + page * 5);
        }
        if (page<pages-1){
        }else if(page==pages-1){
            $(this).text("到底");
            $(this).attr('disabled',true);
        }else {
            $(this).text("到底");
            $(this).attr('disabled',true);
            for (var i=1;i<=5;i++) {
                $('ul.pagination li a:eq(' + i + ')').attr('href','javascript:void(0);');
                $('ul.pagination li a:eq(' + i + ')').text('');
            }
            for (var i=1;i<=last;i++) {
                $('ul.pagination li a:eq(' + i + ')').attr('href', url+'page=' + (i + page * 5));
                $('ul.pagination li a:eq(' + i + ')').text(i + page * 5);
            }
        }
    });

    pre.click(function (e) {
    e.preventDefault();
    if ($(this).attr('disabled')){
        return;
    }
    var page = parseInt(nav.attr('data-page'));
    nav.attr('data-page',page-1);
    next.html('<span aria-hidden="true">&raquo;</span>');
    next.attr('disabled',false);
    if (page>2){

    }else {
        $(this).text("到头");
        $(this).attr('disabled',true);
    }
    for (var i=1;i<=5;i++){
        $('ul.pagination li a:eq('+i+')').attr('href',url+'page='+(i+page*5-10));
        $('ul.pagination li a:eq('+i+')').text(i+page*5-10);
    }
    });
});