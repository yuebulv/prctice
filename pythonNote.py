import tkinter as tk
from tkinter import filedialog
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    Folderpath = filedialog.askdirectory(title='请选择prj文件所在文件夹')
    Filepath = filedialog.askopenfilename(title='请选择prj文件所在文件夹', filetypes=[('prj files', '*.prj')])
    print(f'Folderpath:{Folderpath}')
    print(f'Filepath :{Filepath}')