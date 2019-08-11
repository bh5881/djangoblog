$(()=>{
   //1点击刷新图片验证码
    $('.captcha-graph-img img').click(function () {
        $(this).attr('src','/image_code/?rand='+Math.random())
    });
    //校验功能
    //定义一些状态变量
    let isUsernameReady = false,
        isPasswordReady = false,
        isMobileReady = false,
        isSmsCodeReady = false;
    let $username = $('#username');
    $username.blur(fnCheckUsername);
    function fnCheckUsername() {//es6一般用驼峰命名，fn代表函数
        // 可以先使用alert来测试鼠标移开的效果
        // alert('ok')
        //校验用户名
        isUsernameReady = false;
        //获取输入的用户名
        let sUsername = $username.val();
        //这里需要校验
        if(sUsername ===''){
            message.showError('用户名不能为空');
            return//注意此处的return，否则会继续往下执行
        }
        if (!(/^\w{5,20}$/).test(sUsername)){
            //注意上面的额正则表达式和test的由来
            message.showError('请输入5-20个字符的用户名');
            return
        }
        $
            .ajax({
            url:'/username/'+sUsername + '/', //注意此处三个/的位置
            type: 'GET',
            dataType:'json',
            success:function (res) {//浏览器会将返回的json数据赋值给res
                if (res.data.count !== 0){
                    //此处注意返回的直接是一个字典，因此直接取值，不能用res.data.count
                    message.showError(res.data.username+'用户名已经注册，请重新输入')
                }else{
                    message.showInfo(res.data.username+'可以正常使用');
                    isUsernameReady = true;
                    return
                }
            },
                error:function () {
                message.showError('服务器超时，请重新输入')

                }
        })
    }
    // 3.检测密码是否一致
    //获取鼠标离开第二个密码框的事件
    let $passwordRepeat = $('input[name="password_repeat"]');
    $passwordRepeat.blur(fnCheckPassword);

    function fnCheckPassword () {
        isPasswordReady = false;
        let password = $('input[name="password"]').val();
        let passwordRepeat = $passwordRepeat.val();
        if (password === '' || passwordRepeat === ''){
            message.showError('密码不能为空');
            return
        }
        if (password !== passwordRepeat){
            message.showError('两次密码输入不一致');
            return
        }
        if (password === passwordRepeat){
            isPasswordReady = true
        }
    }

        // 4.手机号码校验
    let $mobile = $('input[name="mobile"]');
    $mobile.blur(fnCheckMobile);

    function fnCheckMobile() {
        isMolibleReady = false;
        let sMobile = $mobile.val();
        if (sMobile === ''){
            message.showError('手机号码不能为空！');
            return
        }

        if(!(/^1[3-9]\d{9}$/).test(sMobile)){
            message.showError('手机号码格式不正确！');
            return
        }
        // 发送ajax
        $
            .ajax({
                url: '/mobile/' + sMobile + '/',
                type: 'GET',
                dataType: 'json'
            })
            .done((res)=>{
                if(res.data.count !== 0){
                    message.showError(res.data.mobile + '手机号已经注册，请重新输入！')
                }else{
                    message.showInfo(res.data.mobile + '可以正常使用！');
                    isMolibleReady = true
                }
            })
            .fail(()=>{
                message.showError('服务器超时，请重试！')
            })

    }

    //5发送短信验证码
    let $smsButton = $('.sms-captcha');
    $smsButton.click(()=>{
        //拿到数据
        let sCaptcha = $('input[name="captcha_graph"]').val();
        if (sCaptcha===''){
            message.showError('请输入图形验证码')
            return
        }
        //判断手机号码是否准备好
        if(!isMobileReady){
            fnCheckMobile();
            // alert('so')
            return
        }
        $
            .ajax({
                url:'/sms_code/',
                type:'POST',
                data:{
                    mobile:$mobile.val(),
                    captcha:sCaptcha,
                },
                dataType:'json'
            })
            .done((res)=>{
                console(res)
                if (res.errno !=='0'){
                //if (res.errmsg)
                //     message.showError(res.errmsg)
                    message.showError("完成错误")
                }else{
                    // message.showSuccess(res.errmsg);
                    message.showSuccess("完成成功");
                    $smsButton.attr('disabled', true);
                    //倒计时
                    let num = 60;
                    //设置计时器
                    let t = setInterval(function () {
                        $smsButton.html('倒计时'+num+'秒');
                        if(num===1){
                            clearInterval(t);
                            $smsButton.removeAttr('disabled');
                            $smsButton.html('获取短信验证码')
                        }
                        num --;
                    }, 1000)
                }
            })
            .fail(()=>{
                message.showError('服务器超时，请重试')
            });
    })




});









