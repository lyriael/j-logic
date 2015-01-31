import pyparsing

proofConstant = pyparsing.Regex('[a-z][a-zA-z0-9]*')
proofConstant.setParseAction(lambda x: ('proofCon', x[0]))
termConstant = pyparsing.Regex('([A-W]|Z)[a-zA-Z0-9]*')
termConstant.setParseAction(lambda x: ('termCon', x[0]))
xVariable = pyparsing.Regex('X[0-9]*')
xVariable.setParseAction(lambda x: ('xVar', x[0]))
yVariable = pyparsing.Regex('Y[0-9]*')
yVariable.setParseAction(lambda x: ('yVar', x[0]))

operators = [('->', 2, pyparsing.opAssoc.LEFT, lambda x: ('->', x[0][0], x[0][2])),
             # ('!', 2, pyparsing.opAssoc.LEFT, lambda x: ('!', x[0][0], x[0][2])),
             # ('+', 2, pyparsing.opAssoc.LEFT, lambda x: ('+', x[0][0], x[0][2])),
             # ('*', 2, pyparsing.opAssoc.LEFT, lambda x: ('*', x[0][0], x[0][2])),
             (':', 1, pyparsing.opAssoc.RIGHT, lambda x: (':', x[0][0], x[0][2]))]

