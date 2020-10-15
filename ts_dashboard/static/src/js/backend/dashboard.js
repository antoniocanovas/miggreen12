odoo.define('ts_dashboard.backend.ts_dashboard', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var session = require('web.session');
    var field_utils = require('web.field_utils');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');

    var Dashboard = AbstractAction.extend(ControlPanelMixin, {
        template: 'ts_dashboard.DashboardMain',

        events: {
            "click .card-option": "_onCardOptionClick",
            "click .full-card": "_onCardOptionMaximize",
            "click .export-pdf": "_onCardOptionExportPDF",
            "click .close-card": "_onCardOptionClose",
            "click .edit-card": "_onCardOptionEdit",
        },

        jsLibs: [
            '/ts_dashboard/static/src/lib/jquery.ui.touch-punch.min.js',
            '/ts_dashboard/static/src/lib/gridstack.js',
            '/ts_dashboard/static/src/lib/gridstack.jQueryUI.js',
            '/ts_dashboard/static/src/lib/jsPDF.js',
        ],
        cssLibs: [],

        init: function (parent, menu, params) {
            this._super(parent, menu, params);
            this.board_id = menu.params.board_id;
            this.dashboards_templates = ['ts_dashboard.dashboard_body'];
            this.chart_container = {};
            this.chart_details = {};
            this.update_interval_selection = {
                '0': 'Not Set',
                '10000': '10 Seconds',
                '20000': '20 Seconds',
                '30000': '30 Seconds',
                '40000': '40 Seconds',
                '60000': '1 minute',
                '120000': '2 minutes',
                '180000': '3 minutes',
                '300000': '5 minutes',
                '600000': '10 minutes',
                '1200000': '20 minutes'
            };
        },

        willStart: function() {
            var self = this;
            return $.when(ajax.loadLibs(this), this._super()).then(function() {
                return self.fetch_data();
            });
        },

        start: function () {
            var self = this;
            return this._super().then(function () {
                self.update_cp();
                self.render_dashboards();
                self._render_charts(self.data);
            });
        },

        save_grid_position: function (grid_position, interval_value) {
            var self = this;
            self.refresh_interval = interval_value;
            rpc.query({
                model: 'ts.dashboard',
                method: 'save_grid_position',
                args: [[], grid_position, interval_value]
            }).then(function (return_vals) {

            }, function (err, ev) {

            });
        },

        on_attach_callback: function () {
            var self = this;
            self.set_update_interval();
        },

        set_update_interval : function(){
            var self = this;
            function UpdateInterval() {
                    $.when(self.fetch_data()).then(function () {
                            self.render_dashboards();
                            self._render_charts(self.data);
                        });
                }
            if (self.refresh_interval !== '0'){
                self.UpdateDashboard = setInterval(UpdateInterval, self.refresh_interval);
            }
        },

        on_detach_callback : function(){
            var self = this;
            self.remove_update_interval();
        },

        remove_update_interval : function(){
            var self = this;
            clearInterval(self.UpdateDashboard)
        },

        on_reverse_breadcrumb: function() {
            var self = this;
            self.update_cp();
            $.when(this.fetch_data()).then(function () {
                self.render_dashboards();
                self._render_charts(self.data);
            });
        },

        update_cp: function () {
            var self = this;
            if (!this.$searchview) {
                this.$searchview = $(QWeb.render("ts_dashboard.DateRangeButtons", {
                    widget: this,
                    update_interval_selection: self.update_interval_selection,
                    refresh_interval:self.refresh_interval
                }));
                this.$searchview.on('click', 'button.js_add_position', function (e) {
                self.do_action({
                    type: 'ir.actions.act_window',
                    res_model: 'ts.dashboard',
                    view_id: 'ts_dashboard.ts_dashboard_view_form',
                    views: [
                        [false, 'form']
                    ],
                    target: 'current',
                    'clear_breadcrumb': true,
                    context: {
                        'board_id': self.board_id || false
                    },
                }, {
                    on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                });
            });
            this.$searchview.on('click', 'button.js_save_position', function (e) {
                this.serializedData = _.map($('.grid-stack > .grid-stack-item:visible'), function (el) {
                    el = $(el);
                    var node = el.data('_gridstack_node');
                    return {id: node.id, x: node.x, y: node.y, width: node.width, height: node.height};
                }, this);
                var update_interval = document.getElementById("interval_value");
                var interval_value = update_interval.options[update_interval.selectedIndex].value;
                self.remove_update_interval();
                self.save_grid_position(this.serializedData, interval_value);
                $('.grid-stack').data('gridstack').movable('.grid-stack-item', false);
                $('.grid-stack').data('gridstack').resizable('.grid-stack-item', false);
                $('.o_form_buttons_view').toggleClass('o_hidden');
                $('.o_form_buttons_edit').toggleClass('o_hidden');
                $('.close-card').toggleClass('o_hidden');
                $('.edit-card').toggleClass('o_hidden');
                self.set_update_interval();
            });
            this.$searchview.on('click', 'button.js_edit_position', function (e) {
                self.remove_update_interval();
                $('.grid-stack').data('gridstack').movable('.grid-stack-item', true);
                $('.grid-stack').data('gridstack').resizable('.grid-stack-item', true);
                $('.o_form_buttons_view').toggleClass('o_hidden');
                $('.o_form_buttons_edit').toggleClass('o_hidden');
                $('.close-card').toggleClass('o_hidden')
                $('.edit-card').toggleClass('o_hidden');
            });
            this.$searchview.on('click', 'button.js_cancel_position', function (e) {
                $('.grid-stack').data('gridstack').movable('.grid-stack-item', false);
                $('.grid-stack').data('gridstack').resizable('.grid-stack-item', false);
                $('.o_form_buttons_view').toggleClass('o_hidden');
                $('.o_form_buttons_edit').toggleClass('o_hidden');
                $('.close-card').toggleClass('o_hidden');
                $('.edit-card').toggleClass('o_hidden');
                var update_interval = document.getElementById("interval_value");
                var interval_value = update_interval.options[update_interval.selectedIndex].value;
                self.set_update_interval();
                $.when(self.fetch_data()).then(function () {
                    self.render_dashboards();
                    self._render_charts(self.data);
                });
            });
            }
            this.update_control_panel({
                cp_content: {
                    $searchview: this.$searchview
                },
            });
        },

        render_dashboards: function () {
            var self = this;
            self.$('.o_ts_dashboard_content').empty();
            _.each(this.dashboards_templates, function (template) {
                self.$('.o_ts_dashboard_content').append(QWeb.render(template, {widget: self}));
            });
            var options = {
                staticGrid: true,
                disableDrag: true,
                disableResize: true,
                animate: true,
                float: false
            };
            this.$('.grid-stack').gridstack(options);
//            this.$('.grid-stack').css("position", "relative")

            this.$('.grid-stack').find('.grid-stack-item').css("position", "absolute")

        },

        /**
         * Fetches dashboard data
         */
        fetch_data: function () {
            var self = this;
            return this._rpc({
                route: '/ts_dashboard/get_dashboard_data',
                params: {board_id:self.board_id}
            }).done(function (result) {
                self.data = result.dashboards;
                self.refresh_interval = result.refresh_interval;
            });
        },

        render_monetary_field: function (value, currency_id) {
            var currency = session.get_currency(currency_id);
            var formatted_value = field_utils.format.float(value || 0, {digits: currency && currency.digits});
            if (currency) {
                if (currency.position === "after") {
                    formatted_value += currency.symbol;
                } else {
                    formatted_value = currency.symbol + formatted_value;
                }
            }
            return formatted_value;
        },

        _onCardOptionClick: function (ev) {
            if ($(ev.target.firstChild).hasClass('fa-chevron-right')) {
                $('.card-option').animate({
                    'width': '35px'
                });
            } else {
                $('.card-option').animate({
                    'width': '180px'
                });
            }
            $(ev.target.firstChild).toggleClass("fa-chevron-right").fadeIn('slow');
        },
        _onCardOptionMaximize: function (ev) {
            var port = $(ev.currentTarget).parents('.card').first();
            port.toggleClass("full-card");
            port.toggleClass("grid-stack-item-content ui-draggable-handle");
        },

        _onCardOptionExportPDF: function (ev) {
            var chart_id = $(ev.currentTarget).attr('chart-id')
            var name = this.chart_details[chart_id].name
            var base64_image = this.chart_container[chart_id].toBase64Image()
            var doc = new jsPDF('p', 'mm');
            doc.addImage(base64_image, 'PNG', 5, 10, 200, 0);
            doc.save(name);
        },

        _onCardOptionClose: function (ev) {
            self = this;
            Swal.fire({
              title: 'Are you sure?',
              text: "You are going to Deactivate dashboard item!",
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Yes, Deactive it!',
              width: '350px',
            }).then((result) => {
                if (result.value) {
                    var record_id = $(ev.target).parents('.grid-stack-item')[0].getAttribute('data-gs-id');
                    self._rpc({
                        model: 'ts.dashboard',
                        method: 'toggle_active',
                        args: [parseInt(record_id)]
                    }).then(function (records) {
                        Swal.fire(
                          'Deactivated!',
                          'Your record has been deactivated.',
                          'success'
                        );
                        $.when(self.fetch_data()).then(function () {
                            self.render_dashboards();
                            self._render_charts(self.data);
                        });
                    })
                }
            })
        },

        _onCardOptionEdit: function(e){
            var self = this;
            var record_id = $(e.currentTarget).parent().closest('.grid-stack-item').attr('data-gs-id');
            if (record_id){
                self.do_action({
                    type: 'ir.actions.act_window',
                    res_model: 'ts.dashboard',
                    view_id: 'ts_dashboard.ts_dashboard_view_form',
                    res_id: parseInt(record_id),
                    views: [
                        [false, 'form']
                    ],
                    target: 'current',
                    'clear_breadcrumb': true,
                    context: {
                        'form_view_initial_mode':'edit',
                        'board_id': self.board_id || false
                    },
                }, {
                    on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                });
            }
        },

        _render_charts: function (result) {
            for (var i = 0, len = result.length; i < len; i++) {
                if (result[i].type === 'line' || result[i].type === 'bar' || result[i].type === 'pie' || result[i].type === 'polarArea') {
                    var ctx = this.$('.grid-stack').find("#"+result[i].id.toString())[0].getContext("2d");
                    if (result[i].type === 'line' || result[i].type === 'bar') {

                        var bar_dataset =  { color: 'white', display: function(context) { return context.dataset.data[context.dataIndex] > 15; }, font: { weight: 'bold' }, formatter: Math.round }
                        var line_dataset = { backgroundColor: function(context) { return context.dataset.backgroundColor; }, borderRadius: 4, color: 'white', font: { weight: 'bold' }, formatter: Math.round }

                        var myChart = new Chart(ctx, {
                            type: (result[i].type === 'bar') ? result[i].bar_type : result[i].type, //(result[i].type === 'bar') ? true : false
                            data: {
                                labels: result[i].line_chart_labels,
                                datasets: result[i].line_chart_data,
                            },
                            options: {
//                             scaleLabel: function(label) {return value.toLocaleString("en-US",{style:"currency", currency:"USD"})},
                                maintainAspectRatio: false,
                                responsiveAnimationDuration: 1000,
                                animation: {
                                    easing: 'easeInQuad',
                                },
                                responsive: true,
                                legend: {
                                    position: "top"
                                },
                                tooltips: {
                                    enabled: true,
                                    intersect: !1,
                                    mode: "nearest",//point
                                    xPadding: 10,
                                    yPadding: 10,
                                    caretPadding: 10
                                },
                                scales: {
                                    yAxes: [{
                                        stacked: result[i].is_stacked_bar,
                                        ticks: {
                                            callback: function(value) {
                                                 var ranges = [
                                                    { divider: 1e6, suffix: 'M' },
                                                    { divider: 1e3, suffix: 'k' }
                                                 ];
                                                 function formatNumber(n) {
                                                    for (var i = 0; i < ranges.length; i++) {
                                                       if (n >= ranges[i].divider) {
                                                          return (n / ranges[i].divider).toString() + ranges[i].suffix;
                                                       }
                                                    }
                                                    return n;
                                                 }
                                                 return (isNaN(value) === true) ? value :'$' + formatNumber(value);
                                              },
                                              padding: 10,
                                        },
                                        gridLines: {
                                            drawTicks: false,
                                            display: false
                                        },
                                        scaleLabel: {
                                            display: true,
                                            labelString: (result[i].type === 'bar' && result[i].bar_type === 'horizontalBar') ? result[i].xAxes_labelString : result[i].yAxes_labelString

                                            // fontColor: "green"
                                        }

                                    }],
                                    xAxes: [{
                                        stacked: result[i].is_stacked_bar,
                                        gridLines: {
                                            drawTicks: false,
                                            display: false
                                        },
                                        ticks: {
                                            callback: function(value) {
                                                 var ranges = [
                                                    { divider: 1e6, suffix: 'M' },
                                                    { divider: 1e3, suffix: 'k' }
                                                 ];
                                                 function formatNumber(n) {
                                                    for (var i = 0; i < ranges.length; i++) {
                                                       if (n >= ranges[i].divider) {
                                                          return (n / ranges[i].divider).toString() + ranges[i].suffix;
                                                       }
                                                    }
                                                    return n;
                                                 }
                                                 return (isNaN(value) === true) ? value :'$' + formatNumber(value);
                                            },
                                            padding: 10,
                                        },
                                        scaleLabel: {
                                            display: true,
                                            labelString: (result[i].type === 'bar' && result[i].bar_type === 'horizontalBar') ? result[i].yAxes_labelString : result[i].xAxes_labelString,
                                        }
                                    }]
                                },
                                plugins: {
                                    colorschemes: {
                                        scheme: result[i].chart_colors
                                    },
                                    datalabels:(result[i].type === 'bar') ? bar_dataset : line_dataset
                                }
                            }
                        });
                        this.chart_container[this.$('.grid-stack').find("#"+result[i].id.toString())[0].id] = myChart;
                        this.chart_details[this.$('.grid-stack').find("#"+result[i].id.toString())[0].id] = result[i];
                    }else if (result[i].type === 'polarArea') {
                        var mypolarAreaChart = new Chart(ctx, {
                            type: 'polarArea',
                            responsive: true,
                            data: {
                                labels: result[i].line_chart_labels,
                                datasets: result[i].line_chart_data
                            },
                            fillOpacity: 1.3,
                            options: {
                                maintainAspectRatio: false,
                                responsiveAnimationDuration: 1000,
                                animation: {
                                    easing: 'easeInQuad',
                                },
                                responsive: true,
                                legend: {
                                    position: "top"
                                },
                                tooltips: {
                                    custom: function(tooltip) {

                                    },
                                    mode: 'single'
                                  },
                                scale: {
                                    reverse: false,
                                    ticks: {
                                      min: 0
                                    }
                                  },
                                plugins: {
                                    colorschemes: {
                                        scheme: result[i].chart_colors
                                    },
                                    datalabels: {
                                        backgroundColor: function(context) {
                                            return context.dataset.backgroundColor;
                                        },
                                        borderRadius: 4,
                                        color: 'white',
                                        font: {
                                            weight: 'bold'
                                        },
                                        formatter: Math.round
                                    }
                                }
                            }
                        });
                        this.chart_container[this.$('.grid-stack').find("#"+result[i].id.toString())[0].id] = mypolarAreaChart;
                        this.chart_details[this.$('.grid-stack').find("#"+result[i].id.toString())[0].id] = result[i];
                    }
                    else {
                        var myPieChart = new Chart(ctx, {
                            type: result[i].pie_type,
                            data: {
                                labels: result[i].line_chart_labels,
                                datasets: result[i].line_chart_data
                            },
                            options: {
                                rotation: (result[i].is_semi_circle_bar === true) ? 1 * Math.PI  : -0.5 * Math.PI,
                                circumference: (result[i].is_semi_circle_bar === true) ? 1 * Math.PI  : 2 * Math.PI,
                                maintainAspectRatio: false,
                                responsiveAnimationDuration: 1000,
                                animation: {
                                    easing: 'easeInQuad',
                                },
                                responsive: true,
                                legend: {
                                    position: "top"
                                },
                                tooltips: {
                                    enabled: true,
                                    intersect: !1,
                                    mode: "point",//nearest
                                    xPadding: 10,
                                    yPadding: 10,
                                    caretPadding: 10
                                },
                                plugins: {
                                    colorschemes: {
                                        scheme: result[i].chart_colors
                                    },
                                    datalabels: {
                                        backgroundColor: function(context) {
                                            return context.dataset.backgroundColor;
                                        },
                                        borderColor: 'white',
                                        borderRadius: 25,
                                        borderWidth: 2,
                                        color: 'white',
                                        display: function(context) {
                                            var dataset = context.dataset;
                                            var count = dataset.data.length;
                                            var value = dataset.data[context.dataIndex];
                                            return value > count * 1.5;
                                        },
                                        font: {
                                            weight: 'bold'
                                        },
                                        formatter: Math.round
                                    }
                                }
                            }
                        });
                        this.chart_container[this.$('.grid-stack').find("#"+result[i].id.toString())[0].id] = myPieChart;
                        this.chart_details[this.$('.grid-stack').find("#"+result[i].id.toString())[0].id] = result[i];
                    }

                }
            }
        }
        // statustic end

    });
    core.action_registry.add('backend_ts_dashboard', Dashboard);

    return Dashboard;
});
