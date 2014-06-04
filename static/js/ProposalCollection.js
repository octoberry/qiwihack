define('ProposalCollection',  ['ProposalModel','localstorage'], function(ProposalModel) {
    return Backbone.Collection.extend({

        localStorage: new Backbone.LocalStorage("proposal-store"),

        model: ProposalModel,

        nextId: function() {

            if(!this.length) {
                return 1
            }

            return this.last().get('id') + 1;

        }
    });
});