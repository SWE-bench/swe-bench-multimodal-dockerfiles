- And in a case like `m#/$#` how would one escape a literal `#` in the regex?
- Are there limitations on which characters may follow `m` to denote a regex "enclosure"?
- If not are certain character more common by convention?
This is valid Perl code.
```
use 5.010;
my $test = qq"test";
if ($test =~ m#test#) {
	say "m#test#: ", 1;
}
if ($test =~ m.test.) {
	say "m.test.: ", 1;
}
if ($test =~ m+test+) {
	say "m+test+: ", 1;
}
```

> Are there limitations on which characters may follow m to denote a regex "enclosure"?

//EDIT:
I do not know the BNF of Perl.
I guess all non-apphanum cars and brackets <>(){}[]!! and so on.
https://perldoc.perl.org/perlre#The-Basics
https://perldoc.perl.org/perlop#Gory-details-of-parsing-quoted-constructs
Ok. But in a case like m#...# how would one escape a literal # inside the regex?  Or is that not possible?

In a normal regex evidently a backslash escape may be used (assuming our grammar is correct):

```
/\//
```

So how do I write:

```
m###
```

Where the inside # is part of the regex?
> Ok. But in a case like m#...# how would one escape a literal # inside the regex? Or is that not possible?

Ok, in this case i guess `m#\##`
That would be simple enough.  Could you confirm your guess?
Regular case is to escape the opening or closing char if part of a regex.

I will come back the next days if i know more on special syntax of Perl quoting.
> When searching for single-character delimiters, escaped delimiters and \\ are skipped. For example, while searching for terminating /, combinations of \\ and \/ are skipped. If the delimiters are bracketing, nested pairs are also skipped. For example, while searching for a closing ] paired with the opening [, combinations of \\, \], and \[ are all skipped, and nested [ and ] are skipped as well. _However, when backslashes are used as the delimiters (like qq\\ and tr\\\), nothing is skipped. During the search for the end, backslashes that escape delimiters or other backslashes are removed (exactly speaking, they are not copied to the safe location)._

I was following this right up until the end. What is the last part trying to say?  I thought I was following along with "skipped" until they said "nothing is skipped" and then changed to using "removed".
The last sentence describes a separate process, and the sentence before that is a special case:  If you use `\` as a delimiter, then you can't escape characters with `\`. The first occurrence of `\` terminates the construct, since `\\` is not "skipped" (so, contradicting the claim of the first sentence, which explains the "However").
The last sentence can be best explained with an example:
```print ('qwertz' =~ s z\zzyzr) # prints 'querty' ```
The delimiter is `z`.  The search string contains an escaped delimiter `\z` which is skipped while searching for the end (as written in the first sentence).  The last sentence says that the `\` is removed before this escaped delimiter, so that the search string actually is a literal `z` and not an end-of-string assertion `\z` (I actually have some doubts that backslashes that escape other backslashes are removed in that step, but don't want to dig deeper since this shouldn't be relevant for syntax highlighting).

On using `#` as a delimiter:
> That would be simple enough. Could you confirm your guess?

Indeed, `m#\##` works as intended to escape a literal `#`.
However, `#` has another quirk (and I don't recommend its use as delimiter): while `m#\##` is a valid pattern match, `m #\##` is a lonely `m` followed by the comment `\##`.

Here's a compilation of some common and some annoying Perl delimiters.  Perl's substitution s/a/b/ is challenging because it allows for an odd number of delimiters, in particular with quotes as delimiters.  GitHub's highlighting seems to get almost all of them right:

```perl
use 5.020;
use strict;
use warnings;

sub saeaoagr () {
    print "foo";
    qr/x/;
}

# Those are the most popular
say ("fee" =~ s/e/o/gr  . "bar");
say ("fee" =~ s!e!o!gr  . "bar");
say ("fee" =~ s|e|o|gr  . "bar");
say ("fee" =~ s{e}{o}gr . "bar");
say ("fee" =~ s(e)(o)gr . "bar");
say ("fee" =~ s[e][o]gr . "bar");

# Those have syntactic significance
say ("fee" =~ s?e?o?gr  . "bar");
say ("fee" =~ s'e'o'gr  . "bar");  # ' # quote to fix

# Those are valid, but infrequent (and weird)
say ("fee" =~ s"e"o"gr  . "bar");  # " # quote to fix
say ("fee" =~ s aeaoagr . "bar");
say ("fee" =~ s#e#o#gr  . "bar");

# Those must not be confused with the previous two
say ("fee" =~ saeaoagr  . "bar");  # calls saeaoagr()
say ("fee" =~ s #e#o#gr              that's a comment, not a regex
     (e)(o)gr . "bar");            # and here's the regex.

```
Are are all those delimiters valid for all regex "types"/operations (not sure what to call them)?

`s`, `tr`, `y`, `m`, `qr` ?

Yes, they are.  Perl calls the whole lot ["Quote and Quote-like operators"](https://perldoc.perl.org/perlop#Quote-and-Quote-like-Operators).