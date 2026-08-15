Previous Prettier version formatted it with a space after first `:` which is also inconsistent with Angular docs. How do you propose to have a discussion? [Angular style guide](https://angular.io/guide/styleguide) has nothing on the matter, [angular.io](https://angular.io) has plenty of examples that go against prettier formatting, so does angular source code:
```html
{{ model | json }}
<div class="form-group">
  <label for="name">Name</label>
  <input type="text" class="form-control" id="name"
         required
         [(ngModel)]="model.name" name="name">
</div>

<div class="form-group">
  <label for="alterEgo">Alter Ego</label>
  <input type="text"  class="form-control" id="alterEgo"
         [(ngModel)]="model.alterEgo" name="alterEgo">
</div>

<div class="form-group">
  <label for="power">Hero Power</label>
  <select class="form-control"  id="power"
          required
          [(ngModel)]="model.power" name="power">
    <option *ngFor="let pow of powers" [value]="pow">{{pow}}</option>
  </select>
</div>
```
There are a couple of cases with spaces in the docs, but majority indeed use no spaces at all. I have never heard of the standard or official code style regarding this though. Angular repository `Discussions` section is read-only and dedicated to RFCs only. I have created a tweet poll and will ask my friends to help with more reach:
https://twitter.com/Waterplea/status/1595441003325964290
So I've managed to get a little over 500 votes on the matter, with help of other Angular devs retweets. The distribution pretty much settled around 60/40 in favor of current formatting rather early on and fluctuated around 1%, so I believe it should be fair to extrapolate the result as indicative of general public opinion.
Just updated to latest prettier version and was shocked. 
I instantly thought it looks like the result part of a conditional ternary operator. And not like key - value(s)/argument(s) anymore.

Wouldn't it be a possibility to be able to turn this off via config?
Would be the easiest fix IMO for this minor version.


What I would add to the discussion featurewise:

Our preferred approach looks like this: 

```
{{ (user$ | async).credit | currency: 'CAD' : 'symbol-narrow' : '4.2-2' }}
{{ (user$ | async).items | slice: 1 : 5 }}
```

So basically, the first value after the pipe (pipe name) does NOT have a space between itself and the colon at all times, but after that, there are spaces between the arguments.

Previously mentioned survey was comparing new format with Angular documentation format. We can probably try running one more, comparing different proposed formats. So far 4 formats were proposed:

1. Angular docs one: `value | pipe:arg1:arg2`
2. Old prettier: `value | pipe: arg1:arg2`
3. New prettier: `value | pipe : arg1 : arg2`
4. Alternative: `value | pipe: arg1 : arg2`

@nseni @sosukesuzuki @nedecoTHo @pedroestabruxelles @fisker would that be a way forward you agree upon? Anything else to add, any other idea?
If you take `translate` or `date` pipe as an example, it looks much better the old way:

`'translation.key' | translate: { group: organization.name }`
`lastYearDate | date: DateFormat.shortDate`


So I would vote for option 2.
I can accept options two and four but not options one and three.
Same here, as @HyperLife1119 said I like options two and four. Thanks for asking!
I prefer 2 as default, 4 as optional.
I prefer 1 or 2. I vote for reverting this change which has caused confusion across multiple projects for my teams.
I have created another poll with all proposed options, sorted by the amount of spaces they use. If this question is important to you, please cast your vote and help with reach:
https://twitter.com/Waterplea/status/1615568765747597313
The poll has ended. 421 people voted.
![image](https://user-images.githubusercontent.com/47851128/214026996-e686b8ad-efa4-4af7-9125-66b754051359.png)

It's interesting that the "Old prettier" formatting has the least votes, so a change to formatting is indeed needed.
Note that majority (68,9%) voted not in favor of the new formatting. But option "Angular docs" has won only by a small margin. So it's not conclusive. I don't know, could the "Alternative" formatting become a compromise? Or simply accept the poll results and implement the option with the most votes.
I wouldn't say a vote on twitter is more representative than a github issue created in response to a certain change.
Anybody could vote (except the people without a twitter account btw).
But only people that really care about this issue would go and create a github issue or write comments in one in favor of something.

The ability to configure the behavior ourselves would surely be the most flexible option though.
> I wouldn't say a vote on twitter is more representative

I'd agree with this, especially after a significant exodus or at least the deactivation of many people's Twitter accounts due to Elon.

Either way, there's significant feedback that the recently implemented formatting is not desirable.
Well, it's up to maintainers and community at this point, but I think I'll add my reasoning behind spaces and why initially we asked for this change.

Prettier generally introduces spaces because it's easier to read. Typical changes done by default config prettier:

`import {Item} from 'package'` -> `import { Item } from 'package'`
`Value {{interpolation}}` -> `Value {{ interpolation }}`
`type Type = 'union'|'type'` -> `type Type = 'union' | 'type'`
`array = [1,2,3,4]` -> `array = [1, 2, 3, 4]`
`func(arg1,arg2)` -> `func(arg1, arg2)`
`arg1+arg2` -> `arg1 + arg2`
`ternary?operator:usage` -> `ternary ? operator : usage`
`value||'fallback'` -> `value || 'fallback'`

And many many more. It's arguably much harder to find a case where prettier **removes** spaces. It feels like it **always** introduces spaces around individual entities, except in cases of commas with space only _after_ the comma, because that's how we use commas to list multiple items in real life.

I get the idea for `arg1: arg2: arg3` of using space only after `:`, because that's how we typically use it in general writing, like `,` in array. But I'd argue that it's not really a semicolon semantically in that case but rather just a divider, akin to `|` in union types.

I also don't understand the backlash. How come `1.5` is one value, but `1:5` is passing two values to the pipe? It's additional cognitive strain to have the need to keep in mind what symbol breaks value in two values and what is a valid part of a single value. Especially considering that natively many countries use `,` to separate decimal part. It's way easier to determine individual arguments with spaces around the separator. 

You really prefer this:
`value | pipeName:'string_value':1.2:value`
over this:
`value | pipeName : 'string_value' : 1.2 : value`
?

If I understood correctly, no one in this thread really prefers this:
`value | pipeName:'string_value':1.2:value`
over this:
`value | pipeName : 'string_value' : 1.2 : value`

This twitter poll got that back into discussion, but I upvoted @ilyakonrad in this regard because IMO he is right.

After getting a bit more used to the new "all spaces in pipes" approach, I would still prefer the 4th option, but am also fine with the 3rd (from your post above, quoted below).

If easily possible, I would prefer the 3rd format as a new standard and the 4th one as an easily configurable alternative.

> Previously mentioned survey was comparing new format with Angular documentation format. We can probably try running one more, comparing different proposed formats. So far 4 formats were proposed:
> 
> 1. Angular docs one: `value | pipe:arg1:arg2`
> 2. Old prettier: `value | pipe: arg1:arg2`
> 3. New prettier: `value | pipe : arg1 : arg2`
> 4. Alternative: `value | pipe: arg1 : arg2`

Yeah, 4th option is a fine one too, because it highlights that pipe name differs from the arguments and it's kind of semantic use of `:` as in `feed these arguments to the pipe in use`. If that change satisfies people who are unhappy with added spaces, I'm all for it.
Just updated prettier and this came up as a big change. I would prefer any of the options that doesn't have a space after the pipe name for the same reason you don't want to see json look like `{ key : value }`. More spaces doesn't make more readable.
The twitter poll agrees because 68.9% of people picked an option without that.
Can someone please make a final decision on this formatting issue? This thread has been open for 4 months and I'm hesitant about reformatting all our solutions if another one comes along that modifies it again.

Personally, I don't care what it looks like, that's why I use prettier. But please pick one and stick to it.
@fisker @sosukesuzuki looks like `value | pipeName: arg1 : arg2` is the most welcomed format, i.e. we only need to remove space after pipe name.
I started working on the code change for this and the issue becomes a lot more complex with a short print width (or long pipe arguments)
```typescript
//option 1A
{{
  birthdate
    | date:
      "longDate"
}}
```
or 
```typescript
//option 1B
{{
  .birthdate
    | date
      : "longDate"
}}
```
?

Then theres
```typescript
//option 2A
{{
  price
    | currency:
      "USD"
      : true
}}
```
vs
```typescript
//option 2B
{{
  price
    | currency
      : "USD"
      : true
}}
```

I think the second one looks nicer, but it breaks the consensus here about "no space after pipe name".

Also, we probably also want an exception for multiline objects or arrays so:
```typescript
//option 3A
{{
  value
    | pipeA: {
        keyA: reallySuperLongValue,
        keyB: shortValue
      } : {
        keyA: reallySuperLongValue,
        keyB: shortValue
      }
}}
```
instead of 
```typescript
//option 3B
{{
  value
    | pipeA:
        {
          keyA: reallySuperLongValue,
          keyB: shortValue
        }
      : {
          keyA: reallySuperLongValue,
          keyB: shortValue
        }
}}
```

Personally I think we go option A across the board here. even though in the second one it is less aesthetic.
Are there any actions taking place? It's been open for 5 months and Prettier keeps introducing unnecessary changes to the code.
I would love to see this change to be changed or opinionated in order to use pipes like seen in the angular docs and code.

I also assumed that you would do more research on your changes, not just a twitter poll in your own bubble, as in the end, if your research wasn't good, it's up to the developer to explain why we still should keep prettier for now ,even if the chosen path isn't what the team wants to see right now. It went down to a may be we change next year to something more predicable, but I hope this will change.