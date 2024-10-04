import os
import pandas as pd

def remove_duplicates_in_all_subdirectories():
    # 현재 작업 디렉토리 내의 모든 하위 폴더와 파일 목록을 가져옴
    for foldername, subfolders, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            if filename.endswith(".csv"):
                csv_file_path = os.path.join(foldername, filename)
                print(f"처리 중: {csv_file_path}")

                # CSV 파일 불러오기
                df = pd.read_csv(csv_file_path)

                # 원래 행 수 출력
                original_rows = len(df)
                print(f"원래 행 수: {original_rows}")

                # '본문' 열을 기준으로 중복된 행 제거
                df_no_duplicates = df.drop_duplicates(subset=['본문'])

                # 삭제된 내용 출력
                deleted_content = df[df.duplicated(subset=['본문'], keep=False)]
                print("삭제된 내용:")
                print(deleted_content)

                # 총 삭제된 수 출력
                total_deleted = len(df) - len(df_no_duplicates)
                print(f"\n총 삭제된 수: {total_deleted}")

                # 중복이 제거된 데이터프레임을 덮어쓰기
                df_no_duplicates.to_csv(csv_file_path, index=False)
                
                # 새로운 행 수 출력
                new_rows = len(df_no_duplicates)
                print(f"저장 완료. 새로운 행 수: {new_rows}\n")

    print("현재 위치의 모든 하위 폴더에서 CSV 파일에서 중복된 '본문' 행을 삭제하고 저장했습니다.")

# 함수 호출
remove_duplicates_in_all_subdirectories()
