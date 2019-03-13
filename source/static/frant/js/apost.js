$(function () {
    var ue = UE.getEditor('editor', {
        serverUrl: '/ueditor/upload/',
        initialFrameHeight: '500',
    });

    $('#submit').click(function (event) {
        event.preventDefault();
        var titleE = $('input[name=title]');
        var board_idE = $('select[name=board_id]');

        var title = titleE.val();
        var board_id = board_idE.val();

        var content = ue.getContent();

        csrfajax.post({
            url: '/apost/',
            data: {
                'title': title,
                'board_id': board_id,
                'content': content
            },
            success: function (data) {
                if (data.code == 200) {
                    stalert.alertConfirm({
                        title: '保存成功',
                       cancelText : '继续编辑',
                        confirmText: '完成',
                        confirmCallback: function () {
                            window.location.href = '/'
                        }

                    })
                } else {
                    stalert.alertInfo(data.message)
                }
            },
            fail: function () {
                stalert.alertNetworkError()
            }
        })

    });
});