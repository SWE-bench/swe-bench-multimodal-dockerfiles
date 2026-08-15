The reason the selected feature is above the geolocation is because:

> Selected features are added to an internal unmanaged layer.
> — <cite>http://openlayers.org/en/latest/apidoc/module-ol_interaction_Select-Select.html</cite>

And unmanaged layers are always rendered above other layers:

> Allowing the user to set the Z-index of unmanaged layers was discussed, but it seems the merged PR forces `zIndex: Infinity` on unmanaged layers.
> — <cite>https://github.com/openlayers/openlayers/issues/4113#issuecomment-140776509</cite>

Not sure what the workaround is though.
A nice improvement would be the ability to configure Select, Draw and Modify interactions with a `layer`. If anyone is able to create a pull request, it would be appreciated.
I made #8507 for this. Thanks for being open to pull requests for this. Looking forward to it being reviewed and hopefully merged.