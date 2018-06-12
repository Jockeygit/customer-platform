/*------------------------------------------------------
    Author : www.webthemez.com
    License: Commons Attribution 3.0
    http://creativecommons.org/licenses/by/3.0/
---------------------------------------------------------  */

(function ($) {
    "use strict";
    var mainApp = {

        initFunction: function () {
            /*MENU 
            ------------------------------------*/
            $('#main-menu').metisMenu();
			
            $(window).bind("load resize", function () {
                if ($(this).width() < 768) {
                    $('div.sidebar-collapse').addClass('collapse')
                } else {
                    $('div.sidebar-collapse').removeClass('collapse')
                }
            });

            /* MORRIS BAR CHART
			-----------------------------------------*/
            Morris.Bar({
                element: 'morris-bar-chart',
                data: [{
                    y: '2018-01',
                    a: 2500,
                    b: 2100
                }, {
                    y: '2018-02',
                    a: 2850,
                    b: 2650
                }, {
                    y: '2018-03',
                    a: 2200,
                    b: 2700
                }, {
                    y: '2018-04',
                    a: 2350,
                    b: 2650
                }, {
                    y: '2018-05',
                    a: 2500,
                    b: 2400
                }, {
                    y: '2018-06',
                    a: 2250,
                    b: 2750
                }],
                xkey: 'y',
                ykeys: ['a', 'b'],
                labels: ['预收费', '实收费'],
                barColors: [
                '#A6A6A6','#2DAFCB',
                '#67C69D'
                 ],
                hideHover: 'auto',
                resize: true
            });

            /* MORRIS DONUT CHART
			----------------------------------------*/
            Morris.Donut({
                element: 'morris-donut-chart',
                data: [{
                    label: "已完成",
                    value: 4
                }, {
                    label: "进行中",
                    value: 6
                }, {
                    label: "未开始",
                    value: 3
                }],
                 colors: [
                    '#A6A6A6','#2DAFCB',
                    '#F98484'
                 ],
                resize: true
            });



            /* MORRIS LINE CHART
			----------------------------------------*/
            Morris.Line({
                element: 'morris-line-chart',
                data: [{
                    y: '2018-01',
                    a: 100,
                    b: 80
                }, {
                    y: '2018-02',
                    a: 75,
                    b: 75
                }, {
                    y: '2018-03',
                    a: 50,
                    b: 55
                }, {
                    y: '2018-04',
                    a: 75,
                    b: 85
                }, {
                    y: '2018-05',
                    a: 50,
                    b: 40
                }, {
                    y: '2018-06',
                    a: 75,
                    b: 65
                }],
                xkey: 'y',
                ykeys: ['a', 'b'],
                labels: ['预期增长量', '实际增长量'],
                hideHover: 'auto',
                resize: true,
                pointFillColors:['#ffffff'],
                pointStrokeColors: ['black'],
                lineColors:['gray','#2DAFCB']

            });
           
     
        },

        initialization: function () {
            mainApp.initFunction();

        }

    }
    // Initializing ///

    $(document).ready(function () {
        mainApp.initFunction();
    });

}(jQuery));
