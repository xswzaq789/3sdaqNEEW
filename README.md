# 3sdaqNEEW
## flowchart
![NEW_flowchart](./NEW_flowchart.PNG)
## Function
- 주식 매매: 주식 매수와 매도를 할 수 있습니다.
- 차트 분석: 선택한 회사의 주식 차트를 볼 수 있습니다.
- 내 계좌: 자산, 보유한 주식 종목을 볼 수 있습니다.
- 게시판: 유저들과 소통할 수 있는 게시판입니다.
- Guide
- My page
## Who maed this?
@xswzaq789   
@yourms  
@likeaAI  
@liveAnyware 
## How to use this?
1. 다운 받으세요.
2. 파이참 등을 여신 후에 terminal로 갑니다.
3. 다음과 같은 명령어를 이용해 autosys 디렉토리로 갑시다.
   - **cd 3sdaq-master**
   - **cd web**
   - **cd autoSys**
4. 유저, 회사 정보를 생성할 명령어를 입력하세요.
   - **python pri_data.py**
   - **python fakeData.py**
5. 데이터가 생성된 후 장 마감 시간을 설정할 명령어를 입력하세요.
   - **python bbsclosing.py**
6. 터미널을 추가 후 autoSys 디렉토리에서 Dummy 유저의 트레이딩을 시작할 명령어를 입력하세요.
   - **python autoTrade.py**
7. 터미널을 추가 후 web 디렉토리에서 서버를 실행할 명령어를 입력하세요.
   - **python manage.py runserver**
8. 나온 링크(http://127.0.0.1:8000/)로 들어가서 보면 됩니다.

어디선가 막히신다면 **python manage.py collectstatic** 를 합시다!
