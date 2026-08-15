Does not reproduce with the given config: https://codepen.io/kurkle/pen/yLgLrxv

Are you perhaps changing the scale ticks in some way?
@kurkle 
Thanks for for testing
> Are you perhaps changing the scale ticks in some way?

Negativ, i do not set scale ticks with global settings.
```
{
    "type": "scatter",
    "data": {
        "labels": [],
        "datasets": [
            {
                "label": "Reni",
                "unit": "%",
                "hoverRadius": 18,
                "pointRadius": 16,
                "hitRadius": 22,
                "backgroundColor": "rgba(192,57,43,0.85)",
                "borderColor": "rgba(192,57,43,0.85)",
                "data": [
                    {
                        "x": 17.65,
                        "y": 17.8
                    },
                    {
                        "x": 17.65,
                        "y": 17.8
                    },
                    {
                        "x": 18.01,
                        "y": 17.84
                    },
                    {
                        "x": 17.61,
                        "y": 17.95
                    },
                    {
                        "x": 17.78,
                        "y": 17.87
                    },
                    {
                        "x": 16.76,
                        "y": 17.98
                    },
                    {
                        "x": 17.11,
                        "y": 17.89
                    }
                ]
            },
            {
                "label": "Peter",
                "unit": "%",
                "hoverRadius": 18,
                "pointRadius": 16,
                "hitRadius": 22,
                "backgroundColor": "rgba(230,126,34,0.85)",
                "borderColor": "rgba(230,126,34,0.85)",
                "data": [
                    {
                        "x": 12.36,
                        "y": 22.51
                    },
                    {
                        "x": 12.23,
                        "y": 22.42
                    },
                    {
                        "x": 12.23,
                        "y": 22.42
                    },
                    {
                        "x": 12.22,
                        "y": 22.48
                    },
                    {
                        "x": 12.51,
                        "y": 22.6
                    },
                    {
                        "x": 12.25,
                        "y": 22.45
                    },
                    {
                        "x": 12.35,
                        "y": 22.53
                    }
                ]
            }
        ]
    },
    "options": {
        "units": "",
        "layout": {},
        "chartArea": {
            "backgroundColor": "transparent"
        },
        "hover": {
            "mode": "nearest",
            "intersect": true
        },
        "elements": {},
        "spanGaps": true,
        "plugins": {
            "title": {},
            "tooltip": {},
            "legend": {
                "display": true,
                "position": "top"
            },
            "scales": {}
        },
        "animation": {},
        "onResize": null,
        "scales": {
            "x": {
                "axis": "x",
                "type": "linear",
                "ticks": {
                    "minRotation": 0,
                    "maxRotation": 50,
                    "mirror": false,
                    "textStrokeWidth": 0,
                    "textStrokeColor": "",
                    "padding": 3,
                    "display": true,
                    "autoSkip": true,
                    "autoSkipPadding": 3,
                    "labelOffset": 0,
                    "minor": {},
                    "major": {},
                    "align": "center",
                    "crossAlign": "near",
                    "color": "#ecf0f1"
                },
                "display": true,
                "offset": false,
                "reverse": false,
                "beginAtZero": false,
                "bounds": "ticks",
                "grace": 0,
                "grid": {
                    "display": true,
                    "lineWidth": 0.55,
                    "drawBorder": true,
                    "drawOnChartArea": true,
                    "drawTicks": true,
                    "tickLength": 8,
                    "offset": false,
                    "borderDash": [
                        2,
                        1
                    ],
                    "borderDashOffset": 0,
                    "color": "#d3d7cf",
                    "zeroLineWidth": 8
                },
                "title": {
                    "display": false,
                    "text": "",
                    "padding": {
                        "top": 4,
                        "bottom": 4
                    },
                    "color": "#ecf0f1"
                },
                "id": "x",
                "position": "bottom"
            },
            "y": {
                "axis": "y",
                "type": "linear",
                "ticks": {
                    "minRotation": 0,
                    "maxRotation": 50,
                    "mirror": false,
                    "textStrokeWidth": 0,
                    "textStrokeColor": "",
                    "padding": 3,
                    "display": true,
                    "autoSkip": true,
                    "autoSkipPadding": 3,
                    "labelOffset": 0,
                    "minor": {},
                    "major": {},
                    "align": "center",
                    "crossAlign": "near",
                    "color": "#ecf0f1"
                },
                "display": true,
                "offset": false,
                "reverse": false,
                "beginAtZero": false,
                "bounds": "ticks",
                "grace": 0,
                "grid": {
                    "display": true,
                    "lineWidth": 0.55,
                    "drawBorder": true,
                    "drawOnChartArea": true,
                    "drawTicks": true,
                    "tickLength": 8,
                    "offset": false,
                    "borderDash": [
                        2,
                        1
                    ],
                    "borderDashOffset": 0,
                    "color": "#d3d7cf",
                    "zeroLineWidth": 8
                },
                "title": {
                    "display": false,
                    "text": "",
                    "padding": {
                        "top": 4,
                        "bottom": 4
                    },
                    "color": "#ecf0f1"
                },
                "id": "y",
                "position": "left"
            }
        }
    }
}
```
Does not reproduce with that config either. What is the `scales` plugin?
@kurkle 
> What is the `scales` plugin?


