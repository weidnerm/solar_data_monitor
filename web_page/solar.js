$( function() {

    $.ajaxSetup({
       async: false
    });
    
    var parameters = getUrlVars();

    //Getting html parameters to pass to php
    var days_ago = 0
    if ("daysago" in parameters){
        var days_ago = getUrlVars()['daysago'];
    }
        
    //Getting html parameters to pass to php
    var input_channel = 'Panel'
    if ("inputchannel" in parameters){
        input_channel = getUrlVars()['inputchannel'].replace('+',' ');
    }
        
    // take the parameters from the URL and put them back into the input form as defaults
    (new URL(window.location.href)).searchParams.forEach((x, y) =>
        {document.getElementById(y).value = x;});
       
        
    //Get parameters from url to pass to php
    function getUrlVars() {
        var vars = {};
        var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
            vars[key] = value;
        });
        return vars;
    }
    
    function getData(day){
        //~ var result = [1,2,3,4,5];
        var result = [1,2,3,4,5];
        //~ var result = {};

        $.getJSON("solar.php?day=" + day , function(res) {
            //~ $.each(res, function(key, val) {
                //~ result[key] = val
                //~ console.log(key,val);
            //~ });
            result = res;
            //~ console.log('got to getData() callback');
            //~ console.log(res)
       });

        return result;
    }

    
    function get_mA_color(mA, fade){
        var color = '#000000'
        if (mA < 0) {
            color = '#ff0000' }
        else if (mA > 0) {
            color = '#00ff00' }
            
        if (fade == true)
            color = color+'20'
            
        return color;
    }

    function getDateList(maxDays){
        var result = "[]";

        $.getJSON("solar.php?maxDays=" + maxDays, function(res) { result = res; });

        //~ result = JSON.parse(result)
        return result;
    }
    
    function getLiveData(liveSource){
        var result = "[]";

        $.getJSON("solar.php?liveSource=" + liveSource, function(res) { result = res; });

        //~ result = JSON.parse(result)
        return result;
    }
    
    
    var myChart = {
        chart: {
            zoomType: 'xy',
            //~ styledMode: 1
        },
        title: {
            text: 'Solar - Panel',
                style: {
                    fontSize: "25px"
                }
        },

        xAxis: {
            type: 'datetime',
            //~ dateTimeLabelFormats: 
                //~ { hour: '%H:%M'},
            labels: {
                format: '{value:%H:%M}',
                style: { fontSize: "20px" },
            },
        },


        yAxis: [{ // Primary yAxis
            labels: {
                style: {
                    color: "#00ff00",
                    fontSize: "20px"
                }
            },
            title: {
                text: 'Current (mA)',
                style: {
                    color: "#00ff00",
                    fontSize: "20px"
                }
            }
        }, { // Secondary yAxis
            title: {
                text: 'Voltage (V)',
                style: {
                    color: "#ffa500",
                    fontSize: "20px"
                }
            },
            labels: {
                style: {
                    color: "#ffa500",
                    fontSize: "20px"
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,
            itemStyle: { fontSize: "15px"
            },
            title: {                style: {
                        fontSize: "20px"
                    }
            },
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || // theme
                'rgba(255,255,255,0.25)'
        },
        series: []
    };
    
    var myChartWaterfall = {
        chart: {
            type: 'waterfall'
        },

        title: {
            text: 'Solar Energy Summary'
        },

        xAxis: {
            type: 'category'
        },

        yAxis: {
            labels: {
                style: {
                    fontSize: "20px"
                }
            },
            title: {
                text: 'AHr',
                style: {
                    fontSize: "20px"
                }
            }
        },

        legend: {
            enabled: false
        },

        //~ tooltip: {
            //~ pointFormat: '<b>${point.y:,.2f}</b> USD'
        //~ },

        series: [{
            upColor: '#00ff00',
            color: '#ff0000',
            data: [],
            dataLabels: {
                enabled: true,
                formatter: function () {
                    return Highcharts.numberFormat(this.y , 1, '.') ;
                },
                style: {
                    fontWeight: 'bold'
                }
            },
            pointPadding: 0
        }]
    }
    
    var myLiveBatts = {
        chart: {
            type: 'column'
        },
        legend:{ enabled:false },
        title: {
            text: 'Battery State'
        },
        xAxis: {
            categories: ['Batt 1<br>110mA<br>1.555W', 'Batt 2', 'Batt 3', 'Batt 4', 'Batt 5']
        },
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: 'Battery Charge State'
            },
            stackLabels: {
                enabled: false,
                style: {
                    fontWeight: 'bold',
                    color: ( // theme
                        Highcharts.defaultOptions.title.style &&
                        Highcharts.defaultOptions.title.style.color
                    ) || 'gray'
                }
            }
        },

        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true
                }
            }
        },
        series: [
        {
            dataLabels: {
                enabled: false
            },
            groupPadding:0.0,
            borderWidth:0,
            color: '#404040',
            data: [51, 27, 40, 70, 20]
        },
         {
            borderWidth:0,
            groupPadding:0.0,
            data: [{y:49, color:'#ff0000'},{y:73, color:'#00ff00'},{y:60, color:'#ff0000'},{y:30, color:'#ff0000'},{y:80, color:'#ffff00'}]
        }]
    }

    var myLiveToday = {
        chart: {
            type: 'column'
        },
        legend:{ enabled:false },
        title: {
            text: 'Panel/Batt/Load Energy'
        },
        xAxis: {
            categories: ['Panel<br><br>8.4AH', 'Batt<br>92%<br>1.5AH', 'Load<br><br>16.8AH']
        },
        yAxis: {
            min: 0,
            max: 12,
            title: {
                text: 'Accumulated Energy'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: ( // theme
                        Highcharts.defaultOptions.title.style &&
                        Highcharts.defaultOptions.title.style.color
                    ) || 'gray'
                }
            }
        },

        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true
                }
            }
        },
        series: [{
            borderWidth:0,
            groupPadding:0.0,
            data: [{y:6, color:'#ff0000'},{y:3, color:'#00ff00'},{y:5, color:'#ffff00'}]
        }]
    }

    var myLiveNow = {
        chart: {
            type: 'column'
        },
        legend:{ enabled:false },
        title: {
            text: 'Panel/Batt/Load Power'
        },
        xAxis: {
            categories: ['Panel<br>14.124V', 'Batt<br>14.124V', 'Load<br>14.124V']
        },
        yAxis: {
            min: 0,
            max: 12,
            title: {
                text: 'Power Transfer'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: ( // theme
                        Highcharts.defaultOptions.title.style &&
                        Highcharts.defaultOptions.title.style.color
                    ) || 'gray'
                }
            }
        },

        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true
                }
            }
        },
        series: [{
            borderWidth:0,
            groupPadding:0.0,
            data: [{y:5, color:'#ff0000'},{y:3, color:'#00ff00'},{y:2, color:'#ffff00'}]
        }]
    }

  
    var date_list = getDateList();
    //~ console.log(date_list);
    
    
    if(input_channel == 'BattEnergy') {
        document.getElementById('left').setAttribute("style","display:inline-block;width:100%");
        document.getElementById('left').style.width='100%';
        document.getElementById('middle').setAttribute("style","display:none");
        document.getElementById('middle').style.width='0%';
        document.getElementById('right').setAttribute("style","display:none");
        document.getElementById('right').style.width='0%';


        console.log(myChartWaterfall['series'][0]['data'] )
        myChartWaterfall['series'][0]['data'] = []

        for(var dayago_index=0 ; dayago_index<days_ago ; dayago_index++)
        {
            var date_text = date_list[date_list.length+dayago_index-days_ago]
        
            var raw_data = getData(date_text);
            var time = 0;
            var batt_day_ma_sec = 0;
            var panel_day_ma_sec = 0;
            var load_day_ma_sec = 0;
            
            for(var index=0; index<raw_data.length-1; index++)  // subtract 1 since last entry is blank
            {

                var entry = JSON.parse(raw_data[index]);
                //~ console.log(entry);
                
                if(entry.hasOwnProperty('time')) 
                {
                    var inputs = entry['inputs'];
                    var key_list = Object.keys(inputs)
                    for ( var key_index=0; key_index<key_list.length ; key_index++)
                    {
                        if (key_list[key_index].startsWith('Batt'))
                        {
                            var input_data = inputs[key_list[key_index]];
                            var total_mA_sec = input_data[0]
                            
                            batt_day_ma_sec += total_mA_sec
                        }
                        if (key_list[key_index].startsWith('Panel'))
                        {
                            var input_data = inputs[key_list[key_index]];
                            var total_mA_sec = input_data[0]
                            
                            panel_day_ma_sec += total_mA_sec
                        }
                        if (key_list[key_index].startsWith('Load'))
                        {
                            var input_data = inputs[key_list[key_index]];
                            var total_mA_sec = input_data[0]
                            
                            load_day_ma_sec += total_mA_sec
                        }
                    }
                    
                }
            }

            series_entry = {
                    name: date_text+ '<br>load',
                    y: -load_day_ma_sec/1000/60/60};
            myChartWaterfall['series'][0]['data'].push(series_entry);
            console.log(batt_day_ma_sec)

            series_entry = {
                    name: date_text+'<br>panel',
                    y: panel_day_ma_sec/1000/60/60};
            myChartWaterfall['series'][0]['data'].push(series_entry);
            console.log(batt_day_ma_sec)
        }

        Highcharts.chart('left', myChartWaterfall);
    }
    else if(input_channel == 'Live') {
        document.getElementById('left').setAttribute("style","display:inline-block;width:50%");
        document.getElementById('left').style.width='50%';
        document.getElementById('middle').setAttribute("style","display:inline-block;width:25%");
        document.getElementById('middle').style.width='25%';
        document.getElementById('right').setAttribute("style","display:inline-block;width:25%");
        document.getElementById('right').style.width='25%';
            
        var raw_data = getLiveData('192.168.86.44');
            
        Highcharts.chart('left', myLiveBatts);
        Highcharts.chart('middle', myLiveToday);
        Highcharts.chart('right', myLiveNow);
    }
    else {
        document.getElementById('left').setAttribute("style","display:inline-block;width:100%");
        document.getElementById('left').style.width='100%';
        document.getElementById('middle').setAttribute("style","display:none");
        document.getElementById('middle').style.width='0%';
        document.getElementById('right').setAttribute("style","display:none");
        document.getElementById('right').style.width='0%';

        var date_text = date_list[date_list.length-1-days_ago]
    
        var raw_data = getData(date_text);
        var time = 0;
        var avg_volt_series = []
        var min_volt_series = []
        var max_volt_series = []
        var avg_mA_series = []
        var min_mA_series = []
        var max_mA_series = []
        
        for(var index=0; index<raw_data.length-1; index++)  // subtract 1 since last entry is blank
        {

            var entry = JSON.parse(raw_data[index]);
            //~ console.log(entry);
            
            if(entry.hasOwnProperty('time')) 
            {
                var time_str = entry["time"];
                //~ console.log(time_str);
                var time_str_fields = time_str.split(':');
                var time_hours = (parseInt(time_str_fields[0])*60*60 + parseInt(time_str_fields[1])*60 + parseInt(time_str_fields[2]))/(60*60);
                //~ console.log(time_int);
                
                var inputs = entry['inputs'];
                var total_mA_sec = 0
                var avg_volt = 0
                var min_volt = 0
                var max_volt = 0
                var avg_mA = 0
                var min_mA = 0
                var max_mA = 0
                if (input_channel == 'All Batts') {
                            console.log('input_channel '+ input_channel)
                    var key_list = Object.keys(inputs)
                    var batt_count = 0
                    for ( var key_index=0; key_index<key_list.length ; key_index++) {
                        if (key_list[key_index].startsWith('Batt')) {
                            var input_data = inputs[key_list[key_index]];
                            total_mA_sec += input_data[0]
                            avg_volt += input_data[1]
                            min_volt += input_data[2]
                            max_volt += input_data[3]
                            avg_mA += input_data[4]
                            min_mA += input_data[5]
                            max_mA += input_data[6] 
                            batt_count += 1
                        }
                    }
                    if (batt_count != 0) {
                        avg_volt /= batt_count
                        min_volt /= batt_count
                        max_volt /= batt_count
                    }
                } else {
                    var input_data = inputs[input_channel];
                    total_mA_sec = input_data[0]
                    avg_volt = input_data[1]
                    min_volt = input_data[2]
                    max_volt = input_data[3]
                    avg_mA = input_data[4]
                    min_mA = input_data[5]
                    max_mA = input_data[6]
                }
                    
                //~ console.log(input_data);

                time_hours = time_hours *60*60*1000
                avg_volt_series.push([time_hours,avg_volt])
                min_volt_series.push([time_hours,min_volt])
                max_volt_series.push([time_hours,max_volt])
                avg_mA_series.push({ x:time_hours, y:avg_mA, color: get_mA_color(avg_mA, false) })
                min_mA_series.push({ x:time_hours, y:min_mA, color: get_mA_color(min_mA, true) })
                max_mA_series.push({ x:time_hours, y:max_mA, color: get_mA_color(max_mA, true) })
                //~ min_mA_series.push([time_hours,min_mA])
                //~ max_mA_series.push([time_hours,max_mA])
            }
        }
        var series_entry;
        
        series_entry = {
                name: input_channel+' Avg Voltage',
                color: "#ffa500",
                type: 'line',
                yAxis: 1,
                data: avg_volt_series,
                tooltip: { valueSuffix: ' volts' }};
        myChart['series'].push(series_entry);
        
        series_entry = {
                name: input_channel+' Min Voltage',
                color: "#ffa50020",
                marker: {enabled: false},
                type: 'line',
                yAxis: 1,
                data: min_volt_series,
                tooltip: { valueSuffix: ' volts' }};
        myChart['series'].push(series_entry);
        
        series_entry = {
                name: input_channel+' Max Voltage',
                color: "#ffa50020",
                marker: {enabled: false},
                type: 'line',
                yAxis: 1,
                data: max_volt_series,
                tooltip: { valueSuffix: ' volts' }};
        myChart['series'].push(series_entry);
        
        
        series_entry = {
                name: input_channel+' Avg mA',
                zoneAxis: 'y',
                zones: [{value:0, color:'#ff0000'}, {color:'#00ff00'}],
                color: '#00ff0020',
                type: 'line',
                yAxis: 0,
                data: avg_mA_series,
                tooltip: { valueSuffix: ' mA' }};
        myChart['series'].push(series_entry);
        
        series_entry = {
                name: input_channel+' Min mA',
                zoneAxis: 'y',
                zones: [{value:0, color:'#ff000020'}, {color:'#00ff0020'}],
                color: '#00ff0020',
                marker: {enabled: false},
                type: 'line',
                yAxis: 0,
                data: min_mA_series,
                tooltip: { valueSuffix: ' mA' }};
        myChart['series'].push(series_entry);
        
        series_entry = {
                name: input_channel+' Max mA',
                zoneAxis: 'y',
                zones: [{value:0, color:'#ff000020'}, {color:'#00ff0020'}],
                color: '#00ff0020',
                marker: {enabled: false},
                type: 'line',
                yAxis: 0,
                data: max_mA_series,
                tooltip: { valueSuffix: ' mA' }};
        myChart['series'].push(series_entry);
        
        
        myChart['title']['text'] = 'Solar - '+input_channel + ' - ' + date_text
        
        
        //~ console.log(Object.keys(myChart));
        //~ console.log(avg_volt_series);
    //~ var btn = document.createElement("BUTTON");   // Create a <button> element
    //~ btn.innerHTML = "CLICK ME";                   // Insert text
    //~ document.body.appendChild(btn);               // Append <button> to <body>


        Highcharts.chart('left', myChart);
    }

 });
