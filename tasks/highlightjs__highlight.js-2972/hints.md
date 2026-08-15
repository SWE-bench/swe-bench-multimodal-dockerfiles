Can you be more specific, are you referring to the types in the source code, or the types in the comments - or both?  I think both I'm just wanting to clarify.

https://github.com/highlightjs/highlight.js/commit/07e30ad6f725e2a24193c378ede5e1ff7f0b5b88 would be very easy to extend.

I'd say all of this looks quite possible.  @Lemmingh Interested in working on a PR?

Off the top of my head:

- Add a new comment rule to match `# type:` comments, then search for types as keywords
- Expand the return type ` -> ` rule to use the same list of types
- Add these same types to the keywords for the argument list (to avoid mis identifying variable names you might need a more complex rule here to match `:` and end on perhaps `,` or `)` so that only types after a : are matched.
> are you referring to the types in the source code, or the types in the comments - or both?

**Both**.
Annotations (the types in the source code) at least.

As you can see, Magic Python and GitHub highlight *function annotations* (PEP 3107) and *variable annotations* (PEP 526), besides, Magic Python highlights *type comments*.

> Interested in working on a PR?

Sorry. I'm afraid I'm a little bit busy this month.

---

Here are a few more complex cases:

```python
mapping = None  # type: Dict[int, Any]

co = None  # type: Coroutine[List[str], str, int]  # Introduced in version K.

u, v, w = [], [], []  # type: List[int], List[int], List[str]
x, y, z = [], [], []  # type: (List[int], List[int], List[str])
a, b, *c = range(5)   # type: float, float, List[float]

stats: ClassVar[Dict[str, int]] = {}  # PEP 526

def average(root: TreeNode,
            depth: int = 2
            ) -> List[float]:
```
Thanks for more samples!
I wonder if some of our "built_ins" should move to "type" such as str, int, etc?
<img width="689" alt="Screen Shot 2021-01-13 at 1 56 43 PM" src="https://user-images.githubusercontent.com/6473/104496595-2eeb3d00-55a7-11eb-9762-c4be29c4dc48.png">
