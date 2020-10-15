odoo.define('ts_dashboard.dashboard_chart_preview', function (require) {
    "use strict";

    var session = require('web.session');
    var field_utils = require('web.field_utils');
    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var QWeb = core.qweb;
    var registry = require('web.field_registry');

    var ChartPreview = AbstractField.extend({

        supportedFieldTypes: ['char'],

        resetOnAnyFieldChange: true,

        init: function (parent, state, params) {
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            self.set_default_chart_view();
            core.bus.on("DOM_updated", this, function () {
                if(self.shouldRenderChart && self.$el.find('#canvas_chart_id').length>0) self.renderChart();
            });
            return this._super();
        },

        set_default_chart_view: function () {
            Chart.plugins.register({
                afterDraw: function (chart) {
                    if (chart.data.labels.length === 0) {
                        var ctx = chart.chart.ctx;
                        var height = chart.chart.height;
                        var width = chart.chart.width;
                        chart.clear();
                        ctx.save();
                        ctx.textBaseline = 'middle';
                        ctx.textAlign = 'center';
                        ctx.fillText('No data to Display', width / 2, height / 2);
                        ctx.font = "3rem 'Lucida Grande'";
                        ctx.restore();
                    }
                }
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

        _render: function () {
            this.$el.empty();
            if (this.recordData.type === 'pie' || this.recordData.type === 'line' || this.recordData.type === 'bar') {
                if(this.recordData.dashboard_model_id){
                    this._getChartData();
                }else{
                    this.$el.append($('<div>').text("Select a Model first."));
                }
            }
            if (this.recordData.type === 'tile') {
                if(this.recordData.dashboard_model_id){
                    this._getTileData();
                }else{
                    this.$el.append($('<div>').text("Select a Model first."));
                }
            }
            if (this.recordData.type === 'list') {
                if(this.recordData.dashboard_model_id){
                    if(this.recordData.list_type==='non_group' && this.recordData.list_view_fields){
                        this._getListData();
                    }
                    else if(this.recordData.list_type==='group' && this.recordData.list_view_groupby_fields && this.recordData.groupby_field_id){
                        this._getListData();
                    }
                    else{
                        this.$el.append($('<div>').text("Please select Mandatory Fields!!!"));
                    }
                }else{
                    this.$el.append($('<div>').text("Select a Model first."));
                }
            }
        },

        _getChartData: function () {
            var self = this;
            self.shouldRenderChart = true;
            var field = this.recordData;
            var chart_name;
            if (field.name) chart_name = field.name;
            else if (field.dashboard_model_name) chart_name = field.dashboard_model_id.data.display_name;
            else chart_name = "Name";

            this.chart_data = JSON.parse(this.recordData.chart_data);

            var $chartContainer = $(QWeb.render('chart_renderer_container_from', {
                chart_name: chart_name
            }));
            self.$el.append($chartContainer);

            if(self.$el.find('#canvas_chart_id').length>0){
                self.renderChart();
            }
            if(this.$el.find('canvas').height() < 250){
                this.$el.find('canvas').height(250);
            }
        },

        _getTileData: function () {
            var self = this;
            var tile_data = JSON.parse(this.recordData.chart_data);
            let $tileContainer = $(QWeb.render('tile_renderer_container_from', {
                dashboard: this.recordData,
                display_result:tile_data,
                widget: self
            }));
            self.$el.append($tileContainer);
        },

        _getListData: function(){
            var self = this;
            var list_data = JSON.parse(this.recordData.chart_data);
            if (! $.isEmptyObject(list_data)){
                let $listContainer = $(QWeb.render('list_renderer_container_from', {
                    dashboard: list_data,
                    display_result:this.recordData,
                    widget: self
                }));
                self.$el.append($listContainer);
            }
        },

        renderPieChart: function(){
            var self = this;
            var myPieChart = new Chart(self.$el.find('#canvas_chart_id')[0].getContext("2d"), {
                type: this.recordData.pie_type,
                data: {
                    labels: this.chart_data['labels'],
                    datasets: this.chart_data.datasets,
                },
                options: {
                    rotation: (this.recordData.is_semi_circle_bar === true) ? 1 * Math.PI  : -0.5 * Math.PI,
                    circumference: (this.recordData.is_semi_circle_bar === true) ? 1 * Math.PI  : 2 * Math.PI,
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
                            scheme: this.recordData.chart_colors
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
        },

        renderLineBarChart: function(){
            var self = this;
            var bar_dataset =  { color: 'white', display: function(context) { return context.dataset.data[context.dataIndex] > 15; }, font: { weight: 'bold' }, formatter: Math.round }
            var line_dataset = { backgroundColor: function(context) { return context.dataset.backgroundColor; }, borderRadius: 4, color: 'white', font: { weight: 'bold' }, formatter: Math.round }

            var myChart = new Chart(self.$el.find('#canvas_chart_id')[0].getContext("2d"), {
                type: (this.recordData.type === 'bar') ? this.recordData.bar_type : this.recordData.type, //(this.recordData.type === 'bar') ? true : false
                data: {
                    labels: this.chart_data['labels'],
                    datasets: this.chart_data.datasets,
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
                            stacked: this.recordData.is_stacked_bar,
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
                                labelString: (this.recordData.type === 'bar' && this.recordData.bar_type === 'horizontalBar') ? this.chart_data.xAxes_labelString : this.chart_data.yAxes_labelString
                            }

                        }],
                        xAxes: [{
                            stacked: this.recordData.is_stacked_bar,
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
                                labelString: (this.recordData.type === 'bar' && this.recordData.bar_type === 'horizontalBar') ? this.chart_data.yAxes_labelString : this.chart_data.xAxes_labelString,
                            }
                        }]
                    },
                    plugins: {
                        colorschemes: {
                            scheme: this.recordData.chart_colors
                        },
                        datalabels:(this.recordData.type === 'bar') ? bar_dataset : line_dataset
                    }
                }
            });
        },

        renderChart: function(){
            var self = this;
            if (self.recordData.type==='pie'){
                self.renderPieChart();
            }
            else if (self.recordData.type==='line' || self.recordData.type==='bar'){
                self.renderLineBarChart();
            }
        },
    });

    registry.add('dashboard_chart_preview', ChartPreview);

    return {
        ChartPreview: ChartPreview,
    };

});