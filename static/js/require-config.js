/**
 * Created by echuvelev on 03/06/14.
 */
var require = {
    baseUrl: '/static',
    paths: {
        'jquery': 'bower_components/jquery/dist/jquery.min',
        'backbone': 'bower_components/backbone/backbone',
        'underscore': 'bower_components/underscore/underscore',
        'jquery.ui.widget': 'js/vendor/jquery.ui/jquery.ui.widget',
        'handlebars': 'bower_components/handlebars/handlebars.min',
        'text': 'bower_components/text/text'
    },

    bundles: {
        'fileupload': [
            'js/vendor/jquery.fileupload/jquery.fileupload',
            'js/vendor/jquery.fileupload/jquery.iframe-transport'
        ]
    },

    shim: {

        'handlebars': {
            exports: 'Handlebars'
        }

    }
};