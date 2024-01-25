
from dotenv import load_dotenv

from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.reduce import ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.text_splitter import CharacterTextSplitter


def summary_docs(text:str, chunk_size=1000, model:str="gpt-4", chunk_overlap=10, verbose = False)->str:

    llm = ChatOpenAI(temperature=0.1, model=model)

    # Map
    map_template = """이것은 문서의 집합이야.
    
    \"\"\"
    {docs}
    \"\"\"

    당신은 저널리스트다. 이 문서 목록을 기반으로 주제를 파악하여 아래처럼 구조화된 노트를 작성해줘.
 
    요약된 노트:
    """
    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt, verbose=verbose)

    # Reduce
    reduce_template = """이것은 요약 노트의 집합이야.:

    \"\"\"
    {doc_summaries}
    \"\"\"
    
    이를 취합하여 주요 주제를 최종적으로 통합한 요약을 작성하줘. 
    요약 노트:
    """
    reduce_prompt = PromptTemplate.from_template(reduce_template)
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt, verbose=verbose)


    # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="doc_summaries"
    )

    # Combines and iteravely reduces the mapped documents
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=4000,
        verbose=verbose
    )

    # Combining documents by mapping a chain over them, then combining results
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="docs",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
        verbose=verbose
    )

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = Document( page_content=text, metadata={"source":"local"} )
    split_docs = text_splitter.split_documents([docs])

    result = map_reduce_chain.run(split_docs)
    return result

def clean_up_sentence_punctuation_and_fix_errors(text:str, hint_to_fix:str, chunk_size:int=1000, max_token:int=3000, model:str="gpt-4", verbose:bool = False )->str:


    llm = ChatOpenAI(temperature=0.0, model=model, max_tokens=max_token)

    # Setup Map process
    correct_template = PromptTemplate.from_template("""
    아래 텍스트에의 문장부호를 다 정리해줘. 그리고 소리나는대로 잘못 적은 단어를 고쳐줘. 내용상 나뉘어야 하면 줄바꿈도 해줘. 고유명사 틀린것도 수정해줘.
    그리고 아래 예제처럼 자주 틀리는 것들이 있으니 참고해서 수정해줘. {hint_to_fix}
    
    \"\"\"
    {docs}
    \"\"\"
                                                    
    출력양식
    문서:""")



    # Create docs from text
    docs = Document( page_content=text, metadata={"source":"local"} )

    # Split text
    if verbose:
        print(f'chunk_size = {chunk_size}')

    text_splitter = CharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap  = 0,
        length_function = len,
        separator = " ",
    )

    splited_docs = text_splitter.split_documents([docs])

    # Run chain
    merged_document = ""
    for doc in splited_docs:
        chain = LLMChain(llm=llm,prompt=correct_template, verbose=verbose)        
        corrected_doc = chain.run( 
            {
                "docs":doc.page_content,
                "hint_to_fix": hint_to_fix
             } 
        )
        merged_document += corrected_doc
        merged_document += '\n\n'

    return merged_document
