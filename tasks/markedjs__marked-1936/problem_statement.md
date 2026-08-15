Lexer: Space after list appears in last list_item
marked 2.0.0

Sorry if it is not a bug, but a feature... 

In a semantic tree (marked.lexer) an empty space between List and Paragraph appears in a last `list_item`. It looks unlogical. 

While traverse the tree, you should write additional code for exclude this empty space from `list_item`. And then write code to add space between List and Paragraph. 

Expected: Space node should be at the first level of the semantic tree, between the List and the next Paragraph  

for reproduce, please visit: 
https://codesandbox.io/s/markedjs-klt1h?file=/src/marked8lexer.js

```javascript
import marked from "marked";

const markdownText = `This is paragraph 

this is a list with 3 items: 

- item one 
- item two 
- item tree 

Here is another paragrah.`;

const lexerArray = marked.lexer(markdownText);

console.log(lexerArray);
```
![Screenshot from 2021-02-15 19-40-18](https://user-images.githubusercontent.com/1222611/107973010-b8869400-6fc5-11eb-839b-ac9d66c0500d.png)


