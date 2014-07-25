/**
* jquery.redirect.js v1.0
* Redirect the browser while submitting data using post or get methods
* https://github.com/skyrpex/jquery.redirect.js
*
* Copyright 2013, Cristian Pallarés
* Released under the MIT license.
*/
(function($) {
    $.redirect = function(options) {
        var settings = $.extend({
            url: '',
            method: 'post',
            data: {}
        }, options);

        var form = $("<form>");
        form.attr({
            action: settings.url,
            method: settings.method
        }).css({
            display: 'none'
        });

        for(var name in settings.data) {
            $('<input>').attr({
                type: 'hidden',
                name: name,
                value: settings.data[name]
            }).appendTo(form);
        }

        form.appendTo('body');
        form.submit();
    };
})(jQuery);
