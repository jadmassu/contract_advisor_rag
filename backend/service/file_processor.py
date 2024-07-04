from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from utils import fil

class FileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.loaded_text = None
       

    def load_file(self):
        try:
            # Attempt to load the text
            loader = TextLoader(self.file_path)
            self.loaded_text = loader.load()
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the File: {e}")

    def split_file(self, chunk_size=700, chunk_overlap=50):
        try:
            if self.loaded_text is None:
                raise RuntimeError("No text loaded. Please load a File first.")

            text_splitter = RecursiveCharacterTextSplitter(
                # Set a really small chunk size, just to show.
                separators=[
                    "\n\n",
                    "\n",
                    " ",
                    ".",
                    ",",
                    "\u200b",  # Zero-width space
                    "\uff0c",  # Fullwidth comma
                    "\u3001",  # Ideographic comma
                    "\uff0e",  # Fullwidth full stop
                    "\u3002",  # Ideographic full stop
                    "",
                ],
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                is_separator_regex=False,
            )

            documents = text_splitter.split_documents(self.loaded_text)
            return documents
        except Exception as e:
            raise RuntimeError(f"An error occurred while splitting the File: {e}")

