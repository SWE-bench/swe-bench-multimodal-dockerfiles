Plugin event filters receive normalized event type and fail when normalization occurs
### Discussed in https://github.com/chartjs/Chart.js/discussions/9580

<div type='discussions-op-text'>

<sup>Originally posted by **beibean** August 25, 2021</sup>
Hi there,

I am using a touchscreen on a embedded device and after migrating from v2.9.4 to v3.5.1 I am not able to show tooltip as used to show it before.

I only need to show tooltip when user touches any part of the graph. We detect touches with ***pointerdown*** and ***pointerup events***. After the library upgrade only the point is hover but the tooltip won't show:

![image](https://user-images.githubusercontent.com/21239979/130746913-786e3664-9bd2-4562-904c-03d09089020f.png)


[Here is a project to reproduce it](https://stackblitz.com/edit/angular-component-df9lph?file=src%2Fapp%2Fapp.component.ts).

Any new configuration I overlooked or any suggestion to fix this?

</div>

## Description

This originates from https://github.com/chartjs/Chart.js/pull/8876

The event type is changed here:
https://github.com/chartjs/Chart.js/blob/fca030922360a1a2d1292f6936276ad11a7cf7d9/src/platform/platform.dom.js#L106

Original types are used to filter and it does not match.

This can be worked around by adding the normalized events: `events: ['mousedown', 'mouseup']` to `options.plugins.tooltip`

