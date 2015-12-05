#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] layer-from-color
#[desc] 
#前景色の部分を独立したレイヤにし、その透明度からマスクも生成する
#[version]
#0.1 初期リリース
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
#   Copyright (C) 2013 dothiko(http://dothiko.blog.fc2.com/) 






from gimpfu import *

def layer_from_color(a_img,color,remove_original):
    ct=pdb.gimp_context_get_sample_threshold()
    pdb.gimp_context_set_sample_threshold(0.0)

    cl=a_img.active_layer
    al=pdb.gimp_layer_copy(cl,False)
    pdb.gimp_image_insert_layer(a_img,al,None,-1)

    pdb.gimp_layer_add_alpha(al)
    pdb.gimp_image_select_color(a_img,2,al,color)
    pdb.gimp_selection_invert(a_img)
    pdb.gimp_edit_cut(al)

    if remove_original:
        pdb.gimp_layer_add_alpha(cl)
        pdb.gimp_image_select_color(a_img,2,cl,color)
        pdb.gimp_edit_cut(cl)

    pdb.gimp_selection_none(a_img)
    pdb.gimp_context_set_sample_threshold(ct)

def python_fu_layer_from_color(a_img,a_drawable):

    # start of groping undoable operations
    pdb.gimp_image_undo_group_start(a_img)
    try:

        layer_from_color(a_img,pdb.gimp_context_get_foreground(),True)
    except Exception,e:
        print(str(e))
    finally:
        # end of grouping undoable operations
        pdb.gimp_image_undo_group_end(a_img)


register(
        "python_fu_layer_from_color",
        "layer-from-color",
        "generate a layer from color of current layer",
        "dothiko",
        "kakukaku world",
        "dec 2013", 
        "<Image>/Python-Fu/layer/layer-from-color", 
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_layer_from_color)


main()

