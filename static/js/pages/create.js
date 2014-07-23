$(function () {
    var $form = $('form[role="presentSubmit"]'),
        $uploadPhotoButtonWrapper = $('.present__photo_fileupload-button'),
        $uploadPhotoButton = $('button', $uploadPhotoButtonWrapper),
        $photoContainer = $('.present__photo'),
        $cardnumberField = $('#card', $form),
        $errorContainer = $('#form-errors', $form);

    function updateGift(link) {
        var imageUrl = $('input[name="image"]', $form);
        imageUrl.attr('value', link);
        $photoContainer.find('.present__photo_icon').hide();
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
    $form.on('submit', function(event){
        $cardnumberField.val($cardnumberField.val().replace(/-/g,''));
    });

});

