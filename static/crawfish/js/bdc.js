!function ($) {
    var count = 1; // word count

    var add_self_note_to_page = function (note) {
        $('#self-notes-ol').append('<li id="note-'+note['id']+'" class="row">\
                    <div class="span9"><div class="index pull-left">*.</div>\
                    <div class="pull-left content"><span>' + note['content'] + '</span>\
                </div><div class=""><div class="actions btn-group \
                 pull-right"><a note-id="'+note['id']+'" class="btn delete-note"\
                  style="display: \
                   inline;">删除</a></div></div><div class="edit-note-box">\
                <div class="modal hide edit-note-modal" style="display: none;">\
                <div class="modal-header"> <button class="close"\
                 data-dismiss="modal">&nbsp;</button><h3>编辑笔记</h3></div>\
                 <div class="modal-body"><p></p><form><textarea class="note-textarea span7"\
            rows="4">' + note['content'] + '</textarea></form><p></p></div>\
                 <div class="modal-footer"><a href="#" class="btn"\
                  data-dismiss="modal">关闭</a> <a href="#" class="btn\
                   btn-danger delete" data-dismiss="modal">删除</a> <a href="#"\
                   class="btn btn-primary save" data-dismiss="modal">保存</a>\
                </div></div></div></div></li>');
        delete_note()
    };

    var fill_content = function (index) {
        var word = data['words'][index];
        $('#word-content').text(word['content']);
        $('#cn_definition').text(word['cn_definition']);

        // add others notes
        if (data['others_notes']) {
            var others_notes = data['others_notes'][index];
            var htmlStr = '';
            for (var j = 0; j < others_notes.length; j++) {
                htmlStr += '<li class="row"><div class="span9"> <div\
            class="index pull-left">' + j + '.</div><div class="pull-left content">\
            <span>' + others_notes[j]['content'] + '</span></span> <div \
             class="author">作者<a>' + others_notes[j]['user_name'] + '</a>\
            </div></div><div class="edit-note-box"></div></div></li>';
            }
            $('#other-notes-ol').append(htmlStr);
        }

        //add self-note
        if (data['self_notes']) {
            var self_notes = data['self_notes'][index];
            var htmlStr2 = '';
            for (var i = 0; i < self_notes.length; i++) {
                htmlStr2 +=
                    '<li id="note-'+self_notes[i]['id']+'" class="row">\
                    <div class="span9"><div class="index pull-left">*.</div>\
                    <div class="pull-left content"><span>' + self_notes[i]['content'] + '</span>\
                </div><div class=""><div class="actions btn-group \
                 pull-right"><a note-id="'+self_notes[i]['id']+'" class="btn\
                  delete-note" style="display:\
                   inline;">删除</a></div></div><div class="edit-note-box">\
                <div class="modal hide edit-note-modal" style="display: none;">\
                <div class="modal-header"> <button class="close"\
                 data-dismiss="modal">&nbsp;</button><h3>编辑笔记</h3></div>\
                 <div class="modal-body"><p></p><form><textarea class="note-textarea span7"\
            rows="4">' + self_notes[i]['content'] + '</textarea></form><p></p></div>\
                 <div class="modal-footer"><a href="#" class="btn"\
                  data-dismiss="modal">关闭</a> <a href="#" class="btn\
                   btn-danger delete" data-dismiss="modal">删除</a> <a href="#"\
                   class="btn btn-primary save" data-dismiss="modal">保存</a>\
                </div></div></div></div></li>';
            }
            $('#self-notes-ol').append(htmlStr2);
        }


        $.get('/get_sentence/?shanbay_id=' + word['shanbay_id'], function (response) {
            if (response != null) {
                $('#affix').after(response["sentence"])
            }
        }, 'json');

        $.getJSON('http://words.bighugelabs.com/api/2' +
            '/eb4e57bb2c34032da68dfeb3a0578b68/'+word['content']+'/json?callback=', function (response) {
            var result = '';
            for (var item in response) {
                for (var x in response[item]) {
                    if (response[item][x] && response[item][x].length >= 2) {
                        result += response[item][x][0] + '; ' + response[item][x][1];
                        $('#synonyms').text(result);
                        return;
                    }
                }
            }
        });

    };

    $('.note-user-box-tab').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })

    $('.note-mine-box-tab').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })

    $('#create-note').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })

    //init
    fill_content(0);
    // next word
    $('.continue-button').on('click', function () {
        if (count == data['words'].length) {
            window.location.href = '/finished_today';
        }
        $('#learning-examples-box').remove();
        $('#self-notes-ol').empty();
        $('#other-notes-ol').empty();
        $('#synonyms').text('');
        fill_content(count);
        count += 1;
    })

    // add note
    $('#add-note').click(function (e) {
        e.preventDefault();
        var content = $('#add-note-text').val();
        if (!content) {
            alert("笔记内容不能为空");
        } else {
            $.post('/add_note', {
                'content': content,
                'word_id': data['words'][count - 1]['word_id']
            }, function (response) {
                if (response['code'] == 0) {
                    add_self_note_to_page(response['note']);
                    $('#add-note-text').val('');
                    $('.note-mine-box-tab').trigger('click');
                } else {
                    alert('添加笔记失败');
                }
            }, 'json')
        }
    });
    
    //delete note
    var delete_note = function() {
        $('.delete-note').on('click', function (e) {
            e.preventDefault();
            var note_id = $(this).attr('note-id');
            $.post('/delete_note', {
                'note_id': note_id
            }, function (response) {
                if (response['code'] == 0) {
                    $('#note-' + note_id).remove();
                } else {
                    alert("删除笔记失败");
                }
            }, 'json')
        })
    }
    delete_note();
}(jQuery)