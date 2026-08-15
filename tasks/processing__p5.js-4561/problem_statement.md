FES: validateParameters speed + repetitive logging
#### Most appropriate sub-area of p5.js?
- [x] Other (Friendly errors)

#### Feature enhancement details:
I am working on the FES as part of my GSoC project and I will be starting by addressing the known issues in `validateParameters`. 

validateParameters is responsible for a slowdown as it runs every time a p5 function is called. I had first thought that this must largely be due to `lookupParamDocs` but this isn't entirely the case. `lookupParamDocs` runs a linear search on `data.json`, and it can be done in constant time using object lookups. Moreover the contents of data.json take up about 1.7 MB. Removing the unnecessary stuff cuts it to 400 KB, thus reducing the final library size by 1.3 MB. 

Doing all this only speeds up the first run. Over subsequent runs, scoring and matching the formats repeatedly is redundant if the same sequence of arguments repeats. This can be prevented by caching the argument types and returning if an earlier sequence of types repeats. In repeated calls, this should improve performance as long as the type sequence lookup is faster than scoring. This is the case for functions with a lot of formats and overloads. This would also solve the problem of the FES flooding the console in repeated runs of a function. 
<img src="https://user-images.githubusercontent.com/38867671/82134746-9bdfe480-9818-11ea-8a3d-59e4205a24b8.png" width="300">
Also, trailing undefined arguments are not accounted for by validateParamters, but I think that needs a separate issue? @stalgiag
