@dakahn  I just retested this on mac w/Chrome & VO and confirmed it fails. 
I also tested it on MacOS mac with Safari and in this case the label is announced twice. 
and last,  when tested on Win10 with JAWS on Chrome or FF, as well as iOS with Safari and VO it works as expected.   
Good find, @keithkade. You are correct that the `aria-label="Radio button label"` isn't needed, because it's already in the content of the label.

@dakahn The `aria-label` attribute on the `<label>` should just be deleted. That will fix the VO+Safari duplication. Not sure if it will fix the VO+Chrome problem (needs testing), but it is incorrect code that should be deleted anyhow.