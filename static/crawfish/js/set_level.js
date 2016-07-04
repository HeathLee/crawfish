
!function ($) {
    $('.span10').on('click', function () {
        level = $(this).attr('data');
        $.post('/set_level/',
            {
                level: level
            },
        function (data) {
            if (data['code'] != 0) {
                alert('修改level失败')
            } else {
                window.location.href = '/index'
            }
        }, 'json')
    });
}(jQuery);

