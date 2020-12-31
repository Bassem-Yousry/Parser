# --------------------------------------------Imports-------------------------------------------------------------------#
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox as t
from graphviz import *
import graphviz as s
import os

root = Tk()
root.geometry('600x600')
root.title('TINY-Language-Compiler')
# -------------------------------------------------VariablesDeclerations-----------------------------------------------#
global source
global CodeLines
global lines
global file_name
ReservedWord = ['read', 'if', 'then', 'else', 'end', 'repeat', 'until', 'write']

TOKENS = []
CodeLines = []
source = []
lines = []

global root1
# global TStat
global SCAN
TinyLang = True
SCAN = False


class State:
    def __init__(self, data):
        self.children = []
        # super(Node, self).__init__()
        self.data = data

    def insert(self, data, baba):  # Compare the new value with the parent node
        if self.data == baba:
            self.children.append(State(data))
            return
        else:
            for l in self.children:
                l.insert(data, baba)

    def Print(self):
        StatList = []
        print('Node--->', self.data)
        if self.children:
            for l in range(len(self.children)):
                StatList.append(str(self.children[l].data))
            for l in self.children:
                l.Print()

    def CheckTiny(self):
        global TinyLang
        if self.children:
            for l in range(len(self.children) - 1):
                if 'if' in self.children[l].data['line'] or 'else' in self.children[l].data['line'] or 'repeat' in \
                        self.children[l].data['line']:
                    continue
                if not (';' in self.children[l].data['line']):
                    errormessage('statements are not accepted by TINY language')
                    TinyLang = False
                    return
            if ';' in self.children[-1].data['line']:
                errormessage('statements are not accepted by TINY language')
                TinyLang = False
            for l in self.children:
                if not TinyLang: return
                l.CheckTiny()


# ------------------------------------Show Errors-----------------------------------------------------------------------#
def errormessage(str, event=None):
    t.showerror("Error", str)


def infomessage(str, event=None):
    t.showinfo("Info", str)


# --------------------------------------------------------------------------------------------------------------------

