define('ProposalModel', ['backbone-validation'], function() {

    return Backbone.Model.extend({

        defaults: function() {
            return {
                image: '',
                description: '',
                amount: '',
                card: ''
            }
        },

        validation: {
            image: {
                required: true,
                msg: 'Загрузите картинку'
            },
            description: {
                required: true,
                msg: 'Укажите описание'
            },
            amount: {
                required: true,
                msg: 'Укажите сумму'
            },
            card: {
                required: true,
                msg: 'Укажите номер карты'
            }
        }

    });

});