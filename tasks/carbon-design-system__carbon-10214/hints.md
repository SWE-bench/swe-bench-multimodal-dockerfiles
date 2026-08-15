Typo in my screenshot, should say th not the word the twice :P 
@TannerS At a glance I would agree that the `...rest` should be placed on the `th`. There may be a reason as to why it is placed on the button, but I'm not sure. It's likely that moving the `...rest` could cause problems for folks expecting those props to be passed to the `button` and not the `th`. If so, we'd need to put this behind a flag for the v11 release.

Another thing to look into would be adding an `id` prop that is placed on the `th` to solve the a11y issue. That wouldn't be a breaking change.
> @TannerS At a glance I would agree that the `...rest` should be placed on the `th`. There may be a reason as to why it is placed on the button, but I'm not sure. It's likely that moving the `...rest` could cause problems for folks expecting those props to be passed to the `button` and not the `th`. If so, we'd need to put this behind a flag for the v11 release.
> 
> Another thing to look into would be adding an `id` prop that is placed on the `th` to solve the a11y issue. That wouldn't be a breaking change.

Ya I can see that, diff odd to have ...rest in the th for non sortables then not have it for sortables lol, but one thing is clear, i cant pass a `id` prop down to the th element to help fix a few issues, so if there is soke breakage with moving the ...rest, can we find an alternative to set the id for the th? maybe a th id specific prop?
Yeah definitely, we can make it so that the `id` prop is consistently placed on the outer `<th>` element 👍  What do you think @tay1orjones?
@joshblack  if so I dont mind giving a wack at it 
@joshblack yeah let's go for it. 

@TannerS That would be awesome of you to contribute a fix! 🏅 Let me know if I can help.