def drawer():  # this is the parser code
    global SCAN
    if not SCAN:
        infomessage('Click SCAN First')
        return
    SCAN = False

    class Node:
        def __init__(self, data):
            self.children = []
            # super(Node, self).__init__()
            self.data = data
            self.graph = Graph(filename='rank_same.gv', format='png')
            self.graph.attr(overlap='false', splines='true')

        def insert(self, data, baba):  # Compare the new value with the parent node
            if self.data == baba:
                self.children.append(Node(data))
                return
            else:
                for l in self.children:
                    l.insert(data, baba)

        def PrintTree(self):
            lop = []
            # print('Node--->',self.data)
            if self.children:
                for l in range(len(self.children)):
                    lop.append(str(self.children[l].data['Token']))
                #   print('children->',"-".join(lop))
                for l in self.children:
                    l.PrintTree()

        def DrawTree(self):
            Shape = ['ID', 'op', 'else']
            if self.children:
                with  root1.graph.subgraph() as s:
                    s.attr(rank='same')
                    # create nodes
                    for l in range(len(self.children)):
                        sh = 'box'
                        if str(self.children[l].data['Type']) in Shape:
                            sh = 'ellipse'
                        s.attr('node', shape=sh)
                        if self.children[l].data['Token'] != 'else':
                            s.node(str(self.children[l].data['TokenNumber']), str(self.children[l].data['Token']))
                    #          print(self.children[l].data)
                    # draw edges
                    for l in range(len(self.children) - 1):
                        if not (self.children[l].data['Type'] in Shape) and not (
                                self.children[l + 1].data['Type'] in Shape):
                            s.edge(str(self.children[l].data['TokenNumber']),
                                   str(self.children[l + 1].data['TokenNumber']), constraint='false')
                if self.data['Token'] == '0':
                    pass
                elif self.data['Token'] == 'if':
                    root1.graph.edge(str(self.data['TokenNumber']), str(self.children[0].data['TokenNumber']))
                    root1.graph.edge(str(self.data['TokenNumber']), str(self.children[1].data['TokenNumber']))
                    for l in range(2, len(self.children)):
                        if (str(self.children[l].data['Token']) != 'else'):
                            root1.graph.edge(str(self.data['TokenNumber']), str(self.children[l].data['TokenNumber']),
                                             color='white', constraint='false')
                        else:
                            root1.graph.edge(str(self.data['TokenNumber']),
                                             str(self.children[l + 1].data['TokenNumber']), constraint='false')
                            break
                elif self.data['Type'] == 'op':
                    root1.graph.edge(str(self.data['TokenNumber']), str(self.children[0].data['TokenNumber']))
                    root1.graph.edge(str(self.data['TokenNumber']), str(self.children[1].data['TokenNumber']))
                elif self.data['Token'] == 'repeat':
                    root1.graph.edge(str(self.data['TokenNumber']), str(self.children[0].data['TokenNumber']))
                    for l in range(1, len(self.children) - 1):
                        root1.graph.edge(str(self.data['TokenNumber']), str(self.children[l].data['TokenNumber']),
                                         color='white')
                    root1.graph.edge(str(self.data['TokenNumber']), str(self.children[-1].data['TokenNumber']))
                elif 'assign' in self.data['Token']:
                    root1.graph.edge(str(self.data['TokenNumber']), str(self.children[0].data['TokenNumber']))
                elif 'write' in self.data['Token']:
                    root1.graph.edge(str(self.data['TokenNumber']), str(self.children[0].data['TokenNumber']))
                for l in self.children:
                    l.DrawTree()

        def DrawT(self):
            self.DrawTree()
            self.graph.view()

    try:
        stack = [{'Token': '0', 'TokenNumber': '0', 'TokenType': '0', 'Type': '0'}]
        List = []
        for a, i in enumerate(TOKENS):
            if i['Type'] == 'ID':
                dummy = 'id'
                if i['TokenType'] == 'NUMBER':
                    dummy = 'const'
                i['Token'] = dummy + '\n(' + i['Token'] + ')'
            i['TokenNumber'] = a
            List.append(i)

        root1 = Node({'Token': '0', 'TokenNumber': '0', 'TokenType': '0', 'Type': '0'})
        ID = 0
        Flag = False
        for n, o in enumerate(List):
            if List[n]['Token'] == 'read':
                id = List[n + 1]['Token']
                id = id[id.find('(') + 1:-1]
                s = o['Token'] + '\n(' + id + ')'
                o['Token'] = s
                List.pop(n + 1)
                root1.insert(o, stack[-1])
                stack.append(o)
            elif List[n]['Type'] == 'ID':
                ID = o
            elif List[n]['Token'] == 'else':
                if stack[-1]['Token'] == 'if':
                    root1.insert(o, stack[-1])
            elif List[n]['Token'] == 'repeat':
                root1.insert(o, stack[-1])
                stack.append(o)
            elif List[n]['Token'] == 'write':
                root1.insert(o, stack[-1])
                stack.append(o)
            elif List[n]['Token'] == 'then':
                if ID != 0:
                    root1.insert(ID, stack[-1])
                    ID = 0
                if stack[-1]['Token'] == '=' or stack[-1]['Token'] == ':=' or stack[-1]['Type'] == 'op': stack.pop(-1)
                continue
            elif List[n]['Token'] == ';':
                if ID != 0:
                    root1.insert(ID, stack[-1])
                    ID = 0
                # if stack[-1]['Token'] != '0' : stack.pop(-1)
                while stack[-1]['Type'] == 'op' or stack[-1]['Type'] == 'assign' or stack[-1]['Type'] == 'read' or \
                        stack[-1]['Type'] == 'write':
                    stack.pop(-1)
                if Flag:
                    if stack[-1]['Token'] == 'repeat': stack.pop(-1)
                    Flag = False
            elif List[n]['Token'] == 'if':
                root1.insert(o, stack[-1])
                stack.append(o)
            elif List[n]['Type'] == 'op':
                o['Token'] = 'op\n(' + o['Token'] + ')'
                root1.insert(o, stack[-1])
                stack.append(o)
                root1.insert(ID, stack[-1])
                ID = 0
            elif List[n]['Token'] == ':=':
                id = ID['Token']
                id = id[id.find('(') + 1:-1]
                s = o['Type']
                s += '\n(' + id + ')'
                o['Token'] = s
                root1.insert(o, stack[-1])
                stack.append(o)
                ID = 0
            elif List[n]['Token'] == 'until':
                Flag = True
                continue
            elif List[n]['Token'] == 'end':
                if stack[-1]['Token'] == 'if': stack.pop(-1)
        root1.DrawT()
    except:
        errormessage('Invalid input')


