$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var telephoneE = $('input[name=telephone]') ;
        var passwordE = $('input[name=password]');
        var rememberE = $('input[name=remember]');

        var tel = telephoneE.val();
        var pwd = passwordE.val();
        var remember = rememberE.prop('checked') ? 1 : 0;


        csrfajax.post({
            url: '/signin/',
            data: {
                telephone: tel,
                password: pwd,
                remember: remember
            },
            success: function (data) {
                if (data.code == 200) {
                    var return_to = $('#return-to').text();
                    window.location = return_to
                } else {
                    stalert.alertInfo(data.message)
                }
            },
            fail: function (data) {
                stalert.alertNetworkError()
            }
        })

    })

});