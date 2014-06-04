/**
 * Created by echuvelev on 03/06/14.
 */
var require = {
    baseUrl: '/static',
    paths: {

        // libs && vendors
        'jquery': 'bower_components/jquery/dist/jquery.min',
        'backbone': 'bower_components/backbone/backbone',
        'localstorage': 'bower_components/Backbone.localStorage/backbone.localStorage',
        'backbone-validation': 'bower_components/backbone-validation/dist/backbone-validation-amd',
        'underscore': 'bower_components/underscore/underscore',
        'handlebars': 'bower_components/handlebars/handlebars.min',
        'text': 'bower_components/text/text',
        'jquery.ui.widget': 'js/vendor/jquery.ui/jquery.ui.widget',
        'jquery.fileupload': 'js/vendor/jquery.fileupload/jquery.fileupload',
        'jquery.iframe-transport': 'js/vendor/jquery.fileupload/jquery.iframe-transport',
        'jquery.serializeObject': 'js/vendor/jquery.serializeObject',

        // app
        'ProposalModel': 'js/ProposalModel',
        'ProposalCollection': 'js/ProposalCollection'
    },

    shim: {

        'handlebars': {
            exports: 'Handlebars'
        }

    }
};