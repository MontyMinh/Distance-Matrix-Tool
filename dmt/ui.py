from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from dmt import *
from dmt.distances import *


class UserInterface():
    """Generate distance matrix from uploaded addresses"""
    @classmethod
    def upload_file(cls):
        """Function to collect the file path"""

        filepath = askopenfile(mode='r',
                               filetypes=[('Excel Files', '.xlsx .xlsm')])

        # Delete button for new text
        try:
            cls.upload_text.destroy()
            cls.upload_text = Label(cls.root)
            cls.upload_text.grid(row=1, columnspan=3)
        except:
            cls.upload_text = Label(cls.root)
            cls.upload_text.grid(row=1, columnspan=3)

        if filepath is None:
            cls.upload_text['text'] = 'No File Uploaded, Retry!'
            cls.upload_text['foreground'] = 'red'
        else:
            cls.filepath = filepath.name
            cls.upload_text[
                'text'] = f"{cls.filepath[-filepath.name[::-1].index('/'):]} \nUploaded Successfully!"
            cls.upload_text['foreground'] = 'green'

            cls.upload_button = 'Reupload'
            DistanceMatrix.filepath = cls.filepath
            

    @classmethod
    def run_generation(cls):
        """Generate distance matrix from factories to customers"""

        try:
            cls.generate_text.destroy()
        except:
            cls.generate_text = Label(cls.root,
                                      text='Generating Distances ...')
            cls.generate_text.grid(row=3, columnspan=3, padx=10)
        else:
            cls.generate_text = Label(cls.root,
                                      text='Generating Distances ...')
            cls.generate_text.grid(row=3, columnspan=3, padx=10)

        try:
            DistanceMatrix.generate_distances()
        except:
            cls.generate_text[
                'text'] = 'Error! See terminal for details\n Fix the error and click Execute to continue'
            cls.generate_text['foreground'] = 'red'
        else:
            cls.generate_text['text'] = 'Distances Generated Successfully'
            cls.generate_text['foreground'] = 'green'

    @classmethod
    def user_interface(cls):
        """Upload and generate distance on a user interface"""

        cls.root = Tk()
        cls.root.title('Distance Matrix Tool')
        cls.root.geometry('500x250')

        # Upload file
        cls.upload_prompt = Label(cls.root, text='Upload Data File')
        cls.upload_prompt.grid(row=0, column=0, padx=10)

        cls.upload_button = Button(
            cls.root,
            text='Upload File ',
            command=cls.upload_file,
        )
        cls.upload_button.grid(row=0, column=1)

        # Program prompt
        cls.generate_prompt = Label(cls.root, text="Optimize Program")
        cls.generate_prompt.grid(row=2, column=0, padx=10)

        # Execute button
        cls.generate_button = Button(cls.root,
                                     text='Execute',
                                     command=cls.run_generation)
        cls.generate_button.grid(row=2, column=1)

        cls.root.mainloop()