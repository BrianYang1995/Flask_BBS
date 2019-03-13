$(function () {
    $('#save').click(function (event) {
        event.preventDefault();
        self = $(this)
        var modal = $('#add-banner');
        var nameE = modal.find('input[name=title]');
        var img_urlE = modal.find('input[name=img_url]');
        var link_urlE = modal.find('input[name=link_url]');
        var priorityE = modal.find('input[name=priority]');

        var name = nameE.val();
        var img_url = img_urlE.val();
        var link_url = link_urlE.val();
        var priority = priorityE.val();


        console.log(name, img_url, link_url, priority)
        if (!name || !img_url || !link_url || !priority) {
            stalert.alertInfo('数据不完整')
            return;
        }


        data_type = self.attr('data-type');
        if (data_type == 'update') {
            url = '/cms/ubanner/';
            data_id = self.attr('data-id');
        } else {
            url = '/cms/abanner/';
            data_id = '0';
        }

        csrfajax.post({
            url: url,
            data: {
                name: name,
                img_url: img_url,
                link_url: link_url,
                priority: priority,
                banner_id: data_id
            },
            success: function (data) {
                modal.modal('hide');
                if (data.code == 200) {
                    window.location.reload()
                } else {
                    stalert.alertInfo(data.message)
                }
            },
            fail: function (data) {
                stalert.alertNetworkError();
            }
        })
    })
});


$(function () {
    $('.edit-banner').click(function (event) {
        event.preventDefault();
        var modal = $('#add-banner');
        modal.modal('show');
        self = $(this)
        var tr = self.parent().parent()

        var name = tr.attr('data-name')
        var img_url = tr.attr('data-img_url')
        var link_url = tr.attr('data-link_url')
        var priority = tr.attr('data-priority')
        var id = tr.attr('data-id')

        console.log(name, img_url, link_url, priority, id)

        var nameE = modal.find('input[name=title]');
        var img_urlE = modal.find('input[name=img_url]');
        var link_urlE = modal.find('input[name=link_url]');
        var priorityE = modal.find('input[name=priority]');

        nameE.val(name)
        img_urlE.val(img_url)
        link_urlE.val(link_url)
        priorityE.val(priority)

        var save_btn = modal.find('#save');
        save_btn.attr('data-type', 'update');

        save_btn.attr('data-id', id)
    })
});

$(function () {
    $('#add').click(function (event) {
        var modal = $('#add-banner');
        var nameE = modal.find('input[name=title]');
        var img_urlE = modal.find('input[name=img_url]');
        var link_urlE = modal.find('input[name=link_url]');
        var priorityE = modal.find('input[name=priority]');

        nameE.val('');
        img_urlE.val('');
        link_urlE.val('');
        priorityE.val('');

        var save_btn = modal.find('#save');
        save_btn.attr('data-type', 'add');

    })
});


$(function () {
    $('.delete-banner').click(function (event) {
        event.preventDefault()
        self = $(this)
        var tr = self.parent().parent()

        var banner_id = tr.attr('data-id')

        stalert.alertConfirm({
            msg: '确认删除轮播图？',
            confirmCallback: function () {
                csrfajax.post({
                    url: '/cms/dbanner/',
                    data: {
                        banner_id: banner_id
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

    qiniu.setUp({
        'domain': 'http://s.xpythonx.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/c/uptoken/',
        'success': function (up, file, info) {
            var imageInput = $("input[name='img_url']");
            imageInput.val(file.name);
        }
    });

});

$(function () {
    $('#upload-btn').click(function (event) {
        event.preventDefault();
    })
});