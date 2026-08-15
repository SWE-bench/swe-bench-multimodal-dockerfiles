[revealjs] `width` and `height` in % are not quoted in template
### Discussed in https://github.com/quarto-dev/quarto-cli/discussions/4059

<div type='discussions-op-text'>

<sup>Originally posted by **witszymanski** January 23, 2023</sup>
Hi all!
According to this: https://quarto.org/docs/reference/formats/presentations/revealjs.html#slide-layout I can use width in percentage. However, when I do that, the presentation is not appearing at all. Blank screen. 

```
---
title: "Title"
subtitle: "Subtitle"
author: "Me Me"
institute: Institute
date: "January 23, 2023"
date-format: "DD MMMM YYYY"
format: 
  revealjs:
    theme: default
    width: "100%"
    height: "100%"
editor: source
---


# Hello

## What is Lorem Ipsum? {auto-animate="true"}

Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. 

-   bullets

    -   bullet 1
    -   bullet 2
    -   bullet 3
    -   bullet 4

-   boaleadasf

    -   again1

    -   again2

```
![image](https://user-images.githubusercontent.com/15866068/214030549-f84e05c8-2964-4838-9feb-cf302cffb616.png)


If I exchange the % with pixels, it works:
```
  revealjs:
    theme: default
    width: 1600
    height: 900
```

![image](https://user-images.githubusercontent.com/15866068/214030510-dc17d63a-3542-472f-b6c5-e07de1181c97.png)


What am I doing wrong? 
Greets</div>
