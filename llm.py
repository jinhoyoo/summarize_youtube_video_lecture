import os
import time 
import openai
from dotenv import load_dotenv

def correct_text(text, max_token=3000, model="gpt-3.5-turbo", language="ko"):

    prompt = {
        "ko":"아래 문장의 문장부호를 다 정리해줘. 그리고 소리나는대로 잘못 적은 단어를 고쳐줘. 내용상 나뉘어야 하면 줄바꿈도 해줘.", 
        "en":"Please organize the punctuation marks in the following sentences. Also, correct any incorrectly written words as you hear them. If there should be divisions in content, please include line breaks"
    }

    positioned_command = {
        "ko": "한국어로 교정한 글들",
        "en": "Corrected text"
    }

    prompt = \
f"""
{prompt[language]}

{text}
"""
    
    time.sleep(0.5) # Avoid the bad request error. 
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a university student."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_token
    )

    corrected_text = response.choices[0].message.content
    return corrected_text


def summarize_text(text, max_token=3000, model="gpt-3.5-turbo", language="ko"):

    positioned_command = {
        "ko": "한국어로 요약한 글",
        "en": "Summary note"
    }
        
    prompt = f"""

    아래 글들을 노트로 정리해줘. 중요한건 -표시로 Markdown처럼 아래처럼 구조적으로 정리해줘. 그리고 정리한 내용과 원문을 다시 보고, 중요한건 -표시로 Markdown처럼 구조적으로 정리해줘. 가장 마지막에 정리한 것만 출력해줘.
----------
{text}

        """

    time.sleep(0.5) # Avoid the bad request error. 
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a university student."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_token
    )

    corrected_text = response.choices[0].message.content
    return corrected_text



def clean_up_sentence_punctuation_and_fix_errors(text:str, hint_to_fix:str, chunk_size:int=1000, max_token:int=3000, model:str="gpt-3.5-turbo", verbose:bool = False )->str:

    from langchain import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.chat_models import ChatOpenAI
    from langchain.docstore.document import Document
    from langchain.text_splitter import CharacterTextSplitter

    llm = ChatOpenAI(temperature=0.0, model_name=model, max_tokens=max_token)

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
        separator = '. '
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