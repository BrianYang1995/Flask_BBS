$(function () {
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = randomparam.setParam(src,'new',Math.random());
        self.attr('src',newsrc);
    })

    $('#msm-btn').click(function (event) {
        event.preventDefault()
        var self = $(this)
        var tel = $('input[name=telephone]').val()

        if (!(/^1[34578]\d{9}$/.test(tel))) {
            stalert.alertInfoToast('手机号格式错误')
            return ;
        }

        var timestamp = (new Date()).getTime()
        var sign = md5(tel + 'jfla&klga#lav%78^hfak83u89t3fa3i&j389' + timestamp )
        csrfajax.post({
            url: '/c/sms_captcha/',
            data: {
                telephone: tel,
                timestamp: timestamp,
                sign: sign
            },
            success: function (data) {
                if (data.code == 200){
                    self.attr('disabled', 'disabled')
                    var time_count = 60
                    timer = setInterval(function () {
                        self.text(time_count+'秒后重新获取')
                        if (time_count-- == 0) {
                            clearInterval(timer)
                            self.removeAttr('disabled')
                            self.text('获取短信验证码')
                        }
                    }, 1000)
                } else {
                    stalert.alertInfoToast(data.message)
                }

            },
            fail : function (data) {
                stalert.alertNetworkError()
            }
        })
    })
})

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault()
        var telephoneE = $('input[name=telephone]');
        var sms_captchaE = $('input[name=sms-captcha]');
        var usernamE = $('input[name=username]')
        var passwordE = $('input[name=password]')
        var password2E = $('input[name=password2]')
        var img_captchaE = $('input[name=captcha]')

        var telephone = telephoneE.val()
        var sms_captcha = sms_captchaE.val()
        var username = usernamE.val()
        var password = passwordE.val()
        var password2 = password2E.val()
        var img_captcha = img_captchaE.val()

        csrfajax.post({
            url: '/signup/',
            data: {
                telephone: telephone,
                username: username,
                password: password,
                password2: password2,
                sms_captcha: sms_captcha,
                img_captcha: img_captcha
            },
            success: function (data) {
                if (data.code == 200) {
                    var return_to = $('#return-to').text();
                    window.location = return_to;
                } else {
                    stalert.alertInfo(data.message);
                }
            },
            fail: function (data) {
                stalert.alertNetworkError()
            }
        })



    })

})