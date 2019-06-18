/**
 * Created by zhuzhengyang on 2019/6/6.
 */
$(function () {
    var url = window.location.href;
    if (url.match(/\/service/)){
        $("li.service-li").css("background-color","red");
    }
    else if(url.match(/\/solution/)){
        $("li.solution-li").css("background-color","red");
    }
    else if(url.match(/\/info/)){
        $("li.info-li").css("background-color","red");
    }
    else if(url.match(/\/about/)){
        $("li.about-li").css("background-color","red");
    }
    else if(url.match(/http\:\/\/.*?5002\/$/)){
        $("li.index-li").css("background-color","red");
    }
})