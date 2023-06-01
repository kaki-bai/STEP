Design Document
=========
## 目標：
電卓の一部機能を実装する。

## アルゴリズム：
### 「*」「/」機能
```python
def calculate_multi_divide(tokens):
```
* 問題点：
  * 算術演算子には優先順位がある
* 解決方法：
  * 「+」「-」機能を呼び出す前に，「*」「/」機能を先に呼び出す


## 括弧の対応
```python
def calculate_brackets(tokens):
```
* 問題点：
  * 括弧は複数のレベルを持つ場合がある
* 解決方法：
  * 最内層の括弧を見つけて，内側から外側に向かって再帰的に括弧内の値を計算する。
  * スタックを利用して，”(”のindexを記録し，”)”に出会う場合，一番新しい”(”のindexを取り出して，その間の値を計算する。


## function (abs, int, round)の追加
```python
def function_abs(tokens):
def function_int(tokens):
def function_round(tokens):
```
* 問題点：
  * functionがどの括弧の中での計算値に対応するかわからない
* 解決方法：
  * functionにつながる最外層の括弧を見つけて，その中の値を計算する
		
		
## functionの実装
* abs:
```python
if answer_in_brackets < 0:
               answer_abs = -1 * answer_in_brackets
           else:
               answer_abs = answer_in_brackets
```
* int:
```python
answer_int = answer_in_brackets // 1
```
* round:
```python
if answer_in_brackets * 10 % 10 >= 5:
               answer_round = answer_in_brackets // 1 + 1
           else:
               answer_round = answer_in_brackets // 1
```

