$(() => {
    // 1. 点击返回
    $('.box-footer button.back').click(() => {
        $('#content').load(
            $('.sidebar-menu li.active a').data('url'),
            (response, status, xhr) => {
                if (status !== 'success') {
                    message.showError('服务器超时，请重试！')
                }
            }
        );
    });
    // 2. 点击修改
    $('.box-footer button.save').click(function () {
        // 发送ajax
        $
            .ajax({
                url: $(this).data('url'),
                data: $('form').serialize(),
                type: $(this).data('type')
            })
            .done((res) => {
                if (res.errno === '0') {
                    message.showSuccess(res.errmsg);
                    // 跳转到 用户列表
                    $('#content').load(
                        $('.sidebar-menu li.active a').data('url'),
                        (response, status, xhr) => {
                            if (status !== 'success') {
                                message.showError('服务器超时，请重试！')
                            }
                        }
                    );
                }else{
                    // 失败了返回的是渲染了额错误信息的html
                    // 替换原有内容
                    $('#content').html(res)
                }
            })
            .fail(() => {
                message.showError('服务器超时，请重试！')
            })
    });

    // 3.复选框逻辑
    // 点击一级菜单，二级菜单联动
    // 勾选一级菜单，二级参数全选，取消一级菜单，二级菜单全取消
    $('div.checkbox.one').each(function () {
        let $this = $(this);
        $this.find(':checkbox').click(function () {
            if($(this).is(':checked')){
                // 选中状态
                $this.siblings('div.checkbox.two').find(':checkbox').prop('checked', true)
            }else{
                // 取消状态
                $this.siblings('div.checkbox.two').find(':checkbox').prop('checked', false)
            }
        })
    });

    // 点击二级菜单，一级菜单联动
    // 选中二级菜单，对应的一级菜单选中，取消所有二级菜单，对应的一级菜单取消
    $('div.checkbox.two').each(function () {
        let $this = $(this);
        $this.find(':checkbox').click(function () {
            if($(this).is(':checked')){
                // 选中
                $this.siblings('div.checkbox.one').find(':checkbox').prop('checked', true)
            }else{
                // 取消
                if(!$this.siblings('div.checkbox.two').find(':checkbox').is(':checked')){
                    $this.siblings('div.checkbox.one').find(':checkbox').prop('checked', false)
                }
            }
        })

    })

});