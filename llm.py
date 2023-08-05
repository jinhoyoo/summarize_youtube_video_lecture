import os
import time 
import openai
from dotenv import load_dotenv

def correct_text(text, max_token=3000, model="gpt-3.5-turbo", language="ko"):

    positioned_command = {
        "ko": "한국어로 교정한 글들",
        "en": "Corrected text"
    }

    prompt = f"""
    Maintain the given language accordingly and correct all the typos and rectify any inaccuracies in names or locations in the given text.

    these are the examples for correction.

    태러다임 -> 패러다임 
    어보이친사 -> 어버이 친 자
    규족 -> 귀족 

    ----------
    {text}

    {positioned_command[language]}:
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
        Summarize the text below as well-organized note.
        ----------
        {text}

        {positioned_command[language]}:
        """

    time.sleep(0.5) # Avoid the bad request error. 
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a sophmore student."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_token
    )

    corrected_text = response.choices[0].message.content
    return corrected_text



def rectify_and_summarize_text(text, max_token=3000, model="gpt-3.5-turbo", language="ko"):

    positioned_command = {
        "ko": "한국어로 요약한 글",
        "en": "Summary note"
    }
        
    prompt = f"""
Ensure adherence to the provided language, rectify any typographical errors, and then create a well-structured summary of the following text with bullet points.
----------
{text}

{positioned_command[language]}:
        """

    time.sleep(0.5) # Avoid the bad request error. 
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a sophmore student."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_token
    )

    corrected_text = response.choices[0].message.content
    return corrected_text


def main():

    # Setup OpenAI API key 
    load_dotenv()

    text = """
        이것은 철학적. 이것은 그래서 태러다임이라고도 말하고 Basic Assumption, 기본전제예요. 우리가 세계를 이해하는 기본전제가 자기한테 있거든요. 윤석열이 말하는 걸 보면 기본전제가 뭐라는 걸 금방 알 수 있지 않습니까? 기본전제가 뭐예요? 친일파예요. 친일적 생각을 하고 있다.그냥 친일을 하는 건 일본하고 친하게 지진하는 지는 지는 자기가 아니에요. 역사학자 존용 선생님이 말해 보면 그 친자는 어보이친사라는 거.그래서 친일이라는 말은 그냥 일본하고 친하게 지진다는 게 아니라 일본을 어보이로 성기겠다는 뜻이란 말이죠. 실제로 그렇게 성긴 사람들이 나중에 뭐예요? 다 규족, 자기를 받고 어마어마한 재산을 하사받고 총독으로부터 하사받고 그러지 않습니까? 

        튼튼한 철학적 기반을 어디서 어디서 얻을 수 있을 거예요. 대학에서 얻는 겁니다. 그래서 대학은 입문하기에 중요한 거예요. 철학적 사유가 없이는 그걸 기반으로 이론을 만들어낼 수가 없기 때문입니다. 이론이 만들어내봐야 미국 사람들이 만들어낸 거 우리가 외워서 뱉여다가 여기서 그냥 대학에서 가르치는 그런 이론 밖에 나올 수 있는 게 없어요. 우리가 만들어낸 철학에서 우리가 이론을 철학에 바탕으로 이론을 만들어내서 그걸 가지고 우리가 서로 토론하고 더 좋은 것이 뭔지를생각해낼 수 있어야 되잖아요. 그래서 제가 성취해충 모형이라는 책을 이론적으로 썼습니다. 방법만을 쓴 거죠. 철학이 있으면 그걸 가지고 이론을 만들어내야 되는데 이론은 되게 방법론을 가지고 있어요. 그래서 방법론이 없으면 이론이라기 보기 어렵죠. 그건 철학이나 마찬가지죠. 그러니까 이론에는 반드시 방법론이 있어야 되는데 그 방법론을 가지고 구체적인 수단과 도구를 만들어내는 겁니다. 구체적인 수단과 도구를 가지고 현실에서 쓰는 거죠. 집행하는 겁니다. 
    """

    # revised_text = correct_text(text)
    # print(revised_text)

    # print('/n')

    # summary_note = summarize_text(revised_text)
    # print(summary_note)

    summary_note = rectify_and_summarize_text(text)
    print(summary_note)

if __name__ == "__main__":
    main()