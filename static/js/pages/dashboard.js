


$(function () {

  'use strict';
	
		//  var plot = $.plot('#flotChart', [{
        //   data: flotSampleData3,
        //   color: '#38b8f2',
        //   lines: {
        //     fillColor: { colors: [{ opacity: 0 }, { opacity: 0.5 }]}
        //   }
        // },{
        //   data: flotSampleData4,
        //   color: '#ec4b71',
        //   lines: {
        //     fillColor: { colors: [{ opacity: 0 }, { opacity: 0.5 }]}
        //   }
        // }], {
    	// 		series: {
    	// 			shadowSize: 1,
        //     lines: {
        //       show: true,
        //       lineWidth: 2,
        //       fill: true
        //     }
    	// 		},
        //   grid: {
        //     borderWidth: 0,
        //     labelMargin: 8
        //   },
    	// 		yaxis: {
        //     			show: true,
    	// 				min: 0,
    	// 				max: 100,
        //     			ticks: [[0,''],[20,'20K'],[40,'40K'],[60,'60K'],[80,'80K']],
        //     			tickColor: 'rgba(255, 255, 255, 0.10)',
		// 				font: {
		// 					color: '#666666'
		// 				  }
    	// 		},
    	// 		xaxis: {
        //     			show: true,
        //     			color: 'rgba(255, 255, 255, 0.10)',
        //     			ticks: [[25,'OCT 21'],[75,'OCT 22'],[100,'OCT 23'],[125,'OCT 24']],
		// 				font: {
		// 					color: '#666666'
		// 				  }
        //   }
        // });
	
		
	
		var options = {
            chart: {
                height: 435,
                type: 'bar',
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '55%'	
                },
            },
            dataLabels: {
                enabled: false
            },
			colors: ["#FF2829", '#40a2ed'],
            stroke: {
                show: true,
                width: 2,
                colors: ['transparent']
            },
            series: [{
                name: 'Disbursed',
                data: [76, 85, 101, 98, 87, 105, 91]
            }, {
                name: 'Paid Back',
                data: [35, 41, 36, 26, 45, 48, 52]
            }],
            xaxis: {
                categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Set', 'Sun'],
            },
            fill: {
                opacity: 1

            },
			  legend: {
				position: 'top',
				horizontalAlign: 'left'
			  },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return "$ " + val + " thousands"
                    }
                }
            }
        }

        var chart = new ApexCharts(
            document.querySelector("#userflow"),
            options
        );

        chart.render();
	
	
		var options = {
		  chart: {
			height: 383,
			type: 'line',
			shadow: {
			  enabled: false,
			  color: '#bbb',
			  top: 3,
			  left: 2,
			  blur: 3,
			  opacity: 1
			},
		  },
		  stroke: {
			width: 5,
			curve: 'smooth'
		  },
		  series: [{
			name: 'Likes',
			data: [4, 3, 10, 9, 29, 19, 22, 9, 12, 7, 19, 5, 13, 9, 17, 2, 7, 5]
		  }],
		  xaxis: {
			type: 'datetime',
			categories: ['1/11/2000', '2/11/2000', '3/11/2000', '4/11/2000', '5/11/2000', '6/11/2000', '7/11/2000', '8/11/2000', '9/11/2000', '10/11/2000', '11/11/2000', '12/11/2000', '1/11/2001', '2/11/2001', '3/11/2001', '4/11/2001', '5/11/2001', '6/11/2001'],
			axisBorder: {
			  show: true,
			  color: '#bec7e0',
			},  
			axisTicks: {
			  show: true,
			  color: '#bec7e0',
			},    
		  },
		  fill: {
			type: 'gradient',
			gradient: {
			  shade: 'dark',
			  gradientToColors: ['#40a2ed'],
			  shadeIntensity: 1,
			  type: 'horizontal',
			  opacityFrom: 1,
			  opacityTo: 1,
			  stops: [0, 100, 100, 100]
			},
		  },
		  markers: {
			size: 4,
			opacity: 0.9,
			colors: ["#FF2829"],
			strokeColor: "#fff",
			strokeWidth: 2,
			style: 'inverted', // full, hollow, inverted
			hover: {
			  size: 7,
			}
		  },
		  yaxis: {
			min: -10,
			max: 40,
			title: {
			  text: 'Engagement',
			},
		  },
		  grid: {
			row: {
			  colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
			  opacity: 0.2
			},
			borderColor: '#f7f7f7'
		  },
		  responsive: [{
			breakpoint: 600,
			options: {
			  chart: {
				toolbar: {
				  show: false
				}
			  },
			  legend: {
				show: false
			  },
			}
		  }]
		}

		var chart = new ApexCharts(
		  document.querySelector("#growth"),
		  options
		);

		chart.render();
	
	
	var options = {
        series: [17, 22, 19, 47],
        chart: {
          type: 'donut',
			width: '100%',
      		height: 240
        },
		colors:['#40a2ed', '#33ac2e', '#25b5b5', '#FF2829'],
		legend: {
		  show: false,
		},
		dataLabels: {
			enabled: false,
		  },
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              width: 200
            },
          }
        }]
      };

      var chart = new ApexCharts(document.querySelector("#earning-chart"), options);
      chart.render();
	
	
	
	
	var options1 = {
        series: [{
          data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54]
        }],
        chart: {
          type: 'line',
          width: 100,
          height: 80,
          sparkline: {
            enabled: true
          }
        },
		 stroke: {
          curve: 'smooth',
			 width: 3,
        },
		 
		markers: {
			size: 0,
		},
        tooltip: {
			theme: 'dark',
          fixed: {
            enabled: false
          },
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function (seriesName) {
                return ''
              }
            }
          },
          marker: {
            show: false
          }
        }
      };

      var chart1 = new ApexCharts(document.querySelector("#visitors-char"), options1);
      chart1.render();
		
      
	
}); // End of use strict