This was configuration option error, but was never used. 
Even if I remove it, the error still comes. 
All other charts work perfectly, only with the scatter graph this error occurs when I set the layout globally. 

My problem is that I can't do it in any simple test case. I only see that when it occurs:
```
let delta = ticks.length> 3? 
                  ticks [2] .value - ticks [1] .value: 
                  ticks [1] .value - ticks [0] .value;
```
In the event of an error, `ticks.length == 0` and therefore the error is thrown when calculating `ticks [1] .value - ticks [0] .value`.

Only way I can reproduce, is setting `sampleSize: 0` in scale tick options. Anything about `sampleSize` in your code? 
@kurkle 

> Only way I can reproduce, is setting `sampleSize: 0` in scale tick options. Anything about `sampleSize` in your code?

Thanks. No i do not set the sampleSize ?

The global setting are:
```
{
    "animation": {
        "duration": 1000,
        "easing": "easeOutQuart"
    },
    "backgroundColor": "rgba(0,0,0,0.1)",
    "borderColor": "rgba(0,0,0,0.1)",
    "color": "#666",
    "datasets": {
        "bar": {
            "datasetElementType": false,
            "dataElementType": "bar",
            "categoryPercentage": 0.8,
            "barPercentage": 0.9,
            "grouped": true,
            "animations": {
                "numbers": {
                    "type": "number",
                    "properties": [
                        "x",
                        "y",
                        "base",
                        "width",
                        "height"
                    ]
                }
            }
        },
        "bubble": {
            "datasetElementType": false,
            "dataElementType": "point",
            "animations": {
                "numbers": {
                    "type": "number",
                    "properties": [
                        "x",
                        "y",
                        "borderWidth",
                        "radius"
                    ]
                }
            }
        },
        "doughnut": {
            "datasetElementType": false,
            "dataElementType": "arc",
            "animation": {
                "animateRotate": true,
                "animateScale": false
            },
            "animations": {
                "numbers": {
                    "type": "number",
                    "properties": [
                        "circumference",
                        "endAngle",
                        "innerRadius",
                        "outerRadius",
                        "startAngle",
                        "x",
                        "y",
                        "offset",
                        "borderWidth"
                    ]
                }
            },
            "cutout": "50%",
            "rotation": 0,
            "circumference": 360,
            "radius": "100%",
            "indexAxis": "r"
        },
        "line": {
            "datasetElementType": "line",
            "dataElementType": "point",
            "showLine": true,
            "spanGaps": false
        },
        "polarArea": {
            "dataElementType": "arc",
            "animation": {
                "animateRotate": true,
                "animateScale": true
            },
            "animations": {
                "numbers": {
                    "type": "number",
                    "properties": [
                        "x",
                        "y",
                        "startAngle",
                        "endAngle",
                        "innerRadius",
                        "outerRadius"
                    ]
                }
            },
            "indexAxis": "r",
            "startAngle": 0
        },
        "pie": {
            "datasetElementType": false,
            "dataElementType": "arc",
            "animation": {
                "animateRotate": true,
                "animateScale": false
            },
            "animations": {
                "numbers": {
                    "type": "number",
                    "properties": [
                        "circumference",
                        "endAngle",
                        "innerRadius",
                        "outerRadius",
                        "startAngle",
                        "x",
                        "y",
                        "offset",
                        "borderWidth"
                    ]
                }
            },
            "cutout": 0,
            "rotation": 0,
            "circumference": 360,
            "radius": "100%",
            "indexAxis": "r"
        },
        "radar": {
            "datasetElementType": "line",
            "dataElementType": "point",
            "indexAxis": "r",
            "showLine": true,
            "elements": {
                "line": {
                    "fill": "start"
                }
            }
        },
        "scatter": {
            "datasetElementType": "line",
            "dataElementType": "point",
            "showLine": false,
            "spanGaps": false,
            "fill": false
        }
    },
    "elements": {
        "arc": {
            "borderAlign": "center",
            "borderColor": "#fff",
            "borderWidth": 0,
            "offset": 0,
            "backgroundColor": "rgba(0,0,0,0.1)"
        },
        "line": {
            "borderCapStyle": "butt",
            "borderDash": [],
            "borderDashOffset": 0,
            "borderJoinStyle": "miter",
            "borderWidth": 3,
            "capBezierPoints": true,
            "cubicInterpolationMode": "default",
            "fill": false,
            "spanGaps": false,
            "stepped": false,
            "tension": 0.225,
            "backgroundColor": "rgba(0,0,0,0.1)",
            "borderColor": "rgba(0,0,0,0.1)"
        },
        "point": {
            "borderWidth": 0,
            "hitRadius": 8,
            "hoverBorderWidth": 1,
            "hoverRadius": 8,
            "pointStyle": "circle",
            "radius": 3,
            "rotation": 0,
            "backgroundColor": "rgba(0,0,0,0.1)",
            "borderColor": "rgba(0,0,0,0.1)"
        },
        "bar": {
            "borderSkipped": "start",
            "borderWidth": 0,
            "borderRadius": 0,
            "backgroundColor": "rgba(0,0,0,0.1)",
            "borderColor": "rgba(0,0,0,0.1)"
        }
    },
    "events": [
        "mousemove",
        "mouseout",
        "click",
        "touchstart",
        "touchmove"
    ],
    "font": {
        "family": "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
        "size": 12,
        "style": "normal",
        "lineHeight": 1.2,
        "weight": null
    },
    "hover": {
        "onHover": null
    },
    "indexAxis": "x",
    "interaction": {
        "mode": "nearest",
        "intersect": true
    },
    "maintainAspectRatio": true,
    "onHover": null,
    "onClick": null,
    "parsing": true,
    "plugins": {
        "decimation": {
            "algorithm": "min-max",
            "enabled": false
        },
        "filler": {
            "propagate": true
        },
        "legend": {
            "display": true,
            "position": "top",
            "align": "center",
            "fullSize": true,
            "reverse": false,
            "weight": 1000,
            "onHover": null,
            "onLeave": null,
            "labels": {
                "boxWidth": 8,
                "padding": 10,
                "usePointStyle": true
            },
            "title": {
                "display": false,
                "position": "center",
                "text": ""
            },
            "show": false
        },
        "title": {
            "align": "center",
            "display": false,
            "font": {
                "style": "bold"
            },
            "fullSize": true,
            "padding": 10,
            "position": "top",
            "text": "",
            "weight": 2000,
            "color": "#666"
        },
        "tooltip": {
            "enabled": true,
            "external": null,
            "position": "average",
            "backgroundColor": "#ecf0f1",
            "titleColor": "#2c3e50",
            "titleFont": {
                "family": "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                "size": 12,
                "style": "bold",
                "lineHeight": 1.2,
                "weight": null
            },
            "titleSpacing": 2,
            "titleMarginBottom": 6,
            "titleAlign": "left",
            "bodyColor": "#2c3e50",
            "bodySpacing": 2,
            "bodyFont": {
                "family": "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                "size": 12,
                "style": "normal",
                "lineHeight": 1.2,
                "weight": null
            },
            "bodyAlign": "left",
            "footerColor": "#2c3e50",
            "footerSpacing": 2,
            "footerMarginTop": 6,
            "footerFont": {
                "family": "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                "size": 12,
                "style": "bold",
                "lineHeight": 1.2,
                "weight": null
            },
            "footerAlign": "left",
            "padding": 6,
            "caretPadding": 2,
            "caretSize": 5,
            "cornerRadius": 6,
            "multiKeyBackground": "#fff",
            "displayColors": true,
            "borderColor": "rgba(0,0,0,0)",
            "borderWidth": 0,
            "animation": {
                "duration": 400,
                "easing": "easeOutQuart"
            },
            "animations": {
                "numbers": {
                    "type": "number",
                    "properties": [
                        "x",
                        "y",
                        "width",
                        "height",
                        "caretX",
                        "caretY"
                    ]
                },
                "opacity": {
                    "easing": "linear",
                    "duration": 200
                }
            },
            "callbacks": {}
        }
    },
    "responsive": true,
    "scale": {
        "display": true,
        "offset": false,
        "reverse": false,
        "beginAtZero": false,
        "bounds": "ticks",
        "grace": 0,
        "grid": {
            "display": true,
            "lineWidth": 0.55,
            "drawBorder": true,
            "drawOnChartArea": true,
            "drawTicks": true,
            "tickLength": 8,
            "offset": false,
            "borderDash": [
                2,
                1
            ],
            "borderDashOffset": 0,
            "color": "#d3d7cf",
            "zeroLineWidth": 8
        },
        "title": {
            "display": false,
            "text": "",
            "padding": {
                "top": 4,
                "bottom": 4
            },
            "color": "#666"
        },
        "ticks": {
            "minRotation": 0,
            "maxRotation": 50,
            "mirror": false,
            "textStrokeWidth": 0,
            "textStrokeColor": "",
            "padding": 3,
            "display": true,
            "autoSkip": true,
            "autoSkipPadding": 3,
            "labelOffset": 0,
            "minor": {},
            "major": {},
            "align": "center",
            "crossAlign": "near",
            "color": "#666"
        }
    },
    "scales": {
        "category": {
            "ticks": {}
        },
        "linear": {
            "ticks": {}
        },
        "logarithmic": {
            "ticks": {
                "major": {
                    "enabled": true
                }
            }
        },
        "radialLinear": {
            "display": true,
            "animate": true,
            "position": "chartArea",
            "angleLines": {
                "display": true,
                "lineWidth": 1,
                "borderDash": [],
                "borderDashOffset": 0,
                "color": "rgba(0,0,0,0.1)"
            },
            "grid": {
                "circular": false
            },
            "startAngle": 0,
            "ticks": {
                "showLabelBackdrop": true,
                "backdropColor": "rgba(255,255,255,0.75)",
                "backdropPadding": 2,
                "color": "#666"
            },
            "pointLabels": {
                "backdropPadding": 2,
                "display": true,
                "font": {
                    "size": 10
                },
                "padding": 5,
                "color": "#666"
            }
        },
        "time": {
            "bounds": "data",
            "adapters": {},
            "time": {
                "parser": false,
                "unit": false,
                "round": false,
                "isoWeekday": false,
                "minUnit": "millisecond",
                "displayFormats": {}
            },
            "ticks": {
                "source": "auto",
                "major": {
                    "enabled": false
                }
            }
        },
        "timeseries": {
            "bounds": "data",
            "adapters": {},
            "time": {
                "parser": false,
                "unit": false,
                "round": false,
                "isoWeekday": false,
                "minUnit": "millisecond",
                "displayFormats": {}
            },
            "ticks": {
                "source": "auto",
                "major": {
                    "enabled": false
                }
            }
        }
    },
    "showLine": true,
    "layout": {
        "padding": {
            "top": 24,
            "left": 0,
            "right": 0,
            "bottom": 0
        }
    },
    "animations": {
        "colors": {
            "type": "color",
            "properties": [
                "color",
                "borderColor",
                "backgroundColor"
            ]
        },
        "numbers": {
            "type": "number",
            "properties": [
                "x",
                "y",
                "borderWidth",
                "radius",
                "tension"
            ]
        }
    },
    "transitions": {
        "active": {
            "animation": {
                "duration": 400
            }
        },
        "resize": {
            "animation": {
                "duration": 0
            }
        },
        "show": {
            "animations": {
                "colors": {
                    "from": "transparent"
                },
                "visible": {
                    "type": "boolean",
                    "duration": 0
                }
            }
        },
        "hide": {
            "animations": {
                "colors": {
                    "to": "transparent"
                },
                "visible": {
                    "type": "boolean",
                    "easing": "linear"
                }
            }
        }
    }
}
```
I am also getting the same error at the same line reported, with the following config:


