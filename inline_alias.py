import fileinput
import re

num_registers = 16
special_registers = {'sp': 13, 'lr': 14, 'pc': 15}

regex_inline_alias = re.compile(r'\w+:\w+')
regex_unreq_all = re.compile(r'\s*\.unreq\s+all')
regex_register_num = re.compile(r'r\d+')

str_req = '    {0} .req {1}'
str_unreq = '    .unreq {0}'

def parse_register(name):
    name = name.lower()
    if regex_register_num.fullmatch(name):
        n = int(name[1:])
        if n >= num_registers:
            return None
        else:
            return n
    elif name in special_registers:
        return special_registers[name]
    else:
        return None

def strip_line_comments(line):
    line = line.strip()
    if line.startswith('#'):
        return ''
    return line.split('@')[0].strip()

def main():
    registers = [None] * num_registers
    for line in fileinput.input():
        line_stripped = strip_line_comments(line)
        inline_defs = regex_inline_alias.findall(line_stripped)
        for idef in inline_defs:
            alias, reg = idef.split(':')
            if idef == line_stripped:
                # definition only, delete the line
                line = ''
            else:
                line = line.replace(idef, alias, 1)
            if alias in registers:
                print(str_unreq.format(alias))
                registers[registers.index(alias)] = None
            regnum = parse_register(reg)
            if regnum is not None:
                if registers[regnum] is not None:
                    print(str_unreq.format(registers[regnum]))
                registers[regnum] = alias
            print(str_req.format(alias, reg))
        if regex_unreq_all.fullmatch(line_stripped):
            for alias in registers:
                if alias is not None:
                    print(str_unreq.format(alias))
            registers = [None] * num_registers
        else:
            print(line.strip('\n'))

if __name__ == "__main__":
    main()