def Exit():
    root.destroy()


# -------------------------------------Print Side Numbers---------------------------------------------------------------#

def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')


def on_content_changed(event=None):
    update_line_numbers()


def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output


# ----------------------------------------Open FIle---------------------------------------------------------------------#


def open_file(event=None):
    global source
    global errors
    source = []
    i = 0
    file = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                              filetypes=[("All Files", "*.*"), ("TXT Files", "*.txt")])
    if file:
        text.delete(1.0, END)
        with open(file) as f:
            text.insert(1.0, f.read())
        with open(file, 'r') as f:
            source = f.read().splitlines()
    on_content_changed()


# -------------------------------------------Write In File--------------------------------------------------------------#
def write(file_name):
    try:
        content = errorText.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except:
        print(0)


# ------------------------------------------Save/Save As File-----------------------------------------------------------#
def save_as():
    global source
    file = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("All Files", "*.*"), ("TXT Files", "*.txt")])
    if file:
        global file_name
        file_name = file
        write(file_name)
    return "break"


def save():
    global file_name
    global source
    try:
        write(file_name)
    except:
        save_as()


# ----------------------------------------------------------------------------------------------------------------------

def showoutput():
    OutputText.delete(1.0, END)
    for l in TOKENS:
        line_num = l['LineNum']
        t = l['Token']
        tt = l['TokenType']
        String = '<' + str(line_num) + '>\t' + t + ',' + tt
        OutputText.insert(INSERT, String + '\n')


def CheckWord(ID, line_num):
    # return 0 -->error , 1-->number  , 2-->Identifier
    b = ID[0]
    # check if number
    if b >= '0' and b <= '9':
        for i in range(1, len(ID)):
            b = ID[i]
            if b >= '0' and b <= '9':
                continue
            else:
                errormessage(f'Syntax Error at line{line_num} : "{ID}"')
                return 0
        return 1
    # check if identifier
    elif ((b >= 'a' and b <= 'z') or (b >= 'A' and b <= 'Z')):
        for i in range(1, len(ID)):
            b = ID[i]
            if ((b >= 'a' and b <= 'z') or (b >= 'A' and b <= 'Z') or (b >= '0' and b <= '9')):
                continue
            else:
                errormessage(f'Syntax Error at line{line_num} : "{ID}"')
                return 0
        return 2
    else:
        errormessage(f'Syntax Error at line{line_num} : "{ID}"')
        return 0


def ExtractToken(line, line_num):
    global TOKENS
    AddSemiColon = True
    Token = line.split(' ')
    for i, t in enumerate(Token):
        if not t:
            continue
        if t in ReservedWord:
            if t == 'end':
                AddSemiColon = False
            Type = t
            TokenType = t.upper()
        elif t == '+':
            Type = 'op'
            TokenType = 'PLUS'
        elif t == '-':
            Type = 'op'
            TokenType = 'MINUS'
        elif t == '*':
            Type = 'op'
            TokenType = 'MULT'
        elif t == '/':
            Type = 'op'
            TokenType = 'DIV'
        elif t == '=':
            Type = 'op'
            TokenType = 'EQUAL'
        elif t == ':=':
            Type = 'assign'
            TokenType = 'ASSIGN'
        elif t == '<':
            Type = 'op'
            TokenType = 'LESSTHAN'
        elif t == '>':
            Type = 'op'
            TokenType = 'GREATERTHAN'
        elif t == ';':
            if not AddSemiColon:
                continue
            Type = 'SC'
            TokenType = 'SEMICOLON'
            AddSemiColon = False
        elif t == '(':
            Type = 'OB'
            TokenType = 'OPENBRACKET'
        elif t == ')':
            Type = 'CB'
            TokenType = 'CLOSEDBRACKET'
        else:
            Word = int(CheckWord(t, line_num))
            if Word == 0:
                return
            elif Word == 1:
                Type = 'ID'
                TokenType = 'NUMBER'
            else:
                Type = 'ID'
                TokenType = 'IDENTIFIER'
        t = {
            'Token': t,
            'TokenType': TokenType,
            'Type': Type,
            'LineNum': line_num
        }
        TOKENS.append(t)
    if AddSemiColon:
        TOKENS.append({
            'Token': ';',
            'TokenType': 'SEMICOLON',
            'Type': 'SC',
            'LineNum': line_num
        })


