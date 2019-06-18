
$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        if(that.children('a').attr('href') == '#'){
            event.preventDefault();
        }
        if(that.parent().hasClass('unfold')){
            that.parent().removeClass('unfold');
        }else{
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
    });

    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration','none');
    });
});


$(function () {
    var url = window.location.href;
    if(url.indexOf('profile') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(0).addClass('active').siblings().removeClass('active');
    }  else if(url.indexOf('resetemail') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(2).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('postings') >= 0){
        var postManageLi = $('.posting');
        postManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('boards') >= 0){
        var boardManageLi = $('.board-manage');
        boardManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('post_manage') >= 0){
        var boardManageLi = $('.post-manage');
        boardManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('banner_manage') >= 0) {
        var bannerManageLi = $('.banner-manage');
        bannerManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('message') >= 0) {
        var userManageLi = $('.message');
        userManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
});