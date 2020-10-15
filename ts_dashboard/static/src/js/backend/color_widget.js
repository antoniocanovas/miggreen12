odoo.define('ts_dashboard.ts_dashboard_color_box', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var QWeb = core.qweb;

    var ColorBox = AbstractField.extend({

        _render: function () {
            var color_list = []
            var self = this;
            self.$el.empty();
            if (self.value) {
                var color_list = self.value.split(',')
            }
            var $view = $(QWeb.render('ts_dashboard_color_box', {color_list: color_list}));
            self.$el.append($view)
        }
    });

    registry.add('ts_dashboard_color_box', ColorBox);

    return {
        ColorBox: ColorBox
    };
});

odoo.define('ts_dashboard.ts_dashboard_list_color_box', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var QWeb = core.qweb;

    var ListColorBox = AbstractField.extend({

        events: _.extend({}, AbstractField.prototype.events, {
            'click .color_list': 'color_list_click',
        }),

        _render: function () {
            var color_list = []
            var self = this;
            self.$el.empty();
            var $view = $(QWeb.render('ts_dashboard_list_color_box'));
            if (self.value) {
                $view.find("span[id='" + self.value + "']").toggleClass('pallet_hide')
            }
            self.$el.append($view)
            if (this.mode === 'readonly') {
                this.$el.find('.list_view_theme_container').addClass('readonly_mode');
            }
        },

        color_list_click: function (e) {
            var self = this;
            var $box = $(e.currentTarget).find(':input');
            if ($box.is(":checked")) {
                self.$el.find('.mark_list_theme').prop('checked', false)
                $box.prop("checked", true);
            } else {
                $box.prop("checked", false);
            }
            self._setValue($box[0].value);
        },
    });

    registry.add('ts_dashboard_list_color_box', ListColorBox);

    return {
        ListColorBox: ListColorBox
    };

});