def ParseLine(Line):
    i = 0
    LineSize = len(Line)
    Line = Line + '    '
    Symbols = ['+', '-', '*', '/', '>', '<', ':', '=', ';', '(', ')']
    while i <= LineSize:
        if Line[i] in Symbols:
            a = Line[0:i] + ' '  # i+1
            if Line[i + 1] == '=':
                b = ' ' + Line[i + 2:]
                s = Line[i:i + 2]
                i += 3
                LineSize += 3
            else:
                b = ' ' + Line[i + 1:]
                s = Line[i:i + 1]
                i += 2
                LineSize += 2
            Line = a + s + b
        i = i + 1
    return Line


def CheckTinyLang():
    global TinyLang
    TinyLang = True
    TStat = State({'Num': '0', 'line': '0'})
    SStack = [{'Num': '0', 'line': '0'}]
    for l in CodeLines:
        if 'if' in l['line']:
            TStat.insert(l, SStack[-1])
            SStack.append(l)
        elif 'repeat' in l['line']:
            TStat.insert(l, SStack[-1])
            SStack.append(l)
        elif 'else' in l['line']:
            SStack.pop(-1)
            TStat.insert(l, SStack[-1])
            SStack.append(l)
        elif 'end' in l['line']:
            SStack.pop(-1)
            TStat.insert(l, SStack[-1])
        elif 'until' in l['line']:
            SStack.pop(-1)
            TStat.insert(l, SStack[-1])
        else:
            TStat.insert(l, SStack[-1])
    TStat.CheckTiny()


def ScanCode():
    global source
    global CodeLines
    global SCAN
    source = []
    CodeLines = []
    content = text.get(1.0, END)
    source = content.splitlines()
    global TOKENS
    TOKENS = []
    print(source)
    if not source[0]:
        infomessage("input the source code")
        return
    SCAN = True
    for c, line in enumerate(source):
        line = ParseLine(line)
        line = line.strip()
        if not line:
            continue
        opentag = line.find('{')
        if opentag != -1:
            closetag = line.find('}')
            if closetag != -1:
                if opentag == 0:
                    if line[-1] == '}':
                        continue
                    else:
                        line = line[closetag + 1:]
                else:
                    line = line[0:opentag]
            else:
                errormessage("missing '}' at line" + str(c + 1))
                return
        CodeLines.append({'Num': str(c + 1), 'line': line})
        ExtractToken(line, c + 1)
    showoutput()
    CheckTinyLang()


# ---------------------------------------------Tkinter Declerations-----------------------------------------------------#

global num_spaces

num_spaces = 0
inputframe = LabelFrame(root, text="input")
show_line_number = IntVar()
show_line_number.set(1)
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', underline=0, command=save)
file_menu.add_command(label='Save as', command=save_as)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt+F4', command=Exit)
menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_command(label='Scan', command=ScanCode)
menu_bar.add_command(label='Parse', command=drawer)

root.config(menu=menu_bar)
line_number_bar = Text(inputframe, width=4, padx=3, takefocus=0, border=0,
                       background='grey40', state='disabled', wrap='none', fg='grey80')
line_number_bar.pack(side='left', fill='y')
text = Text(inputframe, bg='grey25', fg='white')


def viewall(*args):
    text.yview(*args)
    line_number_bar.yview(*args)


OutputFrame = LabelFrame(root, text='Output')
text.pack(expand='yes', fill='both')
OutputText = Text(OutputFrame, takefocus=0, relief=RAISED, border=0, background='grey20', wrap='none', fg='grey95')
scroll_bar = Scrollbar(text)
scroll_bar1 = Scrollbar(OutputFrame)
text.configure(yscrollcommand=scroll_bar.set)
OutputText.configure(yscrollcommand=scroll_bar1.set)
line_number_bar.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=viewall)
scroll_bar1.config(command=OutputText.yview())
scroll_bar.pack(side='right', fill='y')
scroll_bar1.pack(side='right', fill='y')
text.bind('<Any-KeyPress>', on_content_changed)
text.bind('<Control-s>', save)

inputframe.pack(expand='yes', fill='both')

OutputText.pack(expand='yes', fill='both')
OutputFrame.pack(expand='yes', fill='both')
root.mainloop()

