I cannot reproduce this issue locall as well as [on our demo](https://demo.bpmn.io):

![capture 81fp5l_optimized](https://user-images.githubusercontent.com/58601/76798057-1f586780-67cf-11ea-9123-07c47630592d.gif)

Please spend some time to [understand the changes since the upgrade](https://github.com/bpmn-io/bpmn-js/compare/v6.3.0...v6.3.3) and provide some additional context how you use the toolkit.

I am able to reproduce the issue on demo.bpmn.io.

It is not about selecting but about completing direct editing with an empty label. That resizes the element accidentally to the empty labels bounds (width `0px`):

![capture ZnZ8sj_optimized](https://user-images.githubusercontent.com/58601/77805963-a0dbaf80-7083-11ea-98f3-ba5183a2af78.gif)

#### Steps to reproduce

1. Start direct editing on element with external label.
2. Complete direct editing with empty text

This broke via https://github.com/bpmn-io/bpmn-js/commit/e4e789bd3eecc47597d97d6c8f1e71b941dee066#diff-642682e3de745f747ccb55e702973a89L107.
Updated the issue description accordingly.