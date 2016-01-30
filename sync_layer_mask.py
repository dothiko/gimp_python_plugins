#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] sync-layer-mask
#[desc] 
# レイヤのマスクをワンタッチで同期させるスクリプト
# 指定された正規表現にマッチしたレイヤを適合させたり
# 兄弟レイヤのマスクを統一したり
# アクティブレイヤをベースレイヤ(マスクが存在しない場合は不透明部分）と同じマスクにすることができる。
# 兄弟レイヤやベースレイヤの関係性は、基本的にレイヤの名前から決定される.
#
# なお、sync-layergroup-maskについては若干挙動が異なり、「アルファ相続」「クリッピングレイヤー」
# 的な挙動を行うためのものになっている。
# 所属するレイヤグループの最下層のレイヤのアルファ値と、その他の兄弟レイヤのマスクを同期するというものだ。
# 子グループについては「再帰して処理を行う」
# トップレベルレイヤについてはこのsync-layergroup-maskは機能しない（常にではないが大抵の場合、
# 最下層が完全に不完全なキャンバスな事が多く、まず機能せず混乱を招くだけという考え）
#
#[version]
#0.1 初期リリース
#0.2 グループの最下層レイヤーのアルファ値に同期させる（クリッピングレイヤー｜アルファ相続)関数を追加
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
#   Copyright (C) 2015 dothiko(http://dothiko.blog.fc2.com/) 


from gimpfu import *
import re

SIBLING_PATTERN='^%s(-\S+)?$'

def python_fu_sync_layer_mask(a_img,a_drawable,src_layer,regexp_pattern):
    if src_layer==None:
        src_layer=a_img.active_layer

    sync_layer_mask(a_img,src_layer,re.compile(regexp_pattern),None)

def python_fu_sync_layer_mask_of_sibling(a_img,a_drawable):
    names=a_img.active_layer.name.split('-')
    head=names[0]
    sync_layer_mask(a_img,a_img.active_layer,re.compile(SIBLING_PATTERN % head),None)

def python_fu_sync_layer_mask_of_base(a_img,a_drawable):

    names=a_img.active_layer.name.split('-')
    head=names[0]

    # searching '-base' layer
    regexp=re.compile('^%s-base$' % head)
    for bl in a_img.layers:

        mo=regexp.search(bl.name)
        if mo:
            if bl==a_img.active_layer:
                gimp.message("アクティブレイヤがベースレイヤです")
            else:
                sync_layer_mask(a_img,re.compile(SIBLING_PATTERN % head),bl,targets=(a_img.active_layer,))

            return
    
    gimp.message("ベースレイヤ(%s-base)は発見できませんでした" % head)

def python_fu_sync_layergroup_mask(a_img,a_drawable,limit_to_linked,limit_to_has_mask,apply_prev_mask):

    cl=a_img.active_layer
    if len(cl.children)>0:
        # this is the layer group
        target_layers=cl.children
    elif cl.parent==None:
        gimp.message("グループに所属するレイヤにのみ有効です")
        return
    else:
        target_layers=cl.parent.children

    cl=target_layers[-1] # the last child used as unified mask source.
    sync_layer_mask(a_img,None,cl,targets=target_layers,
            limit_to_linked=limit_to_linked,
            limit_to_has_mask=limit_to_has_mask,
            apply_prev_mask=apply_prev_mask,
            force_other_mask=True)


def python_fu_sync_layer_mask_to_below(a_img,a_drawable,apply_prev_mask):
    al=a_img.active_layer
    if al.parent:
        plst=al.parent.children
    else:
        plst=a_img.layers

    curidx=pdb.gimp_image_get_item_position(a_img,al)
    
    if curidx < len(plst):
        sync_layer_mask(a_img,None,plst[curidx+1],(a_img.active_layer,),apply_prev_mask=apply_prev_mask)
    else:
        gimp.message("これより下にレイヤがありませんので、同期できません")

