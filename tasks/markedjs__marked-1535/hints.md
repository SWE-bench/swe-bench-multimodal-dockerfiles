task list items is a [GFM extension](https://github.github.com/gfm/#task-list-items-extension-) which is why they don't render as checkboxes in the [CommonMark Demo](https://spec.commonmark.org/dingus/?text=-%20Tasks%0A-%20%5Bx%5D%20Task1%0A-%20%5B%20%5D%20Task2%0A%0A-%20%5B%20%5D%20Another%20Task%0A)

in GFM they render as:

---
- Tasks
- [x] Task1
- [ ] Task2

- [ ] Another Task
---

When a blank line is in the middle of a list it is considered a [loose list](https://github.github.com/gfm/#example-294) so each list item is wrapped in a `<p>` tag.

It looks like marked doesn't include the checkbox in the `<p>` tag.