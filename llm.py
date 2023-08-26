
from dotenv import load_dotenv

from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.reduce import ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.text_splitter import CharacterTextSplitter


def summary_docs(text:str, chunk_size=1000, chunk_overlap=10, verbose = False)->str:

    llm = ChatOpenAI(temperature=0)

    # Map
    map_template = """이것은 문서의 집합이야.
    
    \"\"\"
    {docs}
    \"\"\"

    당신은 대학생입니다. 이 문서 목록을 기반으로 주제를 파악하여 아래 처럼 구조화된 노트를 작성해보세요.
    
    - 주제 1
       - 소주제1
    - 주제 2
       - 소주제1
 
    요약된 노트:"""
    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt, verbose=verbose)

    # Reduce
    reduce_template = """이것은 요약 노트의 집합이야.:

    \"\"\"
    {doc_summaries}
    \"\"\"
    
    이를 취합하여 주요 주제를 최종적으로 통합한 요약을 작성하세요. 
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

def clean_up_sentence_punctuation_and_fix_errors(text:str, hint_to_fix:str, chunk_size:int=1000, max_token:int=3000, model:str="gpt-3.5-turbo", verbose:bool = False )->str:


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


def main():

    # Setup OpenAI API key 
    load_dotenv()


    text = """
제가 그 자료를 찾다가 시간이 없어서 그냥 가져왔는데 독일을 보면 알아요. 독일이 뭐냐면 정부 부채가 국가부채죠. 정부 부채가 약 GDP의 80%까지 올라갔었어요. 왜냐하면 시리아 난민을, 독일 얘기입니다. 2015년에 시리아 난민을 대거 들어왔잖아요. 100만 명 넘게 들어오는 바람에 그거에 대한 재정 지출을 하지 않을 수 없었잖아요. 그러니까 부채 비율이 70%, 80%까지 올라갔다가 그것을 점점 낮춰서 약 40%까지 낮췄었어요. 그런데 2019년이 어떻게 됐어요? 코로나 사태가 불거졌잖아요. 그러니까 코로나 때문에 자영업자들에 대한 생계를 보존해 주기 위해서 문 닫아도, 가게 문을 닫아도 다 그 수입을 보존해 줬어요. 완벽하게 보존해 줬죠. 그때 메르켈 정부였잖아요. 메르켈 정부에서 부총리 겸 재무부 장관을 했었던 사람이 누구예요? 지금 총리 하는 올라프 숄츠예요. 그래서 이 민주주의에 있는 사람들이 계속 예찬을 포함한 많은 사람들이 계속 얘기했던 거예요. 재난지원금을 지급하라.
    """

    note = """
- 문재인 정부가 막판에 재난지원금을 주지 않았다고 함.
- 홍남기가 세수 추계를 잘못하여 추가적인 예산이 필요해짐.
- 해당 예산으로 60조를 추가로 사용하였고, 만약 55조로 사용했다면 상황이 어땠을지 생각해봄.
- 윤석열 등 일부 세력은 국가의 통치를 위협하는 존재로 여겨짐.
    """

    rewritten_note = rectify_note_with_summarized_note_and_original_text(note, text)
    print(rewritten_note)



if __name__ == "__main__":
    main()