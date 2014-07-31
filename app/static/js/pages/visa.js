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
                else {
                    app.formValidate({error: 'Произошла ошибка'}, $errorContainer);
                }
            },
            beforeSend: function() {
                app.clearErrors();
            },
            complete: function() {
                $cardnumberField.trigger('keyup');
            },
            error: function() {
                app.formValidate({error: 'Произошла ошибка'}, $errorContainer);
            }
        })
    });

});

