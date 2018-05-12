import json

# Lets get dat config
configh = open('./modules/ftools/config.json', 'r')
config = json.loads(configh.read())
configh.close()

# Y u do dis python
true = True
false = False


def col(fg=0, bg=false, style=0):
    """white, red, green, yellow, blue, purple, blue, gray"""
    out = '\x1b['+str(style)+';3'+str(fg)
    if bg != false:
        out += ';4'+str(bg)+'m'
    else:
        out += 'm'
    return out


colend = '\x1b[0m'


def debug(stringing):
    if config['debug']:
        print(col(6)+' Debug: '+str(stringing)+colend)
        return true
    else:
        return false


def error(string):
    print(col(1, style=1)+' ERROR: '+string+colend)


def warn(string):
    print(col(3)+' Warning: '+string+colend)