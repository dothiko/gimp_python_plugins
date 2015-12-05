#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] fill-smooth-area
#[desc] fill smooth-edged area with current foreground color
#description_of_plugin
#[version]
#0.1 初期リリース
#0.2 選択領域を解除するようにした
#0.3 インクツールの大きさで選択領域の大きさを変えるようにした。
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

#GROW_SIZE=2

from gimpfu import *

def python_fu_fill_smooth_area(a_img,a_drawable,sample_arg=True):

    # start of groping undoable operations
    pdb.gimp_image_undo_group_start(a_img)

    t=pdb.gimp_context_get_ink_size()
    if t > 20:
        grow_size=5
    elif t > 10:
        grow_size=3
    elif t > 2:
        grow_size=2
    else:
        grow_size=1

    pdb.gimp_selection_grow(a_img,grow_size)
    pdb.gimp_edit_fill(a_drawable,0) # Foreground fill
    pdb.gimp_selection_none(a_img)

    # end of grouping undoable operations
    pdb.gimp_image_undo_group_end(a_img)



register(
        "python_fu_fill_smooth_area",
        "fill-smooth-area",
        "fill smooth selected area by expanding it,with current foreground color",
        "dothiko",
        "kakukaku world",
        "sep 2013", 
        "<Image>/Python-Fu/others/fill-smooth-area", 
        "RGB*,GRAY*",
        [
           #(PF_BOOL,"sample_arg","sample of argument",True),
        ],
        [],
        python_fu_fill_smooth_area)


main()

