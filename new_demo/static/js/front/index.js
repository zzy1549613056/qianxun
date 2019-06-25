/**
 * Created by zhuzhengyang on 2019/6/7.
 */

function add_active(e) {
    $('li.solution-1').attr('class','solution-1');
    $('li.solution-2').attr('class','solution-2');
    $('li.solution-3').attr('class','solution-3');
    e.attr('class',function (i,val) {
        return val + ' active';
    });
};

function resize_width() {
    var width_1 = $('div.service-content>div').css('width');
    var width_div_1 = (1.4*Number(width_1.replace('px',''))).toString()+'px';
    $('div.service-content>div').css('height',width_div_1);
    var width_font1 = (0.12*Number(width_1.replace('px',''))).toString()+'px';
    $('div.service-title').css('font-size',width_font1);
    var width_font12 = (0.06*Number(width_1.replace('px',''))).toString()+'px';
    $('div.service-tip').css('font-size',width_font12);
    var width_font13 = (0.2 *Number(width_1.replace('px',''))).toString()+'px';
    $('div.service-pic').css('font-size',width_font13);
    var width_2 = $('div.info-content>div>div').css('width');
    var width_div_2 = (0.67*Number(width_2.replace('px',''))).toString()+'px';
    $('div.info-content>div>div:first-child').css('height',width_div_2);
    var width_font2 = (0.05*Number(width_2.replace('px',''))).toString()+'px';
    $('div.info-title').css('font-size',width_font2);

    var width_font3 = (0.06*Number(width_2.replace('px',''))).toString()+'px';
    $('ul.solution-bar li').css('font-size',width_font3);
};

$(function () {
    resize_width();
    $(window).resize(function () {
        resize_width();
    });

    $('.solution-banner').carousel({
        interval:false
    });
    $('li.solution-1').click(function (e) {
        e.preventDefault();
        add_active($(this));
        $('.solution-banner').carousel(0);
        $('.solution-tag').attr('href','/solution/1');
    });
    $('li.solution-2').click(function (e) {
        e.preventDefault();
        add_active($(this));
        $('.solution-banner').carousel(1);
        $('.solution-tag').attr('href','/solution/2');
    });
    $('li.solution-3').click(function (e) {
        e.preventDefault();
        add_active($(this));
        $('.solution-banner').carousel(2);
        $('.solution-tag').attr('href','/solution/3');
    });
})