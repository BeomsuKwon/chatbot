import pandas as pd

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def find_best_answer_leven(self, input_sentence):
        similarities = sorted(self.questions, key = lambda x  : self.calc_leven_distance(input_sentence,x))
        for value in similarities:
            if value:
                best_match_index = self.questions.index(value)
                break
        
        return self.answers[best_match_index]

    # 레벤슈타인 거리계산
    def calc_leven_distance(self, aText, bText):
        aLen = len(aText) + 1
        bLen = len(bText) + 1
        
        # 2차원 표(len(aText) + 1, len(bText) + 1) 준비
        # 비교를 공집합부터 시작하기 때문에 '문자열 길이 + 1'크기의 표를 준비
        matrix = [ [] for a in range(aLen) ]
        for i in range(aLen):
            matrix[i] = [0 for a in range(bLen)]
            
        # 0일때 초기값을 설정, 첫번째 행, 열을 문자열 길이로 초기화
        for i in range(bLen):
            matrix[0][i] = i
        for i in range(aLen):
            matrix[i][0] = i
        
        cost = 0 # 초기값
        
        # 레벤 슈타인 거리 계산
        for i in range(1,aLen):
            for j in range(1,bLen):
                if aText[i-1] != bText[j-1]:
                    cost = 1 # 문자가 다르면 cost가 1
                else :
                    cost = 0 # 문자가 동일할 때 cost가 0
                addNum = matrix[i-1][j] + 1 # 문자 삽입 시
                minusNum = matrix[i][j-1] + 1 # 문자 제거 시
                modiNum = matrix[i-1][j-1] + cost # 문자 변경 시
                
                # 게산된 각 패턴의 값 중 최소값을 표에 저장
                minNum = min([addNum,minusNum,modiNum]) 
                matrix[i][j] = minNum

        # 알고리즘을 통해 계산된 레벤슈타인 거리를 반환
        return matrix[aLen-1][bLen-1]

# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer_leven(input_sentence)
    print('Chatbot:', response)