Does adding `alignSelf` to `nameProps` achieve what you are looking for?

```
<NameValueList
    nameProps={{ alignSelf: 'center' }}
    valueProps={{ width: "auto", align: "start" }}
  >
  ...
  ```
Thanks for your help. If I try this I get the following error:

```
Type '{ alignSelf: string; }' is not assignable to type '{ align?: string | undefined; width?: WidthType | undefined; }'.
  Object literal may only specify known properties, and 'alignSelf' does not exist in type '{ align?: string | undefined; width?: WidthType | undefined; }'.ts(2322)
index.d.ts(8, 3): The expected type comes from property 'nameProps' which is declared here on type 'IntrinsicAttributes & NameValueListExtendedProps'
```

It seems alignSelf does not exist in NameValueList?
I played around with NameValueList and didn't find a way to get the desired behavior. Marking this as an enhancement
> I played around with NameValueList and didn't find a way to get the desired behavior. Marking this as an enhancement

According to https://v2.grommet.io/namevaluelist?#align and "The NameValueList component can be customized with any of the properties available in [Grid](https://v2.grommet.io/grid)." `<NameValueList `align="center"` ... />` should be supported.

Is "bug" more appropriate?
prop is accepted here: https://github.com/grommet/grommet/blob/7a50c754cb98635fa14d5806ac0b03d6d094e29c/src/js/components/NameValueList/NameValueList.js#L10 but never applied.

Putting up a fix now.
> According to https://v2.grommet.io/namevaluelist?#align and "The NameValueList component can be customized with any of the properties available in [Grid](https://v2.grommet.io/grid)." <NameValueList align="center" ... /> should be supported.
> 
> Is "bug" more appropriate?

Good note and thanks for looking into this more. I'll switch the label on this from 'enhancement' to 'bug'