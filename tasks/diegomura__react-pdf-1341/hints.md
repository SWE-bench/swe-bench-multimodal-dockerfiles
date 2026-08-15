It seems by not using the short form `flex` you can sidestep this problem. So `flexGrow`, `flexShrink` and `flexBasis`.
This still seems to be a bug though … maybe open the issue again.
I've had a quick look at stylesheet/flex.js processFlex, it is expecting the value to always be a string.  This seems to be recently introduced, as the prior version looks like it checked isNumber first, but had no test coverage for the check, so easy to miss in a refactor.

flex: 1 causes .split is not a function error
flex: '1' has no issues.

Interestingly, I'm not sure flex: '1' is also being expanded correctly.

[Some people on stackoverflow seem to think flex: 1 should expand to 1 1 0.](https://stackoverflow.com/questions/37386244/what-does-flex-1-mean)

```
  test('should process flex shorthand 1', () => {
    const styles = processFlex('flex', 1);

    expect(styles).toEqual({
      flexGrow: 1,
      flexShrink: 1,
      flexBasis: 0,
    });
  });

  test('should process flex \'1\'', () => {
    const styles = processFlex('flex', '1');

    expect(styles).toEqual({
      flexGrow: 1,
      flexShrink: 1,
      flexBasis: 0,
    });
  });
```
  
- The first tests highlight the first issue of not handling flex: 1
- The second test highlights the potential issue of flex: '1' not being expanded correctly.
There was a fix done by @diegomura https://github.com/diegomura/react-pdf/pull/1325 but the latest published version does not have this fix. Do we know when can we expect this fix to be published
I have pretty the same problem:

<img width="481" alt="Zrzut ekranu 2021-05-29 o 17 04 06" src="https://user-images.githubusercontent.com/4519335/120075063-0ec4a200-c0a0-11eb-845c-81d9a64c1fe7.png">
<img width="1665" alt="Zrzut ekranu 2021-05-29 o 17 03 47" src="https://user-images.githubusercontent.com/4519335/120075066-108e6580-c0a0-11eb-8610-e138c9c5d4cd.png">
