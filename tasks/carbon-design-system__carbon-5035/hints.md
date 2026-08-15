I've been messing around with this but since that container tab is a flex item, it doesn't want to truncate. A quick fix would be to just set it back to `inline-block`, but that would cause the tab label to be aligned to the top. 

<img width="937" alt="Screen Shot 2020-01-13 at 1 36 53 PM" src="https://user-images.githubusercontent.com/11928039/72294252-033b1d00-360a-11ea-9427-fbe0770cf43b.png">

😐 hmm yeah I don't think we want it to top align the text.
Seems that the ellipsis thing slipped from the checklist when the container tab was implemented (sorry). I haven't got time to look into this, but if flex item doesn't work, some other tricks in this space I can think of are `display: table-cell` or changing line height (to the height of the tab).