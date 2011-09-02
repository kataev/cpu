/**
 * Created by .
 * User: kd
 * Date: 27.07.11
 * Time: 10:36
 * To change this template use File | Settings | File Templates.
 */

dojo.require("dojo.date.locale");
dojo.require('dojo.date');
dojo.addOnLoad(function() {
    chart = new dojox.charting.Chart2D('chart', null);
    chart.addPlot("default",
            {
//              labels: false,
                type: "Lines",
                markers: true,
                tension: "S"
            });
    var tip = new dojox.charting.action2d.Tooltip(chart, "default");
    var magnify = new dojox.charting.action2d.Magnify(chart, "default");

    chart.setTheme(dojox.charting.themes.Claro);

    chart.addAxis("y", {vertical: true });
    selectableLegend = false;

    var l = {minute:'минут',hour:'часов',day:'дней',second:'секунд'};

    form = new dijit.form.Form(null, 'form');
    dojo.connect(form, 'onSubmit', function(e) {
//            dojo.stopEvent(e);
        e.preventDefault();
        if (form.isValid()) {
            var values = form.get("value");
        } else {
            return;
        }
        //'../store_avg/dvt22/minute/20/'
        var i;
        i = 0;
        console.log(values);

        var url = '../store_avg/' + values.model + '/' + values.avg + '/' + values.limit + '/';
        if (values.date){
//            var date = values.date;
            url+= dojo.date.stamp.toISOString(values.date)+'/'
        }

        dojo.xhrGet({'url':url,handleAs:'json'}).then(function(data) {

            var store = new dojo.data.ItemFileReadStore({'data':data});
//            console.log('store',store);
            var total=0
            store.fetch({query:{id:'*'} ,onBegin: function(t){total = t} });
            if (!total){
                alert('Запрос пустой');
                return 0;
            }
            var labelfTime = function(o) {
                var d = ''
//                        console.log(o);
                var dt = new Date(o);
//                        console.log(dt)
                d = dojo.date.locale.format(dt, {
                            selector: "date",
                            formatLength: "short",
                            locale: "ru",
                            datePattern: 'h:m:s'
                        });
            };

            chart.addAxis("x");
//            console.log(store.query({id:'*'}))
            var s = chart.addSeries(dijit.byId('id_model').attr('displayedValue') + ' <b>'
                + dijit.byId('id_value').attr('displayedValue') + '</b> за '
                + values.limit + ' ' + l[values.avg]+' от '+dojo.date.locale.format(values.date  || new Date(), {
            selector: "date",
            datePattern: 'MMM d, yyyy'
        }),
                    new dojox.charting.DataSeries(
                            store, {query: {id: "*"}
                                    }, function(store, item) {
                                var o = {
                                    x: ++i,//store.getValue(item, 'id'),
                                    y: store.getValue(item, values.value),
                                    tooltip: dojo.date.locale.format(new Date(store.getValue(item, 'date')), {
                                                selector: "date",
                                                formatLength: "short",
                                                locale: "ru",t a
                                                datePattern: 'd MMM h:m'
                                            }) + ' ' + dijit.byId('id_value').attr('displayedValue') + ': <b>' + Math.round(store.getValue(item, values.value),2)+'</b>'
                                };
//                                console.log(o)
                                return o;
                            }));
//            console.log(chart, s)
            chart.render();
            if (selectableLegend) {
                selectableLegend.refresh()
            }
            else {
                selectableLegend = new dojox.charting.widget.SelectableLegend({'chart': chart, horizontal: false}, "selectableLegend");
            }

        });
    })

})
        ;
