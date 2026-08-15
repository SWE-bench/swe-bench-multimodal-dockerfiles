Interesting, thanks for reporting! A few shorter examples:

## Line gaps in the last list are removed

**Prettier 3.3.0**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEBadAdKAzCECMSWABMasQEYCGATvvliWZbfgEyNSnnV0DMnXBDZEuzXmwZQmPWmw7SxsmmwGKhfUdxY0+UmTr4KDvPmvSpOAWVoBrACYQA7lBAAaEBAAOMAJbQAZ2RQWhpnAAVaBCCUKgAbJyoATyCPChoqMFs4GABlKgBbOAAZXyg4ZGx4gLg0jKyc3K9MsoBzZBgaAFdakBqC3w7u3rgADy84Gl8i2HiAFUmoWl84GKq4mo8Atri4AEUuiHhK6t6AKwDR3J39w+Okdc2QAEc7uHCwrxiQKgDUcrg9kB7hAnSovjibQAwhACgUqMgfnE4iDtlBWrsAIIwTq+ChdeDhSalconDa9AAWMAKcQA6hTfPAAs0wHBctFGb4AG6MpKIsABVIgLk9ACSUCBsFyYCmPkxEtyMCSuzJTy8YRqtIyXkR6tWky5FQ8ZRqNBgHyorXhqt6zRopsR8JoDmcrg86rKMFpvnsMApyAAHAAGDw0OCvXxhi1WhEPU4eGBUCje33+pBsDxdGpzJNreMgOAFCiAoH2YpUdFdS1wABiEBo8JxbURVAJEBAAF8O0A)
<!-- prettier-ignore -->
```sh
--parser markdown
```

**Input:**
<!-- prettier-ignore -->
```markdown
---
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo3:
  - bar31

  - bar32

  - bar33
---

Markdown
```

**Output:**
<!-- prettier-ignore -->
```markdown
---
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo3:
  - bar31
  - bar32
  - bar33
---

Markdown

```

### Line gaps in last list are _not_ removed if followed by a comment

**Prettier 3.3.0**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEBadAdKAzCECMSWABMasQEYCGATvvliWZbfgEyNSnnV0DMnXBDZEuzXmwZQmPWmw7SxsmmwGKhfUdxY0+UmTr4KDvPmqwBiYgGcIAWzjFIdh7E7pUnALK0A1gBMIAHcoEAAaEAgABxgAS2hrZFBaGmCABVoERJQqABsgqgBPRIiKGiowXzgYAGUqBwAZWKg4ZGw86zhS8srqmqiK5oBzZBgaAFcukE67WNGJqbgADyi4GljXGDyAFTWoWli4bPbczojrYdy4AEVxiHg2jqmAK2slmsubu4ekE7OQACO3zgaVSUWyICo1lQLTg-jh4RAYyosVywwAwvY7FRkJDcrlERcoEMrgBBGBjWIUcbwNJrJotR6nKYACxgdlyAHUWbF4NYBmA4DUsrzYgA3XmFXFgawlEBiyYASSg8NgNTA6xipJVNRghSuTP+UVSnU55SiuONRzWYtaEWanRoMFBVCG2MNUwGNEduOxNACwVCEWNzRgnNi-hgLOQAA4AAwRGhwIGxJMut0435PCJbCjhyPRpBsCLjTrbKgUY7ZkBwOwUOHw-wNKjE8auuAAMQgNGxFOGuKoNIgIAAviOgA)
<!-- prettier-ignore -->
```sh
--parser markdown
```

**Input:**
<!-- prettier-ignore -->
```markdown
---
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo3:
  - bar31

  - bar32

  - bar33

# some comment

---

Markdown
```

**Output:**
<!-- prettier-ignore -->
```markdown
---
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo3:
  - bar31

  - bar32

  - bar33
# some comment
---

Markdown

```

### Line gaps in last list are _not_ removed if followed by another key

**Prettier 3.3.0**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEBadAdKAzCECMSWABMasQEYCGATvvliWZbfgEyNSnnV0DMnXBDZEuzXmwZQmPWmw7SxsmmwGKhfUdxY0+UmTr4KDvPmqxCALEmKXjUdKk4BZWgGsAJhADuUEABoQCAAHGABLaABnZFBaGh8ABVoEaJQqABtvKgBPaMCKGiowNzgYAGUqAFs4ABkwqDhkbAzIuHzC4tKy4KL6gHNkGBoAVzaQVsqwwZGxuAAPYLgaMOrYDIAVJahaMLhU5vTWwMj+9LgARWGIeCaWsYArSLmy04urm6QDo5AAR3e4BLxYKpEBUSKoBpwDxQgIgIZUMLpfoAYQglUqVGQoPS6VhJygfTOAEEYEMwhRhvAEks6g1bocxgALGCVdIAdUZYXgkR6YDgZRSXLCADcudksWBInkQMLRgBJKDQ2BlMDLUJExVlGDZM7077BeKtNmFYJYg17JbCxqBeqtGgwQFUPoYvVjHo0O1YjE0Tw+PyBA31GBssIeGCM5AADgADIEaHA-mF447nZjPndAjAqBQQ2GI0g2IFhq11tn9hmQHBKhQodCPDUqAThk64AAxCA0DGk-pYqiUiAgAC+g6AA)
<!-- prettier-ignore -->
```sh
--parser markdown
```

