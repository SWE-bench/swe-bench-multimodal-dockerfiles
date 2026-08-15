After pairing with @creativecoder to dig into possible approaches, we've come up with a plan forward.

- Update post views endpoint to query correct historical data* and accept a date range argument
- Update the Posts list to use the endpoint and display "x Recent Views" (with a more descriptive title text) that links to the full stats page for that post
- Possibly add a batch endpoint for the updated post views requests

^ I'll update the tasks with the above.

*There seems to be a bug with the way historical post views are queried from the post views endpoint. They're correctly queried in the top posts endpoint, which explains a large part of the performance difference between the two in terms of response time. We're hoping that updating the post views endpoint to use the same method will significantly cut down on the 1 month views request time. If that doesn't work, we don't really have a way forward b/c our options all have significant compromises (i.e. showing view data that doesn't include the current day, or only being able to query an insignificant period of views data for each post).
@michaeldcain and I have dug into the code and further developed this plan for supporting post list views with the API:

(As stated above), instead of displaying all views for a post, we'll display "Recent views". This will use the post views endpoint (`/sites/%s/stats/post/%d`), as before, but with the following changes:

1. Modify the endpoint to get a summary of the data. All we need here is the views for the post, not any other details.
    - In combination with D17677-code, this will half the number of database queries used to generate this information, compared to before.

1. Generate the number of views for each post in the last 30 days.
    - This will prevent the issue from before where older posts generated hundred's of queries to count total views (1 for each day since the post was published).

1. (TBD, still researching this) Modify the API call so that we can batch view summary results for multiple posts, rather than needing a separate request for each post.
    - This won't reduce the number of database queries, but will cut down on network requests.

@jmdodd Please let us know your questions, concerns, or suggestions. Thanks!
If you are interested in cutting down on network requests, there is a batch endpoint that we use for likes: https://developer.wordpress.com/docs/api/1.1/get/batch/

I'd like to make a case for fetching views for multiple posts from a single database query; batching on a `stats` endpoint with a new `post_ids` parameter would cut down on both network and database queries.
Note: updated task list in description to reflect our plan to use a new "posts views" endpoint.
Here's an initial design for a "post views" endpoint to support this feature.

Url: `https://public-api.wordpress.com/rest/v1.1/sites/$site/stats/post-views`

Query params
- The usual: `context`, `http_envelope`, `pretty`, `meta`, `fields`, `callback`
- `post_ids=1,2,3` specify which posts to query by id
- `date=YYYY-MM-DD` most recent day to include in results, default: today
- `num=30` number of periods to get, default: 1
- `period=day|week|month|year` which period to use for date range, default: day
- `offset=-4` number of hours from GMT, default: site's offset

Response params
- `"date": "YYYY-MM-DD"` end date
- `"posts": [ { "ID": 1, "views": 20 } ]` array of posts with id and views

@jmdodd I copied the `num` and `period` parameters from some of the other stats endpoints, like `video-plays` and `country-views`. Maybe `period` isn't appropriate if we are limiting the number of queries for each post. What is a reasonable maximum number of days? What about for post ids?
Let's start with a simple period = day, num = 30, maximum number = 30 for testing; this can be expanded later as long as we continue to use `post_ids` to batch things reasonably.