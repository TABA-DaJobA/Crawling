import requests
import json

# URL 및 페이지 설정
id_base_url = "https://api.jumpit.co.kr/api/positions?sort=rsp_rate&highlight=false&page="
start_page = 1
end_page = 1    # 한페이지당 데이터 16개정도

# 저장할 데이터를 위한 리스트 초기화
COMPANY = []              # 회사이름
GROUP_INTRO = []          # 회사소개
WORKING_AREA = []         # 근무지역
TITLE = []                # 제목
EMPLOYMENT_TYPE = []      # 고용형태 ex. full_time
MAINDUTIES = []           # 주요업무
QUALIFICATION = []        # 자격요건
PREFERENTIAL = []         # 우대사항
BENEFITS = []             # 혜택 및 복지
RECRUIT_DEADLINE = []     # 채용마감날짜
TITLE_IMG = []            # 대표이미지
LOGO_IMG = []             # 로고이미지
JOB_POSTING_URL = []      # 채용공고URL
COMPANY_URL = []          # 회사URL
JOB_GROUP = 518

# 각 페이지에 대한 요청 및 ID 추출
for page in range(start_page, end_page + 1):
    response = requests.get(id_base_url + str(page))
    parsed_data = response.json()
    positions = parsed_data['result']['positions']

    # 각 포지션에 대한 상세 URL 생성
    for position in positions:
        position_url = f"https://api.jumpit.co.kr/api/position/{position['id']}"

        # 상세 정보 요청 및 데이터 추출
        response = requests.get(position_url)
        try:
            data = response.json()
            COMPANY.append(data['result']['companyName'])
            GROUP_INTRO.append(data['result']['serviceInfo'])
            WORKING_AREA.append(data['result']['jobPostingForSearchEngine']['jobLocation']['address']['streetAddress'])
            TITLE.append(data['result']['title'])
            EMPLOYMENT_TYPE.append(data['result']['jobPostingForSearchEngine']['employmentType'])
            MAINDUTIES.append(data['result']['responsibility'])
            QUALIFICATION.append(data['result']['qualifications'])
            PREFERENTIAL.append(data['result']['preferredRequirements'])
            BENEFITS.append(data['result']['welfares'])
            RECRUIT_DEADLINE.append(data['result']['closedAt'])
            TITLE_IMG.append(data['result']['cacheCompanyImages'][0]['imagePath'])
            LOGO_IMG.append(data['result']['logo'])
            JOB_POSTING_URL.append(data['result']['jobPostingForSearchEngine']['url'])
            COMPANY_URL.append(data['result']['companyUrl'])


        except ValueError:
            print("응답오류")
            # JSON 파일로 저장





# 회사 정보를 담을 리스트
company_info_list = []

# companyNames와 serviceInfos 리스트의 길이가 같다고 가정
for i in range(len(COMPANY)):
    # 각 회사에 대한 정보를 딕셔너리로 생성
    company_info = {
        'COMPANY': COMPANY[i],
        'GROUP_INTRO': GROUP_INTRO[i],
        'WORKING_AREA': WORKING_AREA[i],
        'TITLE': TITLE[i],
        'MAINDUTIES': MAINDUTIES[i],
        'QUALIFICATION': QUALIFICATION[i],
        'PREFERENTIAL': PREFERENTIAL[i],
        'BENEFITS': BENEFITS[i],
        'RECRUIT_DEADLINE': RECRUIT_DEADLINE[i],
        'TITLE_IMG': TITLE_IMG[i],
        'LOGO_IMG': LOGO_IMG[i],
        'JOB_POSTING_URL': JOB_POSTING_URL[i],
        'COMPANY_URL': COMPANY_URL[i],
        'JOB_GROUP': JOB_GROUP
        
    }
    company_info_list.append(company_info)

# 각 회사 정보를 JSON 형식으로 출력
for info in company_info_list:
    print(json.dumps(info, ensure_ascii=False, indent=4))
