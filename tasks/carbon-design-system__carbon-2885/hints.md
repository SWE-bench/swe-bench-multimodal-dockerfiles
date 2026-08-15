it seems this directly opposes the feedback provided here https://github.com/carbon-design-system/carbon/issues/1794
With regard to #1794 - It states: (One screen reader that I tried said "Checkbox OffOn OffOn checked" :) 
You might want to try adding aria-hidden="true" to either the Off or On span, depending on the current state.
------------------
My understanding of issue #1794 is the screen reader is announcing both "OffOn" for a checked toggle, rather than "On". 
Adding aria-hidden="true" to the appropriate state would stop the screen reader from announcing the label associated with the inactive state.
For example: 
If the state is aria-checked="true" the Off label should have aria-hidden="true" so the screen reader only announces the "On" label. 
If the state is aria-checked="false" the On label should have aria-hidden="true" so the screen reader only announces the "off" label.

Hi, @snidersd!

Thinking about this even more, I've realized that "On" and "Off" are actually _not_ the toggle's label.
"On" and "Off" are the state, and that is already communicated effectively in screen readers as "checked" or "not checked/unchecked" (JAWS&NVDA/VoiceOver).

The _label_ would be the string that says what the toggle is for, i.e. "Show preview" or "Enable autocorrect".

If we allow the screen reader to read the "On" or "Off", then we get the following, which are redundant and potentially even confusing (i.e. what does "Off not checked" mean? Does it mean "On"?):
- JAWS and NVDA:
  - On checkbox checked
  - Off checkbox not checked

- VoiceOver:
  - On, checked, checkbox
  - Off, unchecked, checkbox

So I think it would be best to keep the "On" and "Off" strings hidden from screen readers - do you agree?

@emyarod and @asudoh, please note: A Toggle should _always_ have a label - otherwise, how are users supposed to know what they are toggling? The label can be visible (preferred) or invisible (using either `aria-label` or `class="bx--assistive-text"`). It would be great if Carbon could promote labels more in the examples. :)
Hi @carmacleod, If the toggle only uses On/Off as a state and not a label, I agree that they can be hidden. But as you mentioned, there is still an issue with the component since the  [APG for a checkbox](https://www.w3.org/TR/wai-aria-practices-1.1/#checkbox) requires a label.
@dakahn Please add this issue to the IBM Carbon Copy Milestone. Thx!
ok so if I understand correctly:

* the on/off text is not a label and should not be a `label` element (and can be hidden)

* the current toggle example (see below) using `fieldset` and `legend` to label the toggle is not ideal and should be replaced with an actual `label`

```html
<!-- current toggle example with "label" -->
<fieldset class="bx--fieldset">
  <legend class="bx--label">Toggle w/ Label</legend>
  <div class="bx--form-item">
    <input class="bx--toggle" id="toggle2" type="checkbox">
    <label class="bx--toggle__label" for="toggle2">
      <span class="bx--toggle__text--left">Off</span>
      <span class="bx--toggle__appearance"></span>
      <span class="bx--toggle__text--right">On</span>
    </label>
  </div>
</fieldset>
```

is that right?
@emyarod Yes, that is correct. The legend is used for a group of controls to highlight common attributes of all controls, for example, to advise that all fields in the group are required. Then as shown in the APG each toggle must have an associated label. Also see additional information on [Grouping Controls](https://www.w3.org/WAI/tutorials/forms/grouping/). 
In case it's helpful, Scott O'Hara has some decent accessible switch (aka toggle) examples here: https://scottaohara.github.io/aria-switch-control/

Looks like he was playing around with using different html elements - there's a couple that are implemented with button, one with div, one with anchor, and the last one "Enable something" uses a checkbox input inside an html label.

See also: https://scottaohara.github.io/a11y_styled_form_controls/src/checkbox--switch/