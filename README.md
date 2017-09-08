# Regex String To API

Converts regex pattern from a string into an API that can be used in a regex compiler.

This is my code from a challenge problem in Udacity's [Design of Computer Programs](https://www.udacity.com/course/design-of-computer-programs--cs212) 
to help learn how a parsing expression grammar works (https://en.wikipedia.org/wiki/Parsing_expression_grammar).

`regrammar.py` contains my code.

`REGRAMMAR` contains the grammar rules which the `parse()` function uses to parse to parse a regex pattern string.

`convert()` takes the tree output from `parse()` and converts it into a string containing functions that can be used by a regex compiler.

This is based upon code from Unit 3 which you can view here: https://www.udacity.com/wiki/cs212/unit-3-code


