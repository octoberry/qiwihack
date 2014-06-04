/**
 * Created by echuvelev on 03/06/14.
 */
define(['jquery', 'underscore', 'backbone', 'handlebars',
    'ProposalModel', 'ProposalCollection',
    'text!/static/templates/create-proposal.html','jquery.serializeObject'],
    function($, _, Backbone, Handlebars, ProposalModel, ProposalCollection, CreateProposalTemplate){


    _.extend(Backbone.Validation.callbacks, {
        valid: function(view, attr, selector) {

        },
        invalid: function(view, attr, error, selector) {
            var classError = 'form-item__error--show',
                $blockError1 = $('#block-error1'),
                $blockError2 = $('#block-error2');

            switch (attr) {
                case 'image':
                    $blockError1.append(error + ' / ').addClass(classError);
                    break;
                case 'description':
                    $blockError1.append(error + ' / ').addClass(classError);
                    break;
                case 'amount':
                    $blockError2.append(error + ' / ').addClass(classError);
                    break;
                case 'card':
                    $blockError2.append(error + ' / ').addClass(classError);
                    break;
            }
        }
    });

    var ProposalList = new ProposalCollection();

    var CreateProposalView = Backbone.View.extend({

        el: $('#app-container'),

        template: Handlebars.compile(CreateProposalTemplate),

        events: {
            'submit form[role="presentSubmit"]': 'saveProposal'
        },

        initialize: function(){
            var self = this;

            this.render();
            this.uploadImage();
            this.model = new ProposalModel;

            require(['jquery.fileupload','jquery.iframe-transport'], function(){
                $('#fileupload').fileupload({
                    dataType: 'json',
                    done: function (e, data) {
                        self.uploadImage(data);
                    }
                });
            });

            Backbone.Validation.bind(this);
        },

        render: function(){
            this.$el.html(this.template());
            return this;
        },

        uploadImage: function(data){
            var imageUrl = $('#image')[0],
                $imageWrapper = $('.present__photo'),
                $button = $('.present__fileupload-button');

            if(data){
                imageUrl.value = data.result.file.url
            }

            $imageWrapper.css('background-image', 'url(' + imageUrl.value + ')');

            if(imageUrl.value){
                $('.present__icon').hide();
                $button.html('Изменить');
                $('.form-item__error', $imageWrapper).removeClass('form-item__error--show');
            }
        },

        saveProposal: function(event) {
            event.preventDefault();

            var $cardField = $('#present\\[cardnumber\\]');
            $cardField.val($cardField.val().replace(/-/g,''));

            $('#block-error1, #block-error2').html('').removeClass('form-item__error--show');

            var proposalData = $('form[role="presentSubmit"]').serializeObject();

            this.model.set(proposalData);

            if( this.model.isValid(true) ){
//                ProposalList.add(this.model); // for normal use sync
                ProposalList.create(proposalData); // for localStorage adapter
            }
        }

    });

    var CreateProposalViewPage = new CreateProposalView

});