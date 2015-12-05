#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from gimpfu import *
import os

# 「以前のダイナミクス」を保存するテキストファイル。OSに合わせて変更する。
DYNAMICS_INFO="/tmp/gimp_dynamics_info"
DYNAMICS_DEFAULT='Pressure Opacity'
USE_FILE=True # テキストファイルに保存しない場合はFalse。
              # OSに依存せず処理できるようになるが、この場合はダイナミクスはデフォルトとoffで切り替わる

def python_fu_dynamics_toggle(a_img,a_drawable):

    # start of groping undoable operations
    pdb.gimp_image_undo_group_start(a_img)

    try:

        dyn=pdb.gimp_context_get_dynamics()
        if dyn=="Dynamics Off":
            if os.path.exists(DYNAMICS_INFO) and USE_FILE:
                fp=open(DYNAMICS_INFO,'r')
                dyn=fp.read()
                fp.close()
            else:
                dyn=DYNAMICS_DEFAULT
            pdb.gimp_context_set_dynamics(dyn)
        else:
            if USE_FILE:
                fp=open(DYNAMICS_INFO,'w')
                fp.write(dyn)
                fp.close()

            pdb.gimp_context_set_dynamics('Dynamics Off')

    finally:
        # end of grouping undoable operations
        pdb.gimp_image_undo_group_end(a_img)



register(
        "python_fu_dynamics_toggle",
        "dynamics-toggle",
        "動的特性をoffとで切り替える",
        "dothiko",
        "kakukaku world",
        "sep 2013", 
        "<Image>/Python-Fu/others/dynamics-toggle", 
        "RGB*,GRAY*",
        [
            #(PF_BOOL,"sample_arg","sample of argument",True),
        ],
        [],
        python_fu_dynamics_toggle)


main()

