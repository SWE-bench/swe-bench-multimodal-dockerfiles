Thanks for the report. I agree that it would be better to only report the condition here.
It sounds like `line`, `column`, `endLine`, and `endColumn` show the location of the node in which the error is found. In the first example, the `nodeType` is `IfStatement`, and the location listed is the entire if-statement where the first `true` is found. In the second example, the `nodeType` is `ConditionalExpression`, and the location listed is the entire conditional expression where the second `true` is found.
That's correct. I think this issue is occurring because the rule reports the entire `IfStatement` node when it should really just report the condition in the `if` statement. (The `line`, `column`, `endLine`, and `endColumn` are automatically added to the report based on the node that was reported.)
would the ideal case be: just reporting the position of the constant condition (so the `true`)?

so for the IfStatement, can we report with the `loc: {start: {line:nodestartPosition, column:node.test.range[0]}, end: {line:nodestartPosition, column:node.test.range[1]}}`?

haven't checked if there is a case that catches the correct position across the board, but I imagine they might be similar.
We can just report `node.test` as the node, and then all of that information will be automatically added to the report.