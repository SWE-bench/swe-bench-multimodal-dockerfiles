Hi @vldmr1986 -- when using the `sort` prop, if you indicate `external: true` then the docs indicate that "the caller will take care of sorting the 'data' via 'onSort': https://v2.grommet.io/datatable#sort, but in your codesandbox you were not sorting the data.

If you'd like DataTable to handle the sorting for you, you can remove `external: true` from your sort prop like this: https://codesandbox.io/s/friendly-microservice-ggt1q4?file=/src/App.js

Can you let me know if this solves your issue?
@taysea the problem is neither in the data nor in their sorting The problem is in the incorrect arrows in the header.
Pay attention to the property sort={{ property, direction }} 
<img width="1408" alt="Screenshot 2022-08-29 at 22 16 28" src="https://user-images.githubusercontent.com/17574496/187291555-f008834f-c8ef-4b54-bc0c-8aa1301b5f5f.png">

I 
I noticed that the behavior of the arrows only changes if you manually click on the header. but if you change the sort property through the state or navigation, the arrow does not react.

Assumption: The Table uses the external sort property on componentWillMount only, and then defines the internal local state of these values. So when the Table component is mounted, and the "sort" property is changed, the component won't rerender

If so, the solution could be something like that:
```
useEffect(()=>{
// re-setSate local sort ptoperty inside Table component
}, [sort.direction, sort.property])
```
Thanks for clarifying. From your initial code sandbox, I was able to see the arrow change when adjusting the search params in the url -- however, I am now able to replicate the issue with state. I am looking into a solution.
Once you adjust the search params directly in the URL (manual), it will cause reload the page, so it will trigger componentWillMount (so sort will be correct).
But, if you will use useSearchParams hook(react-router-dom), it won't reload the whole page.
Steps to reproduce:
1. Click on the header "B"
2. Click on the "backward" arrow navigation button from the built-in browser

 however,  the fix with the local state should fix navigation as well