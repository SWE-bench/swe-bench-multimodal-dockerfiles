Im unable to recreate in either my local testing environment or [CodeSandbox](https://codesandbox.io/s/carbon-v11-x5pmsg)

(CodeSandbox seems to be sporadically working for me right now ymmv)

Could you potentially give me some more context as to how you're using the component, a code example? 
Just including the code snippet from the site causes the error for us.

```
    <DatePicker dateFormat="m/d/Y" datePickerType="simple">
      <DatePickerInput
        id="date-picker-default-id"
        placeholder="mm/dd/yyyy"
        labelText="Date picker label"
        type="text"
      />
    </DatePicker>
```

If I take out datePickerType it works fine. As soon as that is added we get the error.  The GIF above is just a page with the above code snippet in render().
Gotcha, yeah.That code snippet causes no error for me in either my local testing area or on CodeSandbox (when i can get it to load 😓). Could you provide some more information about how your app is using Carbon v11 so we can try and recreate? 

Does it mostly follow this example:
https://codesandbox.io/s/carbon-v11-x5pmsg?file=/src/index.js
Pretty straight forward I think.  We had no issue with this with React 18 and Carbon 10.  Carbon 11 migration introduced this.

Current related packages:

```
    "@carbon/charts": "0.58.0-latest-carbon-v11-beta.0",
    "@carbon/charts-react": "^0.57.0",
    "@carbon/pictograms-react": "^11.26.2",
    "@carbon/react": "^1.2.0",
    "core-js": "^3.22.2",
    "react": "^18.1.0",
    "react-app-polyfill": "^3.0.0",
    "react-dom": "^18.1.0",
    "react-router-dom": "^5.3.1",
    "react-scripts": "^5.0.1",
    "typescript": "^4.6.3"
```

Overall every component except DatePicker and Tabs works fine.  But those two are throwing different errors on load.
@dabrad26 Sorry again about the codesandbox issues. If it helps for reproductions, the vite example we have in the repo [works well on stackblitz](https://stackblitz.com/github/carbon-design-system/carbon/tree/main/examples/vite?file=src%2FApp.jsx).

I made [a specific one](https://stackblitz.com/edit/github-4nannp?file=src%2FApp.jsx) configured to use the snippet from the website and react v18.
@dabrad26 looking at your GIF - `start` is a `ref.current`, and the `addEventListener` call is behind a conditional

https://github.com/carbon-design-system/carbon/blob/c62220c5c03d4056b50ed5558abb6a929ebc2419/packages/react/src/components/DatePicker/next/DatePicker.js#L386-L387

Could you share the value of `start` from your environment and/or what might cause the check to be truthy, then fail the `addEventListener` call?
Thanks for the Vite thing.  With that I debugged more.  The issue seems to be the component does not like being wrapped and returned...


For example for our TypeScript usage (to load our own types so we can migrate to Carbon 11 without official types from) we use:

```
export class DatePickerInput extends React.Component<DatePickerInputProps> {
  render(): React.ReactNode {
    return <CarbonComponents.DatePickerInput {...this.props} />;
  }
}
```


This is done for every Carbon component we use.

If I just use `export const DatePicker = CarbonComponents.DatePicker;` it works fine... So not sure why it is unhappy in the render wrapping.  

We use this approach as Carbon 11 does not have type definitions. So to keep some control over types we define the types ourselves and wrap on this component; to avoid the apps using any as the type for Carbon components. This ensures we don't end up with invalid props and skipping type check on build.  

Since it seems to be an issue with our usage I will close the issue. But not sure why this is happening as passing components through a wrapped component should work.