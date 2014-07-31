Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

app.formValidate = function(errors, $errorContainer){

    var $errorListContainer = $('.form-errors__list', $errorContainer);

    $errorListContainer.html('');

    if( Object.size(errors) ) {

        $errorContainer.addClass('form-errors--show');

        for (var error in errors) {

            var $field = $('[name="'+ error +'"]'),
                $fieldWrapper = $field.parents('.input-item');

            $fieldWrapper.addClass('input-item--error');

            var $errorNode = $('<span/>',{
                class: 'form-errors__item',
                text: errors[error],
                title: errors[error],
                'data-id': error,
                click: function() {
                    var $field = $('#' + $(this).data('id'));
                    $('body').animate({
                        scrollTop: $field.offset().top
                    }, 300);
                    $field.focus();
                }
            });

            $errorListContainer.append($errorNode);
        }

    }
};

app.clearErrors = function($errorContainer) {
    $('.form-errors__list', $errorContainer).html('');
    $('.input-item--error').removeClass('input-item--error');
};