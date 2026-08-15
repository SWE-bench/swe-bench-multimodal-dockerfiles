Node DeprecationWarning: Buffer() is deprecated due to security and usability issues. Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.
**Describe the bug**

A depreciation warning about `Buffer()` is shown when a pdf has been rendered. In the future `Node` versions, `Buffer()` will be removed. Which will broke the rendering process.

**To Reproduce**

Have `Node` `v10.15.3` or more.

1. Render a new pdf.
2. Open the browser console.
3. See the warning.

**Screenshots**
![Untitled](https://user-images.githubusercontent.com/31422467/57094611-f5917180-6cde-11e9-9274-287aa4778cd8.png)

**Desktop:**
 - OS: Windows
 - Browser: Chromium (Electron)
 - @react-pdf/renderer: 1.5.4,
 - @react-pdf/styled-components: 1.4.0
