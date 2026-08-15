[As I found out](https://github.com/carbon-design-system/carbon/issues/10002#issuecomment-1019327397), validation messages can also be top-aligned (Safari). So if this is implemented, that should be taken into consideration.
> The invisible underlying input is not positioned correctly to display validation errors at a suitable location.

I think this part has been fixed, the other issue though remains to my knowledge
Hey @brunnerh 

> The invisible underlying input is not positioned correctly to display validation errors at a suitable location.

Above issue has been fixed by [PR](https://github.com/carbon-design-system/carbon/pull/15435)

I can't reproduce the other issue, and I didn't encounter any errors popup in the CodeSandbox link provided with the bug report. 
![grp-tile](https://github.com/carbon-design-system/carbon/assets/63502271/a8d00794-180f-4948-b13f-ebabd6b5b912)

Also, based on the screenshots provided in the bug(Attached above this as well), it seems that the observed behavior is related to `RadioButtonGroup` and `RadioButton`, rather than `TileGroup` and `RadioTile`.
i.e 
[CodeSandbox-Link](https://codesandbox.io/p/sandbox/radio-button-required-misalignment-pj40n?file=%2Fsrc%2Findex.js%3A11%2C1-15%2C1)
```
<FormGroup>
        <RadioButtonGroup name="group" legendText="Storage tier (disk)">
          <RadioButton required labelText="Free (1 GB)" value="free" />
          <RadioButton required labelText="Standard (10 GB)" value="standard" />
          <RadioButton required labelText="Pro (128 GB)" value="pro" />
        </RadioButtonGroup>
</FormGroup>
```

Could you confirm this or further help with a CodeSandbox that reproduces this issue with `TileGroup` and `RadioTile`. Thanks :)




This is about `TileGroup`, and the problem still exists (at least in v10).
The sandbox broke due to not linking to a fixed version of the packages.

I updated [the link](https://codesandbox.io/p/sandbox/required-tile-group-q33x2q).
In v11, native validation is _completely broken_ in the React package, because `required` is not set/forwarded.

https://github.com/carbon-design-system/carbon/blob/0376df7e71958354474882e1c1b11aa13cda88c3/packages/react/src/components/RadioTile/RadioTile.tsx#L144-L156

[StackBlitz](https://stackblitz.com/edit/github-hmmjg4)
Hey @brunnerh Thanks for quick response, we are looking into this. 