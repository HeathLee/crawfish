!function ($) {
    $('.note-user-box-tab').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })

    $('.note-mine-box-tab').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })

    $('.note-user-box-tab').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })

    $('#word-content').text(data['words'][0]['content']);
    $('#cn_definition').text(data['words'][0]['cn_definition']);
    $.get('/get_sentences?word=' + data['words'][0]['content'], function (response) {
        if (response != null) {
            $('#affix').after(response["sentence"])
        }
    }, 'json')

    var count = 1
    $('.continue-button').on('click', function () {
        if (count == data['words'].length) {
            window.location.href = '/finished_today';
        }
        $('#affix').next().remove()
        $('#word-content').text(data['words'][count]['content']);
        $('#cn_definition').text(data['words'][count]['cn_definition']);
        $.get('/get_sentences?word=' + data['words'][count]['content'], function (response) {
            if (response != null) {
                $('#affix').after(response["sentence"])
            }
        }, 'json')
        count += 1;
    })
}(jQuery)