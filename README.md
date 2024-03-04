**크롤링**
- 1~3일 전 기사까지는 크롤링이 잘 되나, 이 이상으로 넘어가면 정상적으로 되지 않는 경우 발생

<br>

**불용어 사전 구축**
- 임베딩 성능 끌어올려 군집화가 원활하게 될 수 있게 하기 위함
- 사전 구축 방법론?
<br>

**군집화**
- TF-IDF Vectorizer 
    - TF-IDF
        - 해당 문장에서는 많이 등장하지만, 전체 문서에서는 적게 사용될수록 분별력 있는 특징이라는 점을 반영
    - hyperparameter
        - min_df : 단어 사전 구축 시 해당 단어가 포함되어야 하는 최소 문서 수 지정
        - analyzer : 학습의 단위를 단어로 설정할 것인지, 글자로 설정할 것인지 지정(word/char)
        - sublinear_tf : TF(단어빈도) 값의 스무딩(smoothing) 여부를 결정(True/False)
            - 단어빈도의 outlier가 있을 때 유용
        - ngram_range : 단어의 묶음 수 지정
            - 단어가 묶여야 의미를 가지는 것들이 있기 때문
        - max_feature : vector의 shape 결정
            - vector가 sparse해지는 문제 해결
- 내부 원소 간 거리 평균이 가장 높게 나온 군집 1개 제거

<br>

**키워드 추출**

<br>

**GPT Prompting**
