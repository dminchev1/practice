import os

class TextFileEditor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            print(file_content)

if __name__ == '__main__':
    directory = input("Enter the directory of the file: ")
    filename = input("Enter the filename: ")
    file_path = os.path.join(directory, filename)

    editor = TextFileEditor(file_path)
    editor.read_file()

