function replaceMask($cardField){
    $cardField.val($cardField.val().replace(/-/g,''));
}

(function(){

    $(function(){

        var $inputCard = $('#present\\[cardnumber\\]');

            $inputCard.mask('0000-0000-0000-0000');

            $('form[role="presentSubmit"]').on('submit', function(){
                replaceMask($inputCard);
            });
    });

})();
