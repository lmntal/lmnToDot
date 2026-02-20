# lmnToDot
[LMNtal メタインタプリタ (McLMNtal)](https://github.com/lmntal/McLMNtal) の状態空間構築プログラムの出力を、 Graphviz による描画に対応した DOT 言語に変換するスクリプトです。

## Requirements
- python 3.x

## Preparation
状態空間の標準出力のために，以下の記述をメタインタプリタ (`state_space_construction.lmn` 等) に追加してください．

```
Ret = state_space(I, M, S, T) :-
Ret = ss(I, M, set.to_list(S), set.to_list(T)).
Ret = ss(I, M, [$x|S], T) :- int($x) |
Ret = ss(I, state_space.state_map_find(M, $x, Res), S, T), state($x, Res).
```

## Usage
標準入力に SLIM の出力を渡すことができます。

```slim --hl --use-buiiltin-rule state_space_construction.lmn | python3 lmnToDot.py```

実行時引数にファイルを指定することもできます。

```python3 lmnToDot.py state_space.out```

以下のようなコマンドで、SLIM での LMNtal プログラム実行 → DOT 言語生成 → Graphviz による描画を一度に行うことができます。

```slim --hl --use-builtin-rule state_space_construction.lmn | python3 lmnToDot.py | dot -T png -o state_space.png```

## Options
- colored
  - ノードに着色するか選択できます
