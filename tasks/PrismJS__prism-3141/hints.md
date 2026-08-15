I'm not sure whether string is the correct token here. Aren't used as identifiers? Can you use backticks and double-quoted strings interchangeably?
In MySQL, they can not be interchanged with one another (Edit: They can be if a config value is set).

The following code:

```mysql
select * from 'Test'
```

Produces the following output (same with double quotes):

>ERROR 1064 (42000) at line 7: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''Test'' at line 1

**Note:** If the [ANSI_QUOTES](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_ansi_quotes) SQL mode is enabled, it is also permissible to quote identifiers within double quotation marks.
After a bit of googling: backtick-quoted strings are [used for identifiers](https://dev.mysql.com/doc/refman/8.0/en/identifiers.html). I'll add an identifier token.
That being done, even with an `identifier` token, it won't *look* much different.

![image](https://user-images.githubusercontent.com/20878432/136280164-a77933b1-3713-4977-97dc-3c6cd9189e36.png)

I would also argue that ticked identifiers shouldn't be highlighted as strings because they aren't strings, they are identifiers.