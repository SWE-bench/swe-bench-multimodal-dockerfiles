So are naked regex (`/blah/` without any type of sigil, etc)) even allowed in Elixir?  We seem to allow for that (which causes this problem) but I can't find any docs showing that in actual usage.

I also find the `%r` variant in addition to `~r` but can't find much on that... can anyone clear this up a bit?
`regex` is basically a type of sigil

See:
 - https://elixir-lang.org/getting-started/sigils.html#regular-expressions
 - https://elixirschool.com/en/lessons/basics/sigils/
> So are naked regex (`/blah/` without any type of sigil, etc)) even allowed in Elixir? 

No, that's not a thing in Elixir.

What @ynfle said. The most common way of writing a regex literal in Elixir is the regex sigil.

`~` starts a sigil. The type of the sigil follows, which is a single letter (upper or lower case), e.g. `~r` for regular expressions, `~s` for strings, `~w` for lists of strings etc. Each sigil can use any of the 8 different allowed delimiters:

```elixir
~r/hello/
~r|hello|
~r"hello"
~r'hello'
~r(hello)
~r[hello]
~r{hello}
~r<hello>
```

On top of that, sigils can have modifiers (letters) after the closing delimiter, e.g. `~r|hello|i` is a case-insensitive regex.

> I also find the %r variant in addition to ~r but can't find much on that... can anyone clear this up a bit?

`%r` does not start regex sigil. On its own, it's not even a valid expression. The only usage of `%` that comes into my mind is to either define or pattern-match maps and structs. `Regex` is a struct, so you technically you could define it like this: `%Regex{source: "hello", opts: "i"}` (equals `~r/hello/i`) but that's super rare. The only usage of `%` followed by a lowercase letter would be to pattern-match a struct name, e.g. 

```elixir
iex(9)> %r{} = ~U[2020-03-02 12:40:00Z]
~U[2020-03-02 12:40:00Z]
iex(10)> r
DateTime
```

(That's an example of a yet another sigil, one that creates a DateTime struct)

Unlike sigils, the only valid delimiter for maps and structs is `{}`.
@angelikatyborska Thanks for all the detail.  We have two variants now: (in additional to sigils, which are counted as strings)

```js
        variants: [
            {
              begin: '/',
              end: '/[a-z]*'
            },
            {
              begin: '%r\\[',
              end: '\\][a-z]*'
            }
```

- naked `/regex/`
- `%r[regex]`

It seems that both of these are either outdated or simply wrong (and of course overly broad with modifiers)... our Elixir grammar could really use some love.  I'll rip these out then and we'll simplify.