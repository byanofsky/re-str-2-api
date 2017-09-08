from grammar import grammar, parse

# Sets regular expression grammar
REGRAMMAR = grammar("""
RE => ALT | RE2
RE2 => SEQ | EXP
EXP => MOD | VAL
MOD => STAR | PLUS | OPT
ALT => RE2 \| RE
GRP => \( RE \)
SEQ => EXP RE2
VAL => GRP | LIT | DOT | EOL
LIT => [^()|?+*.$]
DOT => \.
EOL => \$
STAR => VAL \*
PLUS => VAL \+
OPT => VAL \?
""", whitespace='')


def parse_re(pattern):
    """Parses a regular expression pattern and returns a string in a format
    readable by a custom regex compiler.

    Parameters:
    pattern : a string regex pattern

    Returns:
    string : a string containing regex pattern converted into string of
        functions readable by regex compiler
    """
    return convert(parse('RE', pattern, REGRAMMAR)[0])


def convert(tree):
    """Converts output from PEG parser into regex compiler API code.

    Parameteres:
    tree : a list of lists containing that is the parsed regex pattern

    Returns:
    string : a string containing regex pattern converted into string of
        functions readable by regex compiler
    """
    root = tree[0]
    if root == 'LIT':
        return '{}({})'.format(root.lower(), tree[1])
    elif root in ['DOT', 'EOL']:
        return '{}()'.format(root.lower())
    elif root in ['STAR', 'PLUS', 'OPT']:
        return '{}({})'.format(root.lower(), convert(tree[1]))
    elif root == 'SEQ':
        return '{}({}, {})'.format(root.lower(),
                                   convert(tree[1]),
                                   convert(tree[2]))
    elif root == 'ALT':
        return '{}({}, {})'.format(root.lower(), convert(tree[1]),
                                   convert(tree[3]))
    elif root == 'GRP':
        return '{}({})'.format(root.lower(), convert(tree[2]))
    else:
        return convert(tree[1])


def test_convert():
    # On character patterns
    assert parse_re('a') == 'lit(a)'
    assert parse_re('.') == 'dot()'
    assert parse_re('$') == 'eol()'
    # Sequences
    assert parse_re('ab') == 'seq(lit(a), lit(b))'
    assert parse_re('abc') == 'seq(lit(a), seq(lit(b), lit(c)))'
    assert parse_re('abc$') == 'seq(lit(a), seq(lit(b), seq(lit(c), eol())))'
    # Modifiers
    assert parse_re('a?') == 'opt(lit(a))'
    assert parse_re('a?b+c*') == ('seq(opt(lit(a)), seq(plus(lit(b)), '
                                  'star(lit(c))))')
    # Alternatives
    assert parse_re('a|b') == 'alt(lit(a), lit(b))'
    assert parse_re('a|b|c') == 'alt(lit(a), alt(lit(b), lit(c)))'
    assert parse_re('a*|b|c?') == 'alt(star(lit(a)), alt(lit(b), opt(lit(c))))'
    # Groups
    assert parse_re('(a)') == 'grp(lit(a))'
    assert parse_re('(ab)') == 'grp(seq(lit(a), lit(b)))'
    assert parse_re('(a|b)') == 'grp(alt(lit(a), lit(b)))'
    assert parse_re('(a|b)?') == 'opt(grp(alt(lit(a), lit(b))))'

if __name__ == '__main__':
    test_convert()
    print('tests passed')
