#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] incremental-save
#[desc] 
# ファイル名に、アンダースコアで始まる連番を自動生成して付加して保存する
#[version]
# 2013/08/11 0.1 初期リリース
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
import os
import re

def python_plugin_incremental_save(a_img,a_drawable):

    # start of groping undoable operations
    # pdb.gimp_image_undo_group_start(a_img)

    fname=os.path.basename(a_img.filename)
    fdir=os.path.dirname(a_img.filename)
    mo=re.search("(.*?)_([0-9]+).xcf",fname)
    if mo:
        basefname=mo.group(1)
        curcnt=int(mo.group(2))
    else:
        curcnt=0
        basefname=fname.split('.')[0]

    while 1:
        curcnt+=1
        fname="%s_%d.xcf" % (basefname,curcnt)
        fpath="%s%s%s" % (fdir,os.path.sep,fname)
        if os.path.exists(fpath):
            pass
        else:
            break
    
    pdb.gimp_xcf_save(0,
                      a_img,
                      a_drawable,
                      fpath,
                      fname)

    a_img.filename=fpath

    # to set 'saved flag'.
    pdb.gimp_image_clean_all(a_img)


    # end of grouping undoable operations
    #pdb.gimp_image_undo_group_end(a_img)

register(
        "python_fu_incremental_save",
        "incremental save for easy versioning",
        "incremental save for easy versioning",
        "dothiko",
        "dothiko",
        "2013",
        "<Image>/Python-Fu/incremental-save",
        "RGB*,GRAY*",
        [
        ],
        [],
        python_plugin_incremental_save)

main()






if __name__ == '__main__':

    pass


