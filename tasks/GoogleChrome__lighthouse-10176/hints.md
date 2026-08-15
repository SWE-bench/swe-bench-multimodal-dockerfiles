
> @anniesullie I imagine you're planning to collect this data from the httparchive:lighthouse tables?
> Pending that answer, I'm wondering if we can continue to expose the signals in the JSON, but hide it from the user. TBH I don't think we have a great mechanism for that, but it's something we can noodle on.

Yep, only planning to collect from httparchive:lighthouse tables. Hiding from the user is totally okay with me!
@anniesullie groovy. thanks
@paulirish Updated the detector so each lib has an `id` property: https://github.com/johnmichel/Library-Detector-for-Chrome/pull/149

PR #9888 fixes the loose coupling and updates the version of the library-detector
> Pending that answer, I'm wondering if we can continue to expose the signals in the JSON, but hide it from the user. 

We could add a `secondary` flag in the library-detector and then filter directly in the js-libraries audit. Could something like that work?
> We could add a `secondary` flag in the library-detector and then filter directly in the js-libraries audit. Could something like that work?

Well.. we need the items in the js-libraries audit details for annie's collection to work.  But it needs to be hidden in the UI.

Hmmm...

----------------------

I dont see a way around filtering items like this out in detailsRenderer's `_renderTable`. @brendankenny do you have any ideas?  Changing details shape to add details.hiddenitems??  🤢 
> Well.. we need the items in the js-libraries audit details for annie's collection to work. But it needs to be hidden in the UI.

Ah got it, yep was referring to the UI - but for some reason thought it was tightly coupled to the audit itself

> Changing details shape to add details.hiddenitems?? 🤢

Sounds like we would most probably still need an identifier to distinguish which items should be hidden, and I can definitely add a flag if that's necessary 🙏  
> I dont see a way around filtering items like this out in detailsRenderer's `_renderTable`. @brendankenny do you have any ideas? Changing details shape to add details.hiddenitems?? 🤢

sorry, just saw this.

All audit details (and most of the properties nested within audit details) can have an extra `debugData` property on them, meant for this sort of thing. We use this for e.g. [data not to be visible in the accessibility-audit details tables](https://github.com/GoogleChrome/lighthouse/blob/7fab7e2b9a34bd69bb7fb78326ab3d6a77ed9f8c/lighthouse-core/audits/accessibility/axe-audit.js#L67-L83) ([example in `sample_v2.json`](https://github.com/GoogleChrome/lighthouse/blob/7fab7e2b9a34bd69bb7fb78326ab3d6a77ed9f8c/lighthouse-core/test/results/sample_v2.json#L1693-L1733)), which is somewhat similar to this case.

It does take a little more parsing effort for http archive queries, but it shouldn't be too bad? `debugData` could also contain all the libraries (duplicating the ids of the libraries in the main table) so any queries wouldn't have to combine the main table and the debugData.
oh perfect. @housseindjirdeh wanna take a stab at that too?

> `debugData` could also contain all the libraries (duplicating the ids of the libraries in the main table) so any queries wouldn't have to combine the main table and the debugData.

so it would be something like
```js
"js-libraries": {
  "id": "js-libraries",
  // ...
  "details": {
    "type": "table",
    "headings": [{
      // ...
    }],
    "items": [
      // ...
    ],
    "debugData": {
      "type": "debugdata",
      "allIds": [
        "jquery",
        "jquery-fast",
        "wordpress"
      ]
    }
  }
}
```
for some value of `allIds` :)