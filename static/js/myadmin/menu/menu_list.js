$(() => {
    let $deleteBtns = $('button.delete');       // 删除按钮
    menuId = 0;                                 // 被点击菜单id
    let $currentMenu = null;                    // 当前被点击菜单对象

    $deleteBtns.click(function () {
        let $this = $(this);
        $currentMenu = $this.parent().parent();
        menuId = $this.parent().data('id');
        let menuName = $this.parent().data('name');

        // 改变模态框的显示内容
        $('#modal-delete .modal-body p').html('确定删除菜单:《' + menuName + '》？');
        // 显示模态框
        $('#modal-delete').modal('show');
    });

    // 点击模特框确定删除按钮，发送ajax删除
    $('#modal-delete button.delete-confirm').click(() => {
        deleteMenu()
    });

    // 删除菜单的函数
    function deleteMenu() {
        $
            .ajax({
                url: '/myadmin/menu/' + menuId + '/',
                type: 'DELETE',
                dataType: 'json'
            })
            .done((res)=>{
                if (res.errno === '0'){
                    // 关闭模态框
                    $('#modal-delete').modal('hide');
                    // 删除菜单元素
                    $currentMenu.remove();
                    message.showSuccess(res.errmsg)
                }else{
                    message.showError(res.errmsg)
                }
            })
            .fail(()=>{
                message.showError('服务器超时，请重试！')
            })
    }

    let $editBtns = $('button.edit');           // 编辑按钮
    $editBtns.click(function () {
        let $this = $(this);
        $currentMenu = $this.parent().parent();
        menuId = $this.parent().data('id');

        // 发送ajax
        $
            .ajax({
                url: '/myadmin/menu/' + menuId + '/',
                type: 'GET'
            })
            .done((res)=>{
                // 改变模特框的内容
                $('#modal-update .modal-content').html(res);
                // 显示模特框
                $('#modal-update').modal('show')
            })
            .fail(()=>{
                message.showError('服务器超时，请重试！')
            })
    })

});