def sync_layer_mask(a_img,regexp,src_layer,targets,
    limit_to_linked=False,limit_to_has_mask=False,
    apply_prev_mask=False,force_other_mask=False):
    """
    core function.

    Arguments:
    regexp -- the regular expression object.if this is None,all name should be match.
    targets -- a sequence of target layers.if None,a_img.layers used.

    Returns:
    None
    """


    if targets==None:
        targets=a_img.layers

    if src_layer.mask!=None:
        src_mask=src_layer.mask
    elif src_layer.has_alpha:
        src_mask=pdb.gimp_layer_create_mask(src_layer,2) # 2==ADD ALPHA-COMPONENT MASK
    else:
        gimp.message("この作業には、レイヤ %s にマスクかアルファチャネルが必要です" % src_layer.name)
        return


    # start of groping undoable operations
    pdb.gimp_image_undo_group_start(a_img)

    try:
        ax,ay=src_layer.offsets

        def do_sync(targets):
        # Use this local function ,to recursive call does not needs copy flags.
            for cl in targets:
                if cl!=src_layer:
                    
                    if len(cl.children)>0:
                        # this is layer group.so, walk into layer group
                        do_sync(cl.children) # RECURSIVE CALL
                    else:

                        if regexp:
                            mo=regexp.search(cl.name)
                        else:
                            flag_limit_linked=True
                            if limit_to_linked and not cl.linked:
                                flag_limit_linked=False

                            flag_limit_mask=True
                            if limit_to_has_mask and cl.mask==None:
                                flag_limit_mask=False

                            mo=(flag_limit_linked and flag_limit_mask)

                        if mo:
                           #pdb.gimp_message("processing %s" % cl.name)
                            if cl.mask==None:
                                if force_other_mask:
                                    new_mask=pdb.gimp_layer_create_mask(cl,1) # 1==Completely transparent mask,to composite it.
                                else:
                                    new_mask=pdb.gimp_layer_create_mask(cl,2) # 2==ADD ALPHA-COMPONENT MASK
                            elif apply_prev_mask:
                                pdb.gimp_layer_remove_mask(cl,0) # 0 means 'apply mask and delete it'
                                new_mask=pdb.gimp_layer_create_mask(cl,1) # completely transparent mask,to replace 
                            else:
                                pdb.gimp_layer_remove_mask(cl,1) # 1 means 'simply delete it without changing pixel.'
                                new_mask=pdb.gimp_layer_create_mask(cl,1) # completely transparent mask,to replace 

                            pdb.gimp_layer_add_mask(cl,new_mask)

                            cx,cy=cl.offsets
                            pdb.gimp_channel_combine_masks(cl.mask, src_mask, 0, -cx+ax , -cy+ay) # mask composited.

                            pdb.gimp_layer_set_edit_mask(cl,0)

        # Start processing here.
        do_sync(targets)

    finally:
        # end of grouping undoable operations
        pdb.gimp_image_undo_group_end(a_img)

        if src_layer.mask!=src_mask:
            gimp.delete(src_mask)

register(
        "python_fu_sync_layer_mask",
        "sync-layer-mask",
        "指定された正規表現パターンに適合する名前のレイヤ間で、マスクを同期させる",
        "dothiko",
        "dothiko",
        "apr 2015",
        "<Image>/Python-Fu/mask/sync-layer-mask",
        "RGB*,GRAY*",
        [
            (PF_LAYER,"src_layer","元レイヤ",None),
            (PF_STRING,"regexp_pattern","正規表現パターン(pythonのreモジュールの書式で)","\S+"),
        ],
        [],
        python_fu_sync_layer_mask)

register(
        "python_fu_sync_layer_mask_of_sibling",
        "sync-layer-mask-of-sibling",
        "アクティブレイヤの兄弟レイヤ間で、マスクを同期させる",
        "dothiko",
        "dothiko",
        "apr 2015",
        "<Image>/Python-Fu/mask/sync-layer-mask-of-sibling",
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_sync_layer_mask_of_sibling)

register(
        "python_fu_sync_layer_mask_of_base",
        "sync-layer-mask-of-base",
        "アクティブレイヤのマスクを、ベースレイヤのマスクで同期する",
        "dothiko",
        "dothiko",
        "apr 2015",
        "<Image>/Python-Fu/mask/sync-layer-mask-of-base",
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_sync_layer_mask_of_base)

register(
        "python_fu_sync_layergroup_mask",
        "alpha-inherit-mask",
        "アルファ相続的な動作で、グループの最後尾のアルファと各レイヤーのマスクを同期させる",
        "dothiko",
        "dothiko",
        "apr 2015",
        "<Image>/Python-Fu/mask/sync-layergroup-mask",
        "RGB*,GRAY*",
        [
            (PF_BOOL,"limit_to_linked","リンクされたレイヤに限定",False),
            (PF_BOOL,"limit_to_has_mask","現時点でマスクを持つレイヤに限定",True),
            (PF_BOOL,"apply_prev_mask","対象レイヤが既にマスクを持つ場合、同期前にマスクを適用する",False),
        ],
        [],
        python_fu_sync_layergroup_mask)

register(
        "python_fu_sync_layer_mask_to_below",
        "sync-layer-mask-to-below",
        "真下のレイヤの不透明部分をマスクとして同期させる",
        "dothiko",
        "dothiko",
        "apr 2015",
        "<Image>/Python-Fu/mask/sync-layer-mask-to-below",
        "RGB*,GRAY*",
        [
          (PF_BOOL,"apply_prev_mask","対象レイヤが既にマスクを持つ場合、同期前にマスクを適用する",False),
        ],
        [],
        python_fu_sync_layer_mask_to_below)
main()






if __name__ == '__main__':

    pass


