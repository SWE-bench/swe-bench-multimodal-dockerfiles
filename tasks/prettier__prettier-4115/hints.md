Hi! Can you post a code snippet in https://prettier.io/playground and click on `Copy markdown` ?

You can enable in `Show options` -> `Debug` -> `show second format` to demonstrate things happen after subsequent formats
Ahh that makes more sense. Below is the copied markdown. 

**Prettier 1.11.1**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEBGAdAAkwZQgWzk3gGcZi4APGAGmIAsiBzCAQwBtMBLE4iTeqwBuRGIwEx8nGKwBG7IrLjsIAd0xQ4ZOABNMqrmK5QGPDQFd8SgE5YA6oxMAzCNfysYxppmiYSwogAFazgYTzhrfS52TkhYY3NRflYdPVYTYx0EcjhWMHpiLkJMAAdzEnovBlE5BUwnc2sxCMx0vQamxkiIc3IIJz8ATygwLAAdKAnsbAAeGXkiMHZWEhIAXjGQebrtuABaMmsuEt1NgD4p6bnrC5MrsTOAFS0YGYB6B8vZh8fauHfPndZh8bl9MHNZBAdINbtM4eCYKCgfC5jozgYYgC0WC4aizkosbD4cDEUTidcySiYGiyhVdIScfc0Q4EAzkbiQZTcaTGd80QAxVzuPpQNnEvlnHABMXigFIjkwSHQykAv5nEA0EAQEqeaAkZCgVjWaxqQJGhD6lDCCBcHQakArGDIJwcEhwTWyax5ADWoRwJTyXmQiMSmp0EDAztd7pAxjdTWCrCY7ij7DdmoAViRKAAhL1gX0wKWEAAyxjgqfTWt6ZRgACZg9ZQyAA9Z48gQO5rN7w6ooPaSkdYHZbWJkAAOAAMmsHEDddi9JQ7g60ERE9pCAEdzFwQonk6xKzG3fguI3myQvAoAIrmCDwI+a+YjnRjpB1p9e6JeADCBBTKBQNAFaauUcC-LIloummcAAL6wUAA)
```sh
--parser markdown
```

**Input:**
```markdown
1.  Some test text, the goal is to have the html table below nested within this number. When formating on save Prettier will continue to add an indent each time pushing the table further and further out of sync. 

    <table class="table table-striped">
    <tr>
    <th>Test</th>
    <th>Table</th>
    </tr>
    <tbody>
        <tr>
        <td>will</td>
        <td>be</td>
        </tr>
        <tr>
        <td>pushed</td>
        <td>When</td>
        </tr>
        <tr>
        <td>Format on</td>
        <td>Save</td>
        </tr>
    </tbody>
    </table>
```

**Output:**
```markdown
1.  Some test text, the goal is to have the html table below nested within this number. When formating on save Prettier will continue to add an indent each time pushing the table further and further out of sync.

    <table class="table table-striped">
<tr>
<th>Test</th>
<th>Table</th>
</tr>
<tbody>
    <tr>
    <td>will</td>
    <td>be</td>
    </tr>
    <tr>
    <td>pushed</td>
    <td>When</td>
    </tr>
    <tr>
    <td>Format on</td>
    <td>Save</td>
    </tr>
</tbody>
</table>

```

**Second Output:**
```markdown
1.  Some test text, the goal is to have the html table below nested within this number. When formating on save Prettier will continue to add an indent each time pushing the table further and further out of sync.

        <table class="table table-striped">

    <tr>
<th>Test</th>
<th>Table</th>
</tr>
<tbody>
    <tr>
    <td>will</td>
    <td>be</td>
    </tr>
    <tr>
    <td>pushed</td>
    <td>When</td>
    </tr>
    <tr>
    <td>Format on</td>
    <td>Save</td>
    </tr>
</tbody>
</table>

```
(🤖`@no-response` bot is cool 🍺)