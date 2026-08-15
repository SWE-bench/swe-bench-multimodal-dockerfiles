For our use case, we only need additive blending, but it may be interesting to support additional blending modes in OpenLayers.

For the Canvas renderer, the composition can be configured via the [CanvasRenderingContext2D.globalCompositeOperation](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/globalCompositeOperation). Would it make sense to allow users to configure blending behaviour (for both the Canvas and the WebGL renderer) using a `compositeOperation` parameter (see [Composition examples](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Compositing/Example)). The argument could then be mapped internally to the corresponding parameters of `glBlendEquation()` and `glBlendFunc()`.

```javascript
prepareDraw(frameState, opt_disableAlphaBlend, compositeOperation) {
  ...
  if (compositionOperation === "lighter") {
    glBlendEquation(GL_FUNC_ADD)
  }
  ...
)
```
> For our use case, we only need additive blending, but it may be interesting to support additional blending modes in OpenLayers.
> 
> For the Canvas renderer, the composition can be configured via the [CanvasRenderingContext2D.globalCompositeOperation](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/globalCompositeOperation). Would it make sense to allow users to configure blending behaviour (for both the Canvas and the WebGL renderer) using a `compositeOperation` parameter (see [Composition examples](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Compositing/Example)). The argument could then be mapped internally to the corresponding parameters of `glBlendEquation()` and `glBlendFunc()`.
> 
> ```js
> prepareDraw(frameState, opt_disableAlphaBlend, compositeOperation) {
>   ...
>   if (compositionOperation === "lighter") {
>     glBlendEquation(GL_FUNC_ADD)
>   }
>   ...
> )
> ```

Hi Markus, 

yes I was thinking something like that, but we would need to set actually the _blendFunc_ as well. I was thinking to have enum 1:1 with the WebGL variables.

 ```js
 prepareDraw(frameState, opt_disableAlphaBlend, glBlendEquation, glBlendFuncSRC, glBlendFuncDST) {
   ...
   if (!glBlendEquation && !glBlendFuncSRC&& !glBlendFuncDST){
     # Default OpenLayer behaviour
     gl.blendFunc(
       gl.ONE,
       opt_disableAlphaBlend ? gl.ZERO : gl.ONE_MINUS_SRC_ALPHA
     );
   }else {
     # customized blending
     gl.blendEquation(glBlendEquation)
     gl.blendFunc(glBlendFuncSRC, glBlendFuncDST)
   }
   ...
 )
 ```

where glBlendEquation, glBlendFuncSRC, glBlendFuncDST are defined in the TileLayer style and they can have values:

**glBlendEquation**: GL_FUNC_ADD, GL_FUNC_SUBTRACT, GL_FUNC_REVERSE_SUBTRACT, GL_MIN,  GL_MAX (in our case we need GL_FUNC_ADD, but it is the default parameter)

**glBlendFuncSRC/glBlendFuncDST**: https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/blendFunc#constants

so in this way we would have maximum flexibility. I don't like the idea to have hardcoded presets as https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/globalCompositeOperation with a lot of if conditions in prepareDraw.

Anyway, let's see if OpenLayer developer agree with us and they would like to have an API to srtup customized blending. 
For 2d canvas renderers a globalCompositeOperation can be easily configured/reset at the layer prerender and postrender events:

`evt.context.globalCompositeOperation = 'lighter';`

I don't think it is necessary to provide any additional functionality for 2d canvas layers or replicate those for WebGL.
> For 2d canvas renderers a globalCompositeOperation can be easily configured/reset at the layer prerender and postrender events:
> 
> `evt.context.globalCompositeOperation = 'lighter';`
> 
> I don't think it is necessary to provide any additional functionality for 2d canvas layers or replicate those for WebGL.

Thank you for you feedback. 

Probably I was not clear on our requirements, let me explain in more details. 

We have greyscale images and the user can apply a color function (rgb color, opacity, min/max, etc..., see screenshot below, coloring UI) to the image interactively. The images are pyramidal and the tiles are also rather large (> 10^3x10^3 pixels). 

Therefore we need fast webgl processing, and we can't use cpu processing with the canvas 2D Tile Layer for coloring the image (it is just too slow, while the blending by setting evt.context.globalCompositeOperation was fast enough) .  

----------------------------------------
Fast processing for coloring the images was the reason why we were using an offscreen webgl rendering for coloring the images, then we were passing the image to the canvas 2D tile layer and finally making the blening in openLayer by setting evt.context.globalCompositeOperation = 'lighter' as you described. This workflows worked well, but there was a bottleneck in passing the rendered image as a png from the offscreen render to the canvas 2D tile layer, and that's why we are migrating to the new WebGL Tile Layer with OpenLayer version 6.9.

------------------------


Blending capabilities for the WebGL Tile Layer for me looks a general use cases and many users could benefit from such API. If you still think that it is not worth having such API, we will fork OpenLayer. However, we really would like to avoid forking for a small change like this one ans we hope to agree on some common blending API for teh WebGL Tile Layer to integrate in OpenLayer.

-----------------------

