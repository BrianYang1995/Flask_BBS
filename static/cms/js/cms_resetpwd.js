
$(function () {
    $('#submit').click(function (event) {

        event.preventDefault()
        oldpwdE = $('input[name=oldpwd]')
        newpwdE = $('input[name=newpwd]')
        newpwd2E = $('input[name=newpwd2]')


        oldpwd = oldpwdE.val()
        newpwd = newpwdE.val()
        newpwd2 = newpwd2E.val()

        csrfajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                if (data.code == 200) {
                    stalert.alertSuccessToast('密码修改成功')
                    oldpwdE.val('')
                    newpwdE.val('')
                    newpwd2E.val('')
                } else {
                    stalert.alertInfo(data.message)
                }
            },
            'fail': function (data) {
                stalert.alertNetworkError()
            }
        })

    })
})


