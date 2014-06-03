require(['jquery', '/static/js/vendor/jquery.mask/jquery.mask.min.js'], function(){

    $(function(){
        $('#present\\[cardnumber\\]').mask('0000-0000-0000-0000');
        $('#card_source').mask('0000-0000-0000-0000');
    });

});