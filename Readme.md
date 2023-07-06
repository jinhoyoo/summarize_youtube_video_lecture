
# Youtube Script Summarizer

## Overview

Youtube Script Summarizer is a tool that helps summarize YouTube scripts by chapter creators. It leverages the youtube-transcript-api, langchain, and OpenAI packages to achieve this.

## How it works

The youtube-transcript-api package is used to extract the script from a YouTube video.  The script is then processed using the langchain package to identify the language and translate it if necessary. Finally, the OpenAI package is used to generate a summary of the script for each chapter created.


## Usage

0. Clone this project and setup Python over v3.11.x. 
1. Install dependency 

``` bash 
$ pip install -r requirements.txt
```

2. Open `summary.ipynb`
- Create `.env` file and set `OPENAI_API_KEY` variable. 
- Edit the variables in the "Input variables" cell according to your requirements.
   - Provide the YouTube video ID (`youtube_video_id`) for which you want to generate a summary.
   - Specify the language of the subscription (`language`).
   - Adjust the parameters for generating the summary:
     - `max_token`: The maximum number of tokens in the generated summary.
     - `model`: The OpenAI model to use for generating the summary.
     - `chunk_size`: The size of each chunk of text for processing.
     - `chunk_overlap`: The overlap between each chunk.
  - Copy and paste the time stamps and chapter names from the YouTube video description into the `chapter_part_in_description` variable.

``` Python 

# Youtube video ID
youtube_video_id="MZQ6bc6mPAE"

# Language of subscription 
language = "ko"

# LLM: Recommended parameters for my testing. 
max_token = 3000
model = "gpt-3.5-turbo"
chunk_size = 900
chunk_overlap = 100

# Officially no way to get chapter automatically, 
# so copy and paste the time stamp and chapter in description of Youtube video. 
chapter_part_in_description = """
00:00 시작
05:24 해먹을 결심: 탄핵해야 하는 이유
10:55 댓글 읽어보기
24:27 인사조직론이란 무엇인가?
33:52 (게르만 모형) 왜 직무가 중요한가?
43:11 추미애의 직무인식
49:16 직무의 존재목적, 칸트의 인간관과 경영학적 응용
1:04:40 성과책임의 사회적 의미 (참고)직무의 3대 구성요소
1:06:05 직무개념의 부재
1:07:44 주진우와 양향자
1:11:52 추미애의 고백과 진심
1:35:09 왜 역량인가?
1:35:47 역량의 개념에 대한 이해
1:38:05 《성취예측모형》 프레임워크와 역량사전
1:41:48 진실한 리더십과 인재평가의 프레임워크
1:43:59 DANO 경영플랫폼 운용_리더십이란 무엇인가?
1:49:42 추미애에 대한 오해의 프레임과 추미애의 비전은 무엇인가?
1:53:21 이재명과 추미애 vs. 이낙연과 김진표
1:55:52 푸른 하늘을(김수영 시인, 1960.06.15.)
1:58:57 정리
"""

```

3. Run notebook and you can get the `markdown_note.md`.
   - This file has the script and summary for each chapter. 



## Trobleshooting
- To-Do 


## FAQ 
- To-Do 



