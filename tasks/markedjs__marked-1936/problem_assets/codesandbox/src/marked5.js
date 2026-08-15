import marked from "marked";

const renderer = {
  list(body, ordered, start) {
    return `<div className="list">${body}</div>`;
  }
};
marked.use({ renderer });
const text = `### Grammar [text]

#### This is first h4 header

And this is the paragraph with some of text. It aims to show you power of using markdown everywhere.

- with list
- with **bold**, _italic_, ~~deleted~~
- with some smart content

#### this is second h4 header

Here we provide some [link](https://google.com).

And here is some ![image](https://m.media-amazon.com/images/I/416VUDuqTML._SY346_.jpg)`;

const renderedByMarked = marked(text);

console.log(renderedByMarked);
