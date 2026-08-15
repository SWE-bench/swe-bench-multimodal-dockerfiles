It looks like a bug introduced in v7.3.0 https://codesandbox.io/s/simple-forked-rfvw60?file=/main.js  If you change to an earlier version there is no attribution for the OSM in the hidden group.
Of course it is. (v. 7.2.2 - doesn't have this strange behavior)
Earlier versions do not display attributions for hidden group layers.
The same effect with mousemove, click etc. event over features with hidden group-layer. #14581
This problem was introduced with #14476, but it is not related to #14581.