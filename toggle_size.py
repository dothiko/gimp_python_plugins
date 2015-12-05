#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] toggle-brush-size
#[desc]
#ブラシ（インク）のサイズを好みのサイズ間でトグルする。
#[version]
#0.1 初期リリース
#[plugin]
#[name] adjust_brush_size(_inc/_dec)
#[desc]
#ブラシ（インク）のサイズをプリセットのうちで増減する。
#[version]
#0.1 初期リリース
#0.2 エアブラシなどで別の設定を使用するように変更.また、サイズのステップ変更は使っていないため廃止
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
# size list.you can edit this whatever you want. 
# サイズリスト。好きなように編集してください。
# BRUSH_SIZE is for paintbrush,eraser 
# AIRBRUSH_SIZE is for airbrush (gimp-airbrush)
# PENCIL_SIZE is for pencil (gimp-pencil)
# INK_SIZE is for ink(caligraphy,gimp-ink)tool

### MY CONFIG ###
BRUSH_SIZES=[1.0,3.0,5.0,10.0,15.0,22.0,35.0,50.0,100.0]
AIRBRUSH_SIZES=[16.0,32.0,64.0,96.0,128.0,160.0,192.0,256.0]
PENCIL_SIZES=[1.0,2.0,4.0,8.0,16.0,32.0]
INK_SIZES=[1.0,2.0,3.0,5.0]

def get_method_info():
    curmethod=pdb.gimp_context_get_paint_method()
    if curmethod=='gimp-ink':
        return (curmethod,INK_SIZES,pdb.gimp_context_get_ink_size())
    elif curmethod=='gimp-airbrush':
        return (curmethod,AIRBRUSH_SIZES,pdb.gimp_context_get_brush_size())
    elif curmethod=='gimp-pencil':
        return (curmethod,PENCIL_SIZES,pdb.gimp_context_get_brush_size())
    else:
        return (curmethod,BRUSH_SIZES,pdb.gimp_context_get_brush_size())


def get_nearest_index(a_list,value):
    try:
        return a_list.index(value)
    except:
        i=0
        for v in a_list:
            if v > value:
                return i
            i+=1
        return i-1

def python_fu_toggle_size(a_img,a_drawable,direction=True):

    # there is no undoable operation,so no need to undo group setting.
  # pdb.gimp_image_undo_group_start(a_img)
  #
  # try:

    curmethod,cur_list,cur_size=get_method_info()

    curpos=get_nearest_index(cur_list,cur_size)

    if direction:
        curpos+=1
    else:
        curpos-=1

    curpos=curpos % len(cur_list)
    if curmethod=='gimp-ink':
        pdb.gimp_context_set_ink_size(cur_list[curpos])
    elif curmethod=='gimp-airbrush':
        pdb.gimp_context_set_brush_size(cur_list[curpos])
    elif curmethod=='gimp-pencil':
        pdb.gimp_context_set_brush_size(cur_list[curpos])
    else:
        pdb.gimp_context_set_brush_size(cur_list[curpos])

    brush_list=None



   #finally:
   #    pdb.gimp_image_undo_group_end(a_img)

def python_fu_toggle_size_reverse(a_img,a_drawable):
    python_fu_toggle_size(a_img,a_drawable,False)

    #def python_fu_adjust_brush_size_inc(a_img,a_drawable):
    #    adjust_brush_size(True)
    #def python_fu_adjust_brush_size_dec(a_img,a_drawable):
    #    adjust_brush_size(False)
    #
    #def adjust_brush_size(direction):
    #
    #    curmethod,cur_list,cur_size=get_method_info()
    #
    #    if curmethod=='gimp-ink':
    #        if direction:
    #            cur_size+=1.0
    #        else:
    #            cur_size-=1.0
    #            
    #        if cur_size <= 1.0:
    #            cur_size=1.0
    #
    #        pdb.gimp_context_set_ink_size(cur_size)
    #    else:
    #        if direction:
    #            cur_size+=5.0
    #        else:
    #            cur_size-=5.0
    #            
    #        if cur_size <= 1.0:
    #            cur_size=1.0
    #        pdb.gimp_context_set_brush(cur_size)

    


register(
        "python_fu_toggle_size",
        "toggle-brush-size",
        "お気に入りのブラシ(インク）サイズを切り替える",
        "dothiko",
        "dothiko",
        "2013",
        "<Image>/Python-Fu/others/toggle-brush-size",
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_toggle_size)

register(
        "python_fu_toggle_size_reverse",
        "toggle-brush-size-reverse",
        "お気に入りのブラシ(インク）サイズを逆方向に切り替える",
        "dothiko",
        "dothiko",
        "2013",
        "<Image>/Python-Fu/others/toggle-brush-size-reverse",
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_toggle_size_reverse)


#register(
#        "python_fu_adjust_brush_size_inc",
#        "adjust-brush-size-inc",
#        "ブラシ(インク）サイズを大きくする(more系より微調整）",
#        "dothiko",
#        "dothiko",
#        "2013",
#        "<Image>/Python-Fu/others/adjust-brush-size-inc",
#        "RGB*,GRAY*",
#        [
#        ],
#        [],
#        python_fu_adjust_brush_size_inc)
#register(
#        "python_fu_adjust_brush_size_dec",
#        "adjust-brush-size-dec",
#        "ブラシ(インク）サイズを小さくする(more系より微調整）",
#        "dothiko",
#        "dothiko",
#        "2013",
#        "<Image>/Python-Fu/others/adjust-brush-size-dec",
#        "RGB*,GRAY*",
#        [
#        ],
#        [],
#        python_fu_adjust_brush_size_dec)




main()






if __name__ == '__main__':

    pass


