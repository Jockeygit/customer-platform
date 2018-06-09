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
                    a: 1000,
                    b: 900
                }, {
                    y: '2018-02',
                    a: 750,
                    b: 650
                }, {
                    y: '2018-03',
                    a: 500,
                    b: 700
                }, {
                    y: '2018-04',
                    a: 750,
                    b: 650
                }, {
                    y: '2018-05',
                    a: 500,
                    b: 400
                }, {
                    y: '2018-06',
                    a: 750,
                    b: 750
                }],
                xkey: 'y',
                ykeys: ['a', 'b'],
                labels: ['预收费', '实收费'],
                hideHover: 'auto',
                resize: true
            });

            /* MORRIS DONUT CHART
			----------------------------------------*/
            Morris.Donut({
                element: 'morris-donut-chart',
                data: [{
                    label: "已完成",
                    value: 12
                }, {
                    label: "进行中",
                    value: 9
                }, {
                    label: "未开始",
                    value: 6
                }],
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
                resize: true
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
