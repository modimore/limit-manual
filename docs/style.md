## Coding Style

In order to keep files, especially in the same language, looking consistent, some style rules generally govern the project.

Language-specific exceptions, or concerns that are only important for one language will be covered in their individual sections. If something is not covered, default to what you think would be best for the language in question.

General rules are listed here.

- Indentation width: 2 spaces

#### Python
- Indentation width: 4 spaces

#### Jinja2/HTML

Jinja2 control tags and HTML tags are both indented as shown below.

```html
{% tag %}
  <tag>...</tag>
{% endtag %}
```

This contrasts what is done in the Jinja2 documentation:

```html
{% tag %}
<tag>...</tag>
{% endtag %}
```

#### SCSS
When nesting rules, put new lines between different items as you would at the top level. For example:

```scss
table {
  color: blue;

  thead {
    tr { color: red; }
  }

  tbody {
    tr { color: green; }
  }
}
```
