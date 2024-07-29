import os
import shutil
from langchain_community.document_loaders import PyPDFLoader


def load_documents(directory):
    allpages = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                pages = loader.load_and_split()
                allpages.extend(pages)
                print("Document with", len(pages), "pages processed")
    return allpages


