
!function ($) {
    $('#set-word-limit').on('click', function (e) {
        window.location.href = '/set_word_limit'
    });

    $('#set-level').on('click', function () {
        window.location.href = '/set_level'
    });

    $('#start-learning').on('click', function () {
        if (!$(this).hasClass('disabled')) {
            window.location.href = '/bdc'
        }
    });

}(jQuery);

