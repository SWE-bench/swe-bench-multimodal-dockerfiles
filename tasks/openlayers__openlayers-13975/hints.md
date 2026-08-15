Looks like it with `displacement: [0, 100 / (0.2 + 0.2*markernumber)]` they are aligned at the bottom. Unexpected indeed.
It also happens with regular shape and circle styles https://codepen.io/mike-000/pen/vYRpXNp  These have no anchor option so it may have been intentional.  Both those and icon are subclasses of ol/style/Image.
Thanks for your responses which show that also others can see this behavior.
Could someone who is deeper in the topic (maybe the developer of this code) give a hint if this is the expected behavior, a bug, or how exactly those options should be used / combined (how the different options work together)?
@Razi91 Can you comment on this? Thanks.
![image](https://user-images.githubusercontent.com/5995454/182103925-9033ebae-d170-4346-a665-8091581f3673.png)
https://codepen.io/razi91-the-selector/pen/xxWpaaL
The lower one is without displacement, the higher one is with (the middle is the expected one).

Scaling is done after displacing, so the `[0, 100]` is multiplied by the scale. It could be fixed by doing @MoonE 's calculation in those classes, I could do that, but it would be a breaking change for some projects. Maybe introducing new property like `absoluteDisplacement` would be a better option.
For regular shapes it make sense, e.g. circle style with radius 50 and displacement [0, 50] is always anchored bottom center regardless of scale

![image](https://user-images.githubusercontent.com/49240900/182107951-1d57fe31-c8d4-4025-bbd6-84e11c8bca80.png)

Maybe that should be called `anchor` for consistency with icon style (although for regular shapes the anchor origin would always be `center-center`) and a separate option `displacement` should not be scaled?

The difference is that `displacement` is given in pixels, while `anchor` is relative to the size value. And yes, it's a bit messed up. I think we should fix it. Without `scale` the `displacement` works fine.
Anchor units can be specified as pixels, but are still scaled with the image https://codesandbox.io/s/icon-forked-ku5ly3?file=/main.js
> Anchor units can be specified as pixels, but are still scaled with the image

This is very confusing for the user.

@Razi91 do you have a rough idea until when a fix / improvement will be available? (just asking, because it directly influences if I have to scale my displacement in the code or if I - maybe - will wait a few days and can directly use an improved library)
> This is very confusing for the user.

No, that would be expected as anchor is typically set within or on the edge of the image.

Also note that like anchor (where it is expected) the displacement option is affected by rotation (which might not be expected) e.g. with `rotation: Math.PI/2,` in first example

![image](https://user-images.githubusercontent.com/49240900/182115514-34ae1a7a-760e-4245-afdc-ec8cbb707fc9.png)

For comparison the text style `offsetX` and `offsetY` options are not scaled but are rotated in the vector layer renderer.  They are not rotated with in vector context immediate renderer, although they should be consistent.  https://codesandbox.io/s/icon-scale-forked-63g2il?file=/main.js
I'm not sure if it's enough and safe, but a method in `Image.js`:
```js
  getScaledDisplacement() {
    const scale = this.scale_;
    if (typeof scale == 'number') {
      return this.displacement_.map((p) => p / scale);
    } else if (Array.isArray(scale)) {
      return this.displacement_.map((p, idx) => p / scale[idx]);
    }
    return this.displacement_;
  }
```
to return scaled displacement, and then changing usage of `getDisplacement` to `getScaledDisplacement` in `RegularShape.js` (`Circle.js` extends it) and `Icon.js` should fix it.

I need to check it because right now I have other things to focus on. I also noticed that the calculation of displacement moved from `getOrigin` to `getAnchor`, it might also change its behavior, I'm not sure if I tested it with scale right now.

Well, it definitely requires defining what `displacement` does, that it should move icon in absolute units.
Okay, this solution works (division, not multiplication, I've edited the code in the comment), it makes `displacement` translating the symbol with absolute values.

I'm not sure if it should be done in `RegularShape.js`, or maybe there should be a different name there, now I remember I needed this feature for them, to build more complex styles with that.

Right now it acts that way:
![image](https://user-images.githubusercontent.com/5995454/182198085-2426e588-e718-4162-acf7-bcf7e382936a.png)

after fix it would be:
![image](https://user-images.githubusercontent.com/5995454/182198296-f3821d63-2f01-4767-847c-4545a2e6f593.png)

Any suggestions about changing it, without breaking it in any way? Adding different parameters like `displacementUnit`, where would be by default current `'relative'`, and could be set `'absolute'` (just like now there is for `Icon` properties `anchorXUnits`)?
Just no new properties please. Symbol placement is already messed up more than enough. Please suggest a fix, even if it breaks current applications. Better to make an existing property work like the majority of users would expect, than adding new weird options.
I think it should be fine if one additional parameter would be added which defaults to the current behavior ('relative') and can be set to 'absolute'. This makes it smoother for existing and new projects.
Why not just clarify the meaning of `displacement`, saying `displacement of the symbol in css pixels`, and fix the behavior accordingly. Then at least for this option, it is clear what it does.
Right now for `Icon` we are setting anchor, with either fraction of size or pixels. This is scaled by `scale`. `displacement` should be "above" that, I mean it should be absolute, then I think the current behavior for Icon is wrong and should be fixed (and documentation should be written clearer). So in case of Icon, this is the 'relative' setting.

But what about `RegularShape`, as I posted in the last comment?

I just need to know how (I mean: how those parameters should work, code is easy) to fix it, and I can make PR with a fix for that
> Okay, this solution works (division, not multiplication, I've edited the code in the comment), it makes `displacement` translating the symbol with absolute values.
> 
> I'm not sure if it should be done in `RegularShape.js`, or maybe there should be a different name there, now I remember I needed this feature for them, to build more complex styles with that.
> 
> Right now it acts that way: ![image](https://user-images.githubusercontent.com/5995454/182198085-2426e588-e718-4162-acf7-bcf7e382936a.png)
> 
> after fix it would be: ![image](https://user-images.githubusercontent.com/5995454/182198296-f3821d63-2f01-4767-847c-4545a2e6f593.png)
> 
> Any suggestions about changing it, without breaking it in any way? Adding different parameters like `displacementUnit`, where would be by default current `'relative'`, and could be set `'absolute'` (just like now there is for `Icon` properties `anchorXUnits`)?

To make the handling the same over all modules the behavior in your example makes sense to me. However, this could 'kill' some more complex drawings.
Just as an idea: How would it behave if we scale it 'relative without offset'. Meaning, that we scale it relatively as it is currently, but determining the lowest displacement value and subtracting this value from all displacement values. This would scale the drawing as it is currently, but removing the offset from the baseline. Could this be a solution or do I miss a huge drawback?
@Razi91 The behavior for `RegularShape` should be the same. The difference between `Icon` and `RegularShape` is only that the former is an external graphic, wheres the latter is created by OpenLayers.
@thn80 You know the scale, because you configure it yourself. So you can easily multiply the displacement by the scale on the application level, if you so wish.
> @thn80 You know the scale, because you configure it yourself. So you can easily multiply the displacement by the scale on the application level, if you so wish.

That's true, but as @Razi91 also mentioned a 'displacement' is not assumed to be relative. If something like 'displacementUnit' would be added which defaults to the current behavior 'relative' it would from the usage be similar to anchor and would also be backwards compatible with existing code.
@thn80 Exactly. Displacement as I defined it above (i.e. displacement in css pixels) is not relative. We don't need to be backwards compatible - we'll be releasing v7.0 next, and it is confusing to have two similar properties (`anchor` and `displacement`). So let's fix this rather than adding more confusion.