Ooooo, yikes, yes let's fix that in `simulateDownloadUntil`! Check if it's a non-network protocol and have some constant/option for dealing with the RTT/server response time

https://github.com/GoogleChrome/lighthouse/blob/d50ef9e3c9caee2e73221c7a03d6aabdeb32ef9b/lighthouse-core/lib/dependency-graph/simulator/tcp-connection.js#L112-L123
Given #9834 too we should probably do an audit of our network request usage for data URI mistakes and/or add more data URIs to our smokes :)