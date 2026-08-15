code annotation doesn't work in version 1.3.336
### Bug description

Hello

I've noticed with the latest version that the code annotation doesn't work correctly for PDF, as in the `tikz` package is not included and the `\circled` command is not defined.

I've tried following snippet:

````qmd
# Parallelität

## Reentrancy

### Dis-/Enable Interrupts

::: callout-warning
## Nachteil
:::

### Critical Sections

``` c
#define CriticalVariable() \
  uint8_t cpuSR // <1>
```
1. definiert lokale Variable `cpuSR` für Sicherung des aktuellen Interrupt-Zustandes

``` c
#define EnterCritical()      \
  do {                       \
    __asm (                  \
      "mrs   r0, PRIMASK \n" \ // <1>
      "cpsid i           \n" \ // <2>
      "strb r0, cpuSR    \n" \ // <3>
    );                       \
  } while(0)
```
1. `PRIMASK` wird in `R0` abgespeichert
2. Interrupts deaktivieren
3. `R0` in `cpuSR` abspeichern

``` c
#define ExitCritical()    \
  do {                    \
    __asm(                \
      "ldrb r0, cpuSR \n" \ // <1>
      "msr PRIMASK,r0 \n" \ // <2>
    );                    \
  } while(0)
```
1. Inhalt von `cpuSR` in `R0` laden
2. `R0` nach `PRIMASK` kopieren.

````

I've also tried defining the `\circled`-command in the preamble of the document, which seems to produce the code annotation in the code block, but not the stylized list elements below it.

![grafik](https://user-images.githubusercontent.com/41155337/234010331-0d354cc5-fd81-47b2-8b9c-8b2bd20981d3.png)

If you need anything else from me, just ask! Thank you for the help!

---

## `quarto check`

```
[>] Checking versions of quarto binary dependencies...
      Pandoc version 3.1.1: OK
      Dart Sass version 1.55.0: OK
[>] Checking versions of quarto dependencies......OK
[>] Checking Quarto installation......OK
      Version: 1.3.336
      Path: C:\Users\joelv\AppData\Local\Programs\Quarto\bin
      CodePage: 1252

[>] Checking basic markdown render....OK

[>] Checking Python 3 installation....OK
      Version: 3.10.4
      Path: C:/Users/joelv/AppData/Local/Programs/Python/Python310/python.exe
      Jupyter: 4.9.2
      Kernels: python3

[>] Checking Jupyter engine render....OK

[>] Checking R installation...........OK
      Version: 4.2.2
      Path: C:/PROGRA~1/R/R-4.2.2
      LibPaths:
        - C:/Users/joelv/AppData/Local/R/win-library/4.2
        - C:/Program Files/R/R-4.2.2/library
      knitr: 1.41
      rmarkdown: 2.20

[>] Checking Knitr engine render......OK
```

### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [ ] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [ ] Please document the operating system you're running. If on Linux, please provide the specific distribution.
- [X] Please provide the output of `quarto check` so we know which version of quarto and its dependencies you're running.
