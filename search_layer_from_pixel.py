#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] search-layer-from-pixel
#[desc]
# 選択領域の左上隅の真下にあるピクセルの所属するレイヤを得る。python-fuではインタラクティブにカーソル位置を得られないため、苦肉の策として選択領域を流用。
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

#-----------------------------------------------------------------------
def python_fu_search_layer_from_pixel(a_img,a_drawable,direction=True):

    # there is no undoable operation,so no need to undo group setting.
  # pdb.gimp_image_undo_group_start(a_img)
  #
  # try:
    exists,sx,sy,ex,ey=pdb.gimp_selection_bounds(a_img)

    if exists:
        tl=pdb.gimp_image_pick_correlate_layer(a_img,sx,sy)
        if tl:
            pdb.gimp_image_set_active_layer(a_img,tl)
            gimp.message("レイヤ名「%s」が見つかりました" % tl.name)
        else:
            gimp.message("レイヤが見つかりませんでした")

    pdb.gimp_selection_none(a_img)


   #finally:
   #    pdb.gimp_image_undo_group_end(a_img)

    


register(
        "python_fu_search_layer_from_pixel",
        "search-layer-from-pixel",
        "選択領域左上隅の真下にある画素が所属するレイヤを得てアクティブにする",
        "dothiko",
        "dothiko",
        "2015",
        "<Image>/Python-Fu/layer/search-layer-from-pixel",
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_search_layer_from_pixel)



main()






if __name__ == '__main__':

    pass