Reference: coloring UI
![image](https://user-images.githubusercontent.com/7985338/141274542-46ab5b1e-c650-453a-9e46-8c9ef12d4ca3.png)

I have no problem with the general use proposal using WebGL variables.  I don't think any new options are needed for 2d rendering, and therefore hardcoding `globalCompositeOperation` values to match seems inappropriate in a WebGL setting.

Browsers do use some hardware acceleration for 2d canvas operations, but in my experience it is buggy - there is currently an issue with https://openlayers.org/en/latest/examples/disable-image-smoothing.html in Chrome and Edge (only with hardware acceleration enabled) where you may notice some pixels in the smoothing disabled map show incorrect negative elevations.
> I have no problem with the general use proposal using WebGL variables. I don't think any new options are needed for 2d rendering, and therefore hardcoding `globalCompositeOperation` values to match seems inappropriate in a WebGL setting.
> 

I agree with you in not using hardcoded presets as the one from globalCompositeOperation. I will update the PR to pass directly the WebGL variables as I suggested in https://github.com/openlayers/openlayers/pull/12985#issuecomment-965709612. The idea is that the external app set up the WebGL blending variables in the WebGL Tile Layer style for each tile layer.

> Browsers do use some hardware acceleration for 2d canvas operations, but in my experience it is buggy - there is currently an issue with https://openlayers.org/en/latest/examples/disable-image-smoothing.html in Chrome and Edge (only with hardware acceleration enabled) where you may notice some pixels in the smoothing disabled map show incorrect negative elevations.

I agree, for the moment image processing with 2d canvas is still not optimal and they do not offer enough flexibility as a pure WebGL approach for specific tasks. 
Wouldn't it be possible to use the webgl context available in `prerender` and `postrender` events to do that? See https://github.com/openlayers/openlayers/pull/12933
> Wouldn't it be possible to use the webgl context available in `prerender` and `postrender` events to do that? See #12933

I didn't see that I could have access to the webgl context in the prerender and postrender events. I will try to change the blending vars there. Thanks for pointing out!
@mike-000 @jahow I may have stumbled upon a more fundamental problem. It appears every layer gets rendered into a separate context.

Every layer creates a separate `WebGLTileLayerRenderer`:
https://github.com/openlayers/openlayers/blob/0e19c9aa2b05eb9b28b502aa8d3cd590dabacafa/src/ol/layer/WebGLTile.js#L303-L317

Every renderer creates a separate `WebGLHelper`:
https://github.com/openlayers/openlayers/blob/080fe8ca67da57202ce024ea0267f1e5c8e8a9fa/src/ol/renderer/webgl/Layer.js#L77-L80

Every helper creates a separate canvas/context:
https://github.com/openlayers/openlayers/blob/080fe8ca67da57202ce024ea0267f1e5c8e8a9fa/src/ol/webgl/Helper.js#L255
https://github.com/openlayers/openlayers/blob/080fe8ca67da57202ce024ea0267f1e5c8e8a9fa/src/ol/webgl/Helper.js#L263
> @mike-000 @jahow I may have stumbled upon a more fundamental problem. It appears every layer gets rendered into a separate context.

That will change when #12965 is complete
> > @mike-000 @jahow I may have stumbled upon a more fundamental problem. It appears every layer gets rendered into a separate context.
> 
> That will change when #12965 is complete

Excellent!

I also like @jahow's suggestion to change the blending behavior using event listeners. Together with #12933 we should be all set then, shouldn't we? Or do you have an alternative idea?
> Excellent!
> 
> I also like @jahow's suggestion to change the blending behavior using event listeners. Together with #12933 we should be all set then, shouldn't we? Or do you have an alternative idea?

I think this is the best way to go: these events are here to allow you to tweak the webgl context to your liking right before the `draw` call happens.
Hi @jahow @mike-000 @hackermd I had some times to check on this and unfortunately I can not change the gl parameters in the pre renderer event. The event is called  here https://github.com/openlayers/openlayers/blob/main/src/ol/renderer/webgl/TileLayer.js#L341 and then the blendFunc values are changed everytime in prepareDraw (https://github.com/openlayers/openlayers/blob/87d37937c58f4781b9b15611b44ce30a44293975/src/ol/webgl/Helper.js#L571-L574) and in the postProcessing passes (https://github.com/openlayers/openlayers/blob/main/src/ol/webgl/PostProcessingPass.js#L268).

In this PR I propose to have some API to pass to the PostProcessingPass the blending varibales (i.e.: https://github.com/openlayers/openlayers/pull/12985/commits/18e753124694271dd455d3de9de8f10dc256b506#diff-f85b1dbc2ba8aab5b8a1e1ab0f2306ae493ab085c3e2c98f9cc67942602d36a9R258).

An example how to use the API is here https://github.com/MGHComputationalPathology/dicom-microscopy-viewer/pull/70
:package: Preview the [examples](https://deploy-preview-12985--ol-site.netlify.app/examples/) and [docs](https://deploy-preview-12985--ol-site.netlify.app/apidoc/) from this branch here: https://deploy-preview-12985--ol-site.netlify.app/.
Hi @MoonE, I have applied your last review, please let me know if any other action is required on my side. Thanks!
Hi @MoonE please let us know if there are any additional changes that you would like us to make to the PR. It would be great if this feature could get included into the next release.