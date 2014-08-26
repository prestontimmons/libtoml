# libtoml

A Python <a href="https://github.com/toml-lang/toml">toml</a> parser.
Mostly an experiment to learn the <a href="https://github.com/alex/rply">rply</a>
library.

Parses everything except arrays of tables. Instead, you can just do this:

```
products = [
    {"name": "Book", "price": "6.50", },
    {"name": "Bell", "price": "0.50"}, # trailing comma, no problem
]
```

Python dictionary syntax can be used for variables as well:

```
x = { 1: 2, 3.0: "0.50" }
y = { 
    "hello": "world",
}
```
