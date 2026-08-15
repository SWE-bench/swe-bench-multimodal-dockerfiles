import marked from "marked";

const string1 = `- [ ] first variant 
- [ ] second variant 
- [v] third variant 
`;

const renderer = {
  checkbox: (checked) => null
};

marked.use({ renderer });

const html = marked(string1);

console.log(html);
