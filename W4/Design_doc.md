Design Document
=========
宿題一
=========
## 目標：
あるページから別のページへの最短経路を求める。
![IMG_2652](https://github.com/kaki-bai/STEP/assets/107014844/ff809ecf-84b4-4e89-b76d-2a2dc16951e2)

## アルゴリズム：
```python
def find_shortest_path(self, start, goal):
```
### BFS
* キューを利用する
![IMG_2653](https://github.com/kaki-bai/STEP/assets/107014844/aca2bdd7-3aa5-4840-a5af-842963557b8b)

### 最短経路の表示
```python
prev = {}
```
* 辞書を利用し，前一個のページを記録する
![IMG_2654](https://github.com/kaki-bai/STEP/assets/107014844/7d86cc2a-3382-4920-baef-60ae9acfd1ec)


宿題二
=========
## 目標：
ページランクを計算することで，重要度の高いページトップ10を求める

## アルゴリズム：
```python
def find_most_popular_pages(self):
```
### ページランクの計算
* ノードPのページランクの85%は隣接のーどに均等に分配する
```python
new_page_rank[to_index] += 0.85 * old_page_rank[from_index] / len(link_array)
```
* 残りの15%は全ノードに均等に分配する
```python
new_page_rank[id] += 0.15*page_rank_sum_fifteen / page_num
```
![IMG_2655](https://github.com/kaki-bai/STEP/assets/107014844/020a0232-aa6e-4b9e-a163-c32d3f847be8)

* ノードPに隣接ノードがない場合，100%を全ノードに均等に分配する
```python
new_page_rank[id] += page_rank_sum_hundred / page_num
```
![IMG_2656](https://github.com/kaki-bai/STEP/assets/107014844/1cb22586-1cea-4204-84eb-cdc3e03bd0ef)

### ページランクが安定になったかの判断
* 前回のページランクの計算結果との差の絶対値の総計が0.01以下になる場合，安定だと考える
```python
difference = sum(abs(new_page_rank[id] - old_page_rank[id]) for id in old_page_rank.keys())
if difference < 0.01:
    break
```

宿題二
=========
## 目標：
もっと面白い知識を発見する
=>　「の」の数が一番多いタイトル（どうでもいいけど）

## アルゴリズム：
### 「の」の数の計算
```python
count = value.count('の')
```

## 結果
「の」が8個あるタイトルが4つある。
* '国公立の高等学校における教育の実質的無償化の推進及び私立の高等学校等における教育に係る負担の軽減のための高等学校等就学支援金の支給等に関する法律案', 
* '風のなかで_むしのいのち_くさのいのち_もののいのち',
* '風のなかで_むしのいのち、くさのいのち、もののいのち',
* '鈴懸の木の道で「君の微笑みを夢に見る」と言ってしまったら僕たちの関係はどう変わってしまうのか、僕なりに何日か考えた上でのやや気恥ずかしい結論のようなもの'
