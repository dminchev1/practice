import os

class TextFileEditor:
    def __init__(self, file_path):
        self.file_path = file_path

    def replace_word(self):
        old_word = input("Enter the word to replace: ")
        new_word = input("Enter the new word: ")

        with open(self.file_path, 'r+') as file:
            content = file.read()
            split_words = content.split()
            updated_content = " ".join([new_word if word == old_word else word for word in split_words])

            if old_word not in content:
                print(f"'{old_word}' not found in the file.")
            
            file.seek(0)  # Move the file pointer to the beginning
            file.write(updated_content)
            file.truncate()  # Remove any remaining content if the new content is shorter


if __name__ == '__main__':
    directory = input("Enter the directory of the file: ")
    filename = input("Enter the filename: ")
    file_path = os.path.join(directory, filename)

    editor = TextFileEditor(file_path)
    editor.replace_word()