**Input:**
<!-- prettier-ignore -->
```markdown
---
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo3:
  - bar31

  - bar32

  - bar33

foo4: 42

---

Markdown
```

**Output:**
<!-- prettier-ignore -->
```markdown
---
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo3:
  - bar31

  - bar32

  - bar33

foo4: 42
---

Markdown

```

### Line gaps in last list are _not_ removed if it has duplicate key

**Prettier 3.3.0**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEBadAdKAzCECMSWABMasQEYCGATvvliWZbfgEyNSnnV0DMnXBDZEuzXmwZQmPWmw7SxsmmwGKhI4gGItxACYBXAA4AbAJZgq8YgGs4ATxksafKU958F72nzXpUnACytDZ6EADuUCAANCAQRjBm0ADOyKC0NBEACrQIqShUJuFU9qmxFDRUYHYwAMpUALZwADJmUHDI2IXJcOWV1XB1RlVtAObIMDQGvSA9DWYTUzNwAB5GcDRmTbCFACobULRmcPldJj2xyWMmcACKBhDwnd0zAFbJK7XXdw9PSGcXEAAR1+cCymSM+RAVGSqHacD0CJiIEmVDM5igowAwhAGg0qMhoSYTMirpibgBBGCTMwUAzwLIbVrtZ7nGYACxgDRMAHV2WZ4MlhmA4LU8gKzAA3AX2QlgZJlECS6YASSgiNgtTAmwSFPVtRg9hurMBRkyPR5lSMhLNJw2ko6sTaPRoMHBVFG+JNM2GNBdhPxNFCESisTNbRgPLMehg7OQAA4AAyxGhwEFmVPuz0E-4vWIwKgUKMxuNINixAw9XaF055kBwBoUBGIvTNKiYgweuAAMQgNHx1LGhKo9IgIAAvuOgA)
<!-- prettier-ignore -->
```sh
--parser markdown
```

**Input:**
<!-- prettier-ignore -->
```markdown
---
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo2: ## duplicate key
  - bar31

  - bar32

  - bar33
---

Markdown
```

**Output:**
<!-- prettier-ignore -->
```markdown
---
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo2: ## duplicate key
  - bar31

  - bar32

  - bar33
---

Markdown

```

### Line breaks are _not_ removed in plain yaml

**Prettier 3.3.0**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEAzCECMSA6UAE+AtPgEYCGATppnnoSRdQEx0HFlWYDMb6EzXO0ZVmtKPQ5NmrCcM6VmvOf25CGC7uMkjK3WTs3KQAGhAQADjACW0AM7JQVShADuABSoIHKcgBtXcgBPBzNSSnIwAGs4GABlcgBbOAAZayg4ZFR-OzgwiOjYuItI9IBzZBhKAFc8kFzE60qaurgADws4Smtk2H8AFS6oKms4H2y-XLM7cr84AEVqiHgsnLqAKzs2uNmFpZWkCamQAEd9uHcXCx8QcjsiDLgAE2fTECryaz9ygGEIRMS5GQtz8fjeMygZTmAEEYFVrKRqvB3F00hlVpM6gALGCJPwAdSx1ngdhKYDgcW8xOsADdiUFgWA7KEQDTagBJKAvWBxMDdKzQrlxGBBOYY44WFy5fERCzAyVjLo0zJmdK5SgwS7kMqA8V1EqUdXAoJJMFmSXpGD46xPGBY5AADgADGZKHAztY3VqdUDDmszDByKRrbb7UhmGZqrl+kHxv6QHBEqRni8nilyJDqtq4AAxCCUQFw8rA8hIiAgAC+FaAA)
<!-- prettier-ignore -->
```sh
--parser yaml
```

**Input:**
<!-- prettier-ignore -->
```yaml
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo3:
  - bar31

  - bar32

  - bar33

```

**Output:**
<!-- prettier-ignore -->
```yaml
foo1:
  - bar11

  - bar12

  - bar13

foo2:
  - bar21

  - bar22

  - bar23

foo3:
  - bar31

  - bar32

  - bar33

```

I flicked between markdown and mdx parser, did not find any difference. Looks like a bug in frontmatter to me.
A Note: this only happens in 3.3.0, while the previous versions are good. I think this can help you locating the issue
It seems there is bug in [`stripTrailingHardline`](https://github.com/prettier/prettier/blob/b26f56bd316a3ed11c33f50cd4a3dac44a4ee529/src/document/utils.js#L256)