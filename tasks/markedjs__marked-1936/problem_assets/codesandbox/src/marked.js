import fs from "fs";
import marked from "marked";
const mdFileContent = fs.readFileSync("markdown.md", "utf-8");

const makeArrayFromMarkdown = (mdFileContent) =>
  marked
    .lexer(mdFileContent) // raw array with many unnecessary fields
    .filter((elem) => elem.type !== "space")
    .map((elem) => {
      const { type, depth, text } = elem;
      const joinedType = depth ? type[0] + depth : type[0];
      return { type: joinedType, text };
    });

const markdownArray = makeArrayFromMarkdown(mdFileContent);

/* const chapters = markdownArray
  .filter((elem) => elem.type === "h2")
  .map((elem) => elem.text.trim()); */

// object { key: param }
const parseInfo = (text) => {
  const rowsArray = text.split("\n");
  const info = rowsArray.reduce((prev, item) => {
    const [key, value] = item.split(":");
    return { ...prev, [key]: value.trim() };
  }, {});
  return info;
};

// object with number keys '001, 002, ...'
const parseParagraph = (pText) => {
  const rowsArray = pText.split("\n");
  const info = rowsArray.reduce((prev, item, index) => {
    const rowIndex = (index + 1).toString().padStart(3, "0");
    return { ...prev, [rowIndex]: { text: item.trim() } };
  }, {});
  return info;
};

// console.log(JSON.stringify(markdownArray, null, "\t"));

const groupNodesByChapter = (markdownArray) =>
  markdownArray.reduce((prev, item, index, array) => {
    const { type } = array[index + 1] || {};
    // console.log(index, type)

    const getIntervalBackUpToH1orH2 = () => {
      const chapterInterval = [];
      let stepBack = 0;
      while (stepBack > -20) {
        const elem = array[index + stepBack];
        const { type } = elem || {};
        chapterInterval.push(elem);
        if (type === "h1" || type === "h2") return chapterInterval.reverse();
        else stepBack--;
      }
    };

    if (type === "h1" || type === "h2" || type === undefined) {
      const chapterIntervalBefore = getIntervalBackUpToH1orH2();
      prev.push(chapterIntervalBefore);
      return prev;
    } else return prev;
  }, []);

const nodesByChapter = groupNodesByChapter(markdownArray);

const info = nodesByChapter[0].reduce((prev, item) => {
  const { type, text } = item;
  if (type === "h1") return { title: text };
  if (type === "p") return { ...prev, ...parseInfo(text) };
}, {});

// console.log(info)

const chapters = nodesByChapter.slice(1).reduce(
  (prev, item, index, array) => {
    const { type, text } = item;
    if (type === "p") console.log(parseParagraph(text));
    // console.log(item)
  },
  { info: {}, chapters: {} }
);

markdownArray.forEach((elem, index, array) => {
  const { type, text } = elem || {};
  const { type: nextType, text: nextText } = array[index - 1] || {};
  console.log("***");
  if (type === "p" && nextType === "h3")
    console.log(JSON.stringify(parseParagraph(text), null, "\t"));
  if (type === "p" && nextType === "h1")
    console.log(JSON.stringify(parseInfo(text), null, "\t"));
});

// const contentJs

// console.log(result);
// console.log(markdownArray.length);
// console.log(JSON.stringify(nodesByChapter, null, "\t"));
// console.log(JSON.stringify(markdownArray, null, "\t"));
// console.log(JSON.stringify(result, null, "\t"));
