@shahabblouch do you only want to rotate where the labels are? or do you want to rotate all the points too?
I actually want to rotate whole chart along with the points. 
I think you could try rotating the canvas in CSS, but there's no built in way to achieve this.
There is a undocumented `startAngle` option: https://codepen.io/kurkle/pen/PobybzR
That is documented in the polarArea chart, so we could just copy the same doc to the radar chart https://www.chartjs.org/docs/master/charts/polar#config-options