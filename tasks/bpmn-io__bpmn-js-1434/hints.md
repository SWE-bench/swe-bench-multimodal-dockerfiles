We have the same issue with non-interrupting events, so we should extend the scope of this ticket (alternatively create another ticket). I will investigate
![CopyPasteBug2](https://user-images.githubusercontent.com/42800119/89545397-95ec1500-d803-11ea-9d36-3da23c68150e.gif)

I see two options:

**Alternative I:** We can disallow to drop by adding a new rule to [BpmnRules @canDrop](https://github.com/bpmn-io/bpmn-js/blob/develop/lib/features/rules/BpmnRules.js#L443). But this will then also disallow the replace ("morph") behaviour, which we implemented in [BpmnRules @canReplace](https://github.com/bpmn-io/bpmn-js/blob/develop/lib/features/rules/BpmnRules.js#L660) according to issue [#831](https://github.com/bpmn-io/bpmn-js/issues/831). See gif [here](https://github.com/bpmn-io/bpmn-js/issues/1340#issuecomment-669970364).

**Alternative II:** We can also implement the replace ("morphing") behaviour when copy pasting, but this is something that we don't do at the moment (and what is not described in the _expected behaviour_ above).
Not in scope for 4.2.0 release since this is more complex than initially thought. (see [comment](https://github.com/bpmn-io/bpmn-js/issues/1340#issuecomment-670146825)). We might to implement a new rule bin BpmnRules.
In terms of where we want to go, I suggest that we consider replacing during paste + an updated paste preview to match our existing behavior (https://github.com/bpmn-io/bpmn-js/issues/1340#issuecomment-669970364).

It is otherwise hard to understand for users why pasting won't work if a bigger pattern is pasted.

On a side note, I think this is not too big of a deal, given that the resulting diagram could be linted to indicate + fix the error.
@MaxTru I would like to take up this issue
@imrishabh18 please feel free to go ahead and propose a PR for that. But please note that this does require some changes and according tests (ie. not just a few lines of code).
I want to implement it as

> Alternative II: We can also implement the replace ("morphing") behaviour when copy pasting, but this is something that we don't do at the moment (and what is not described in the expected behaviour above).

So the event will be replaced just like it happens when you move a typed start event.
It makes a lot of sense to go that route and fits very well with our existing interactions :+1:.