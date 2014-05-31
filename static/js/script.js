(function(){

    $(function(){

        // Card mask
        $.getScript('/static/js/jquery.mask.min.js', function(){

            var $inputCard = $('#present\\[cardnumber\\], #card_source');

            $inputCard.mask('0000-0000-0000-0000');

            function replaceMask(){
                $inputCard.val($inputCard.val().replace(/-/g,''));
            }

            $('form[role="presentSubmit"]').on('submit', function(event){
                replaceMask();
            });

            $('form[role="donateSubmit"] .button').on('click', function(){
                replaceMask();
            });
        });

    });

})();