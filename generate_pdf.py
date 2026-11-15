import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 폰트 등록
FONT_PATH = "C:\\Windows\\Fonts\\malgun.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\malgunbd.ttf"

pdfmetrics.registerFont(TTFont("Malgun", FONT_PATH))
if os.path.exists(FONT_BOLD_PATH):
    pdfmetrics.registerFont(TTFont("MalgunBold", FONT_BOLD_PATH))
else:
    pdfmetrics.registerFont(TTFont("MalgunBold", FONT_PATH))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Malgun", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        # 상단 헤더
        self.drawString(40, 810, "⚡ ADsP D-4 초압축 합격 치트시트 & 따라쓰기 워크북")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 804, 555, 804)
        
        # 하단 푸터
        self.line(40, 35, 555, 35)
        page_text = f"- {self._pageNumber} / {page_count} -"
        self.drawCentredString(297.5, 23, page_text)
        self.drawRightString(555, 23, "합격선: 과목당 40% 이상, 전과목 60점 이상")
        self.restoreState()

def create_adsp_workbook(output_filename="ADsP_D4_따라쓰기_필기본_워크북.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='MalgunBold',
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=1, # Center
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='Malgun',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Header1',
        fontName='MalgunBold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        fontName='MalgunBold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Malgun',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )

    blank_style = ParagraphStyle(
        'BlankBody',
        fontName='Malgun',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor("#0F172A")
    )

    tip_style = ParagraphStyle(
        'Tip',
        fontName='MalgunBold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#DC2626")
    )

    story = []

    # 표지 겸 안내
    story.append(Spacer(1, 15))
    story.append(Paragraph("🎯 ADsP D-4 초단기 완성 손글씨 따라쓰기 워크북", title_style))
    story.append(Paragraph("필수 핵심 개념 • 두문자 암기 공식 • 계산 공식 정복 • 손으로 직접 써보는 빈칸 훈련", subtitle_style))
    
    # 4일 합격 전략 박스
    strategy_data = [
        [Paragraph("<b>📅 D-4 벼락치기 완벽 동선</b>", ParagraphStyle('W1', fontName='MalgunBold', fontSize=10, textColor=colors.white)),
         Paragraph("<b>핵심 목표 & 빈출 집중 공략 포인트</b>", ParagraphStyle('W2', fontName='MalgunBold', fontSize=10, textColor=colors.white))],
        [Paragraph("<b>Day 4 (오늘)</b>", body_style), Paragraph("<b>1과목 데이터 이해</b>: DIKW 피라미드, 데이터베이스 특징, 빅데이터 위기요인/통제방안", body_style)],
        [Paragraph("<b>Day 3</b>", body_style), Paragraph("<b>2과목 데이터 분석 기획</b>: 분석 과제 발굴 4가지, 분석 거버넌스 4분면, 분석 조직 3구조", body_style)],
        [Paragraph("<b>Day 2</b>", body_style), Paragraph("<b>3과목 통계 & 기초 분석</b>: 상관분석, p-value 가설검정, 회귀분석 결정계수, 시계열 모형", body_style)],
        [Paragraph("<b>Day 1</b>", body_style), Paragraph("<b>3과목 정밀 분석 & 기출 계산</b>: 혼동행렬 지표(정밀도/재현율/F1), 지지도/신뢰도/향상도, 군집", body_style)],
        [Paragraph("<b>D-Day</b>", tip_style), Paragraph("<b>모의고사 50제 오답 총정리</b> 및 <b>이 워크북 빈칸 최종 자가테스트</b>", tip_style)]
    ]
    t_strat = Table(strategy_data, colWidths=[90, 425])
    t_strat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_strat)
    story.append(Spacer(1, 12))

    # [1과목 데이터 이해]
    story.append(Paragraph("📌 제1과목: 데이터의 이해 (핵심 빈칸 & 따라쓰기)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#3B82F6"), spaceAfter=6))
    
    sub1_data = [
        [Paragraph("<b>항목 / 개념</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#1E3A8A"))),
         Paragraph("<b>핵심 내용 & 빈칸 채우기 (연필로 따라쓰세요)</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#1E3A8A"))),
         Paragraph("<b>암기 꿀팁</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#DC2626")))],
        
        [Paragraph("<b>암묵지와 형식지<br/>상호작용</b>", blank_style),
         Paragraph("• <b>공</b>통화 (암묵지 → 암묵지): 경험 공유, 신체적 체득<br/>"
                   "• <b>표</b>출화 (암묵지 → 형식지): [ __________________ ]화, 개념화<br/>"
                   "• <b>연</b>결화 (형식지 → 형식지): 문서 결합, 체계화<br/>"
                   "• <b>내</b>면화 (형식지 → 암묵지): 독서/훈련을 통한 자기 것 화", blank_style),
         Paragraph("<b>두문자: 공-표-연-내</b><br/>(공통-표출-연결-내면)", tip_style)],

        [Paragraph("<b>DIKW 피라미드</b>", blank_style),
         Paragraph("• Data(데이터): 순수한 객관적 [ ________ ] (예: A마트 100원, B마트 200원)<br/>"
                   "• Information(정보): 데이터를 가공해 [ ________ ] 부여 (예: A마트가 더 싸다)<br/>"
                   "• Knowledge(지식): 정보를 구조화하여 [ ________ ]으로 체득 (예: A마트에 가야겠다)<br/>"
                   "• Wisdom(지혜): 지식을 바탕으로 미래를 [ ________ ] 및 창의적 판단", blank_style),
         Paragraph("<b>데 - 정 - 지 - 지</b><br/>(단순사실 → 의미부여 → 개인경험체득 → 지혜)", tip_style)],

        [Paragraph("<b>빅데이터의 3V / 4V</b>", blank_style),
         Paragraph("• 3V: <b>양(Volume)</b> + <b>속도(Velocity)</b> + <b>다양성(Variety)</b><br/>"
                   "• 4V 확장: + <b>가치(Value)</b> 또는 정확성/진실성(Veracity)<br/>"
                   "• 데이터 변화: 사전처리 → [ __________ ], 표본조사 → [ __________ ]", blank_style),
         Paragraph("전수조사 & 사후처리<br/>질보다 양 우선!", tip_style)],

        [Paragraph("<b>빅데이터 위기요인과<br/>통제 방안</b>", blank_style),
         Paragraph("1. 사생활 침해 ➔ 해결책: [ __________________ ] 원칙 (동의에서 책임으로)<br/>"
                   "2. 책임 원칙 훼손 ➔ 해결책: [ __________________ ] 원칙 강화 (행위 이전 예측처벌 금지)<br/>"
                   "3. 알고리즘 블랙박스 ➔ 해결책: [ __________________ ] 제도 도입", blank_style),
         Paragraph("<b>사-책-알</b><br/>1. 책임강화<br/>2. 결과기반책임<br/>3. 알고리즈미스트", tip_style)],
    ]

    t_sub1 = Table(sub1_data, colWidths=[90, 315, 110])
    t_sub1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sub1)
    story.append(Spacer(1, 10))

    # [2과목 데이터 분석 기획]
    story.append(Paragraph("📌 제2과목: 데이터 분석 기획 (필수 프레임워크 따라쓰기)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D9488"), spaceAfter=6))

    sub2_data = [
        [Paragraph("<b>기획 핵심 영역</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#0F766E"))),
         Paragraph("<b>빈칸 채우기 및 공식 내용</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#0F766E"))),
         Paragraph("<b>암기 꿀팁</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#DC2626")))],

        [Paragraph("<b>분석 과제 발굴<br/>4가지 방식</b>", blank_style),
         Paragraph("• 대상(What) O, 방법(How) O ➔ <b>[ ________________ ] (Optimization)</b><br/>"
                   "• 대상(What) O, 방법(How) X ➔ <b>[ ________________ ] (Solution)</b><br/>"
                   "• 대상(What) X, 방법(How) O ➔ <b>[ ________________ ] (Insight)</b><br/>"
                   "• 대상(What) X, 방법(How) X ➔ <b>[ ________________ ] (Discovery)</b>", blank_style),
         Paragraph("<b>최 - 솔 - 인 - 발</b><br/>O O : 최적화<br/>O X : 솔루션<br/>X O : 통찰<br/>X X : 발견", tip_style)],

        [Paragraph("<b>분석 준비도/성숙도<br/>4분면 포지셔닝</b>", blank_style),
         Paragraph("• 준비도 낮음 + 성숙도 낮음 ➔ <b>[ ____________ ]</b> (기반 부재, 사전준비 필요)<br/>"
                   "• 준비도 높음 + 성숙도 낮음 ➔ <b>[ ____________ ]</b> (인프라는 있으나 역량 초기)<br/>"
                   "• 준비도 낮음 + 성숙도 높음 ➔ <b>[ ____________ ]</b> (조직 역량은 있으나 시스템 미비)<br/>"
                   "• 준비도 높음 + 성숙도 높음 ➔ <b>[ ____________ ]</b> (최상위 완성형 단계)", blank_style),
         Paragraph("<b>준 - 도 - 확 - 정</b><br/>낮/낮 : 준비형<br/>높/낮 : 도입형<br/>낮/높 : 확산형<br/>높/높 : 정착형", tip_style)],

        [Paragraph("<b>분석 거버넌스 체계<br/>5가지 구성요소</b>", blank_style),
         Paragraph("① 분석 [ ______ ] (Organization) &nbsp;&nbsp;&nbsp; ② 분석 [ ______ ] (Process)<br/>"
                   "③ 분석 [ ______ ] (System) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ④ 분석 [ ______ ] (Data)<br/>"
                   "⑤ 분석 [ __________________ ] (Human Resource)", blank_style),
         Paragraph("<b>조 - 프 - 시 - 데 - 인</b><br/>조직, 프로세스, 시스템,<br/>데이터, 인력(HR)", tip_style)],

        [Paragraph("<b>분석 조직 구조 3가지</b>", blank_style),
         Paragraph("• <b>집중형</b>: 전사 분석 전담 조직에서 모든 분석 업무 총괄 (중복 최소, 현업 협업 느림)<br/>"
                   "• <b>기능형</b>: 별도 전담 부서 없이 각 현업 부서에서 자체 분석 (현업 밀착, 중복 발생)<br/>"
                   "• <b>분산형</b>: 전담 조직 인력을 각 현업 부서에 배치하여 전사 조율 + 현업 신속 대응", blank_style),
         Paragraph("집중형 vs 기능형 vs 분산형<br/>특징 비교 단골 출제!", tip_style)],
    ]

    t_sub2 = Table(sub2_data, colWidths=[90, 315, 110])
    t_sub2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F0FDFA")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sub2)

    story.append(PageBreak())

    # [3과목 데이터 분석 - 통계 & 수식 정복]
    story.append(Paragraph("📌 제3과목: 데이터 분석 (수식 깨짐 없는 완벽 계산 노트)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#7C3AED"), spaceAfter=6))

    sub3_math_data = [
        [Paragraph("<b>구분</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#5B21B6"))),
         Paragraph("<b>공식 정의 및 빈칸 계산식 (절대 깨지지 않는 정규 표기)</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#5B21B6"))),
         Paragraph("<b>직관적 꿀팁</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#DC2626")))],

        [Paragraph("<b>혼동행렬<br/>(Confusion Matrix)<br/>핵심 지표</b>", blank_style),
         Paragraph("• <b>정확도 (Accuracy)</b> = (TP + TN) / (TP + FP + FN + TN)<br/>"
                   "• <b>정밀도 (Precision)</b> = TP / (TP + [ ____ ])  ➔ 모델이 True라 한 것 중 맞춘 비율<br/>"
                   "• <b>재현율 (Recall/민감도)</b> = TP / (TP + [ ____ ])  ➔ 실제 True 중 맞춘 비율<br/>"
                   "• <b>특이도 (Specificity)</b> = TN / (FP + TN)  ➔ 실제 False 중 맞춘 비율<br/>"
                   "• <b>F1-Score</b> = 2 × (정밀도 × 재현율) / (정밀도 + 재현율)  ➔ <b>[ ________________ ] 평균</b>", blank_style),
         Paragraph("<b>정-모-예 (FP)</b><br/><b>민-실-재 (FN)</b><br/>F1은 <b>조화평균</b>!<br/>(산술/기하평균 오답)", tip_style)],

        [Paragraph("<b>연관분석<br/>(Association)<br/>3대 핵심지표</b>", blank_style),
         Paragraph("• <b>지지도 (Support)</b> = P(A ∩ B) = (A와 B 동시 구매수) / [ _______________ ]<br/>"
                   "• <b>신뢰도 (Confidence)</b> = P(B|A) = (A와 B 동시 구매수) / [ _______________ ]<br/>"
                   "• <b>향상도 (Lift)</b> = 신뢰도 / P(B) = P(A ∩ B) / (P(A) × P(B))<br/>"
                   "  - Lift = 1 : A와 B는 서로 [ _________ ]<br/>"
                   "  - Lift &gt; 1 : [ _________ ] 상관관계 (A를 사면 B도 살 확률 증가)<br/>"
                   "  - Lift &lt; 1 : [ _________ ] 상관관계", blank_style),
         Paragraph("<b>지전(전체) / 신A(A)</b><br/>향상도 1 기준!<br/>1보다 크면 유의미!", tip_style)],

        [Paragraph("<b>의사결정나무<br/>불순도 지표</b>", blank_style),
         Paragraph("• <b>지니 지수 (Gini)</b> = 1 - ∑ (p_i)^2<br/>"
                   "  - 2개 범주(p, 1-p)일 때 최대값: p = 0.5일 때 지니값 = [ ________ ]<br/>"
                   "• <b>엔트로피 (Entropy)</b> = - ∑ p_i × log2(p_i)<br/>"
                   "• <b>분류 오류율</b> = 1 - max(p_i)<br/>"
                   "• 불순도는 순수할수록(동일 범주만 모일수록) [ ______ ], 섞일수록 [ ______ ]", blank_style),
         Paragraph("<b>지 - 엔 - 분</b><br/>지니 최대값 0.5<br/>불순도 낮을수록 순수!", tip_style)],

        [Paragraph("<b>가설검정과<br/>p-value &amp; 오류</b>", blank_style),
         Paragraph("• <b>귀무가설 (H0)</b>: 차이가 없다, 효과가 없다, 기존과 같다<br/>"
                   "• <b>대립가설 (H1)</b>: 차이가 있다, 효과가 있다, 연구자의 주장<br/>"
                   "• <b>p-value &lt; 0.05</b> 이면 귀무가설을 [ ________ ] ➔ 대립가설 채택(유의미!)<br/>"
                   "• <b>제1종 오류 (α)</b>: 실제로는 귀무가설이 참인데 귀무가설을 기각하는 오류<br/>"
                   "• <b>제2종 오류 (β)</b>: 실제로는 귀무가설이 거짓인데 귀무가설을 채택하는 오류", blank_style),
         Paragraph("<b>p 작으면 H0 기각!</b><br/>1종오류: 무죄인 사람을 유죄로 판결", tip_style)],

        [Paragraph("<b>회귀분석 핵심 공식</b>", blank_style),
         Paragraph("• <b>결정계수 (R²)</b> = SSR / SST = 1 - (SSE / SST) &nbsp;&nbsp; (범위: [ ___ ] ~ [ ___ ])<br/>"
                   "• <b>수정 결정계수 (Adjusted R²)</b>: 독립변수가 늘어나면 R²이 무조건 증가하는 단점 보완<br/>"
                   "• <b>다중공선성 판정 지표</b>: VIF (분산팽창계수) &gt; [ ______ ] 이면 다중공선성 의심", blank_style),
         Paragraph("R²은 0~1<br/>VIF 기준은 보통 10!", tip_style)],
    ]

    t_sub3 = Table(sub3_math_data, colWidths=[90, 315, 110])
    t_sub3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F5F3FF")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sub3)
    story.append(Spacer(1, 10))

    # [3과목 머신러닝 & 비지도학습 요약]
    story.append(Paragraph("📌 제3과목: 머신러닝 앙상블 & 군집분석 & 시계열", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#D97706"), spaceAfter=6))

    sub3_ml_data = [
        [Paragraph("<b>분류 모델 / 기법</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#B45309"))),
         Paragraph("<b>핵심 특징 및 빈칸 테스트</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#B45309"))),
         Paragraph("<b>구분 꿀팁</b>", ParagraphStyle('h', fontName='MalgunBold', fontSize=9, textColor=colors.HexColor("#DC2626")))],

        [Paragraph("<b>앙상블 기법<br/>(Ensemble)</b>", blank_style),
         Paragraph("• <b>배깅 (Bagging)</b>: 복원추출(Bootstrap)로 여러 표본 생성 후 [ ________ ] 학습, 투표/평균 집계<br/>"
                   "• <b>부스팅 (Boosting)</b>: 이전 모델의 오답/가중치를 다음 모델에 반영하는 [ ________ ] 학습 (성능 높으나 과적합 위험)<br/>"
                   "• <b>랜덤 포레스트</b>: 배깅 + 변수 무작위 선택 결합 (과적합 방지, 높은 정확도)", blank_style),
         Paragraph("배깅 = <b>병렬</b><br/>부스팅 = <b>순차+가중치</b>", tip_style)],

        [Paragraph("<b>군집분석 거리 척도</b>", blank_style),
         Paragraph("• 연속형 변수: 유클리디안, 맨하탄, [ __________________ ] (공분산 고려 거리), 민코프스키<br/>"
                   "• 범주형 변수: 자카드 계수(Jaccard), 코사인 유사도, 순위상관계수", blank_style),
         Paragraph("마할라노비스<br/>= <b>공분산/상관관계 고려</b>", tip_style)],

        [Paragraph("<b>시계열 분석<br/>정상성(Stationarity)</b>", blank_style),
         Paragraph("• 정상 시계열의 3대 조건: ① [ ________ ]이 일정, ② [ ________ ]이 시점에 의존 X, ③ 공분산은 시차에만 의존<br/>"
                   "• 비정상 시계열을 정상화하는 법: 평균 불균일 ➔ <b>[ ________ ]</b> / 분산 불균일 ➔ <b>변환</b><br/>"
                   "• ARIMA(p, d, q) 모형: p=[ ___ ] 모형 차수, d=[ ___ ] 횟수, q=[ ___ ] 모형 차수", blank_style),
         Paragraph("ARIMA(p, d, q)<br/>p=AR, d=차분, q=MA<br/>d=0이면 ARMA", tip_style)],
    ]

    t_sub3_ml = Table(sub3_ml_data, colWidths=[90, 315, 110])
    t_sub3_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#FFFBEB")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sub3_ml)

    story.append(PageBreak())

    # [빈칸 정답 및 최종 체크리스트]
    story.append(Paragraph("🎯 [자가 채점용] 빈칸 핵심 정답 & D-Day 파이널 체크", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#059669"), spaceAfter=8))

    answers_text = (
        "<b>[1과목 정답]</b><br/>"
        "• 암묵지/형식지: <b>문서화(또는 매뉴얼화)</b><br/>"
        "• DIKW: <b>사실(Fact) / 의미(Context) / 경험(개인화) / 예측(Insight)</b><br/>"
        "• 4V: <b>사후처리 / 전수조사</b><br/>"
        "• 위기요인 통제: 1. <b>책임원칙</b> / 2. <b>결과기반 책임원칙</b> / 3. <b>알고리즈미스트</b><br/><br/>"
        "<b>[2과목 정답]</b><br/>"
        "• 분석과제 4방식: <b>최적화(Optimization) / 솔루션(Solution) / 통찰(Insight) / 발견(Discovery)</b><br/>"
        "• 거버넌스 4분면: <b>준비형 / 도입형 / 확산형 / 정착형</b><br/>"
        "• 5대 요소: <b>조직 / 프로세스 / 시스템 / 데이터 / 인력(HR)</b><br/><br/>"
        "<b>[3과목 정답]</b><br/>"
        "• 정밀도 분모: <b>FP</b> / 재현율 분모: <b>FN</b> / F1평균: <b>조화평균</b><br/>"
        "• 연관분석: <b>전체 거래수 / A를 포함한 거래수 / 독립 / 양의(증가) / 음의</b><br/>"
        "• 의사결정나무: <b>0.5 / 낮을수록 / 높을수록</b><br/>"
        "• 가설검정: <b>기각</b><br/>"
        "• 회귀분석: <b>0 ~ 1 / 10</b><br/>"
        "• 앙상블: <b>병렬(독립) / 순차(가중치)</b><br/>"
        "• 거리: <b>마할라노비스 거리</b><br/>"
        "• 시계열: <b>평균 / 분산 / 차분(Difference) / AR / 차분 / MA</b>"
    )
    story.append(Paragraph(answers_text, ParagraphStyle('Ans', fontName='Malgun', fontSize=8.5, leading=13, textColor=colors.HexColor("#065F46"))))
    story.append(Spacer(1, 15))

    # 따라쓰기 연습용 방안지 그리드 (손글씨 필기 구역)
    story.append(Paragraph("✍️ 나만의 D-4 약점 극복 손글씨 따라쓰기 노트", h2_style))
    story.append(Paragraph("틀렸거나 헷갈리는 공식/두문자를 직접 3번씩 손으로 적어보세요.", subtitle_style))
    
    note_rows = [
        [Paragraph(f"<b>연습 {i+1}</b>", ParagraphStyle('grid', fontName='MalgunBold', fontSize=8, textColor=colors.HexColor("#64748B"))),
         Paragraph("", body_style)] for i in range(7)
    ]
    t_note = Table(note_rows, colWidths=[60, 455], rowHeights=26)
    t_note.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F1F5F9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_note)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF 워크북 생성 완료: {output_filename}")

if __name__ == "__main__":
    create_adsp_workbook()
