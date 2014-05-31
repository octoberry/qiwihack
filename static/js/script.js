(function(){

    $(function(){

       var presentRequestSend = $.ajax({
           url: '/',
           type: 'post'
       });

        presentRequestSend.done(function(response){
        });

    });

})();