Thanks for filing @Anwardo! I'm seeing a completely different set of styles in PSI now though :/ We should be taking into account gzip if the resource that it was attributed to was gzipped. 

![image](https://user-images.githubusercontent.com/2301202/52423041-e8d4f700-2abc-11e9-97ff-51c7d471a754.png)

Also note if you were testing a few days ago, there was a bug in PSI that was ignoring all gzipped sizes.
Thanks for your response @patrickhulce! I was testing on the day I commented. I think the results you got from PSI were because some of our servers didn't sync with latest version of the repo yet. Because those results are related to an older version of our tool. I think if you try again you should get the correct results. 

Also here some screenshots of the actual request, the requested css content causing the problem.

<img width="1020" alt="schermafbeelding 2019-02-11 om 08 57 56" src="https://user-images.githubusercontent.com/5699234/52551236-e2f05600-2ddb-11e9-9e5e-dbabb7e78e78.png">
<img width="910" alt="schermafbeelding 2019-02-11 om 09 00 12" src="https://user-images.githubusercontent.com/5699234/52551235-e257bf80-2ddb-11e9-9202-ea2bca30783e.png">
<img width="799" alt="schermafbeelding 2019-02-11 om 09 01 21" src="https://user-images.githubusercontent.com/5699234/52551233-e257bf80-2ddb-11e9-9e3e-b7cf6007e149.png">

Ah thanks for clarifying!! In this case we our actually trying to account for GZIP, it's just that our estimate for GZIP savings is pretty far off.

The total uncompressed size here is ~160KB. Because we don't know which resource it came from, we assume the global default GZIP savings of 50% even though the actual asset had a compression savings of 88%. This is responsible for the difference.

We can probably improve a bit on our global default estimate given that we know it's a stylesheet that compresses much better than say a script, but note that we still won't be able to 100% capture the difference here.