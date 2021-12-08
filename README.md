# family

## main program
 - main.py
 - run on gcp cloudfunctions
 - py37

## birthday data
 - saved in gcp datastore
 - kind(table): t_family
 - add new data: 
    - birthday(solar)
    - div("solar" or "lunar")
      - "solar": 阳历
      - "lunar": 农历
    - name
  - age,id,lunar_date,remind_date为程序生成
