from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from database import MongoConnection


# Create your views here.
def overview(request):
    template = loader.get_template('sensor_data/sensor_monitoring.html')
    site_data = MongoConnection.find_data("Sites",conditions=None)
    site_code = []

    for element in site_data:
        sensor_data = []
        for sensor_pars in element["sensors"]:
            sensor_code = sensor_pars["sensor_code"]
            last_10_datavalue_cursor = MongoConnection.find_lastest_data("DataValues", {
                                                                "site_code":element["site_code"],
                                                                "sensor_code": sensor_pars["sensor_code"],
                                                                },10
                                                                )
            last_10_datavalue = []
            for data in last_10_datavalue_cursor:
                last_10_datavalue.append(data["value"])


            if "LIGHT" in sensor_code:
                sensor_icon = "fa fa-sun-o fa-5x"
                pannel_color = "yellow"
            elif "WATER_TEMPERATURE" in sensor_code:
                sensor_icon = "fa fa-tint fa-5x"
                pannel_color = "primary"

            print sensor_pars
            sensor = {
                        "sensor_code": sensor_pars["sensor_code"],
                        "unit": sensor_pars["unit"],
                        "sensor_icon": sensor_icon,
                        "pannel_color": pannel_color
                        }
            if last_10_datavalue != []:
                sensor.update({"value":round(last_10_datavalue[-1],2)})
            else:
                sensor.update({"value":"null"})

            sensor_data.append(sensor)
        site_code.append({"site_code":element["site_code"],
                           "sensors":sensor_data,
                                })
    context = {}
    context.update({"site_code":site_code})


    return HttpResponse(template.render(context, request))

def detail(request):
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import components
    from datetime import datetime

    conditions = dict(request.GET)
    conditions.update({"datetime":{}})
    for key,value in conditions.iteritems():
        if key == "start_time":
            # (conditions["datetime"]).update({"$gte": datetime.strptime(conditions[key][0], "%Y-%m-%d %H:%M:%S" )})
            (conditions["datetime"]).update({"$gte": conditions[key][0]})
        elif key == "end_time":
            # (conditions["datetime"]).update({"$lte": datetime.strptime(conditions[key][0], "%Y-%m-%d %H:%M:%S" )})
            (conditions["datetime"]).update({"$lte": conditions[key][0]})
        elif key == "datetime":
            pass
        else:
            conditions[key] = conditions[key][0]

    conditions.pop('start_time', None)
    conditions.pop('end_time', None)

    if conditions["datetime"]=={}:
        conditions.pop('datetime', None)



    querry_string = '&'.join(["%s=%s"%(k,v) for k,v in conditions.items()])
    url = "/api/datavalues?%s"%(querry_string)
    url = str(url)
    detail_data = MongoConnection.find_data("DataValues",conditions=conditions)
    ploting_data = [[],[]]
    for data in detail_data:
        ploting_data[0].append(datetime.strptime(data["datetime"], '%Y-%m-%d %H:%M:%S.%f'))
        ploting_data[1].append(data["value"])

    #
    plot = figure(x_axis_type="datetime", title="Example plot", plot_width=700, plot_height=400)
    plot.xaxis.axis_label = 'Datetime'
    plot.yaxis.axis_label = 'Celcius'
    plot.line(*ploting_data)
    script, div = components(plot, CDN)

    template = loader.get_template('sensor_data/sensor_detail.html')
    context = {"url":url}
    context.update({"site":conditions})
    context.update({"the_script": script})
    context.update({"the_div": div})

    return HttpResponse(template.render(context, request))
