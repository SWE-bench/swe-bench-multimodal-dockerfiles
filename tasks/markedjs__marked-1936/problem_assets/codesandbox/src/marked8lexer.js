import marked from "marked";

const markdownText = `# Header 
  
Paragraph1 with nested **bold**, *italic*, and double nested **bold _italic_**. А также русский текст. 
	
- list item 1
- list item 2 
- list item 3

paragraph 2

> blockquote line 1
> blockquote line 2
> blockquote line 3
> 
> -- *Mark Awreliy* 

А ещё параграф с русским текстом مَعَ كلمات عَرَبِيَّةٍ أيضا чтобы совсем интересно было. **أخرى عربية** И немного *русского курсива* и **жирного русского**. 


![some image](https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png)

Also here is a media:

[media | https://www.youtube.com/watch?v=dY_yfg9b2jk]

And a quiz: 

Please, answer the question blabla:

- [x] Lorem ipsum dolor sit amet.
- [ ] Lorem ipsum dolor sit amet consectetur adipisicing.
- [ ] Lorem ipsum dolor sit amet.
  `;

const lexerArray = marked.lexer(markdownText, { gfm: false });

console.log(lexerArray);
