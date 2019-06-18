/**
 * Created by zhuzhengyang on 2019/6/16.
 */
$(function () {
    var searchResult_div = $('div.search-container')
    var replaceHtml = searchResult_div.html();
    var search = searchResult_div.attr('data-search');
    reger = new RegExp("(" + search + ")","gim");
    reslut = replaceHtml.replace(reger, "<font color='red'>$1</font>");
    searchResult_div.html(reslut);


})
