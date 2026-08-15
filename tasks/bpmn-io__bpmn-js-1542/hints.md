I was able to root-cause this issue. The Conditions for this to happen are:
- Drop element on a flow so it reconnects
- The Flow has a label
- The drop position is such that the shape outline is before the connection start
![image](https://user-images.githubusercontent.com/21984219/144454561-a47d5829-78b7-498b-ab27-9cdcbe77b81f.png)

We effectively don't have an intersection with the connection, because all points of the connection are inside the shape bounding box. This is missed in our error protection:
https://github.com/bpmn-io/bpmn-js/blob/82a250b014bf5c524c6b84507a221053bbac7f99/lib/features/modeling/behavior/DropOnFlowBehavior.js#L54-L69

We then have a connection with only 1 Waypoint that breaks later when we try to calculate intersections on the line, which fails.

The behavior seems broken even when no label is present:
![recording (58)](https://user-images.githubusercontent.com/21984219/144457366-556fa7be-176f-406c-a157-292395d141bf.gif)

I see 2 options to solve this issue:

:one: Don't handle this edge case as an "drop on flow" and don't connect it to the flow.

:two: Always add a second waypoint to the new connection, e.g. the nearest shape border.

I gravitate strongly to :one:. This would change the requirement for "drop on flow" to "the complete shape is on the flow". Currently only the mid-point is considered, which I don't find intuitive.
Is :one: hard to accomplish? I'd love to see it in action to get a feeling for it.
Should be easy enough, I'll create a branch tomorrow