$(function () {
    var $form = $('form[role="giftSubmit"]'),
        $uploadPhotoButtonWrapper = $('.gift__photo_fileupload-button'),
        $uploadPhotoButton = $('button', $uploadPhotoButtonWrapper),
        $photoContainer = $('.gift__photo'),
        $cardnumberField = $('#card', $form),
        $errorContainer = $('#form-errors', $form);

    function updateGift(link) {
        var imageUrl = $('input[name="image"]', $form);
        imageUrl.attr('value', link);
        $photoContainer.find('.gift__photo_icon').hide();
        $photoContainer.css('background-image', 'url(' + link + ')');
        $uploadPhotoButton.text('Изменить');
        $uploadPhotoButtonWrapper.css({ 'top': 0, 'bottom': 0 });

    }

    // show errors
    app.formValidate(app.errors, $errorContainer);

    // add input mask
    $cardnumberField.mask('0000-0000-0000-0000');

    // get image url from localStorage
    if ( localStorage.giftImageLink ) {
        updateGift(localStorage.giftImageLink);
    }

    // upload image
    $('#fileupload').fileupload({
        dataType: 'json',
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $uploadPhotoButton.text(progress+'%');
        },
        done: function (e, data) {
            localStorage.giftImageLink = data.result.file.url;
            updateGift(data.result.file.url)
        },
        fail:  function (e, data) {
            $uploadPhotoButton.text('Загрузить фотографию');
            alert('Произошла ошибка при загрузке файла.');
        }
    });

    // send form handler
    $form.on('submit', function(e) {
        e.preventDefault();
        $cardnumberField.val($cardnumberField.val().replace(/-/g,''));

        $.ajax({
            method: 'POST',
            data: $form.serialize(),
            dataType: 'json',
            success: function(res) {
                switch (res.status) {
                    case 'success':
                        location.href = res.url;
                        break;
                    case 'card_auth_error':
                        alert('Ошибка авторизации карты');
                        break;
                    case 'validation_failed':
                        app.formValidate(res.errors, $errorContainer);
                        break;
                    default:
                        alert('Произошла ошибка');
                }
            },
            error: function() {
                alert('Произошла ошибка');
            }
        })
    });

});

