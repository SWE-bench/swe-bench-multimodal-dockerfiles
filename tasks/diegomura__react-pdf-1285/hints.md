I'd be willing to solve this issue myself in a near future.
That would be great @DavidMich1 ! Let me know if you can
After inspection it would seem that the issue is not with the package itself but with some of his dependencies.

I found occurrences of `new Buffer(` in

- @react-pdf/fontkit
- @react-pdf/pdfkit
- @react-pdf/png-js
@DavidMich1 could you make any progress on this issue?
@joernroeder See https://github.com/react-pdf/fontkit/pull/6#issuecomment-494450210