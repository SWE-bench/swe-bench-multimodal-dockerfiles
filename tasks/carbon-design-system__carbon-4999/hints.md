Hi 👋 would you want to create a reduced case based on https://codesandbox.io/s/github/carbon-design-system/carbon/tree/master/packages/react/examples/codesandbox? Thanks!
Sure. https://codesandbox.io/s/wizardly-pond-q3uh0?fontsize=14&hidenavigation=1&theme=dark
Seems that the problem does not reproduce in the Sandbox. Downloading the content to the local machine yielded the same result. Also I couldn't open the dropdown in the Sandbox. Probably more work is needed in the Sandbox...?
![image](https://user-images.githubusercontent.com/1077859/72037384-f3090200-32d8-11ea-962c-1ae1025ad47b.png)
@asudoh Did you see the same screen above?

Here is the sample code.
```
import React from 'react';
import { render } from 'react-dom';
import { ComboBox } from 'carbon-components-react';

const App = () => (
  <div>
    <ComboBox
    ariaLabel="Choose an item"
    disabled={false}
    helperText="Optional helper text here"
    id="carbon-combobox-example"
    invalidText="A valid value is required"
    itemToString={(item) => {return item ? item.text : '' }}
    items={[
      {
        id: 'option-0',
        text: 'Option'
      },
      {
        id: 'option-1',
        text: 'Option'
      },
    ]}
    light={false}
    onChange={function noRefCheck(){}}
    placeholder="Filter..."
    size={undefined}
    titleText="Combobox title"
    type="default"
  />
  </div>
);

render(<App />, document.getElementById('root'));

```