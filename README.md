My gimp python plugins
====
These scripts are my python-fu plugins, for gimp 2.8.

これらのファイルは、GIMP 2.8用のpython-fuのプラグインです。

created and tested on Gimp 2.8.16 / Ubuntu linux 14.04.Some of them might not work on windows...

上記の環境で作成・テストしています。Windowsでは動かないものもあるかも知れません…




ファイルの説明 / about scripts 
-----
the scripts which have not been explained here,is internally used as library of other scripts.

ここに説明のないファイルはライブラリとして使用されているものです。

#### blendcolor.py
blend background color into foreground color,and save previous foreground color to palette 'blend history'
if there is no 'blend history' palette,it will be automatically generated.

前景色に背景色を混ぜます。混ぜられる前の前景色は「blend history」という名前のパレットに追加されます。もし「blend history」がなければ自動的に作成されます。

#### color_updown.py
up / down the HSV value of foreground color.this is useful when assigned to keyboard shortcut.
前景色の明度を上げたり下げたりします。キーボードに割り当てて使うと効果的です。

#### del_unnamed_path.py
名前なしのパスをすべて削除します。パスを定規のように使う人には効果的。

#### dynamics_toggle.py
キーボードからダイナミクスを切り替える為に作りました。これを使うと一時的にダイナミクスがオフになります。再度呼ぶと、以前のダイナミクスに戻されます。

#### fillsmootharea.py
Fill a selection area and it is automatically grown.this is useful when fill inside linearts with another layer.
The size of grow rely on inking tool size.
選択領域を自動で拡大して塗りつぶします。主線の内部を別レイヤで塗るときに効果的です。拡大サイズはインクツールのペン先の大きさに由来します。

#### incremental_save.py
add incremented version number to filename and save it.
ファイル名に自動的にバージョン名を付けてセーブしHます。セーブするごとにバージョン番号が自動的に上がります。

#### layer_align.py
レイヤを整列させます。

#### layer_from_color.py
前景色と同じ部分を独立したレイヤにします。手間を省くために作りました。

#### layer_from_selection.py
選択領域を独立したレイヤにします。手間を省くために作りました。

#### layerjump.py
キーボード操作により、あらかじめ設定されたレイヤに移動します。例えばレイヤが多い時に主線レイヤにすぐ移動したいようなときに効果的です。

#### layermove.py
レイヤを数値入力で移動させます。

#### masked_empty_duplicate.py
アクティブなレイヤのアルファチャネルの形をマスクとする、空のレイヤを新規生成します。影付けなどに便利。

#### merge_linked_layer.py
リンクされているレイヤを一つに統合します。

#### perspective_grid.py
アクティブな四角形パスを元に、擬似パースグリッドをレイヤとして生成します。

#### presetblur.py
予め設定されている強さでガウスぼかしをかけます。ダイアログでマウスでも選べますが、キーボードの1-9を使って項目をいきなり呼び出すことが可能です。

#### search_layer_from_pixel.py
選択領域の左上隅の位置の、不透明ピクセルを持つレイヤを探しだしてアクティブにします。ゴミ消し時に便利。

#### sync_layer_mask.py
アクティブなレイヤのマスクを、真下のレイヤや名前で指定したレイヤのアルファチャネルもしくはマスクと同期させます。もしくは、所属するレイヤグループの最下層のレイヤのアルファチャネルと同期します。
擬似クリッピングレイヤーのように使えると思います。

#### toggle_size.py
予め設定されたブラシサイズやインクサイズをトグルすることで、ブラシサイズを設定します。いちいちドット単位でスライダーを動かしたり、キーボードを何度もおすのが面倒なので作りました。


