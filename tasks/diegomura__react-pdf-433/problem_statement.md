Setting a border on a rounded <View> causes unexpected results

**OS:**
macOS 10.13 High Sierra

**React-pdf version:**
@react-pdf/renderer@^1.0.0-alpha.25

**Description:**
I am attempting to draw a circle with a border by rounding a `<View />` and adding a border. 

```
const Quixote = () => (
  <Document>
    <Page style={styles.body}>
      <View style={styles.circle}></View>
    </Page>
  </Document>
);

const styles = StyleSheet.create({
  body: {
    paddingTop: 35,
    paddingBottom: 65,
    paddingHorizontal: 35,
  },
  circle: {
    width: 50,
    height: 50,
    backgroundColor: 'green',
    borderRadius: 50,
    border: '2 solid red'
  }

});

ReactPDF.render(<Quixote />);
```

When I set the `borderRadius` to 1, the border drawn mostly goes around the view. 
![screen shot 2018-11-29 at 12 14 46 pm](https://user-images.githubusercontent.com/4199296/49249306-b037e380-f3d0-11e8-96cd-29eee986683b.png)

When I set `borderRadius` to 3, the border drawn already starts to have issues.
![screen shot 2018-11-29 at 12 14 51 pm](https://user-images.githubusercontent.com/4199296/49249354-c5ad0d80-f3d0-11e8-8e2d-393dee2530e1.png)

As I increase the borderRadius to make the view more circular the rendering gets really strange.
`borderRadius @ 20`
![screen shot 2018-11-29 at 12 14 58 pm](https://user-images.githubusercontent.com/4199296/49249430-f42ae880-f3d0-11e8-9272-cefd5bca1b0d.png)

`borderRadius @ 30`
![screen shot 2018-11-29 at 12 15 02 pm](https://user-images.githubusercontent.com/4199296/49249444-fb51f680-f3d0-11e8-8f24-49d22bc27962.png)

I would love the border implementation to better support rounded views! Thanks a bunch!
