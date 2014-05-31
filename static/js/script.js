(function(){

    $(function(){

        // Card mask
        $.getScript('/static/js/jquery.mask.min.js', function(){

            var $inputCard = $('#present\\[cardnumber\\], #card_source');

            $inputCard.mask('0000-0000-0000-0000');

            $('form[role="presentSubmit"]').on('submit', function(){
                $inputCard.val($inputCard.val().replace(/-/g,''));
            });

        });

    });

})();