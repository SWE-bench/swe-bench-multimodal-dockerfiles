The anchor is an old issue #4829 with all Google icons being treated alike which was never resolved.  According to https://stackoverflow.com/a/22569590/10118270 the interpretation of scale is also inconsistent with Google Earth which scales from 32 pixels, not the 64 pixel original image.

https://kml4earth.appspot.com/icons.html#notes lists specific hotspots used for Google pushpins, arrow-reverse and paddles.  All other Google icons appear to use center-center.

https://stackoverflow.com/a/22569590/10118270 appears to be correct and applies to all icons of any size, not just 64 pixel  Google icons.  `ol/format/KML` currently has a `DEFAULT_IMAGE_SCALE_MULTIPLIER = 0.5` which makes the default icon look correct in OpenLayers.  However when written back the result would be too small in Google Earth.  Correctly implementing initial scaling to 32 pixels will probably need an additional option in `ol/style/Icon` to apply scaling based on the size of the loaded image.
See example with fixes at https://deploy-preview-12674--ol-site.netlify.app/examples/drag-and-drop-custom-kmz.html
That's awesome.  Well done.
Actually, the label anchors are no longer correct.  Should that be another bug report?
The text offset now needs to be based on the normalized 32 pixel image and the specified scale, not the original image size.  That should be done as part of this change.
The labels offsets are now correctly scaled.  The precise position relative to the icon will depend on the icon anchor, as it always did.  Icons which are now correctly center anchored have a label top right while the bottom anchored parking icon has a center right label.
Thanks Mike!