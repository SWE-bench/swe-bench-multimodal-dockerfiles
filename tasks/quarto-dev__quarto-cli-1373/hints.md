Not quite sure about the expected behavior to propose a fix yet, but I think this comes from here: 
https://github.com/quarto-dev/quarto-cli/blob/d89383b3c0d930f5d10de128e57ff9074cea68e9/src/command/render/codetools.ts#L318-L321

Somehow, `code-tools.source` is set back to FALSE because `keep-source` is not resolved to TRUE when `code-tools.source` is a string
https://github.com/quarto-dev/quarto-cli/blob/d89383b3c0d930f5d10de128e57ff9074cea68e9/src/command/render/codetools.ts#L53-L62

Hope it helps fix this. 
