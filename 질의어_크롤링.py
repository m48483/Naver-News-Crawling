# [CODE 1]으로 실행 시 크롤링하는 데이터가 많아
# 요청이 끊기고 응답이 없는 현상 자주 발생
# 특히 keywords[0]이 이 현상이 심합니다
# [CODE 1]이 많이 끊긴다면 [CODE 2] 사용을 권장합니다

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests
import os

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def news(n, keyword,yy, mm, result, start_page, end_page, script_path):
    page = start_page
    count = 0
    while True:
        # 필요한 url (네이버 뉴스에서 기간 옵션 설정)
        news_url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=0&photo=0&field=0&pd=3&ds={yy}.{mm}.01&de={yy}.{mm}.31&cluster_rank=4&mynews=1&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{yy}{mm}01to{yy}{mm}31,a:all&start={(page*10)+1}'
        print(news_url)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        response = requests.get(news_url, headers=headers)
        soupNews = BeautifulSoup(response.text, 'html.parser')
       
        title_list=[]
        articlebody_list=[]
        date_list=[]
        
        # 제목
        tag_tbody = soupNews.find_all('div',attrs={'class':'news_contents'})
                
        for article in tag_tbody:
            title = article.find('a', class_='news_tit').text
            if title:
                title_list.append(title)

        # 날짜
        tag_tbody = soupNews.find_all('div',attrs={'class':'sub_area'})
        
        for article in tag_tbody:
            date = article.find('span', class_='sub_txt').text
            if date:
                date_list.append(date)
        
        # 내용
        tag_tbody = soupNews.find_all('div',attrs={'class':'news_dsc'})
        
        for article in tag_tbody:
            articlebody = article.find('a').text
            if article:
                articlebody_list.append(articlebody)
        
        for item1, item2, item3 in zip(title_list, date_list, articlebody_list):
            print(item1, item2, item3+"\n")
            result.append([item1] + [item2] + [item3])
            count +=1
            
        # 다음 페이지 버튼이 있는지 확인
        next_button = soupNews.find('a', {'class': 'btn_next', 'aria-disabled': 'true'})
        if next_button:
            break  # 다음 페이지 버튼이 비활성화되거나 종료 페이지에 도달하면 종료
        elif page >= end_page:
            break
        else:
            page += 1
            
    yymm = str(yy)+'-'+str(mm)+'-01'

    existing_csv_path = os.path.join(script_path,'질의어크롤링결과.xlsx')
    df_existing = pd.read_excel(existing_csv_path)

    index = 0
    if n == 0:
        index = 2
    elif n == 1:
        index = 5
    elif n == 2:
        index = 8
    elif n ==3:
        index = 11
        
    mask = df_existing['년월'] == yymm
    if not df_existing.loc[mask].empty:
        # 이미 있는 행인 경우 해당 행을 업데이트
        df_existing.loc[mask, df_existing.columns[index]] = [f'{count}']
    else:
        # 새로운 행을 추가
        new_row = {'년월': yymm, df_existing.columns[index]: f'{count}'}
        df_existing = df_existing.append(new_row, ignore_index=True)

    # 업데이트된 데이터프레임을 엑셀 파일에 쓰기
    df_existing.to_excel(existing_csv_path, index=False)

    print(f'크롤링 결과: {count}개')

def main():
    result = []
    start_page = 0
    end_page = 400  # 네이버 뉴스 검색에서 최대 4,000건까지만 기사 제공
    count = 0
    
    script_path = os.path.dirname(os.path.abspath(__file__))
    
    # 네이버 고급 검색 OR == | AND == +
    keywords = ['인공지능|AI','인공지능|AI+윤리','인공지능|AI+이루다', '인공지능|AI|+윤리+교육'] 

    # [CODE 1] 
    #for keyword in keywords:
     #   for yy in range(2020, 2023):
      #      for month in range(1,13):
       #         mm = ''
        #        if(month<10):
         #           mm = '0'+str(month)
          #      else:
           #         mm = str(month)
            #    output_folder_name = str(yy)+"_"+mm
             #   output_folder_path = os.path.join(script_path, output_folder_name)
              #  create_folder_if_not_exists(output_folder_path)
               # news(keyword, yy, mm,result, start_page, end_page, output_folder_path)

    # [CODE 2]
    for index, keyword in enumerate(keywords):
        print(f"{index} : {keyword}")
    keyword = int(input("크롤링할 키워드의 숫자를 입력하세요(0~4) >> "))
    yy = input("연도를 입력하세요(YYYY) >> ")
    mm = input("달을 입력하세요(MM) >> ")
    news(keyword, keywords[keyword], yy, mm,result, start_page, end_page, script_path)

if __name__ == '__main__':
    main()
