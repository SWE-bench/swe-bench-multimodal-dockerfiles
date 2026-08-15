I haven't been able to reproduce, but whoever is looking into this should start with the `no-this-before-super` rule.
Please note that the error goes away when the `for` loop is altered:
```js
class Extender {}
class BugProof extends Extender {

  constructor(props) {
    super(props);

    try {
      for (let i = 0; i < 1; i++) {

      }
    } catch (err) {

    }
  }
}
```

If we keep the `for..of` loop, the error will also go away by one of the following:

- Removing the `extends`
- Removing the `try..catch`
I can recreate this with the latest version of ESLint with the above code and this minimal config:
```json
{
    "env": {
      "es6": true
    },
    "rules": {
      "no-this-before-super": "error"
    }
}
```
@kaicataldo I find <del>the error</del> similar error seems occur in rule `constructor-super`: https://github.com/eslint/eslint/blob/master/lib/rules/constructor-super.js#L132

```js
        function isCalledInSomePath(segment) {
            return segment.reachable && segInfoMap[segment.id].calledInSomePaths;
        }
```
`segInfoMap[segment.id]` sometimes can be undefined. 
It's possible that this is a bug in the core code path analysis logic.
@mysticatea Any insight on this?
Oh, I'm sorry, I had overlooked this issue.
I will take a look.
It looks a bug in code path analysis. If `ForInStatement#right` is the first location which can throw a reference error in the outer `try` block, it has generated wrong code path. I need more investigation.
I haven't been able to reproduce, but whoever is looking into this should start with the `no-this-before-super` rule.
Please note that the error goes away when the `for` loop is altered:
```js
class Extender {}
class BugProof extends Extender {

  constructor(props) {
    super(props);

    try {
      for (let i = 0; i < 1; i++) {

      }
    } catch (err) {

    }
  }
}
```

If we keep the `for..of` loop, the error will also go away by one of the following:

- Removing the `extends`
- Removing the `try..catch`
I can recreate this with the latest version of ESLint with the above code and this minimal config:
```json
{
    "env": {
      "es6": true
    },
    "rules": {
      "no-this-before-super": "error"
    }
}
```
@kaicataldo I find <del>the error</del> similar error seems occur in rule `constructor-super`: https://github.com/eslint/eslint/blob/master/lib/rules/constructor-super.js#L132

```js
        function isCalledInSomePath(segment) {
            return segment.reachable && segInfoMap[segment.id].calledInSomePaths;
        }
```
`segInfoMap[segment.id]` sometimes can be undefined. 
It's possible that this is a bug in the core code path analysis logic.
@mysticatea Any insight on this?
Oh, I'm sorry, I had overlooked this issue.
I will take a look.
It looks a bug in code path analysis. If `ForInStatement#right` is the first location which can throw a reference error in the outer `try` block, it has generated wrong code path. I need more investigation.