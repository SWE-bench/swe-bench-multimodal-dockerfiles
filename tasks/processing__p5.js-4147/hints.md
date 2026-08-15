I don't if this applies to all cases, but using `beginShape(TRIANGLE_FAN)` with version 0.9.0 seems to have the expected outcome.

Hi thank you for the well-written issue!

This issue stems from [this code in the p5.RendererGL.Immediate](https://github.com/processing/p5.js/blob/master/src/webgl/p5.RendererGL.Immediate.js#L190). This section is in need of a refactor. 

Essentially, `immediateMode` doesn't keep track of the relationship between `vertexColors` and `vertices`. So when the linked code tesselates your vertices it gives them a `TRIANGLES` sequencing, which leads to there being 6 vertices but only 4 vertexColors.

Adding `TRIANGLE_STRIP` to the shapeMode argument fixes it because this prevents the vertices from being recalculated. In addition, this can be fixed by giving the final desired `TRIANGLES` sequencing with the appropriate fills.
```js
function setup() {
  createCanvas(500, 500, WEBGL);

  beginShape(TRIANGLES);

  fill(250);
  vertex(150, -150);

  fill(100, 50, 100);
  vertex(-150, 150);

  fill(100, 100, 20);
  vertex(-150, -150);

  fill(100, 50, 100);
  vertex(-150, 150);

  fill(250);
  vertex(150, -150);

  fill(200);
  vertex(150, 150);

  endShape(CLOSE);
}
```

But ideally this would be done automatically with the code you provided at first. In order to do this we need to figure out how to get the correct sequence of colors back out of the `vertexColors` array and rebuild it after the vertices are modified.
Just for a hack-y example of the desired outcome. If we do this starting [on this line](https://github.com/processing/p5.js/blob/master/src/webgl/p5.RendererGL.Immediate.js#L204) then we get desired behavior with your first example:
```js
        const tempVertices = this.immediateMode.vertices.slice();
        const tempVertexColors = this.immediateMode.vertexColors.slice();
        this.immediateMode.vertices = [];
        this.immediateMode.vertexColors = [];
        for (
          let j = 0, polyTriLength = polyTriangles.length;
          j < polyTriLength;
          j = j + 3
        ) {
          const colorIndex = tempVertices.findIndex(vec =>
            vec.equals(
              polyTriangles[j],
              polyTriangles[j + 1],
              polyTriangles[j + 2]
            )
          );
          if (colorIndex !== -1) {
            const colorStart = colorIndex * 4;
            this.curFillColor = [
              tempVertexColors[colorStart],
              tempVertexColors[colorStart + 1],
              tempVertexColors[colorStart + 2],
              tempVertexColors[colorStart + 3]
            ];
          }
          this.vertex(
            polyTriangles[j],
            polyTriangles[j + 1],
            polyTriangles[j + 2]
          );
        }
      }
```
This is a non-ideal solution because it is checking every vertex for its desired vertexColor by searching for a match in the original vertex array. This requires copying two arrays and doing a search in one.