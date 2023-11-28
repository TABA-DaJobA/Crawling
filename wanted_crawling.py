# 원티드 채용공고 크롤링
import requests
import datetime
import json

def crawling_wanted_data(parsed_data, info_keys):
    result={}
    for key in info_keys:
        if key == 'COMPANY':   # 회사 이름
            result['COMPANY'] = parsed_data['job']['company']['name']  
        elif key == 'GROUP_INTRO':   # 회사 소개
            result['GROUP_INTRO'] = parsed_data['job']['detail']['intro'] 
        elif key == 'WORKING_AREA':  # 근무 지역
            result['WORKING_AREA'] = parsed_data['job']['address']['full_location'] 
        elif key == 'TITLE':  # 제목
            result['TITLE'] = parsed_data['job']['position']
        elif key == 'MAINDUTIES': # 주요업무
            result['MAINDUTIES'] = parsed_data['job']['detail']['main_tasks']
        elif key == 'QUALIFICATION':  # 자격요건
            result['QUALIFICATION'] = parsed_data['job']['detail']['requirements']
        elif key == 'PREFERENTIAL':  # 우대사항
            result['PREFERENTIAL'] = parsed_data['job']['detail']['preferred_points']
        elif key == 'BENEFITS':  # 혜택 및 복지
            result['BENEFITS'] = parsed_data['job']['detail']['benefits']
        elif key == 'RECRUIT_DEADLINE':  # 마감날짜 None = 상시
            result['RECRUIT_DEADLINE'] = parsed_data['job']['due_time']
        elif key == 'geo_location': # 근무지역 (위도,경도)
            geo_location = parsed_data['job']['address'].get('geo_location')
            if geo_location:
                result['LAT'] = geo_location['n_location']['lat']
                result['LNG'] = geo_location['n_location']['lng']
            else:
                result['LAT'] = None
                result['LNG'] = None
        elif key == 'JOB_POSTING_URL':
            base = "https://www.wanted.co.kr/wd/"
            result['JOB_POSTING_URL'] = f"{base}{parsed_data['job']['id']}"
        elif key == 'TITLE_IMG':
            result['TITLE_IMG'] = parsed_data['job']['title_img']['origin']
        elif key == 'LOGO_IMG':
            result['LOGO_IMG'] = parsed_data['job']['logo_img']['origin']
    return result

parsed_data = []

timestamp = int(datetime.datetime.now().timestamp())
tag_type_ids = 518
years = -1
limit = 10
offset = 0
# tag_type_ids: 518 개발/ 507 경영-비즈니스 /523 마케팅 /511 디자인 /530 영업 /510 고객서비스-리테일 /524 미디어 /513 엔지니어링-설계
# 517 HR /959 게임 제작 /508 금융 /522 제조-생산 /515 의료-제약-바이오 /10101 교육 /532 물류-무역 /10057 식-음료 /521 법률-법집행기관 /509 건설-시설 /514 공공-복지
# limit -> 100이면 100개씩 데이터추출 (한번에 100밖에 불가)
# offset -> 0번째부터 추출

# 10000개 데이터 가져오기 
total_data_count = 10

base_url = "https://www.wanted.co.kr/api/v4/jobs/"
for offset in range(0, total_data_count, limit):
    
    url = "https://www.wanted.co.kr/api/v4/jobs?{}&country=kr&tag_type_ids={}&job_sort=job.latest_order&locations=all&years={}&limit={}&offset={}".format(timestamp, tag_type_ids, years, limit, offset)
    parse_company = requests.get(url).json()
    
    recur_ids = [temp['id'] for temp in parse_company['data']]
    

    for recur_id in recur_ids:
        detail_url = f"{base_url}{recur_id}?{timestamp}"
        job_data = requests.get(detail_url).json()

        info_keys = ['COMPANY', 'TITLE','GROUP_INTRO', 'WORKING_AREA', 'MAINDUTIES','QUALIFICATION', 'PREFERENTIAL', 'BENEFITS','RECRUIT_DEADLINE', 'geo_location','JOB_POSTING_URL','TITLE_IMG','LOGO_IMG']  # 필요한 정보 키
        crawled_data = crawling_wanted_data(job_data, info_keys)
        
        print(json.dumps(crawled_data, indent=4, ensure_ascii=False))
        
