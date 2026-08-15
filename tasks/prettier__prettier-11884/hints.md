Minimal reproduce:

**Prettier 2.5.0**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEMCeAHOACAYhCbAXmwG0BdAbhABoQIMYBLaAZ2VAEMAnbiAdwAKPBOxScANv05p2dAEbdOYANZwYAZU4BbOABkmUOMgBmk1nAVLV6jRmWGA5shjcArpZBxt8uABM-fz1OKEc3Tkc4fG5tThhmUOQQTjcYCFoQAAsYbQkAdUymeFZ7MDgNUSKmADcitCSwVjkQQwtuGEElR1jTc08AK1YADw0nCTgARTcIeF6JCzp7bjak9CxWMG4mRgyMPgs8pQwkvbg26uM6AEdp+E6GMWTWAFojf38M7jgbpi-OiJ6SDM808Fm0TBc7lBY0mt2MQL6dBgnHkeSYfhgmWQACYkUomBInABhCDaQHJCQSDJuCwAFRRYmBCxA1Q8AEkoIFYBpNtsYABBTkadDjObMvaGGBojFYpAARgAzABfJVAA)
<!-- prettier-ignore -->
```sh
--parser typescript
--print-width 13
--trailing-comma all
```

**Input:**
<!-- prettier-ignore -->
```tsx
type Foo = [];
```

**Output:**
<!-- prettier-ignore -->
```tsx
type Foo = [
  ,
];

```