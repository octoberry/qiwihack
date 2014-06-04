/**
 * Created by echuvelev on 03/06/14.
 */
define(['jquery', 'underscore', 'backbone', 'handlebars',
    'text!/static/templates/create-proposal.html', 'fileupload'], function($, _, Backbone, Handlebars, CreateProposalTemplate){

    var ProposalModel = Backbone.Model.extend({

        defaults: function(){
            return {
                image: '',
                description: '',
                amount: '',
                card: ''
            }
        }

    });

    var ProposalCollection = Backbone.Collection.extend({

        model: ProposalModel,

        nextId: function() {

            if(!this.length) {
                return 1
            }

            return this.last().get('id') + 1;

        }

    });

    var ProposalList = new ProposalCollection([]);

    var CreateProposalView = Backbone.View.extend({

        el: $('#app-container'),

        template: Handlebars.compile(CreateProposalTemplate),

        initialize: function(){

            this.render();

        },

        render: function(){

            this.$el.html(this.template());

            return this;

        },

        uploadImage: function(){



        }

    });

    var CreateProposalViewPage = new CreateProposalView

});