Yes this is a violation but despite the options not being tabbable, they are still operable via arrow keys and are properly announced by screenreaders.

Based on a [conversation](https://ibm-studios.slack.com/archives/G01GCBCGTPV/p1675865500656539) with IBMa, Dropdown needs to be revised to be a [Select-Only Combobox](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/examples/combobox-select-only/).

This means the Dropdown would be `role=combobox`. If the listbox was pointed to by a combobox, this violation would no longer appear.