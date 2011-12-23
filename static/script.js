
var reload_time = 1000 * 60; // 1min
kendo.culture("ru-RU");

var Unit = Backbone.Model.extend({
    initialize:function (data) {
        this.set({label:this.label()});
        this.set({date:new Date(data.date)});
        this.bind('change:value', this.changeValue);
        this.query = this.get('query')
    },
    label:function () {
        id = this.get('id').split('_');
        var d = positions[id[0]][id[1]];
        return  d ? d.pos : undefined;
    },
    changeValue:function () {
        var val = this.get('value')
        this.query = _(this.query).chain().slice(1).push(val.toFixed(1)).value();
    }
});

var Point = Backbone.Model.extend({ })

var Line = Backbone.Collection.extend({
    model:Point,
    url:'./data/'
})

var Data = Backbone.Collection.extend({
    url:'./last/',
    model:Unit
});

var View = Backbone.View.extend({
    initialize:function (args) {
        _.bindAll(this, 'changeValue');
        this.model.bind('change:value', this.changeValue);
        this.model.view = this;
        if (this.model.get('id').split('_')[1] == 'temp') {
            $(this.el).addClass('temp')
        }
    },
    template:_.template($('#view-template').html()),
    tagName:'div',
    className:'cpu',
    events:{
        'click .spark':'show'
    },
    render:function () {
        $(this.el).html(this.template(this.model.toJSON()));
        this.spark();
        return this;
    },
    spark:function () {
        var color = this.model.get('id').split('_')[1] == 'hmdt' ? '#4e6aff' : '#ff7b4c';
        this.$('.spark').sparkline(this.model.query, {width:'100px', fillColor:color, lineColor:'black'});
        this.$('.spark').append('<span class="max">' + _(this.model.query).max().toFixed(1) + '</span>');
        this.$('.spark').append('<span class="min">' + _(this.model.query).min().toFixed(1) + '</span>');
    },
    changeValue:function (val) {
        this.$('span').html(this.model.get('value').toFixed(1));
    },
    show:function (e) {
        $('#chart').empty().append('<img src="/static/kendo/Default/loading.gif">');
        var name = this.$('h2').text()
        var get= {}
        var id = this.model.get('id');
        get['model'] = id.split('_')[0];
        get['aggregate'] = id.split('_')[1];
        get['interval'] = $('#id_interval option:selected').attr('value');
        var start_date = $('#id_start_0').data("kendoDatePicker").value()
        var start_time = $('#id_start_1').data("kendoTimePicker").value()

        var end_date = $('#id_end_0').data("kendoDatePicker").value()
        var end_time = $('#id_end_1').data("kendoTimePicker").value()

        if (start_date){
            get['start_0'] = Highcharts.dateFormat('%Y-%m-%d',start_date*1+1000*60*60*6)
            get['start_1'] = Highcharts.dateFormat('%H:%M',start_time*1+1000*60*60*6)
        }
        if (end_date){
            get['end_0'] = Highcharts.dateFormat('%Y-%m-%d',end_date*1+1000*60*60*6)
            get['end_1'] = Highcharts.dateFormat('%H:%M',end_time*1+1000*60*60*6)
        }

        $.getJSON('./data/', get).success(
            function (data) {
                $('#chart').empty();
                var d = _(data).map(function (m) { return [parseInt(m.date)+1000*60*60*6,
                    parseFloat(m.value.toFixed(2))] });

                var chart = new Highcharts.Chart({
                    chart:{ renderTo:'chart',
                        defaultSeriesType:'line'},
                    title: {text:name, x:0,floating:true},
                    legend: { enabled:false },
                    series:[ {name:name,data:d} ],
                    xAxis:{title:{text:null},type:'datetime',dateTimeLabelFormats:{ month: '%d-%m', year:'%Y'}},
                    yAxis: {
                        title: { text:null },
                        startOnTick: false
//                                    ,showFirstLabel: false
                    },
                    tooltip: {
                        formatter: function() {
                            return '<b>'+ this.series.name+ ':</b> <i>'+ this.y +'</i><br/>'+
                                Highcharts.dateFormat('%d-%m-%Y %H:%M', this.x);
                        }}
                });
            }).error(function (e) {
                $('#chart').empty().append('<h3>Произошла ошибка</h3>')
            });

    }
});
window.data = new Data;
window.data.reset(d);
window.l = new Line;

var WorkSpace = Backbone.Router.extend({
    routes:{
        '':'root'
//                ,'#!/chart/':'chart'
    },
    root:function () {
        window.data.each(function (model) {
            var el = $('#' + model.get('id'));
            var v = new View({model:model, el:el});
            v.render();
        });

        $("#id_start_0").kendoDatePicker({format: "dd-MM-yyyy"});
        $("#id_start_1").kendoTimePicker({format: "HH:mm"});
        $("#id_end_0").kendoDatePicker({format: "dd-MM-yyyy"});
        $("#id_end_1").kendoTimePicker({format: "HH:mm"});
    },
    chart:function () {
        console.log('chart')
    }
});

var refresh = function () {
    $.getJSON('./last/').success(function (json) {
        _.forEach(json, function (d) {
            data.get(d.id).set({value:d.value});
            data.get(d.id).view.spark()
        });
    });
    setTimeout(refresh, reload_time);
};

var draw = function () {
    var w = [];
    var template = _.template($('#group-template').html());
    for (var m in positions) {
        for (var a in positions[m]) {
            var p = positions[m][a].p;
            var place = positions[m][a].place;
            var id = m + '_' + a;
            var gr = $('#' + p).length ? $('#' + p) : $(template({id:p, pos:place})).appendTo('body');
            var el = $(_.template('<div id="<%- id %>"></div>', {id:id})).appendTo(gr);
            w.push({gr:gr, el:el, a:a, m:m, p:p})
        }
        ;
    }
    ;
    var s = _(w).chain().filter(function (e) {
        return e.m == 'termodat22m' && e.p == 'firing'
    })
        .sortBy(
        function (e) {
            return parseInt(e.a.slice(1))
        }).value()
    _(s).each(function (e, key) {
        if (key == 0) {
            return;
        }
        else {
            $(s[key - 1].el).after($(e.el));
        }
    });
    return w;
}

$(function () {
    window.elems = draw();
    new WorkSpace;
    Backbone.history.start();
    refresh();

    $('#time').change(function (e) {
        reload_time = parseInt($("#time option:selected").attr('value')) * 1000
    })
});