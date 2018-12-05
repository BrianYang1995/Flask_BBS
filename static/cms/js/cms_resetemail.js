// 获取验证码
$(function () {
    $('#captcha-btn').click(function (event) {
        email = $('#email').val()
        csrfajax.get({
            'url': '/cms/captcha_email/',
            'data': {
                'email': email
            },
            'success': function (data) {
                console.log(data)
                if (data.code == 200) {
                    stalert.alertSuccessToast('发送验证码成功')
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

// 提交验证码
$(function () {
    $('#submit').click(function (event) {
        event.preventDefault()

        var emailE = $('#email')
        var captchaE = $('#captcha')

        email = emailE.val()
        captcha = captchaE.val()

        csrfajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data.code == 200) {
                    stalert.alertSuccessToast('修改邮箱成功')
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