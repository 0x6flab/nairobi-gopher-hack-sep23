from typing import Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFium2Loader
import openai


class GPT:
    """GPT class to get context from the given text.
    
    This class uses OpenAI API to get context from the given text.
    
    attributes:
        _openai_token (str): OpenAI API Token.
        PROMPT (str): Prompt to get context from the given text.
        CHUNK_SIZE (int): Chunk size to split the given text.
        CHUNK_OVERLAP (int): Chunk overlap to split the given text.
        OPENAI_TEMP (int): OpenAI temperature.
        MAX_GPT_TOKENS (int): Max GPT tokens.
    """
    
    PROMPT = """
    You are an experienced financial analyst and advisor.
    You are helping a client to understand their spending habits.
    Given monthly banl statement from this individual,
    Give an expense anlysis report and budget recommendation for the statement.
    """
    
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    OPENAI_TEMP = 0
    MAX_GPT_TOKENS = 2048
    
    def __init__(self, token: Optional[str] = ""):
        """
        Initialize the GPT class.
        
        Creates embeddings from the given file.
        This helps to to get context from the given text.

        Args:
            token (Optional[str], optional): OpenAI API Token. Defaults to "".
            
        Raises:
            ValueError: If OpenAI API Token is not given.
        """
        self._openai_token = token
        self.model = "gpt-3.5-turbo-0613"
        self.temperature = 0.3
        self.max_tokens = 256
        self.n = 1
        self.stop = None
        self.max_gpt_tokens = 2048

        try:
            if self._openai_token == "":
                raise ValueError("OpenAI API Token is not given.")
            else:
                openai.api_key = token
        except ValueError as e:
            print(f"Error in initializing GPT class: {e}")
    
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE, chunk_overlap=self.CHUNK_OVERLAP
        )

    
    def chat_with_file(self, file: str) -> str:
        """
        Chat with the given file.
        
        Chat with files like PDF will help to get context from the given pdf.
        
        Args:
            file (str): File path.
        
        Returns:
            str: Response from the GPT.
        
        Raises:
            ValueError: If the given file is not a PDF.
        """
        if not file.endswith(".pdf"):
            raise ValueError("File is not a PDF.")
        
        loader = PyPDFium2Loader(file_path=file)
        docs = loader.load()
        splitted_docs = self._text_splitter.split_documents(documents=docs)
        
        combined_doc = ""
        for doc in splitted_docs:
            combined_doc += str(doc)
            
        if len(combined_doc) > self.MAX_GPT_TOKENS:
            combined_doc = combined_doc[:self.MAX_GPT_TOKENS]
            
        reponse = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.PROMPT},
                {"role": "user", "content": combined_doc}
            ],
            temperature=self.temperature,
        )

        return reponse['choices'][0]['message']['content']