```json
{
  "type": "line",
  "data": {
    "labels": [
      0,
      20000,
      306000,
      366000,
      426000,
      487000,
      547000,
      607000,
      668000,
      728000,
      788000,
      848000,
      849000,
      909000,
      969000,
      1032000,
      1092000,
      1153000,
      1213000,
      1274000,
      1334000,
      1394000,
      1454000,
      1514000,
      1575000,
      1598000
    ],
    "datasets": [
      {
        "borderCapStyle": "square",
        "borderColor": {},
        "borderJoinStyle": "bevel",
        "borderWidth": 2,
        "clip": 0,
        "data": [
          {
            "x": 0,
            "y": 0
          },
          {
            "x": 20000,
            "y": 1338
          },
          {
            "x": 306000,
            "y": 2068
          },
          {
            "x": 366000,
            "y": 3017
          },
          {
            "x": 426000,
            "y": 3403
          },
          {
            "x": 487000,
            "y": 4088
          },
          {
            "x": 547000,
            "y": 4575
          },
          {
            "x": 607000,
            "y": 4536
          },
          {
            "x": 668000,
            "y": 4510
          },
          {
            "x": 728000,
            "y": 5097
          },
          {
            "x": 788000,
            "y": 6214
          },
          {
            "x": 848000,
            "y": 7059
          },
          {
            "x": 849000,
            "y": 210
          },
          {
            "x": 909000,
            "y": 9534
          },
          {
            "x": 969000,
            "y": 9189
          },
          {
            "x": 1032000,
            "y": 9588
          },
          {
            "x": 1092000,
            "y": 9578
          },
          {
            "x": 1153000,
            "y": 9986
          },
          {
            "x": 1213000,
            "y": 10039
          },
          {
            "x": 1274000,
            "y": 10830
          },
          {
            "x": 1334000,
            "y": 13411
          },
          {
            "x": 1394000,
            "y": 13987
          },
          {
            "x": 1454000,
            "y": 15090
          },
          {
            "x": 1514000,
            "y": 16786
          },
          {
            "x": 1575000,
            "y": 19129
          },
          {
            "x": 1598000,
            "y": 20876
          }
        ],
        "fill": {
          "target": "origin",
          "above": "rgba(41, 155, 89, 0.1)",
          "below": "rgba(230, 70, 60, 0.1)"
        },
        "pointBorderWidth": 0,
        "pointRadius": 0,
        "normalized": true,
        "parsing": false,
        "showLine": true
      }
    ]
  },
  "options": {
    "animation": {
      "duration": 0.2,
      "delay": 0
    },
    "responsive": true,
    "maintainAspectRatio": false,
    "elements": {
      "line": {
        "tension": 0.4
      },
      "point": {
        "radius": 0
      }
    },
    "plugins": {
      "decimation": {
        "enabled": true
      },
      "filler": {
        "propagate": true
      },
      "tooltip": {
        "backgroundColor": {},
        "caretSize": 0,
        "caretPadding": 0,
        "cornerRadius": 6,
        "displayColors": false,
        "intersect": false,
        "padding": {
          "top": 4,
          "right": 0,
          "bottom": 4,
          "left": 6
        },
        "callbacks": {}
      }
    },
    "scales": {
      "x": {
        "axis": "x",
        "display": true,
        "min": 0,
        "max": 1598000,
        "type": "time",
        "time": {
          "stepSize": 300,
          "parser": false,
          "unit": false,
          "round": false,
          "isoWeekday": false,
          "minUnit": "millisecond",
          "displayFormats": {
            "datetime": "MMM d, yyyy, h:mm:ss aaaa",
            "millisecond": "h:mm:ss.SSS aaaa",
            "second": "h:mm:ss aaaa",
            "minute": "h:mm aaaa",
            "hour": "ha",
            "day": "MMM d",
            "week": "PP",
            "month": "MMM yyyy",
            "quarter": "qqq - yyyy",
            "year": "yyyy"
          }
        },
        "ticks": {
          "display": false,
          "source": "auto",
          "major": {
            "enabled": false
          },
          "minRotation": 0,
          "maxRotation": 50,
          "mirror": false,
          "textStrokeWidth": 0,
          "textStrokeColor": "",
          "padding": 3,
          "autoSkip": true,
          "autoSkipPadding": 3,
          "labelOffset": 0,
          "minor": {},
          "align": "center",
          "crossAlign": "near",
          "color": "#666"
        },
        "grid": {
          "drawBorder": false,
          "display": false,
          "lineWidth": 1,
          "drawOnChartArea": true,
          "drawTicks": true,
          "tickLength": 8,
          "offset": false,
          "borderDash": [],
          "borderDashOffset": 0,
          "color": "rgba(0,0,0,0.1)"
        },
        "bounds": "data",
        "adapters": {},
        "offset": false,
        "reverse": false,
        "beginAtZero": false,
        "grace": 0,
        "title": {
          "display": false,
          "text": "",
          "padding": {
            "top": 4,
            "bottom": 4
          },
          "color": "#666"
        },
        "id": "x",
        "position": "bottom"
      },
      "y": {
        "axis": "y",
        "display": false,
        "min": -25000,
        "max": 25000,
        "ticks": {
          "display": false,
          "minRotation": 0,
          "maxRotation": 50,
          "mirror": false,
          "textStrokeWidth": 0,
          "textStrokeColor": "",
          "padding": 3,
          "autoSkip": true,
          "autoSkipPadding": 3,
          "labelOffset": 0,
          "minor": {},
          "major": {},
          "align": "center",
          "crossAlign": "near",
          "color": "#666"
        },
        "grid": {
          "display": false,
          "drawBorder": false,
          "borderDashOffset": 0,
          "lineWidth": 1,
          "drawOnChartArea": true,
          "drawTicks": true,
          "tickLength": 8,
          "offset": false,
          "borderDash": [],
          "color": "rgba(0,0,0,0.1)"
        },
        "type": "linear",
        "offset": false,
        "reverse": false,
        "beginAtZero": false,
        "bounds": "ticks",
        "grace": 0,
        "title": {
          "display": false,
          "text": "",
          "padding": {
            "top": 4,
            "bottom": 4
          },
          "color": "#666"
        },
        "id": "y",
        "position": "left"
      }
    },
    "spanGaps": true
  }
}
```

could it be something related to ticks being added at further positions in the array, leaving early ticks as non-existent? example:
![Screenshot 2021-03-23 at 14 54 16](https://user-images.githubusercontent.com/15842767/112159409-6ac70200-8be9-11eb-94b0-fa46cc479ca3.png)


This is what I get if I comment out the lines:

![Screenshot 2021-03-23 at 15 09 29](https://user-images.githubusercontent.com/15842767/112159893-e7f27700-8be9-11eb-9a71-47346407a482.png)

I have a live chart up with version 3.0.0-beta-12 working:
https://widget.abiosgaming.com/abios/live_1/277594

Our widgets may disappear after 24~48 hours of match completion, so let me know if you want a new link later in the future :)



