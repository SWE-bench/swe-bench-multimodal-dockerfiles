@carbon-design-system/design thoughts about adding a stroke to the content switcher so it meets WCAG contrast requirements? 
Version 4 and 5 make sense to me. @jeanservaas @aagonzales can we see those in context of some UIs and confirm which of the designs are preferred 
Thanks for this @mbgower. 
> Thanks for this @mbgower.

No problem, @mjabbink. As noted at the end of my admittedly _long_ issue:
> I recommend that a similar assessment of other Carbon components be carried out (using the procedure of stripping out low-contrast visual features) to determine which visual elements need increased contrast in order for each component to pass 1.4.11 Non-text contrast.


I'm going to add this to our sprint backlog to look at in a future sprint. Stay tuned for an answer.
I'm wondering if there's a middle ground here versus changing all the switchers in every context. Here are my thoughts.

### Increase divider contrast
> As stated, a case can be made that neither treatment 4 or 5 is required to meet 1.4.11 for this component; however, a better-contrasted divider may be more understandable by some users

I think in the case where there are 3 or more section in the content switcher then an increased contrast divider should resolve the contrast. The last item doesn't have a divider on the outside so that could be a potential problem area. *A two section switcher would not be allowed in this style.*

![image](https://user-images.githubusercontent.com/11670886/109531163-8f660900-7a85-11eb-8ea9-20249cdb4020.png)


This is a pretty common style in tabs I've been seeing, like in chrome here
![image](https://user-images.githubusercontent.com/11670886/109531019-6180c480-7a85-11eb-90a5-f4cacb1d8d8f.png)


### G20 background color
We can also look at making the background of the non-selected sections darker to gray 20. This will match what we do in our container tabs, however that background still won't pass 3:1 on its own (we'd have to go up to G50 for that). It could help a little with better contrast though. 

![image](https://user-images.githubusercontent.com/11670886/109532187-dd2f4100-7a86-11eb-8480-58f4afdd9b9b.png)


### Adding a new variant
Next I think we could add in a new variant with the outline. I think this could be a good style to have either way and this would be the required style if you only had two sections. 

Note: I think we'd want to keep the shorted divider that doesn't span the full height here.

![image](https://user-images.githubusercontent.com/11670886/109532795-7c543880-7a87-11eb-902e-4021bcb2d498.png)


## In context examples

**Option 4**: Outline + background fill

![1](https://user-images.githubusercontent.com/11670886/109538688-6433e780-7a8e-11eb-967a-fce244116149.png)

**Option 5: Outline**

![2](https://user-images.githubusercontent.com/11670886/109538694-65651480-7a8e-11eb-96b8-470a083cc2a9.png)

**As-is with 3:1 divider for 3 or more sections**

![3](https://user-images.githubusercontent.com/11670886/109538698-65fdab00-7a8e-11eb-82dc-76cf9ac9429d.png)

**G20 background with 3:1 divider**

![4](https://user-images.githubusercontent.com/11670886/109538700-65fdab00-7a8e-11eb-998c-f8fb4e5af2c5.png)

I’m partial to as-is with 3:1 divider and option 5 outline
@aagonzales Option 5 works well to compliment the button switcher on the far right
<img width="825" alt="Screen Shot 2021-03-01 at 3 45 54 PM" src="https://user-images.githubusercontent.com/32881239/109563370-49b93880-7aa5-11eb-9667-c451dbb3cb69.png">

@mjabbink so do you think we should darken the divider of the as-is _and_ also add in a new variant for option 5? 
@aagonzales I think we should have one but I mentioned a second choice (5). That said though I leave the choice as 5 as variant to you and Jeannie 
Here is the spec for the updated content switcher that will pass 3:1 contrast. The default content switcher style is to be updated. This will not be a new version.

![Content Switcher_White Theme](https://user-images.githubusercontent.com/11670886/111193522-9ebe7980-8590-11eb-845d-c78146ca2feb.png)

is the unselected background-color supposed to be transparent or `ui-01`? similarly for disabled, should it be `disabled-01`?
@emyarod  The background color for an unselected section and unselected-disabled section should be `transparent`.