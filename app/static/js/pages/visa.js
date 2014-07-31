$(function () {
    var $form = $('form[role="visaSubmit"]'),
        $cardnumberField = $('#card'),
        $errorContainer = $('#form-errors');

    // show errors
    app.formValidate(app.errors, $errorContainer);

    // add input mask
    $cardnumberField.mask('0000-0000-0000-0000');

    // send form handler
    $form.on('submit', function(e) {
        e.preventDefault();
        $cardnumberField.val($cardnumberField.val().replace(/-/g, ''));

        $.ajax({
            method: 'POST',
            data: $form.serialize(),
            dataType: 'json',
            success: function(res) {
                if (res.url) {
                    location.href = res.url;
                }
                else if (res.errors) {
                    app.formValidate(res.errors, $errorContainer);
                }
                else if (res.status == 'card_auth_error') {
                    alert('Ошибка авторизации карты');
                }
                else {
                    alert('Произошла ошибка');
                }
            },
            beforeSend: function() {
                app.clearErrors();
            },
            complete: function() {
                $cardnumberField.trigger('keyup');
            },
            error: function() {
                alert('Произошла ошибка');
            }
        })
    });

});

