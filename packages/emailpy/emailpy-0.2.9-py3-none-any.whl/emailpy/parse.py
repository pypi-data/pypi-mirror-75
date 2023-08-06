import re

PATTERNS = {'ZOOM': ('Please join Zoom meeting in progress',
                     r'''Join Zoom Meeting\s*
((http|https)://(\w+.)?zoom.us/j/\d{10}(\?pwd=\w+)?)\s*
\s*
Meeting ID: (\d{3} \d{3} \d{4}\s*)
Password: (.*)\s*''')}

COMPILED = {key: (re.compile(value[0]), re.compile(value[1]))
            for key, value in PATTERNS.items()}

class MATCHER:
    def __init__(self, name, cmps):
        self.name = name
        self.subcmp = cmps[0]
        self.bodycmp = cmps[1]
        
    def __call__(self, eml):
        sub = self.subcmp.findall(eml.subject)
        body = self.bodycmp.findall(eml.body)
        if (not sub) or (not body):
            return
        return sub[0], body[0]

    def __repr__(self):
        return 'MATCHER(%s)'%self.name

class NAME:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if type(other) == NAME:
            return self.name == other.name
        if type(other) == str:
            return self.name == other
        if type(other) == bytes:
            return self.name.encode() == other

    def __hash__(self):
        return hash(repr(ord(self.name[0])))

    def __repr__(self):
        return self.name

class MATCHERDICT(dict):
    def __repr__(self):
        return 'MATCHERDICT(%s)'%dict(self.items())
        
for name in PATTERNS.keys():
    globals()[name] = NAME(name)

MATCHERS = MATCHERDICT({NAME(name): MATCHER(name, cmps) for name, cmps in \
            COMPILED.items()})

del PATTERNS
del COMPILED
