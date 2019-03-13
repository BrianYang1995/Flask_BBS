$(function () {
    var ue = UE.getEditor('editor', {
        serverUrl: '/ueditor/upload/',
        toolbars: [
            [
                'anchor', //锚点
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'indent', //首行缩进
                'subscript', //下标
                'superscript', //上标
                'insertcode', //代码语言
                'simpleupload', //单图上传
                'insertimage', //多图上传
                'link', //超链接
                'emotion', //表情
                'spechars', //特殊字符
                'forecolor', //字体颜色
                'insertorderedlist', //有序列表
                'insertunorderedlist', //无序列表
            ],
        ],
        initialFrameHeight: '120',
        maximumWords: 3000,
    });

    window.ue = ue;
});

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var post_id = self.attr('data-post-id');
        var comment_content = window.ue.getContent();

        csrfajax.post({
            url: '/acomment/',
            data: {
                post_id: post_id,
                content: comment_content
            },
            success: function (data) {
                if (data.code == 200) {
                    stalert.alertInfoToast('评论成功')
                    setTimeout(function () {
                        window.location.reload()
                    }, 500)
                } else {
                    stalert.alertInfoToast(data.message)
                }
            },
            fail: function () {
                stalert.alertNetworkError()
            }
        });
    })
});