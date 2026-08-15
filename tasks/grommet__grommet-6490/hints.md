Hi @shb,
I checked and found you need to pass the correct props value for the **gap**.
Gap will work if you pass the correct prop value to it.
I am sharing the gap props value

<img width="171" alt="GapProps" src="https://user-images.githubusercontent.com/36879900/201534359-2a8b12b2-6729-4f5e-ac8d-0db01eb77f8e.PNG">


```Javascript
 <Box direction="row" gap="medium" border="between" pad="medium">
    <Box pad="small" background="dark-3">
      Test 1
    </Box>
    <Box pad="medium" background="light-3">
      Test 2
    </Box>
  </Box>
```

Output:
<img width="161" alt="GapOutput" src="https://user-images.githubusercontent.com/36879900/201534431-9ef0cf7c-9b5c-477d-ab72-645a9d5d0917.PNG">

Thanks,
Umesh