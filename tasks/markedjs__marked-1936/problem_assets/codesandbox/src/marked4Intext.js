import fs from "fs";
import marked from "marked";
const mdFileContent = fs.readFileSync("markdown2.md", "utf-8");
marked.use({ smartypants: true });
const makeArrayFromMarkdown = (mdFileContent) =>
  marked
    .lexer(mdFileContent) // raw array with many unnecessary fields
    .filter((elem) => elem.type !== "space")
    .map((elem) => {
      const { type, depth, tokens = [] } = elem;
      const text = tokens.map((elem) => elem.text).join("");
      const joinedType = depth ? type[0] + depth : type[0];
      return { type: joinedType, text };
    });

const markdownArray = makeArrayFromMarkdown(mdFileContent);

// console.log(JSON.stringify(markdownArray, null, '\t'));

console.log(marked.lexer(mdFileContent));
// console.log(markdownArray);
