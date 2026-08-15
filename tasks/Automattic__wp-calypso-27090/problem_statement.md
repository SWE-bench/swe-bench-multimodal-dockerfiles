Posts: Show view counts in Blog Posts list
As noted on #26708 and p8F9tW-RX-p2, there are a lot of customers that would like to see the view counts on the Blog Posts list brought back.

@Automattic/tanooki is looking into bringing back this functionality (or similar functionality) with a less resource-intensive implementation that delivers better performance for both customers' devices and our servers. There are some possible options to explore mentioned on p8F9tW-RX-p2.

If performance constraints necessitate a change from the original experience, this issue will be updated accordingly.

Before:

<img width="736" alt="screencapture at wed aug 15 13 22 45 edt 2018" src="https://user-images.githubusercontent.com/2098816/44163026-1b62e180-a090-11e8-9378-79271c20464e.png">

After:

<img width="738" alt="screencapture at wed aug 15 13 21 39 edt 2018" src="https://user-images.githubusercontent.com/2098816/44163020-169e2d80-a090-11e8-9160-5b98596b09c1.png">

----

### Acceptance criteria

1.
- Given a site with blog posts with views
- When Blog Posts is visited
- Then the "X Views" counts are present on the post items in the list

2.
- Given a site with blog posts with views
- When Blog Posts is visited
- Then an acceptable number of requests are made to receive necessary data (will work with Systems to make sure that any solution is acceptable)

3.
- Given a customer with multiple sites with blog posts with views
- When Blog Posts is visited in All My Sites mode
- Then the "X Views" counts are present on the post items in the list

4.
- Given a customer with multiple sites with blog posts with views
- When Blog Posts is visited in All My Sites mode
- Then an acceptable number of requests are made to receive necessary data (will work with Systems to make sure that any solution is acceptable)

### Tasks

- [x] [Grant] Design for post-views endpoint that will support getting a total number of views over a date range for all specified posts in one request
- [x] [Grant] Build post-views endpoint
- [x] Write tests for endpoint
- [x] [Cain] Update the Posts list to use the posts-views endpoint (one request for each "page" of posts) and display "x Recent Views" (with a more descriptive title text) that links to the full stats page for that post

## PR

https://github.com/Automattic/wp-calypso/pull/27090
