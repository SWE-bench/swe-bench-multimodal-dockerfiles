Empty Text with defined height throw "Cannot read property '0' of undefined"
**Describe the bug**
 The following snippet throw a TypeError "Cannot read property '0' of undefined"
```javascript
<View>
  <Text style={{ height: 12 }}>{''}</Text>
</View>
```

![screen](https://user-images.githubusercontent.com/1511512/132485670-9c9653b2-e563-438d-b73b-461cc16ed88b.png)
![code](https://user-images.githubusercontent.com/1511512/132486410-efc68c57-bc52-4ce3-80b5-c2a67a3e058d.png)

Maybe add an extra check `node.lines?.[0]` or provide default array for `lines`  ?

