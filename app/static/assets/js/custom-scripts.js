/*------------------------------------------------------
    Author : www.webthemez.com
    License: Commons Attribution 3.0
    http://creativecommons.org/licenses/by/3.0/
---------------------------------------------------------  */
/*
(function ($) {
    "use strict";
    var mainApp = {

        initFunction: function () {

            $('#main-menu').metisMenu();
			
            $(window).bind("load resize", function () {
                if ($(this).width() < 768) {
                    $('div.sidebar-collapse').addClass('collapse')
                } else {
                    $('div.sidebar-collapse').removeClass('collapse')
                }
            });


            Morris.Bar({
                element: 'morris-bar-chart',
                data: [{
                    y: '2006',
                    a: 100,
                    b: 90
                }, {
                    y: '2007',
                    a: 75,
                    b: 65
                }, {
                    y: '2008',
                    a: 50,
                    b: 40
                }, {
                    y: '2009',
                    a: 75,
                    b: 65
                }, {
                    y: '2010',
                    a: 50,
                    b: 40
                }, {
                    y: '2011',
                    a: 75,
                    b: 65
                }, {
                    y: '2012',
                    a: 100,
                    b: 90
                }],
                xkey: 'y',
                ykeys: ['a', 'b'],
                labels: ['Series A', 'Series B'],
				 barColors: [
    '#A6A6A6','#2DAFCB',
    '#67C69D' 
  ],
                hideHover: 'auto',
                resize: true
            });
	 



            Morris.Donut({
                element: 'morris-donut-chart',
                data: [{
                    label: "Download Sales",
                    value: 12
                }, {
                    label: "In-Store Sales",
                    value: 30
                }, {
                    label: "Mail-Order Sales",
                    value: 20
                }],
				   colors: [
    '#A6A6A6','#2DAFCB',
    '#F98484' 
  ],
                resize: true
            });



            Morris.Area({
                element: 'morris-area-chart',
                data: [{
                    period: '2010 Q1',
                    iphone: 2666,
                    ipad: null,
                    itouch: 2647
                }, {
                    period: '2010 Q2',
                    iphone: 2778,
                    ipad: 2294,
                    itouch: 2441
                }, {
                    period: '2010 Q3',
                    iphone: 4912,
                    ipad: 1969,
                    itouch: 2501
                }, {
                    period: '2010 Q4',
                    iphone: 3767,
                    ipad: 3597,
                    itouch: 5689
                }, {
                    period: '2011 Q1',
                    iphone: 6810,
                    ipad: 1914,
                    itouch: 2293
                }, {
                    period: '2011 Q2',
                    iphone: 5670,
                    ipad: 4293,
                    itouch: 1881
                }, {
                    period: '2011 Q3',
                    iphone: 4820,
                    ipad: 3795,
                    itouch: 1588
                }, {
                    period: '2011 Q4',
                    iphone: 15073,
                    ipad: 5967,
                    itouch: 5175
                }, {
                    period: '2012 Q1',
                    iphone: 10687,
                    ipad: 4460,
                    itouch: 2028
                }, {
                    period: '2012 Q2',
                    iphone: 8432,
                    ipad: 5713,
                    itouch: 1791
                }],
                xkey: 'period',
                ykeys: ['iphone', 'ipad', 'itouch'],
                labels: ['iPhone', 'iPad', 'iPod Touch'],
                pointSize: 2,
                hideHover: 'auto',
				  pointFillColors:['#ffffff'],
				  pointStrokeColors: ['black'],
				  lineColors:['#A6A6A6','#2DAFCB'],
                resize: true
            });


            Morris.Line({
                element: 'morris-line-chart',
                data: [
					  { y: '2014', a: 50, b: 90},
					  { y: '2015', a: 165,  b: 185},
					  { y: '2016', a: 150,  b: 130},
					  { y: '2017', a: 175,  b: 160},
					  { y: '2018', a: 80,  b: 65},
					  { y: '2019', a: 90,  b: 70},
					  { y: '2020', a: 100, b: 125},
					  { y: '2021', a: 155, b: 175},
					  { y: '2022', a: 80, b: 85},
					  { y: '2023', a: 145, b: 155},
					  { y: '2024', a: 160, b: 195}
				],
            
				 
      xkey: 'y',
      ykeys: ['a', 'b'],
      labels: ['Total Income', 'Total Outcome'],
      fillOpacity: 0.6,
      hideHover: 'auto',
      behaveLikeLine: true,
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

    //$(document).ready(function () {
        //mainApp.initFunction();
    //});

}(jQuery));*/

/*单选框*/
(function( $ ){
	$.fn.labelauty = function( options )
	{
		return this.each(function()
		{
			var $object = $( this );
			var lable;

            if( $object.is( ":checkbox" ) === false && $object.is( ":radio" ) === false )
				return this;

			lable = $object.next();
            lable.css("margin-right","10px");
			$object.addClass('labelauty');
			$object.css("display", "none");
			lable_text = lable.text();

			block = '<span class="labelauty-unchecked-image"></span>' +
					'<span class="labelauty-unchecked">' + lable_text + '</span>' +
					'<span class="labelauty-checked-image"></span>' +
					'<span class="labelauty-checked">' + lable_text + '</span>' ;

			lable.html(block);
		});
	};

}( jQuery ));

//toastr设置
$(function() {
    //参数设置，若用默认值可以省略以下
    toastr.options = {

        "closeButton": false, //是否显示关闭按钮

        "debug": false, //是否使用debug模式

        //"positionClass": "toast-top-center",//弹出窗的位置

        "showDuration": "300",//显示的动画时间

        "hideDuration": "1000",//消失的动画时间

        "timeOut": "3000", //展现时间

        "extendedTimeOut": "1000",//加长展示时间

        "showEasing": "swing",//显示时的动画缓冲方式

        "hideEasing": "linear",//消失时的动画缓冲方式

        "showMethod": "fadeIn",//显示时的动画方式

        "hideMethod": "fadeOut" //消失时的动画方式

    };
});

