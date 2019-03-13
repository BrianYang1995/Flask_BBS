
$(function () {
    $('#add-board').click(function (event) {
        event.preventDefault();
        stalert.alertOneInput({
            title: '请输入板块名称',
            confirmCallback: function (data) {
                var name = data;
                csrfajax.post({
                    url: '/cms/aboards/',
                    data: {
                        name: name,
                    },
                    success: function (data) {
                        if (data.code == 200) {
                            window.location.reload();
                        } else {
                            stalert.alertInfo(data.message)
                        }
                    },
                    fail: function (data) {
                        stalert.alertNetworkError()
                    }
                })
            }
        })
    })

});

$(function () {
    $('.edit-board').click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();

        var name = tr.attr('data-name');
        var id = tr.attr('data-id');

        stalert.alertOneInput({
            'title': '编辑板块名称',
            'placeholder': name,
            'confirmCallback': function (data) {
               csrfajax.post({
                   url: '/cms/uboards/',
                   data: {
                       'id': id,
                       'name': data
                   },
                   success: function (data) {
                       if (data.code == 200) {
                           window.location.reload()
                       } else {
                           stalert.alertInfo(data.message)
                       }
                   },
                   fail: function (data) {
                       stalert.alertNetworkError()
                   }
               })
           }
        });

    })
});

$(function () {
    $('.delete-board').click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();

        stalert.alertConfirm({
            'title': '确认删除该板块？',
            'confirmCallback': function () {
                var id = tr.attr('data-id');
                csrfajax.post({
                    'url': '/cms/dboards/',
                    'data': {
                        'id':id,
                    },
                    success: function (data) {
                        if (data.code == 200) {
                            window.location.reload()
                        } else {
                            stalert.alertInfo(data.message)
                        }
                    },
                    fail: function () {
                        stalert.alertNetworkError()
                    }
                })
            }
        })


    })
})