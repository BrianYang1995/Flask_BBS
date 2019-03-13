$(function () {
    $('.mark-light').click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();

        var post_id = tr.attr('data-id');
        var mark_light = tr.attr('data-mark-light');

        if (parseInt(mark_light)) {
            var url = '/cms/umark/'
        } else {
            var url = '/cms/mark/'
        }

        csrfajax.post({
            url: url,
            data: {
                post_id: post_id
            },
            success: function (data) {
                if (data.code == 200) {
                    stalert.alertInfoToast('操作成功')
                    setTimeout(function () {
                        window.location.reload()
                    }, 500)
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