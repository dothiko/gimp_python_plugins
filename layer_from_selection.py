#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] layer-from-selection
#[desc] 
#description_of_plugin
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

def python_fu_empty_layer_from_sel(a_img,a_drawable,sample_arg=True):

    # start of groping undoable operations
    pdb.gimp_image_undo_group_start(a_img)

    try:
        is_exist,sx,sy,ex,ey=pdb.gimp_selection_bounds(a_img)
        if is_exist:
            nl=pdb.gimp_layer_new(a_img,ex-sx+1,ey-sy+1,
                    1,#RGBA
                    "from selection",
                    100.0,
                    0 #Normal blend
                    )
            pdb.gimp_image_insert_layer(a_img,nl,a_img.active_layer.parent,-1)
            nl.set_offsets(sx,sy)
            pdb.gimp_selection_none(a_img)
        else:
            gimp.message("選択領域が存在しません")
        

    finally:
        # end of grouping undoable operations
        pdb.gimp_image_undo_group_end(a_img)

def python_fu_layer_from_sel(a_img,a_drawable,sample_arg=True):

    # start of groping undoable operations
    pdb.gimp_image_undo_group_start(a_img)

    try:
        is_exist,sx,sy,ex,ey=pdb.gimp_selection_bounds(a_img)
        if is_exist:
            if pdb.gimp_edit_cut(a_drawable):
                nl=pdb.gimp_layer_new(a_img,ex-sx+1,ey-sy+1,
                        1,#RGBA
                        "from selection",
                        a_drawable.opacity,
                        a_drawable.mode
                        )
                pdb.gimp_image_insert_layer(a_img,nl,a_img.active_layer.parent,-1)
                nl.set_offsets(sx,sy)
                fl=pdb.gimp_edit_paste(nl,True)
                pdb.gimp_floating_sel_attach(fl,nl)
                pdb.gimp_floating_sel_anchor(fl)
               #nl=pdb.gimp_floating_sel_to_layer(fl)
                pdb.gimp_selection_none(a_img)
                
            else:
                gimp.message("カットに失敗しました")
        else:
            gimp.message("選択領域が存在しません")

    finally:
        # end of grouping undoable operations
        pdb.gimp_image_undo_group_end(a_img)




register(
        "python_fu_empty_layer_from_sel",
        "empty-layer-from-selection",
        "create (limited , small) empty layer from selection",
        "dothiko",
        "kakukaku world",
        "sep 2015", 
        "<Image>/Python-Fu/layer/empty-layer-from-selection", 
        "RGB*,GRAY*",
        [
        #   (PF_BOOL,"sample_arg","sample of argument",True),
        ],
        [],
        python_fu_empty_layer_from_sel)

register(
        "python_fu_layer_from_sel",
        "layer-from-selection",
        "make the selected area as independent layer",
        "dothiko",
        "kakukaku world",
        "sep 2015", 
        "<Image>/Python-Fu/layer/layer-from-selection", 
        "RGB*,GRAY*",
        [
        #   (PF_BOOL,"sample_arg","sample of argument",True),
        ],
        [],
        python_fu_layer_from_sel)


main()

