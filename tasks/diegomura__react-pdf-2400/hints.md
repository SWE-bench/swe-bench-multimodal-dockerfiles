Although I had difficulty putting both `fixed` and `minPresenceAhead` on the same header component, I was able to achieve the desired effect by using an empty `View` with `minPresenceAhead` above the `View` that contained the fixed header and body text.

[Fixed REPL link](https://react-pdf.org/repl?code=3187b0760ce02e00403207901281440b2302f0c04471004e02980b6300960038402b990098800da1304e6c0218945400d0c50908b028bc681189de9572118393001cc611261c04422f462355e4684122075892955a28533e8d30b06ac269c011a122ab62316c46094e4a609c52ea008e349c0074300072223041649c6111645a64bc305084d992425ae19cb0e4f4d100823294720aca59047250e4e11ef5b41009f1006644344ae4451460d1709cc0866cda591255ed8d60d676c53ac94d3499ade3ddbdfdc56052f644d1008a347214d4746c8694446032105a30344c50f5c044ed4a049c006e25c1325125d3a8677b44000a000b4e3115ec11f9a8a60419824ecc05512978d1001ab3d288e22878209c2aadc3ae8e25f4a08d768ad0a647f1303e117a3045ce4172dd6c490218c607f282703c6a522dca074728f1606226131c6c06fad32ad5450a96ee40c8d09128a2263a09c76a51610624adc889c21ac4e44c2bbc9645c655db6aecce5dd2e1f070bcdee40fa0cc498c9384ce9c1a28908d1002481c08dc9805968445f0f948e75a03198ac76140711c2154943b95516a434a3593c9c22716d379346880184246d3f114697e6607a7d520a28d9ec1d822606375958a3ecd688a09ce452f389eb2ee2819189e6d3368d26091a408a183a93904102a3e6827001422d998000555a8d66a78311e834c083ed2a1a723e644cc932fe07b04e60b7b01ee8be24c1fc41010109a84c81c100ded0bb282801c6010ec9d40d2ac4499a40bb499180e2361b0232cc9aef5a36e338ac899cdfb12591582522cba29ce58c0841811e13258794e888661a4825996fe048c1af465ae1638c0281ea82bb4fe088b703e94342b0b7c479803f324ea21a20026be121ec8423923485aea99378ac2e9e4024e014835a443800050767e4b039e1e96030000140025160001f079764c0300003c0008880630f0f60f901605c178201112500009e4ca6000379a5943483232800170c000230000c45400bea5745b16c5417623e800ee6c325a94659091053a42503e5001b095e5400f495555c16d5441d58350dc37d530274e40001e930908a382c4168f3110652b5d23a500332f53038d137052e6cdb034029510e95a5a00f8f9400e4c43d0b74089d38050000cae40005e443e5bb408597d0395280010880d4880243e5000b1951540012e6bd0899057d71d5001d554a32358d3144d415a318d0d69620a81a0a56e3434a304c5398f53876c5c4f20e8393f4d534409d84d63f541d28fc598a0d28d851158ad167900370390e520e6a88e08850018a44c41dc89bb9f8eb90378b92d0000)



And just in case someone else runs into a similar problem, my browser would sometimes lock up when I tried to mix `minPresenceAhead` and `fixed` inside of a view that spanned multiple pages. I couldn't reproduce it in the REPL, or get any useful information out of the profiler in my browser, so I didn't include that in my issue. But if someone else runs into such a crash, I was able to circumvent it and achieve the desired effect by using an empty `View` w/ `minPresenceAhead` as described above.
@dylnclrk I checked out your "Fixed REPL link" but it appears that its the same link as your original post (which repliaces the error). 

> I was able to achieve the desired effect by using an empty View with minPresenceAhead above the View that contained the fixed header and body text.

I tried following your instructions for the fix but am not seeing a difference on my end. Do you remember what your fix looked like? Something like this?

```
<Document>
    <Page style={{padding: 100}}>
      <View style={{height: 600}}/>
        <View minPresenceAhead={300} />
        <View fixed>
          <Text style={{color: 'red', fontSize: 30, paddingBottom: 40}}>Header</Text>
        </View>
        <Text>
          {LOREM}
        </Text>
        <Text>
          {LOREM}
        </Text>
    </Page>
  </Document>
```
I don't remember exactly, but I think what I did was similar to what you have. But the minPresenceAhead view was a sibling to a wrapper around the fixed content:
```

<Document>
    <Page style={{padding: 100}}>
      <View style={{height: 600}}/>
        <View minPresenceAhead={300} />
        <View>
         <View fixed>
          <Text style={{color: 'red', fontSize: 30, paddingBottom: 40}}>Header</Text>
         </View>
         <Text>
          {LOREM}
         </Text>
         <Text>
          {LOREM}
         </Text>
        </View>
    </Page>
  </Document>

```