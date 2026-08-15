nice this is a great step, should we expand this for all latencies that weren't realistic?
I can't find the issue now, but we also talked about something like this for when the run was a total disaster...e.g. navStart well after FMP in the trace
@patrickhulce something different than https://github.com/GoogleChrome/lighthouse/blob/1acd240b061092d5bd4643b4927004ee507799f3/lighthouse-core/audits/load-fast-enough-for-pwa.js#L113-L121?

@brendankenny let's think warnings for overall disasters in another PR.
@ebidel yeah I meant including that warning with yours as well. Having one place to call it out more prominently in addition to the current spot might prevent some of the WPT discrepancy frustration cases.
> Do we need something in the JSON report as well (a top-level warning or whatever)?

nahhh.. no need.
Blocked by #1512 