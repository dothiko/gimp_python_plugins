#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] edit_layer_as_image
#[desc] 
# 現在選択中のレイヤを複製し、独立した画像として編集する
#[version]
#0.1 初期リリース
#0.2 元イメージの画像タイプを反映させるように修正
#[end]

#  このプログラムはGPLライセンスver3で公開します。
# 
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You may have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.           
#
#   Copyright (C) 2012 dothiko(http://dothiko.cocolog-nifty.com/) 



from gimpfu import *

def python_fu_edit_layer_as_image(a_img,a_drawable):

    al=a_img.active_layer
    try:

        # start of groped undoable operations
        pdb.gimp_image_undo_group_start(a_img)

        new_img=gimp.Image(al.width,al.height,a_img.base_type)
        cl=pdb.gimp_layer_new_from_drawable(al,new_img)

        new_img.add_layer(cl)
        cl.set_offsets(0,0) # need this when offsetted layer assigned
        gimp.Display(new_img)

    except Exception,e:
        print(str(e))
    finally:

        # end of grouped undoable operations
        pdb.gimp_image_undo_group_end(a_img)

        gimp.displays_flush()



register(
        "python_fu_edit_layer_as_image",
        "レイヤを画像として編集",
        "edit duplicated active layer as a Image",
        "dothiko",
        "kakukaku world",
        "nov 2012", 
        "<Image>/Python-Fu/layer/edit-layer-as-image", 
        "*",
        [
        ],
        [],
        python_fu_edit_layer_as_image)


main()

