In the HTML we'll have in RevealJS config
````html
        // The "normal" size of the presentation, aspect ratio will be preserved
        // when the presentation is scaled to fit different resolutions. Can be
        // specified using percentage units.
        width: 100%,

        height: 100%,
````

leading to 
````
test.html:548 Uncaught SyntaxError: Unexpected token ',' (at test.html:548:20)
````

We should probably make sure to quote those variable in the template as  it seems Pandoc does not do it. 