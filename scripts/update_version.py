def update_value(fname, lineNum, value):
    with open(fname) as f:
        data = f.readlines()
    line = data[lineNum]
    line = line.split('=')[0]
    space = (line[-1] == " ")
    line += ' ' * int(space) + '=' + ' ' * int(space) + '"' + value + '"\n'
    data[lineNum] = line
    with open(fname, 'w') as f:
        f.writelines(data)


def get_line_and_value(fname, keyName):
    with open(fname) as f:
        for i, line in enumerate(f):
            if keyName in line and '=' in line and not '#' in line:
                values = [int(j) for j in line.split('=')[-1].strip()[1:-1].split('.')]
                return i, values
    return None, None

TOML_PATH = "../pyproject.toml"
SPHINX_PATH = "../documentation/source/conf.py"

tomlLine, tomlVersion = get_line_and_value(TOML_PATH, "version")
sphinxLine, sphinxVersion = get_line_and_value(SPHINX_PATH, "release")

if tomlLine is None or sphinxLine is None or tomlVersion is None or sphinxVersion is None:
    exit()

resultVersion = max(tomlVersion, sphinxVersion)

if tomlVersion == sphinxVersion: # If version was NOT manually updated.
    for i in range(len(resultVersion)-1, -1, -1):
        if resultVersion[i] == 9 and i != 0:
            resultVersion[i] = 0
        else:
            resultVersion[i] += 1
            break
resultVersion = '.'.join(map(lambda x: str(x), resultVersion))

update_value(TOML_PATH, tomlLine, resultVersion)
update_value(SPHINX_PATH, sphinxLine, resultVersion)