import os
import shutil

class PDFFileCopier:
    '''Copy and move PDF in binary mode with shutil.copy2.
    Use expected input data type.
    '''
    def __init__(self, source_path: str, destination_path: str):
        self.source_path = source_path
        self.destination_path = destination_path

    def copy(self):
        if self.source_path.lower().endswith(".pdf"):
            shutil.copy2(self.source_path, self.destination_path)
        else:
            print("Invalid source file. Only PDF files are supported.")

if __name__ == '__main__':
    source_path: str = input("Enter PDF file directory: ")
    destination_path: str = input("Enter target directory: ")

    copier = PDFFileCopier(source_path, destination_path)
    copier.copy()