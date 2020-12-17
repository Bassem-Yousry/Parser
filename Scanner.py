# --------------------------------------------Imports-------------------------------------------------------------------#
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox as t

root = Tk()
root.geometry('600x600')
root.title('SCANNER')

# -------------------------------------------------VariablesDeclerations-----------------------------------------------#
global source
global lines
global file_name
ReservedWord = ['read', 'if', 'then', 'else', 'end', 'repeat', 'until', 'write']
TOKENS = []
source = []
lines = []


# ------------------------------------Show Errors-----------------------------------------------------------------------#
def errormessage(str, event=None):
    t.showerror("Error", str)


def infomessage(str, event=None):
    t.showinfo("Info", str)
#--------------------------------------------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------------------------------------

def showoutput():
    OutputText.delete(1.0, END)
    for l in TOKENS:
        OutputText.insert(INSERT, l + '\n')


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
    Token = line.split(' ')
    for t in Token:
        if not t:
            continue
        if t in ReservedWord:
            TOKENS.append(f'<{line_num}>    {t} , {t.upper()}')
        elif t == '+':
            TOKENS.append(f'<{line_num}>    {t} , PLUS')
        elif t == '-':
            TOKENS.append(f'<{line_num}>    {t} , MINUS')
        elif t == '*':
            TOKENS.append(f'<{line_num}>    {t} , MULT')
        elif t == '/':
            TOKENS.append(f'<{line_num}>    {t} , DIV')
        elif t == '=':
            TOKENS.append(f'<{line_num}>    {t} , EQUAL')
        elif t == ':=':
            TOKENS.append(f'<{line_num}>    {t} , ASSIGN')
        elif t == '<':
            TOKENS.append(f'<{line_num}>    {t} , LESSTHAN')
        elif t == '>':
            TOKENS.append(f'<{line_num}>    {t} , GREATERTHAN')
        elif t == ';':
            TOKENS.append(f'<{line_num}>    {t} , SEMICOLON')
        elif t == '(':
            TOKENS.append(f'<{line_num}>    {t} , OPENBRACKET')
        elif t == ')':
            TOKENS.append(f'<{line_num}>    {t} , CLOSEDBRACKET')
        else:
            Word = int(CheckWord(t, line_num))
            if Word == 0:
                return
            elif Word == 1:
                TOKENS.append(f'<{line_num}>    {t} , NUMBER')
            else:
                TOKENS.append(f'<{line_num}>    {t} , IDENTIFIER')


def ParseLine(Line):
    i=0
    LineSize=len(Line)
    Line=Line+'    '
    Symbols=['+','-','*','/','>','<',':','=',';']
    while i <= LineSize:
        if Line[i] in Symbols:
            a = Line[0:i]+' ' #i+1
            if Line[i+1] in Symbols:
                b=' '+Line[i+2:]
                s=Line[i:i+2]
                i += 3
                LineSize += 3
            else:
                b=' '+Line[i+1:]
                s=Line[i:i+1]
                i+=2
                LineSize+=2
            Line = a+s+b
        i=i+1
    return Line

def Scan():
    global source
    source = []
    content = text.get(1.0, END)
    source = content.splitlines()
    global TOKENS
    TOKENS = []
    if not source:
        infomessage("input the source code")
        return
    for c, line in enumerate(source):
        line=ParseLine(line)
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
        ExtractToken(line, c + 1)
    showoutput()


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
menu_bar.add_command(label='Scan', command=Scan)
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
