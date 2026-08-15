Root cause: 

When replacing the root element, we reset the viewport, even when it's not a plane change: https://github.com/bpmn-io/bpmn-js/blob/4e08a1c703e71866ef1b11d2196daa2374a618ec/lib/features/drilldown/DrilldownCentering.js#L14