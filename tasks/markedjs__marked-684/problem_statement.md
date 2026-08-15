Weird list rendering behavior
```
- test
- test
- test
1. test
2. test
3. test
```

Renders as this:

![screenshot 40](https://cloud.githubusercontent.com/assets/87356/5483878/54978340-8639-11e4-961b-7f5f293980c6.jpg)

```
- test
- test
- test

1. test
2. test
3. test
```

Renders as

![screenshot 41](https://cloud.githubusercontent.com/assets/87356/5483883/66d6c32c-8639-11e4-87cf-a18d96fd59e8.jpg)

And this:

```
- test
- test
- test


1. test
2. test
3. test
```

Renders correctly:

![screenshot 42](https://cloud.githubusercontent.com/assets/87356/5483887/7d846408-8639-11e4-9201-a86ded31a5d1.jpg)

Why the weird behavior? Is this normal? Why is 2 spaces required after a list before starting another list? I haven't seen that any in sort of spec for how markdown works. Am I missing something here?

