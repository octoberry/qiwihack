(function(){

    $('#card_source').mask('0000-0000-0000-0000');

    var minWeight = 85,
        $donateWidget = $('.donate-progressbar'),
        donateWidgetWidth = $donateWidget.width() - 15,
        $donateAmount =$('.donate-progressbar__value', $donateWidget);

    function progressBar(amount, goal) {
        var procentAmount = ( parseInt(amount) / parseInt(goal) ) * 100,
            progressBarValue = ( donateWidgetWidth / 100 ) * procentAmount

        if(progressBarValue < minWeight){
            $donateAmount.css({'width': minWeight + 'px'});
        }else if(amount > goal){
            $donateAmount.css({'width': donateWidgetWidth + 'px'});
        }else{
            $donateAmount.css({'width': progressBarValue + 'px'});
        }

        $donateAmount.html(amount.toFixed(2) + ' руб.');
    }

    progressBar(currentAmount, goalAmount);

})();

function attemptTransfer($form) {

    var form = $form[0],
        data = form_data($form),
        $errorContainer = $('#form-errors', $form);

    //TODO add object with errors from backend
    // example response json with error
    var mockObjectWithErrors = {
        'transfer_amount': ['Укажите сумму перевода'],
        'card_source': ['Укажите номер кредитной карты'],
        'exp_month': ['Укажите exp_month кредитной карты'],
        'exp_year': ['Укажите exp_year кредитной карты'],
        'cvv': ['Укажите CVV-код кредитной карты']
    };

    data.card_number = data.card_number.replace(/-/g,'');
    console.log(data);
    $.ajax({
        type: "POST",
        url: $form.attr('action'),
        data: data,
        dataType: 'json',
        beforeSend: function() {
            $('#save').html($('<img>',{
                src: '/static/images/ajax-loader.gif'
            })).css({ 'width': '201px', 'height': '45px'}).attr('disabled','disabled');
        },
        complete: function() {
            $('#save').html('Отправить').removeAttr('disabled');
        },
        success: function(res) {
            console.log(res);
            switch (res.result) {
                case 'required_3ds':
                    $.redirect(res);
                    break;
                case 'validation_failed':
                    app.formValidate(res.errors, $errorContainer);
                    break;
                case 'card_auth_error':
                    alert('Ошибка авторизации карты');
                    break;
                default:
                    alert('Произошла ошибка');
            }
        },
        error: function() {
            alert('Произошла ошибка');
        }
    });
}
function form_data($form) {
    var fields = $form.find('input[name],select[name]');
    var data = {};
    for (var i in fields) {
        var field = fields[i];
        data[field.name] = field.value;
    }
    return data;
}

$(function() {
    var $form = $('form');
    $('#save').on('click', function(e) {
        e.preventDefault();
        attemptTransfer($form);
    });
});
