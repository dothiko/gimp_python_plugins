#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[library]
#[name] dothikoutil
#[desc] 
# 拙作gimpプラグイン用の共通ライブラリ
#[version]
#0.1 初期リリース
#0.2 UUID付加関数を追加
#[end]
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
#   Copyright (C) 2012 dothiko(http://dothiko.blog.fc2.com/)

from gimpfu import *
import gtk

class DHPluginException(Exception):pass

def walk_linked_layers(layers,dlist,append_linked_group_all=False,force_append=False):
    """
    walk layers and if it linked then append it to dlist.
    force_append flag is for mainly internal usage, 
    to append all the children of linked layergroups.

    sample:

        dlist=[]
        walk_linked_layers(img.layers,dlist) # then all linked layer collected into 'dlist'.
        for layer in dlist:
            do something to layer
    """
    for cl in layers:
        if pdb.gimp_item_get_linked(cl)!=0 or force_append:
            dlist.append(cl)

        if pdb.gimp_item_is_group(cl):
            # group itself linked.
            if append_linked_group_all:
                # expand destination to all the children
                # even if theirself are not linked
                walk_linked_layers(cl.children,dlist,append_linked_group_all,True)
            else:
                walk_linked_layers(cl.children,dlist,append_linked_group_all,force_append)


def walk_layers(layers,handler,user_arg,parent=None):
    """
    walk layers and call handler with each layer (including layer group)

    handler needs three arguments,the first is a layer currently found,
    the second is parent layer,which means the parent group layer.
    and the second is user_argument which has passed to walk_layers.
    
    so handler must be such as

    def iterhandler(layer,parent,user_argument):
        (do something)


    sample:

        dlist=[]
        walk_linked_layers(img.layers,dlist) # then all linked layer collected into 'dlist'.
        for layer in dlist:
            do something to layer
    """
    for cl in layers:
        handler(cl,parent,user_arg)
        if pdb.gimp_item_is_group(cl):
            walk_layers(cl.children,handler,user_arg,cl)


def link_layers(layers,state):
    """
    change listed layers link state at once. 
    """
    state=int(state)
    for cl in layers:
        pdb.gimp_item_set_linked(cl,state)

def get_drawable_thumbnail_pixbuf(drawable,requested_width,requested_height):
    """
    get gtk.PixBuf from layer's thumbnail
    CAUTION: dimension arguments are "requested", not actual pixbuf dimension.
             you can get real dimension from Pixbuf.get_width()/get_height()
    """
    acw,ach,bpp,buflen,bufsrc=pdb.gimp_drawable_thumbnail(drawable,requested_width,requested_height)
    pbuf=gtk.gdk.pixbuf_new_from_data(
            str(bytearray(bufsr)), 
            gtk.gdk.COLORSPACE_RGB,
            False,
            8,
            acw,
            ach,
            buflen/ach)
    return pbuf

def create_inputblock(basebox,label,use_spin=True,create_hbox=True):
    """
    utility function for creating GTK input button and spin button
    """
    if create_hbox:
        t_box = gtk.HBox(False,1)
        t_box.show()
    else:
        t_box = basebox
    
    if label:
        t_label= gtk.Label(name)
        t_label.props.justify=gtk.JUSTIFY_RIGHT
        t_label.show()
        t_box.add(t_label)

    t_adj=gtk.Adjustment(init_val,-100000,100000,1,100)
    if use_spin:
        t_spin=gtk.SpinButton(t_adj,1.0,0)
        t_spin.show()
        t_box.add(t_spin)
    else:
        t_box.add(t_adj)
        t_spin=t_adj

    if create_hbox:
        basebox.add(t_box)

    return t_spin

def create_checkbutton(basebox,label,create_hbox=True):
    """
    utility function for creating GTK checkbutton(almost same as checkbox in WinGDI)
    """
    if create_hbox:
        t_box = gtk.HBox(False,1)
        t_box.show()
    else:
        t_box = basebox
    t_check=gtk.CheckButton(label)
    #t_check.set_active(init_val)
    t_check.show()
    t_box.add(t_check)

    if create_hbox:
        basebox.add(t_box)

    return t_check

def get_picture_uuid(image,create_if_not_exist=True):
    """
    return image's UUID string from it's parasite-data.
    """
    import uuid
    PICTURE_UUID='c33f8ff4-872a-11e3-aceb-bc5ff4775e25' # it is parasite name,always same,do not change
    p=image.parasite_find(PICTURE_UUID)
    if not p:
        p=gimp.Parasite(PICTURE_UUID,PARASITE_PERSISTENT,str(uuid.uuid1())) # it is picture-unique UUID
        # picure-unique-UUID should vary each of pictures.
        image.parasite_attach(p)
    return p.data

def get_picture_unique_name(image):
    """
    return image's unique name from file-path
    but,there can be a non-file image...
    """
    import hashlib
    s=hashlib.sha224()
    s.update(image.filename)
    return s.hexdigest()
