import re

from sphinx_markdown_tables import __version__

rst = ''

def get_str_len(in_str):
    str_len = 0
    for s in in_str:
        if s >= '\u4e00' and s <= '\u9fff':
            str_len += 2
        elif s >= '\uff00' and s <= '\uffef':
            str_len += 2
        else:
            str_len += 1
    return str_len

def create_rst_line(length, flag = '-'):
    global rst
    line = "+"
    for i in length:
        line += flag * (i + 2) + "+"
    rst += line + '\n'

def create_rst_body(data, length):
    global rst
    msg = '|'
    for i in range(len(data)):
        print(i)
        sub = length[i] - get_str_len(data[i])
        msg += ' ' + data[i] + ' '*sub +  ' |'
    rst += msg + '\n'
    create_rst_line(length, flag = '-')

def create_rst_title(data, length):
    global rst
    create_rst_line(length)
    msg = '|'
    for i in range(len(data)):
        sub = length[i] - get_str_len(data[i])
        msg += ' ' + data[i] + ' '*sub +  ' |'
    rst += msg + '\n'
    create_rst_line(length, flag = '=')

def create_rst_table(data):
    global rst
    length = data[0]
    create_rst_title(data[1], length)
    for i in data[2:]:
        create_rst_body(i, length)

tex = ''

def create_tex_tail():
    global tex
    tex += '\\end{tabulary}\n' + \
           '\\par\n' + \
           '\\sphinxattableend\\end{savenotes}\n'

def create_tex_body(data):
    global tex
    tex += data[0] + '\n'
    for i in data[1:]:
        tex += '&\n' + i + '\n'
    #tex += '\n' + '\\hline\n'
    #tex += '\n'
    tex += '\\\\%\n' + '\\hline\n'

def create_tex_title(data):
    global tex
    tex += '\\begin{savenotes}\\sphinxattablestart\n' + \
           '\\centering\n' + \
           '\\begin{tabulary}{\\linewidth}[t]{|T|T|T|T|T|T|}\n' + \
           '\\hline\n'
    tex += '\\sphinxstyletheadfamily\n' + data[0] + '\n'
    for i in data[1:]:
        tex += '&\\sphinxstyletheadfamily\n' + i + '\n'
    tex += '\\\\%\n' + '\\hline\n'

def create_tex_table(data):
    create_tex_title(data[1])
    for i in data[2:]:
        create_tex_body(i)
    create_tex_tail()


def setup(app):
    app.connect('source-read', process_tables)
    return {'version': __version__,
            'parallel_read_safe': True}


def process_tables(app, docname, source):
    """
    Convert markdown tables to html, since recommonmark can't. This requires 3 steps:
        Snip out table sections from the markdown
        Convert them to html
        Replace the old markdown table with an html table

    This function is called by sphinx for each document. `source` is a 1-item list. To update the document, replace
    element 0 in `source`.
    """
    global rst
    global tex
    import markdown
    md = markdown.Markdown(extensions=['markdown.extensions.tables'])
    table_processor = markdown.extensions.tables.TableProcessor(md.parser)

    raw_markdown = source[0]
    blocks = re.split(r'(\n{2,})', raw_markdown)

    for i, block in enumerate(blocks):
        if table_processor.test(None, block):
            data = get_table_msg(block)
            #create_rst_table(data)
            create_tex_table(data)
            blocks[i] = tex
            #with open('debug.tex', 'w') as fd:
            #    fd.write(tex)
            #blocks[i] = rst
            #blocks[i] = 'hello'
            tex = ''
            rst = ''
            #html = md.convert(block)
            #styled = html.replace('<table>', '<table border="1" class="docutils">', 1)  # apply styling
            #blocks[i] = styled

    # re-assemble into markdown-with-tables-replaced
    # must replace element 0 for changes to persist
    source[0] = ''.join(blocks)


def get_table_msg(block):
    data = []
    start = 0
    lines = block.split('\n')
    for line in lines:
        if line.find(':-') >= 0 or line.find('-:') >= 0:
            continue
        if start == 1:
            tmp = line.strip('| \n').split('|')
            #tag = tmp[0].strip('[').split('](')[0]
            #link = tmp[0].strip(')').split('](')[1]
            #tmp[0] = "`" + tag + " <" + link + ">`__"
            for i in range(len(tmp)):
                print(tmp[i])
                #if tmp[i].find('](') >= 0:
                #    tag = tmp[i].strip('[').split('](')[0]
                #    tmp[i] = tag
                length = get_str_len(tmp[i]) 
                if length > data[0][i]:
                    data[0][i] = length
            data.append(tmp)
        if start == 0:
            start = 1
            num = []
            tmp = line.strip('| \n').split('|')
            for i in tmp:
                length = get_str_len(i)
                num.append(length)
            data.append(num)
            data.append(tmp)
    return data

