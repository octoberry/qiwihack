$(function () {
    var $form = $('form[role="visaSubmit"]'),
        $cardnumberField = $('#card_number'),
        $errorContainer = $('#form-errors'),
        $overlay = $('#overlay'),
        overlayShowClass = 'overlay--show';

    // show errors
    app.formValidate(app.errors, $errorContainer);

    // add input mask
    $cardnumberField.mask('0000-0000-0000-0000');

    // card number issuer detection
    function MasterCardNotice(field) {
        var $noticeLabel = $('#mc_notice'),
            card = field.val().replace(/-/g, ''),
            mcRegex = '^5[1-5][0-9]{5,}$';

        if (card.match(mcRegex)) {
            $noticeLabel.text('На MasterCard деньги зачисляются до трех дней.')
        } else {
            $noticeLabel.text('')
        }
    }

    $cardnumberField.bind('blur change', function(){
        MasterCardNotice($cardnumberField);
    });

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
                $overlay.addClass(overlayShowClass);
                app.clearErrors();
            },
            complete: function() {
                $overlay.removeClass(overlayShowClass);
                $cardnumberField.trigger('keyup');
            },
            error: function() {
                $overlay.removeClass(overlayShowClass);
                app.formValidate({error: 'Произошла ошибка'}, $errorContainer);
            }
        })
    });

});

