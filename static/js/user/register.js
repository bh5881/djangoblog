$(()=>{
   //1点击刷新图片验证码
    $('.captcha-graph-img img').click(function () {
        $(this).attr('src','/image_code/?rand='+Math.random())
    })
});