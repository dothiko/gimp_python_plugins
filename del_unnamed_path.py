#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from gimpfu import *

UNNAMED=u"名前なし"

def python_del_unnamed_path(a_img,a_drawable,basename=UNNAMED):
    try:
        basename=basename.decode('utf-8')
    except UnicodeEncodeError:
        pass

    pdb.gimp_image_undo_group_start(a_img)

    try:
        for cv in a_img.vectors:
            try:
                cpname=cv.name.decode('UTF-8')
                if cpname.index(basename)==0:
                    pdb.gimp_image_remove_vectors(a_img,cv)
            except ValueError,e:
                pass

    finally:
        pdb.gimp_image_undo_group_end(a_img)


register(
        "python_fu_del_unnamed_path",
        "delete all unnamed pathes",
        "delete all unnamed pathes",
        "dothiko",
        "kakukaku world",
        "2011",
        "<Image>/Python-Fu/path/del-unnamed-path",
        "*",
        [
            (PF_STRING,"basename","無名パスの先頭文字列",UNNAMED)    
        ],
        [],
        python_del_unnamed_path)

main()





if __name__ == '__main__':

    pass


