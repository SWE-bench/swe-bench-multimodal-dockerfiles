Problems with Extending Styled Components
I am trying to use the styled components api as described at https://react-pdf.org/styling#styled-components and further extending styles according to https://www.styled-components.com/docs/basics#extending-styles. However I don't see the overridden styles being applied.

This is a simple example that explains things a little better.

    import React, { Component } from 'react';
    import { Page, Text, Image, View, Document, StyleSheet } from '@react-pdf/renderer';
    import { PDFViewer, PDFDownloadLink } from '@react-pdf/renderer';
    import styled from '@react-pdf/styled-components';

    const DefaultPage = styled.Page`
      flex-direction: row;
      flex-wrap: wrap;
    `
    const ExampleText1 = styled.Text`
      border-left-width: 1pt;
      border-right-width: 1pt;
      border-style: solid;
      border-color: #000;
      border-collapse: collapse;
      min-height: 14pt;
      color: #f00;
    `
    const ExampleText2 = styled(ExampleText1)`
      border-top-width: 1pt;
      border-bottom-width: 1pt;
      color: #0f0;
    `
    const ExampleText3 = styled(ExampleText2)`
      border-color: #888;
      color: #00f;
    `
    class ExamplePrint extends Component {
      render() {
        return (
          <Document title="Example" onRender={blob=>console.log( "Blob", blob )}>
            <DefaultPage size="A4">
              <ExampleText1>Text1</ExampleText1>
              <ExampleText2>Text2</ExampleText2>
              <ExampleText3>Text3</ExampleText3>
            </DefaultPage>
          </Document>
        )
      }
    }

    class PrintBase extends Component {
      render() {
        const document = <ExamplePrint/>
        return(
          <div>
            <PDFViewer width="100%" height="1000">
              {document}
            </PDFViewer>
          </div>
        )
      }
    }

    export default PrintBase```

I would expect the first text to be red and have borders left and right, the second one to be green with borders all round and the last one to be blue and have lighter borders. However they all come out exactly the same.

[Rendered PDF](https://user-images.githubusercontent.com/383834/51480329-aefbb500-1d88-11e9-8b58-3dd8ee9462b6.png)

Looking at the layout data in the blob I can see all the various style elements in there but I don't know if they are in the correct format since the structure is an object with a mixture of css property keys and numeric indices mixed in with undefined values.

[Chrome Console](https://user-images.githubusercontent.com/383834/51480494-187bc380-1d89-11e9-8955-2f2c8f03f554.png)

This is with react-pdf/renderer and styled components v1.2.0. Unfortunately I can't find any sandbox that seems to working with react-pdf when using styled components.
