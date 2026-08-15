Float crossrefs with unlabeled subfloats
### Bug description

Consider the following minimal working example

```
---
title: "MWE"

format:
  pdf:
    documentclass: article
    pdf-engine: xelatex
    keep-tex: true
---

Figures

::: {#fig-elephants layout-ncol="2"}

![Surus](elephant.png)

![Hanno](elephant.png)

Famous Elephants
:::
````

It produces

![Screenshot from 2022-09-19 10-05-42](https://user-images.githubusercontent.com/1506457/190939309-406e9f5b-9c72-4076-90e2-6dbc9e80d7b7.png)

Note that the subfigures are label as normal figures. The LaTeX produced by Quarto is

```
\begin{figure}

\begin{minipage}[t]{0.50\linewidth}

{\centering 

\raisebox{-\height}{

\includegraphics{elephant.png}

}

\caption{Surus}

}

\end{minipage}%
%
\begin{minipage}[t]{0.50\linewidth}

{\centering 

\raisebox{-\height}{

\includegraphics{elephant.png}

}

\caption{Hanno}

}

\end{minipage}%

\caption{\label{fig-elephants}Famous Elephants}

\end{figure}
```

Now compare the minimal working example with a patched version of it that has cross reference information.

```
---
title: "MWE"

format:
  pdf:
    documentclass: article
    pdf-engine: xelatex
    keep-tex: true
---

Figures

::: {#fig-elephants layout-ncol="2"}

![Surus](elephant.png){#fig-surus}

![Hanno](elephant.png){#fig-hanno}

Famous Elephants
:::
```

It produces

![Screenshot from 2022-09-19 10-09-03](https://user-images.githubusercontent.com/1506457/190939525-b562596f-f386-498f-9db8-ee804938e07c.png)

Note that the subfigures are label properly. The LaTeX produced by Quarto is

```
\begin{figure}

\begin{minipage}[t]{0.50\linewidth}

{\centering 

\raisebox{-\height}{

\includegraphics{elephant.png}

}

}

\subcaption{\label{fig-surus}Surus}
\end{minipage}%
%
\begin{minipage}[t]{0.50\linewidth}

{\centering 

\raisebox{-\height}{

\includegraphics{elephant.png}

}

}

\subcaption{\label{fig-hanno}Hanno}
\end{minipage}%

\caption{\label{fig-elephants}Famous Elephants}

\end{figure}
```

Would be great if Quarto can generate a cross reference information for the subfigures so that users avoid experience the issue reported in the minimal working example.

### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [X] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [X] Please document the operating system you're running. If on Linux, please provide the specific distribution.
