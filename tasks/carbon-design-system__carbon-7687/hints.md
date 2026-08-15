thoughts?
<img width="656" alt="Screen Shot 2020-03-09 at 11 40 45 AM" src="https://user-images.githubusercontent.com/43969356/76236546-d87cd780-61fa-11ea-86bf-4711773557fa.png">

Also ones still using carets:
<img width="601" alt="Screen Shot 2020-03-09 at 11 41 37 AM" src="https://user-images.githubusercontent.com/43969356/76236621-f6e2d300-61fa-11ea-9d61-d071f9e92f97.png">

I like A B C
- I think the `+` and `-` read better than the chevron icons which are normally used for opening/closing things.
- I can't actually decided between A and C if the full lines or half line is better.
- I like B because it seems like a more natural order for the control. 
Yeah the chevron one could be confusing. I think B is nice visually. But now wondering where error state icon would go. could work better for A or C. 
![sm-320px-4 column](https://user-images.githubusercontent.com/43969356/76261018-12fc6980-6227-11ea-8b3c-d9d009bce96f.png)


Would this just make the mobile version the default? It would be a pretty easy change if we decide to go to B (would just need to change the icons and extend the border, possibly other things my dev eyes are missing)

Current mobile version: 
<img width="205" alt="Screen Shot 2020-03-09 at 1 33 30 PM" src="https://user-images.githubusercontent.com/11928039/76255001-a70c0800-620a-11ea-8c37-94f026764c82.png">


Yeah I was wondering about that too. ^^ I notice the mobile version also does not include the invalid icon. Wasn't sure where to put that other than outside of the field. Looked wonky inside or attached on the outside.


Yeah I agree, we could always render the error icon next to the error text 🤷‍♂ 
![Screen Shot 2020-03-10 at 10 32 48 AM](https://user-images.githubusercontent.com/43969356/76329394-83a09600-62ba-11ea-9380-11e4bcfa0eee.png)


The input alignment could get weird with B if in a form if we want it to have some sort of text alignment. We would prob have to center the input text, and even if we left aligned it, it would never really align with anything because there is a button on the left. 

Kind of thinking C is the best option with full rule lines and is less fussy than A with the shorter rules. (however i know the fluid inputs have a smaller rule because the label is in the field)

--------------------------------------------------------------------------------------------------

Also this is Petes mobile number input for reference:
<img width="779" alt="Screen Shot 2020-03-10 at 11 09 17 AM" src="https://user-images.githubusercontent.com/43969356/76333556-d2046380-62bf-11ea-9096-f65791e22604.png">

Makes sense to me 👍 
## Final design

![Number input (fixed) - White theme.png](https://images.zenhubusercontent.com/5bbba771387e41362246f3dc/dfcf736c-3bd3-469a-8ade-693960e4dad0)

--------------------------------------------------------------------------------------------------------

## Final spec
![Number input (fixed) — Specs.png](https://images.zenhubusercontent.com/5bbba771387e41362246f3dc/e5c58c57-a2e0-49a4-881e-78b2f5835f16)