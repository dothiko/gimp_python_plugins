#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] masked-empty-duplicate
#[desc] 
#現在選択中のレイヤから、そのアルファチャネルをマスクとした空のレイヤを作成する。影付けに便利。
#[version]
#0.1 初期リリース
#0.2 バグ修正
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

def python_fu_masked_empty_duplicate(a_img,a_drawable):

    # start of groping undoable operations
    pdb.gimp_image_undo_group_start(a_img)
    try:

        curlayer=a_img.active_layer
       #t_mask=curlayer.mask
       #if t_mask==None:
       #    t_mask=a_drawable.create_mask(ADD_ALPHA_MASK)

        if curlayer.mask != None:
            pdb.gimp_message("既にマスクが存在します！")
            return

        if curlayer.has_alpha:
            newlayer=pdb.gimp_layer_new_from_drawable(curlayer,a_img)
            pdb.gimp_item_set_lock_content(newlayer,0) # to disable lock opaque pixel
            pdb.gimp_layer_set_lock_alpha(newlayer,0)  # to disable lock alpha

           #a_img.add_layer(newlayer,0)
            pdb.gimp_image_insert_layer(a_img,newlayer,curlayer.parent,-1)
            newmask=pdb.gimp_layer_create_mask(newlayer,ADD_ALPHA_MASK)

            saved_sel=pdb.gimp_selection_save(a_img)
            pdb.gimp_selection_all(a_img)
            pdb.gimp_edit_clear(newlayer)
            pdb.gimp_image_select_item(a_img,CHANNEL_OP_REPLACE,saved_sel)
            pdb.gimp_layer_add_mask(newlayer,newmask)
            pdb.gimp_layer_set_edit_mask(newlayer,0)
        else:
            pdb.gimp_message("アルファチャンネルが必要です")
    
    except Exception,e:
        print(str(e))
    finally:
        # end of grouping undoable operations
        pdb.gimp_image_undo_group_end(a_img)



register(
        "python_fu_masked_empty_duplicate",
        "masked-empty-duplicate",
        "透明度をマスク化し、画像は空の複製レイヤを作成",
        "dothiko",
        "kakukaku world",
        "sep 2013", 
        "<Image>/Python-Fu/mask/masked-empty-duplicate", 
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_masked_empty_duplicate)


main()

