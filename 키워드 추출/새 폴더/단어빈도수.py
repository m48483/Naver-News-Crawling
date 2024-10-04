import os
import pandas as pd
import re
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 현재 스크립트 파일의 위치를 기준으로 한 상대 경로
script_path = os.path.dirname(os.path.abspath(__file__))

# 불용어 설정
stopwords = ['인공지능','인공','지능', '교육청','경기도','마련','우리','개발','김종인','이경전','굉주시','교육부','대해','위원회','부산','기여','기준','박상철','김현경','내년','최근','이번', '네이버', '통해', '관련', '위해', '대한', '지난', '교수', '그룹', '대표','제공','기반']

# 모든 하위 폴더에서 .csv 파일 찾기
for root, dirs, files in os.walk(script_path):
    df_combined = pd.DataFrame()
    for file_name in files:
        if file_name.endswith('.csv'):
            print(file_name)
            file_path = os.path.join(root, file_name)
            try:
                # 'euc-kr' 시도
                df_temp = pd.read_csv(file_path, encoding='euc-kr')
            except UnicodeDecodeError:
                try:
                    # 'cp949' 시도
                    df_temp = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    print(f"Cannot decode {file_path}. Check the encoding of the file.")
                    continue

            df_combined = pd.concat([df_combined, df_temp], ignore_index=True)

    if not df_combined.empty:
        # '본문' 및 '제목' 열의 텍스트 전처리 함수
        def preprocess_text(text):
            text = re.sub(r'[^\w]', ' ', str(text))
            return text

        # '본문' 및 '제목' 열의 텍스트 전처리
        df_combined['Processed_Content'] = df_combined['본문'].apply(preprocess_text) + ' ' + df_combined['제목'].apply(preprocess_text)

        # 전처리된 텍스트를 하나의 문자열로 결합
        message = ' '.join(df_combined['Processed_Content'])

        # 명사 추출
        nlp = Okt()
        message_N = nlp.nouns(message)

        # 불용어 제거
        message_N = [word for word in message_N if word not in stopwords]

        # 추출한 명사의 수
        count = Counter(message_N)

        # 추출한 명사 갯수순 정렬 (상위 80개 단어)
        word_count = dict()
        for tag, counts in count.most_common(20):  # 상위 80개 단어
            if len(str(tag)) > 1:
                word_count[tag] = counts

        # 맑은 고딕체 설정
        font_path = "c:/Windows/fonts/NanumGothic.ttf"
        font_name = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font_name)

        # 히스토그램 시각화
        plt.bar(list(word_count.keys()), list(word_count.values()))
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title(f'{os.path.basename(root)} Top 20 Frequent Words')
        plt.xticks(rotation=45)
        
        # 히스토그램 이미지 저장
        output_histogram_path = os.path.join(script_path, f'{os.path.basename(root)}_histogram.png')
        plt.savefig(output_histogram_path)
        
        # 히스토그램 이미지를 Jupyter Notebook에서 표시
        plt.show()

        # 결과 출력
        print("Top 20 words and their frequencies:")
        for word, frequency in word_count.items():
            print(f"{word}: {frequency}")

        # 결과를 엑셀 파일로 저장
        output_df = pd.DataFrame(list(word_count.items()), columns=['Word', 'Frequency'])
        output_excel_path = os.path.join(script_path, f'{os.path.basename(root)}_word_frequency.xlsx')
        output_df.to_excel(output_excel_path, index=False)
