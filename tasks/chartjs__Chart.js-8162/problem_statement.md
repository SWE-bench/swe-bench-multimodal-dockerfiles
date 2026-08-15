Chart.js v3.0.0-beta.7: Legend and title are rendered twice?


## Expected Behavior

I can't figure out why this happens, because in a simple test case it works. 
It only occurs in the new Chart.js v3.0.0-beta.7 version. 

Everything works with the previous versions.
The representation is rendered correctly at first, but it looks like a redraw is being performed afterwards, which renders the legend and title again.

## Current Behavior

It doesn't happen with the LINE chart.

![Bildschirmfoto 2020-12-09 um 08 30 53](https://user-images.githubusercontent.com/30198737/101600752-0bf3c900-39fc-11eb-9f8a-3e9f05e7f3dd.png)

## Possible Solution

???
## Context

```
{
  type: 'pie',
  data: {
    labels: [
      'Eiweis',
      'Fett',
      'Kohlenhydrate'
    ],
    datasets: [
      {
        unit: 'kal',
        mode: 'current',
        label: 'Makro Nährstoffe',
        backgroundColor: [
          'rgba(115,210,22,0.85)',
          'rgba(245,121,0,0.85)',
          'rgba(52,101,164,0.85)'
        ],
        borderWidth: 0,
        showLine: false,
        data: [
          '887.0',
          '380.0',
          '1268.0'
        ]
      }
    ]
  },
  options: {
    backgroundColor: 'rgba(0,0,0,0.1)',
    borderColor: 'rgba(0,0,0,0.1)',
    color: '#e1e1e1',
    elements: {
      arc: {
        borderAlign: 'center',
        borderColor: '#fff',
        borderWidth: 0,
        offset: 0,
        backgroundColor: 'rgba(0,0,0,0.1)'
      },
      line: {
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0,
        borderJoinStyle: 'miter',
        borderWidth: 3,
        capBezierPoints: true,
        fill: false,
        tension: 0,
        backgroundColor: 'rgba(0,0,0,0.1)',
        borderColor: 'rgba(0,0,0,0.1)'
      },
      point: {
        borderWidth: 0,
        hitRadius: 8,
        hoverBorderWidth: 1,
        hoverRadius: 8,
        pointStyle: 'circle',
        radius: 0.33,
        backgroundColor: 'rgba(0,0,0,0.1)',
        borderColor: 'rgba(0,0,0,0.1)',
        pointRadius: 8
      },
      bar: {
        borderSkipped: 'start',
        borderWidth: 0,
        borderRadius: 0,
        backgroundColor: 'rgba(0,0,0,0.1)',
        borderColor: 'rgba(0,0,0,0.1)'
      }
    },
    events: [
      'mousemove',
      'mouseout',
      'click',
      'touchstart',
      'touchmove'
    ],
    font: {
      family: '"Roboto", "Noto", sans-serif',
      size: 12,
      style: 'normal',
      lineHeight: 1.2,
      weight: null
    },
    hover: {
      mode: 'nearest',
      intersect: true,
      onHover: null
    },
    interaction: {
      mode: 'nearest',
      intersect: true
    },
    maintainAspectRatio: false,
    onHover: null,
    onClick: null,
    plugins: {
      filler: {
        propagate: true
      },
      legend: {
        display: true,
        position: 'bottom',
        align: 'center',
        fullWidth: true,
        reverse: false,
        weight: 1000,
        onHover: null,
        onLeave: null,
        labels: {
          boxWidth: 8,
          padding: 10,
          color: '#e1e1e1',
          usePointStyle: true
        },
        title: {
          display: false,
          position: 'center',
          text: ''
        },
        lineWidth: 0
      },
      title: {
        align: 'center',
        display: true,
        font: {
          style: 'bold'
        },
        fullWidth: true,
        padding: 10,
        position: 'top',
        text: 'Aufteilung Nährstoffe (kal) pro Tag',
        weight: 2000,
        color: '#ff9500'
      },
      tooltip: {
        mode: 'nearest',
        intersect: true,
        enabled: true,
        custom: null,
        position: 'average',
        backgroundColor: '#ecf0f1',
        titleColor: '#647687',
        titleFont: {
          style: 'bold'
        },
        titleSpacing: 2,
        titleMarginBottom: 6,
        titleAlign: 'left',
        bodyColor: '#647687',
        bodySpacing: 2,
        bodyFont: {},
        bodyAlign: 'left',
        footerColor: '#647687',
        footerSpacing: 2,
        footerMarginTop: 6,
        footerFont: {
          style: 'bold'
        },
        footerAlign: 'left',
        yPadding: 6,
        xPadding: 6,
        caretPadding: 2,
        caretSize: 5,
        cornerRadius: 6,
        multiKeyBackground: '#fff',
        displayColors: true,
        borderColor: 'rgba(0,0,0,0)',
        borderWidth: 0,
        animation: {
          duration: 400,
          easing: 'easeOutQuart',
          numbers: {
            type: 'number',
            properties: [
              'x',
              'y',
              'width',
              'height',
              'caretX',
              'caretY'
            ]
          },
          opacity: {
            easing: 'linear',
            duration: 200
          }
        },
        callbacks: {}
      },
      chardbackground: {},
      gradient: {}
    },
    responsive: true,
    showLine: true,
    layout: {
      padding: {
        top: 0,
        right: 24,
        bottom: 24,
        left: 24
      }
    },
    animation: {
      numbers: {
        type: 'number',
        properties: [
          'circumference',
          'endAngle',
          'innerRadius',
          'outerRadius',
          'startAngle',
          'x',
          'y',
          'offset',
          'borderWidth'
        ]
      },
      animateRotate: true,
      animateScale: false
    },
    locale: 'de-DE',
    datasetElementType: false,
    dataElementType: 'arc',
    dataElementOptions: [
      'backgroundColor',
      'borderColor',
      'borderWidth',
      'borderAlign',
      'offset'
    ],
    aspectRatio: 1,
    cutoutPercentage: 0,
    rotation: 0,
    circumference: 360,
    type: 'pie',
    units: '',
    chartArea: {
      backgroundColor: 'transparent'
    },
    spanGaps: true,
    scales: {}
  }
}
```
## Environment

* Chart.js version: Chart.js v3.0.0-beta.7
* Browser name and version: any


