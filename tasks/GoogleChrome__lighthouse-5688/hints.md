We target bitmaps but it looks like this one has a mime type of `image/x-ms-bmp`, we'll expand our regex :)

```
$ curl -sSL -D - https://homepages.cae.wisc.edu/\~ece533/images/sails.bmp -o /dev/null
HTTP/1.1 200 OK
Date: Wed, 18 Jul 2018 23:34:44 GMT
Server: Apache
Last-Modified: Mon, 25 Nov 2002 01:37:36 GMT
ETag: "a28b4-60436-3b03a0a357800"
Accept-Ranges: bytes
Content-Length: 394294
Content-Type: image/x-ms-bmp
```