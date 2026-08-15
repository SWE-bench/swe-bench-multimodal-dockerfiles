Thanks for reporting this, @kikitte. You are right, the success callback should be called after the features are added. Would you be able to create a pull request? Thanks in advance.
@kikitte 
I also encountered this problem, you can try this.
```js
 Promise.resolve().then(vector.getSource().getExtent())
```
It works for me.