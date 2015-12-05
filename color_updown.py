#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] menu_name_of_plugin
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

def python_fu_color_up(a_img,a_drawable,up=True):

    h=pdb.gimp_context_get_foreground().to_hsv()
    STEP=0.07
    if up:
        h.v*=(1.0 + STEP)
        h.s*=(1.0 - STEP)
    else:
        h.v*=(1.0 - STEP)
        h.s*=(1.0 + STEP)

   #print("h.v %f / h.s %f" % (h.v,h.s))

    if h.v > 1.0:
        h.v=1.0
    if h.s > 1.0:
        h.s=1.0

    pdb.gimp_context_set_foreground(h.to_rgb())

def python_fu_color_down(a_img,a_drawable):
    python_fu_color_up(a_img,a_drawable,False)

register(
        "python_fu_color_up",
        "color-up",
        "change foreground color for hilighting",
        "dothiko",
        "kakukaku world",
        "sep 2013", 
        "<Image>/Python-Fu/color/color-up", 
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_color_up)

register(
        "python_fu_color_down",
        "color-down",
        "change foreground color for shadowing",
        "dothiko",
        "kakukaku world",
        "sep 2013", 
        "<Image>/Python-Fu/color/color-down", 
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_color_down)



main()

