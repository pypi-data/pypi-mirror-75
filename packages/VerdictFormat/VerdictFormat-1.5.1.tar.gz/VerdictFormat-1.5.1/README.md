# 判決書格式轉換
## 使用方法
安裝套件
`
    pip install VerdictFormat
`

把正式格式轉成測試格式
```python
from VerdictFormat import Formal_to_Test
Formal_to_Test(Formal_format_path,output_path)
```

把測試格式轉成正式格式
```python
from VerdictFormat import Test_to_Formal
Test_to_Formal(Test_format_path,output_path)
```

把標記好的格式轉成測試格式
```python
from VerdictFormat import Labeled_to_Test
Labeled_to_Test(Labeled_data)
```

正規化多個法條
```python
from VerdictFormat import Multilaws_to_Normalize
Multilaws_to_Normalize(Multilaws,breakline)
```

Formal Format
```python
[
{
    "name": "姓名",
    "statuses": [
        {
          "status":"公務員", 
          "locations": 
          [
            {
              "field":"JFull",
              "start": 28, 
              "end":40
            }
          ]
        }
      ], 
    "positions": [
        {
          "work unit": "勞動部職業安全衛生署南部職業安全衛生中心",
          "title": "檢查員",
          "locations": 
          [
            {
              "field":"JFull",
              "start": 28, 
              "end":40
            }
          ]
        },
        {
          "work unit": "勞動部職業安全衛生署",
          "title": "職員",
          "locations": []
        }
      ],
    "laws": [
        {
          "act": "貪污治罪條例",
          "article": 4, 
          "paragraph":  1,
          "subparagraph": 2, 
          "locations": 
          [
            {
              "field":"JLaw",
              "start": 28, 
              "end":40
            }, 
            {
              "field":"JLaw",
              "start": 156, 
              "end":168
            }
          ]
        } 
      ]  
  }
]

  ```

Test Format
```python
[
{
		"content_id" : "1" ,
		"name" : "柯森" ,
		"job_location" : [] ,
		"job_title" : [] ,
		"laws" : ["中華民國刑法第276條第1項","中華民國刑法第140條"]
    },{
		"content_id" : "2" ,
		"name" : "吳柯森" ,
		"job_location" : ["停車場"] ,
		"job_title" : ["管理員"] ,
		"laws" : ["中華民國刑法第276條第1項","中華民國刑法第140條"]
    }
]
```

Multilaws Normalize
```python

Multilaws="貪汙治罪條\\r\\n例第五條、第\r\n八條\\r\\n第五項第六款、第 \r\n 十 \\r\\n 條第六項第七款"
Normalized_laws_list=['貪汙治罪條例第五條', '貪汙治罪條例第八條第五項第六款', '貪汙治罪條例第十條第六項第七款']


```