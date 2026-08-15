Excessive vertical space before definition/theorem/etc environments in latex output. 
### Bug description

There is excessive vertical space before definition/theorem/etc environments in latex output. 

Reproduce:
```
# Chapter

## Section

### Subsection

#### Subsubsection

Some text before the definition.

::: {#def-def}
Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Ut purus elit,
vestibulum ut, placerat ac, adipiscing vitae, felis. Curabitur dictum gravida 
mauris.
:::

::: {#exm-exm}
Nam dui ligula, fringilla a, euismod sodales, sollicitudin vel, wisi. Morbi
auctor lorem non justo. Nam lacus libero, pretium at, lobortis vitae, ultricies et, tellus.
:::

Some text before the theorem.

::: {#thm-thm}
Nulla malesuada porttitor diam. Donec felis erat, congue non, volutpat
at, tincidunt tristique, libero. Vivamus viverra fermentum felis.
:::
::: {.proof}
Quisque ullamcorper placerat ipsum. Cras nibh. Morbi vel justo vitae lacus
tincidunt ultrices. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
In hac habitasse platea dictumst.
:::

Some text afterwards.
```
Quarto configuration is the standard when creating a new quarto project in RStudio. So, the latex class is set as `documentclass: scrreprt`. However, the issue is noticeable in other classes.

Pdf render where the amount of inter space can be appreciated:
<img width="341" alt="image" src="https://user-images.githubusercontent.com/98791224/209750130-ef67d3fa-666b-4d30-8a5f-f9fd7f05bf39.png">

Compare with the hand written latex version using same class:
<img width="331" alt="image" src="https://user-images.githubusercontent.com/98791224/209750343-c58ce541-73ce-4188-866e-5292508e18aa.png">

Examining the generated tex file i see every definition (and similar) environment is prepended with some extra code. For example, for the definition we have:

```
Some text before the definition.

\leavevmode\vadjust pre{\hypertarget{def-def}{}}%
\begin{definition}[]\label{def-def}

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Ut purus elit,
vestibulum ut, placerat ac, adipiscing vitae, felis. Curabitur dictum
gravida mauris.

\end{definition}
```
I don't know what is the purpose of `\leavevmode\vadjust pre{\hypertarget{def-def}{}}` but it is adding unwanted vertical space. In fact, removing it solves the issue.

But there is another thing not related to aforementioned extra code. Note the height where the proof QED symbol (the white box) is placed. In the quarto version is below normal position. From my tests, i see that an empty line between the end of the proof text and the end proof tag makes a difference. That is, quarto generates the proof as follows:

```
\begin{proof}

Quisque ullamcorper placerat ipsum. Cras nibh. Morbi vel justo vitae
lacus tincidunt ultrices. Lorem ipsum dolor sit amet, consectetuer
adipiscing elit. In hac habitasse platea dictumst.

\end{proof}
```

But if we just remove the final empty line to have:

```
\begin{proof}

Quisque ullamcorper placerat ipsum. Cras nibh. Morbi vel justo vitae
lacus tincidunt ultrices. Lorem ipsum dolor sit amet, consectetuer
adipiscing elit. In hac habitasse platea dictumst.
\end{proof}
```

then the QED symbol goes up where we expect it to be.

More info:

- Quarto 1.2.280
- R studio 2022.12.0 Build 353
- Windows 11 Pro 22H2

### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [X] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [X] Please document the operating system you're running. If on Linux, please provide the specific distribution.
