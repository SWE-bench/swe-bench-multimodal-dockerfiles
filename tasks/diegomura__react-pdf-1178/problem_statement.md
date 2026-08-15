margin auto is broken in v2
**Describe the bug**
Run a some snapshot tests with react-pdf examples for v1/v2 and seems like margin auto doesn't work

https://github.com/diegomura/react-pdf/blob/master/packages/examples/src/knobs/index.js#L20

![index-test-js-renders-correctly-1-diff](https://user-images.githubusercontent.com/6726016/113850039-b8736b00-97a2-11eb-857d-50470f1d52c2.png)
> v1 on the left side v2 on the right

**To Reproduce**
Steps to reproduce the behavior including code snippet (if applies):
1. run https://github.com/diegomura/react-pdf/blob/master/packages/examples/src/knobs/
2. See error


**Desktop (please complete the following information):**
 - MacOS
 - Node v14.7.0
 - React-pdf version v2.0.0



