from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

from PIL import ImageTk, Image

import psutil, re, threading, platform, os

import carver

class Carver_GUI(object):
    def __init__(self, window = None):
        # Initialize variables
        self.scan_target = StringVar()
        self.save_directory = StringVar()

        self.file_header_list = {}
        self.file_list = []
        self.recovery_log = ''

        self.png_flag = BooleanVar()
        self.jpg_flag = BooleanVar()
        self.bmp_flag = BooleanVar()
        self.gif_flag = BooleanVar()
        self.mp3_flag = BooleanVar()
        self.mp4_flag = BooleanVar()
        self.pdf_flag = BooleanVar()
        self.rtf_flag = BooleanVar()
        self.docx_flag = BooleanVar()
        self.doc_flag = BooleanVar()
        self.xlsx_flag = BooleanVar()
        self.xls_flag = BooleanVar()

        # Set Tkinter instance
        self.window = window

        # Set window background color
        self.window.configure(background = "#ececec")

        # Set window size
        self.window.minsize(807, 405)

        # Set title
        self.window.title("Data Carver")

        # Set preview frame
        self.preview_frame = Frame(window, background = "#ececec", width = 777)
        self.preview_frame.pack(side = TOP, anchor = "nw", padx = (15, 7.5), pady = (15, 0))

        # Set file table frame
        self.file_table_frame = Frame(self.preview_frame, background = "#ececec", width = 540)
        self.file_table_frame.pack(side = LEFT, anchor = "nw", padx = (0, 7.5))

        self.file_table = ttk.Treeview(self.file_table_frame, show = 'headings', height = 15)
        self.file_table['columns'] = ('c1', 'c2', 'c3', 'c4')
        self.file_table.column("# 1", anchor = 'w', stretch = NO, width = 110)
        self.file_table.heading("# 1", text = "File Name")
        self.file_table.column("# 2", anchor = 'w', stretch = NO, width = 75)
        self.file_table.heading("# 2", text = "File Size")
        self.file_table.column("# 3", anchor = 'w', stretch = NO, width = 100)
        self.file_table.heading("# 3", text = "Recoverability")
        self.file_table.column("# 4", anchor = 'w', stretch = NO, width = 250)
        self.file_table.heading("# 4", text = "Path")

        self.file_table.bind("<Double-1>", self.on_double_click)

        self.file_table.pack()

        # Set progress frame
        self.progress_frame = Frame(self.preview_frame, background = "#ececec", width = 222, height = 289)
        self.progress_frame.pack(side = LEFT, anchor = "nw", padx = (7.5, 0))

        self.image_preview_frame = Frame(self.progress_frame, background = "white", width = 222, height = 271)
        self.image_preview_frame.pack(side = TOP, anchor = "nw")

        original = Image.open('bg.png')
        image = ImageTk.PhotoImage(original)

        self.image_preview = Label(self.image_preview_frame, image = image, width = 215, height = 271)
        self.image_preview.pack()

        self.progress_bar = ttk.Progressbar(self.progress_frame, length = 222)
        self.progress_bar.pack(anchor = 'sw', expand = 'true', fill = 'x', side = BOTTOM, pady = (7.5, 0))

        # Set bottom frame
        self.bottom_frame = Frame(window, background = "#ececec")
        self.bottom_frame.pack(side = BOTTOM, anchor = "sw")

        # Set directory frame
        self.directory_frame = Frame(self.bottom_frame, background = "#ececec", width = 777, height = 71)
        self.directory_frame.pack(side = LEFT, anchor = "sw", padx = (15, 7.5), pady = (7.5, 18))

        # Set scan frame
        self.scan_frame = Frame(self.directory_frame, background = "#ececec", width = 540, height = 30)
        self.scan_frame.pack(pady = (0, 7.5))

        self.scan_target_label = Label(self.scan_frame, background = "#ececec", width = 10, text = "Scan target:", anchor = "w")
        self.scan_target_label.pack(side = LEFT, padx = (0, 7.5))

        self.scan_target_textbox = Entry(self.scan_frame, width = 20, textvariable = self.scan_target, bd = 0)
        self.scan_target_textbox.pack(side = LEFT, padx = (7.5, 7.5))

        self.scan_target_button = Button(self.scan_frame, background = "#ececec", width = 10, text = "Browse", bd = 0, command = self.select_scan_target)
        self.scan_target_button.pack(side = LEFT, padx = (7.5, 0))


        # Set save directory frame
        self.save_directory_frame = Frame(self.directory_frame, background = "#ececec", width = 540, height = 30)
        self.save_directory_frame.pack(pady = (7.5, 0))

        self.save_directory_label = Label(self.save_directory_frame, background = "#ececec", width = 10, text = "Save directory:", anchor = "w")
        self.save_directory_label.pack(side = LEFT, padx = (0, 7.5))

        self.save_directory_textbox = Entry(self.save_directory_frame, width = 20, textvariable = self.save_directory, bd = 0)
        self.save_directory_textbox.pack(side = LEFT, padx = (7.5, 7.5))

        self.save_directory_button = Button(self.save_directory_frame, background = "#ececec", width = 10, text = "Browse", bd = 0, command = self.select_save_directory)
        self.save_directory_button.pack(side = LEFT, padx = (7.5, 0))

        # Set file header frame
        self.file_header_frame = Frame(self.bottom_frame, background = "#ececec", width = 222, height = 71)
        self.file_header_frame.pack(side = LEFT, anchor = "sw", padx = (7.5, 7.5), pady = (7.5, 15))

        # Set file header column 1
        self.file_header_column_1 = Frame(self.file_header_frame, background = "#ececec", width = 64, height = 71)
        self.file_header_column_1.pack(side = LEFT, anchor = "sw")

        self.file_header_checkbox_1 = Checkbutton(self.file_header_column_1, background = "#ececec", text="PNG", variable = self.png_flag, command = lambda:print(self.png_flag.get()))
        self.file_header_checkbox_1.pack(anchor = "w", pady = (0, 1))

        self.file_header_checkbox_2 = Checkbutton(self.file_header_column_1, background = "#ececec", text="JPG", variable = self.jpg_flag, command = lambda:print(self.jpg_flag.get()))
        self.file_header_checkbox_2.pack(anchor = "w", pady = (1, 1))

        self.file_header_checkbox_3 = Checkbutton(self.file_header_column_1, background = "#ececec", text="BMP", variable = self.bmp_flag, command = lambda:print(self.bmp_flag.get()))
        self.file_header_checkbox_3.pack(anchor = "w", pady = (1, 0))

        # Set file header column 2
        self.file_header_column_2 = Frame(self.file_header_frame, background = "#ececec", width = 64, height = 71)
        self.file_header_column_2.pack(side = LEFT, anchor = "sw")

        self.file_header_checkbox_4 = Checkbutton(self.file_header_column_2, background = "#ececec", text="GIF", variable = self.gif_flag, command = lambda:print(self.gif_flag.get()))
        self.file_header_checkbox_4.pack(anchor = "w", pady = (0, 1))

        self.file_header_checkbox_5 = Checkbutton(self.file_header_column_2, background = "#ececec", text="MP3", variable = self.mp3_flag, command = lambda:print(self.mp3_flag.get()))
        self.file_header_checkbox_5.pack(anchor = "w", pady = (1, 1))

        self.file_header_checkbox_6 = Checkbutton(self.file_header_column_2, background = "#ececec", text="MP4", variable = self.mp4_flag, command = lambda:print(self.mp4_flag.get()))
        self.file_header_checkbox_6.pack(anchor = "w", pady = (1, 0))

        # Set file header column 3
        self.file_header_column_3 = Frame(self.file_header_frame, background = "#ececec", width = 64, height = 71)
        self.file_header_column_3.pack(side = LEFT, anchor = "sw")

        self.file_header_checkbox_7 = Checkbutton(self.file_header_column_3, background = "#ececec", text="PDF", variable = self.pdf_flag, command = lambda:print(self.pdf_flag.get()))
        self.file_header_checkbox_7.pack(anchor = "w", pady = (0, 1))

        self.file_header_checkbox_8 = Checkbutton(self.file_header_column_3, background = "#ececec", text="RTF", variable = self.rtf_flag, command = lambda:print(self.rtf_flag.get()))
        self.file_header_checkbox_8.pack(anchor = "w", pady = (1, 1))

        self.file_header_checkbox_9 = Checkbutton(self.file_header_column_3, background = "#ececec", text="DOCX", variable = self.docx_flag, command = lambda:print(self.docx_flag.get()))
        self.file_header_checkbox_9.pack(anchor = "w", pady = (1, 0))

        # Set file header column 4
        self.file_header_column_4 = Frame(self.file_header_frame, background = "#ececec", width = 64, height = 71)
        self.file_header_column_4.pack(side = LEFT, anchor = "sw")

        self.file_header_checkbox_10 = Checkbutton(self.file_header_column_4, background = "#ececec", text="DOC", variable = self.doc_flag, command = lambda:print(self.doc_flag.get()))
        self.file_header_checkbox_10.pack(anchor = "w", pady = (0, 1))

        self.file_header_checkbox_11 = Checkbutton(self.file_header_column_4, background = "#ececec", text="XLSX", variable = self.xlsx_flag, command = lambda:print(self.xlsx_flag.get()))
        self.file_header_checkbox_11.pack(anchor = "w", pady = (1, 1))

        self.file_header_checkbox_12 = Checkbutton(self.file_header_column_4, background = "#ececec", text="XLS", variable = self.xls_flag, command = lambda:print(self.xls_flag.get()))
        self.file_header_checkbox_12.pack(anchor = "w", pady = (1, 0))

        # Set action frame
        self.action_frame = Frame(self.bottom_frame, background = "#ececec")
        self.action_frame.pack(side = LEFT, anchor = "sw", padx = (7.5, 15), pady = (7.5, 18))

        # Set start frame
        self.start_frame = Frame(self.action_frame, background = "#ececec", width = 540, height = 30)
        self.start_frame.pack(pady = (0, 10))

        self.start_button = Button(self.start_frame, background = "#ececec", width = 10, text = "Start", command = lambda:threading.Thread(target = self.start, daemon = True).start())
        self.start_button.pack(side = LEFT)

        # Set logs frame
        self.logs_frame = Frame(self.action_frame, background = "#ececec", width = 540, height = 30)
        self.logs_frame.pack(pady = (7.5, 0.5))

        self.logs_button = Button(self.logs_frame, background = "#ececec", width = 10, text = "View Logs", state = 'disabled', command = lambda:self.view_logs())
        self.logs_button.pack(side = LEFT)

        #Run main loop
        self.window.mainloop()
    def start(self):
        print("Starting...\n")

        if(self.scan_target.get() != '' and self.save_directory.get() != '' and self.file_header_checker()):
            self.file_table.delete(*self.file_table.get_children())
            self.disable_buttons()
            self.progress_bar.start()
            worker = carver.Carver(self.scan_target, self.save_directory, self.file_header_list)

            self.file_list = worker.start()

            counter = 0
            for i in self.file_list:
                self.file_table.insert(parent='', index=counter, iid=counter, text='', values=i)
                counter += 1

            self.file_table.pack()

            self.recovery_log = worker.get_log()
            self.logs_button['state'] = 'normal'


        else:
            messagebox.showerror(title='Incomplete Parameters', message='Please select a valid scan target, save directory, and file types to recover.')

        self.progress_bar.stop()
        self.enable_buttons()

    def view_logs(self):
        root = Tk()
        root.title('View Logs')

        root.maxsize(400, 300)
        root.minsize(400, 300)

        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=Y)
        textbox = Text(root)
        textbox.pack()

        for i in self.recovery_log:
            textbox.insert('1.0', i)

        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)

        root.mainloop()

    def file_header_checker(self):
        self.file_header_list = {}
        if self.png_flag.get():
            self.file_header_list['png'] = [b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', b'\x49\x45\x4E\x44\xAE\x42\x60\x82']

        if self.jpg_flag.get():
            self.file_header_list['jpg'] = [b'\xFF\xD8',b'\xFF\xD9']

        if self.bmp_flag.get():
            self.file_header_list['bmp'] = [b'\x42\x4D', b'']

        if self.gif_flag.get():
            self.file_header_list['gif'] = [b'\x47\x49\x46\x38\x39\x61', b'\x00\x3B']

        if self.mp3_flag.get():
            self.file_header_list['mp3'] = [b'\x49\x44\x33', b'']

        if self.mp4_flag.get():
            self.file_header_list['mp4'] = [b'\x66\x74\x79\x70\x69\x73\x6F\x6D', b'']

        if self.pdf_flag.get():
            self.file_header_list['pdf'] = [b'\x25\x50\x44\x46', b'\x0A\x25\x25\x45\x4F\x46']

        if self.rtf_flag.get():
            self.file_header_list['rtf'] = [b'\x7B\x5C\x72\x74\x66\x31', b'\x7D']

        if self.docx_flag.get():
            self.file_header_list['docx'] = [b'\x50\x4B\x03\x04\x14\x00\x06\x00', b'\x50\x4B\x05\x06']

        if self.doc_flag.get():
            self.file_header_list['doc'] = [b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', b'']

        if self.xlsx_flag.get():
            self.file_header_list['xlsx'] = [b'\x50\x4B\x03\x04\x14\x00\x06\x00', b'\x50\x4B\x05\x06']

        if self.xls_flag.get():
            self.file_header_list['xls'] = [b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', b'']

        return bool(self.file_header_list)

    def select_save_directory(self):
        filename = filedialog.askdirectory()
        self.save_directory.set(filename)
        print(filename)

    def select_scan_target(self):
        partitions = psutil.disk_partitions()
        device_id = StringVar()

        filename = filedialog.askdirectory()
        print(filename)

        reg = ''

        if platform.system() == 'Windows':
            filename = os.path.splitdrive(filename)
            for x in partitions:
                if filename[0] in x[1]:
                    reg = r'^\w{1}:'
                    self.scan_target.set(re.match(reg, x[0]).group())
                    print(self.scan_target)

        else:
            reg = ''

            for x in partitions:
                if x[1] in filename:
                    if platform.system() == 'Darwin':
                        reg = r'^(\/dev\/disk\d{1,})'

                    elif platform.system() == 'Linux':
                        reg = r'^(\/dev\/sd\w{1})'

                    self.scan_target.set(re.match(reg, x[0]).group())
                    print(self.scan_target)

    def resize_preview(self, original):
        if original.width > original.height:
            width = 222
            height = width * (original.height / original.width)

        elif original.width == original.height:
            width = 222
            height = 222

        else:
            height = 271
            width = 271 / (original.height / original.width)

        return (int(width), int(height))

    def on_double_click(self, event):
        item = int(self.file_table.selection()[0])

        original = Image.open(self.file_list[item][3])
        size = self.resize_preview(original)
        image_resized = original.resize((size), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image_resized)

        self.image_preview.config(image = image, height = 271, width = 215)
        self.image_preview.image = image

    def disable_buttons(self):
        self.scan_target_textbox['state'] = 'disabled'
        self.scan_target_button['state'] = 'disabled'

        self.save_directory_textbox['state'] = 'disabled'
        self.save_directory_button['state'] = 'disabled'

        self.file_header_checkbox_1['state'] = 'disabled'
        self.file_header_checkbox_2['state'] = 'disabled'
        self.file_header_checkbox_3['state'] = 'disabled'
        self.file_header_checkbox_4['state'] = 'disabled'
        self.file_header_checkbox_5['state'] = 'disabled'
        self.file_header_checkbox_6['state'] = 'disabled'
        self.file_header_checkbox_7['state'] = 'disabled'
        self.file_header_checkbox_8['state'] = 'disabled'
        self.file_header_checkbox_9['state'] = 'disabled'
        self.file_header_checkbox_10['state'] = 'disabled'
        self.file_header_checkbox_11['state'] = 'disabled'
        self.file_header_checkbox_12['state'] = 'disabled'

        self.start_button['state'] = 'disabled'
        self.logs_button['state'] = 'disabled'

    def enable_buttons(self):
        self.scan_target_textbox['state'] = 'normal'
        self.scan_target_button['state'] = 'normal'

        self.save_directory_textbox['state'] = 'normal'
        self.save_directory_button['state'] = 'normal'

        self.file_header_checkbox_1['state'] = 'normal'
        self.file_header_checkbox_2['state'] = 'normal'
        self.file_header_checkbox_3['state'] = 'normal'
        self.file_header_checkbox_4['state'] = 'normal'
        self.file_header_checkbox_5['state'] = 'normal'
        self.file_header_checkbox_6['state'] = 'normal'
        self.file_header_checkbox_7['state'] = 'normal'
        self.file_header_checkbox_8['state'] = 'normal'
        self.file_header_checkbox_9['state'] = 'normal'
        self.file_header_checkbox_10['state'] = 'normal'
        self.file_header_checkbox_11['state'] = 'normal'
        self.file_header_checkbox_12['state'] = 'normal'

if __name__ == '__main__':
    root = Tk()
    Carver_GUI(window = root)
