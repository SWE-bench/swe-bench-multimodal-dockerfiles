Quarto uses the comment syntax for the code block to detect annotations. In this case, since the code blocks are `c` code blocks, we're expecting comments like `/* <1> */`:

````markdown
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
      "mrs   r0, PRIMASK \n" \ /* <1> */
      "cpsid i           \n" \ /* <2> */
      "strb r0, cpuSR    \n" \ /* <3> */
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
      "ldrb r0, cpuSR \n" \ /* <1> */
      "msr PRIMASK,r0 \n" \ /* <2> */
    );                    \
  } while(0)
```
1. Inhalt von `cpuSR` in `R0` laden
2. `R0` nach `PRIMASK` kopieren.
````

When I update your example to this syntax, all appear to work correctly. 
Oh shoot, didn't know that.

I've used your modified snippet and well, it's switched around now.

![grafik](https://user-images.githubusercontent.com/41155337/234022016-8f285331-eaa6-48ca-ba3a-0dfac8dc1caf.png)

I've tried using only the `/* <#> */` syntax, but it doesn't seem to work on my side. It just shows the same like above (except for the first element ; circled list but no circled annotation)

Yes I'm seeing the same thing - it looks to me like the c style comments are actually tripping up the LaTeX processing we do to deal with the annotations. I'm having a look now!