Indeed you have discovered a bug thanks very much for filing @piehei! To explain what's going on here, the audit is erroneously flagging the `304 Not Modified` requests as lacking the content-encoding header even though it's obviously not necessary since there is no content to return.

To fix this we should probably ignore:
* status codes 3xx
* records with transferSize <= gzip size