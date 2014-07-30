function expdate($form) {
    var exp_month = $form.find('[name="exp_month"]').val();
    var exp_year = $form.find('[name="exp_year"]').val();
    $form.find('[name="card_expdate"]').val(exp_month + exp_year);
}

$(function() {
    $('[name="exp_month"], [name="exp_year"]').on('change', function() {
        expdate($(this).closest('form'))
    });
});