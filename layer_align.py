#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[desc] レイヤグループ対応のシンプルなレイヤ整列スクリプト
#[version] 0.4

#  layer_align.py 
#
#  a plugin to align linked-layers or all the grouped sibling layers.
#  リンクされたレイヤ、もしくは同一のレイヤグループに属するレイヤを整列させるプラグイン
#  
#  ver 0.1  initial release
#  ver 0.2  align_position_* added
#  ver 0.3  calling autocrop-layer automatically feature added (needs plug_in_autocrop_layer)
#  ver 0.4  some description comment added
#
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
from dothikoutil import *

ALIGN_NONE=0
ALIGN_VERT_TOP,ALIGN_VERT_CENTER,ALIGN_VERT_BOTTOM=range(1,4)
ALIGN_HORZ_LEFT,ALIGN_HORZ_CENTER,ALIGN_HORZ_RIGHT=range(4,7)

ALIGN_BASE_TOPLEFT,ALIGN_BASE_CENTER=range(0,2)
ALIGN_POSITION_INSIDE,ALIGN_POSITON_OUTSIDE=range(0,2)

def python_fu_layer_align(a_img,a_drawable,horz_align=ALIGN_NONE,vert_align=ALIGN_NONE,align_position_x=ALIGN_POSITION_INSIDE,align_position_y=ALIGN_POSITION_INSIDE,linked=0,autocrop=False):

    al=a_img.active_layer
    if al!=None:

        # start of groping undoable operations
        pdb.gimp_image_undo_group_start(a_img)

        try:

            base_x,base_y=al.offsets
            base_max_x=base_x + al.width
            base_max_y=base_y + al.height
            base_cx=base_x+al.width/2
            base_cy=base_y+al.height/2


            def do_align(layer,do_x,do_y):
                dx,dy=layer.offsets
                if do_x:
                    if horz_align==ALIGN_HORZ_LEFT:
                        if align_position_x==ALIGN_POSITION_INSIDE:
                            dx=base_x
                        else:
                            dx=base_x-layer.width
                    elif horz_align==ALIGN_HORZ_RIGHT:
                        if align_position_x==ALIGN_POSITION_INSIDE:
                            dx=base_max_x-layer.width
                        else:
                            dx=base_max_x
                    elif horz_align==ALIGN_HORZ_CENTER:
                        dx=base_cx-layer.width/2

                if do_y:
                    if vert_align==ALIGN_VERT_TOP:
                        if align_position_y==ALIGN_POSITION_INSIDE:
                            dy=base_y
                        else:
                            dy=base_y-layer.height
                    elif vert_align==ALIGN_VERT_BOTTOM:
                        if align_position_y==ALIGN_POSITION_INSIDE:
                            dy=base_max_y-layer.height
                        else:
                            dy=base_max_y
                    elif vert_align==ALIGN_VERT_CENTER:
                        dy=base_cy-layer.height/2

                layer.set_offsets(dx,dy)

            if linked==0:
                if al.parent==None:
                    # destination is toplevel
                    layerlst=a_img.layers
                else:
                    layerlst=al.parent.children
            else:
                layerlst=[]
                walk_linked_layers(a_img.layers,layerlst)
                link_layers(layerlst,0)

            if autocrop:
                pdb.plug_in_autocrop_layer(0,a_img,al)

            for cl in layerlst:
                if al!=cl:
                    if autocrop:
                        pdb.plug_in_autocrop_layer(0,a_img,cl)
                    do_align(cl,horz_align!=ALIGN_NONE,vert_align!=ALIGN_NONE)

            if linked!=0:
                link_layers(layerlst,1)

        except DHPluginException,e:
            gimp.message(str(e))
        except:
            gimp.message("内部エラーが発生しました。")
        finally:

            # end of grouping undoable operations
            pdb.gimp_image_undo_group_end(a_img)

            gimp.displays_flush()



register(
        "python_fu_layer_align",
        "シンプルなレイヤ整列ツール",
        "aligning layers by linked or layer-group",
        "dothiko",
        "kakukaku world",
        "nov 2012", 
        "<Image>/Python-Fu/layer/layer-align", 
        "*",
        [   
            (PF_RADIO,"horz_align","横方向の整列方式",0,(("整列しない",0),("左揃え",4),("中央揃え",5),("右揃え",6))), 
            (PF_RADIO,"vert_align","縦方向の整列方式",0,(("整列しない",0),("上揃え",1),("中央揃え",2),("下揃え",3))), 
            (PF_RADIO,"align_position_x","横方向の整列位置",0,(("内側",0),("外側",1))), 
            (PF_RADIO,"align_position_y","縦方向の整列位置",0,(("内側",0),("外側",1))), 
            (PF_RADIO,"linked","操作対象",0,(("同一グループのレイヤ",0),("リンクされたレイヤ",1))), 
            (PF_BOOL,"autocrop","アクティブレイヤを含む対象レイヤを自動切り抜き",False),
        ],
        [],
        python_fu_layer_align)


main()

