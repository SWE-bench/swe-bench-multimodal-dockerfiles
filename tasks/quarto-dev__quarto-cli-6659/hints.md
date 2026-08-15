Thanks for the report. This is quite a edge case to have`character(0)` in `fig-cap` but indeed, this creates some issue as we have a `sprintf` call to create the Markdown image syntax

`fig-cap` is really expected to be a string and passed directly without `expr`. 

Can i ask what use case drives the need to define `caption` from within the chunk itself ? Just curious. 

I'll fix the reported issue.  