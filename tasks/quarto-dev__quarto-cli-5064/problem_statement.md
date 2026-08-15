Code Annotation for C/C++ & VHDL not handled correctly
### Bug description

Hello,
I've noticed, that the code annotation for languages such as C/C++ & VHDL doesn't work correctly. It seems to handle R & Python code neatly, but with the previously mentioned languages, it does detect the annotation, but doesn't replace it with the circle numbering.

## Snippet

Following snippet...

````qmd
``` vhdl
type state is (S0, S1, S2);
signal c_st, n_st : state;

p_seq: process (rst, clk)                       -- <1>
begin
  if rst = ’1’ then
    c_st <= S0;
  elsif rising_edge(clk) then
    c_st <= n_st;
  end if;
end process;

p_com: process (i, c_st)                        -- <2>
begin                                           -- <2>
  -- default assignments                        -- <2>
  n_st <= c_st; -- remain in current state      -- <2>
  o <= ’1’; -- most frequent value              -- <2>
  -- specific assignments                       -- <2>
  case c_st is                                  -- <2>
    when S0 =>                                  -- <2>
      if i = "00" then                          -- <2>
        n_st <= S1;                             -- <2>
      end if;                                   -- <2>
  end case;
end process;
```
1.  [*Memorizing*]{.underline} (sequentielle Logik)
2.  [*Memoryless*]{.underline} (kombinatorische Logik)


```cpp
int main(void) {
  uint8_t test;                                 // <1>
}                                               // <1>

void testing(int a) {                           // <2>
  a += a;                                       // <2>
}                                               // <2>
```
1. Hello World
2. This is just a test

```r
library(tidyverse)
library(palmerpenguins)
penguins |>                                      # <1>
  mutate(                                        # <2>
    bill_ratio = bill_depth_mm / bill_length_mm, # <2>
    bill_area  = bill_depth_mm * bill_length_mm  # <2>
  )                                              # <2>  
```
1. Take `penguins`, and then,
2. add new columns for the bill ratio and bill area.


```python
thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")                 # <1>
print(thislist)                           # <2>
```
1. Remove `banana` from the list
2. Print list
````

...produces:

![grafik](https://user-images.githubusercontent.com/41155337/229271001-5e3efe1a-ba79-46f9-94f7-04042da80b8e.png)

notice the comment blocks right next to the code.

![grafik](https://user-images.githubusercontent.com/41155337/229271022-43acaebb-cf41-46fd-93d8-01138d1b66d4.png)

## `quarto check`

```cmd
[>] Checking versions of quarto binary dependencies...
      Pandoc version 3.1.1: OK
      Dart Sass version 1.55.0: OK
[>] Checking versions of quarto dependencies......OK
[>] Checking Quarto installation......OK
      Version: 1.3.302
      Path: C:\Users\joelv\AppData\Local\Apps\Quarto\bin
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
