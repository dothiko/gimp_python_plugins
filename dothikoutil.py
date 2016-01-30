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
import re
import os
import glob

import pygtk
pygtk.require("2.0")
import gtk

#-------------------------------------------------------------------------------
# Exceptions

class DHPluginException(Exception):pass

#-------------------------------------------------------------------------------
# Global functions

#-------------------------------------------------------------------------------
# Image related

def scale_image(image,w,h,method=2):
    """
    scale image with assigned interpolation method.

    Arguments:
    w - new width
    h - new height
    method -- interpolation method.
                0 = No interpolation.
                1 = Linear
                2 = bicubic (default)
                3 = lanczos
    Returns:
    None
    """

    old_method=pdb.gimp_context_get_interpolation()
    pdb.gimp_context_set_interpolation(method)
    pdb.gimp_image_scale(image,w,h)
    pdb.gimp_context_set_interpolation(old_method)
    
def get_scale_size(image,new_width,new_height):
    """
    returns (wwidth,height) of new scaled size.
    when new_width is -1 or None,width culculated automatically 
    from the ratio of new_height / image.height.
    same way when new_height is -1 or None.
    """
    if new_width<0 or new_width==None:
        ratio=float(new_height) / image.height
        return ( int(image.width*ratio), new_height )
    else:
        ratio=float(new_width) / image.width
        return ( new_width,int(image.height*ratio) )

def save_as_png(image,fpath,opt):
    """
    utility function,to ease saving PNG file.
    """
    pdb.file_png_save(
            image,
            image.active_layer, # VERY IMPORTANT. without this ,completely wrong layer would be saved!!
            fpath,
            os.path.basename(fpath),
            get_option_value(opt,'interrace',0), # do interrace 0=no / 1=yes
            9, # compression 0-9,default is 9
            1, # Write bKGD-background color 0=no / 1=yes
            0, # Write gAMA-gamma
            0, # Write oFFs-image offset
            0, # Write pHYs-physical pixel dimension
            1) # Write tIME-last modification time


def save_as_jpeg(image,fpath,opt):
    """
    utility function,to ease saving JPEG file.

    you can assign option as opt argument,which is dictionary.
    """
    import time
    lt=time.localtime()
    

    pdb.file_jpeg_save(
            image,
            image.active_layer, # VERY IMPORTANT. without this ,completely wrong layer would be saved!!
            fpath,
            os.path.basename(fpath),
            get_option_value(opt,'quality',0.95), # 0.0 - 1.0, 100%=1.0 95%=0.95 
            0, # smoothing 0=None
            1, # optimize  1=do optimize
            get_option_value(opt,'progressive',0), # progressive 0=Not progressive
            "%d dothiko all rights reserved" % lt.tm_year,
            0, # subsampling number,unknown. default=0
            1, # force baseline jpeg 1=force
            0, # restart marker,unknown default=0
            0) # dct algorithm,unknown default=0

def get_maximum_number_of_filename(dirname,fbase,ext):
    """
    with this function,you can get the maximum serialized number of filename

    example:

    when there is multiple number of files 
    which named final_image_X.jpg (X is serialized number) at /hoge/foo ...

    idx=get_maximum_number_of_filename('/hoge/foo','final_image_','.jpg')
    save_as_jpeg(fimg,'/hoge/foo/final_image_%d.jpg' % idx+1,0.98)
    """
    gpat="%s/%s*%s" % (dirname,fbase,ext)
    fpat=re.compile("%s(\d+)\%s" % (fbase,ext))
    hitlist=glob.glob(gpat)

    # needs to extract numbers for sort()
    # because ordinary sort() misunderstand numbered files
    # such as 'hoge10.jpg' is less than 'hoge9.jpg'.
    ro_sort=re.compile('(\d+)\.\S+$')
    def mysort(a,b):
        m=ro_sort.search(a)
        if m:
            a=int(m.groups()[0])
        else:
            return -1

        m=ro_sort.search(b)
        if m:
            b=int(m.groups()[0])
        else:
            return 1

        if a>b:
            return 1
        elif a<b:
            return -1
        else:
            return 0

    if len(hitlist) > 0:
        hitlist.sort(cmp=mysort)
        for idx in range(len(hitlist),0,-1): 
        # for various case,such as hogehoge4c.jpg is last of hitlist. 
        # this will fail to match.
            m=fpat.search(hitlist[idx-1])
            if m:
                return int(m.groups()[0])
            
    return -1

def export_numbered_jpg_file(img,basedir,prefix,quality,size=None):
    """
    utility function,for your convinience

    Arguments:
        size -- with this argument,you can scale export image.
                None means 'do not scale'.

                tuple of (width,height),but only width or height should be set.
                in other words,the other size component should be set as None.
                by setting None either width or height,
                function recognize which component should be used, 
                and calculate the other component automatically.
    """
   #idx=get_maximum_number_of_filename(basedir,prefix,'.jpg')
   #ofpath='%s/%s%d.jpg' % (basedir,prefix,idx+1)
   #simg=pdb.gimp_image_duplicate(img)
   #pdb.gimp_image_merge_visible_layers(simg,1) # clip to image
   #if size:
   #    nw,nh=get_scale_size(simg,size[0],size[1])
   #    scale_image(simg,nw,nh)
   #save_as_jpeg(simg,ofpath,quality)
   #pdb.gimp_image_delete(simg)

    opt={ "quality" : quality }
    # ,"progressive" : 0 }
    return export_numbered_file_common(img,basedir,prefix,".jpg",size,
            save_as_jpeg,opt)

def export_numbered_png_file(img,basedir,prefix,size=None):
    """
    utility function,for your convinience

    Arguments:
        size -- with this argument,you can scale export image.
                None means 'do not scale'.
                tuple of (width,height),but only width or height should be set.
                the other component should be set as None, and culclated automatically.
    """
   #idx=get_maximum_number_of_filename(basedir,prefix,'.png')
   #ofpath='%s/%s%d.png' % (basedir,prefix,idx+1)
   #simg=pdb.gimp_image_duplicate(img)
   #pdb.gimp_image_merge_visible_layers(simg,1) # clip to image
   #if size:
   #    nw,nh=get_scale_size(simg,size[0],size[1])
   #    scale_image(simg,nw,nh)
   #save_as_png(simg,ofpath)
   #pdb.gimp_image_delete(simg)
    
    return export_numbered_file_common(img,basedir,prefix,".png",size,
            save_as_png,None)

def export_numbered_file_common(img,basedir,prefix,ext,size,savefunc,opt):
    """
    utility function,for your convinience

    Arguments:
        size -- with this argument,you can scale export image.
                None means 'do not scale'.
                tuple of (width,height),but only width or height should be set.
                the other component should be set as None, and culclated automatically.
    """
    idx=get_maximum_number_of_filename(basedir,prefix,ext)
    ofpath='%s/%s%d%s' % (basedir,prefix,idx+1,ext)
    simg=pdb.gimp_image_duplicate(img) # because all save plugin need merged image,so dup this.
    pdb.gimp_image_merge_visible_layers(simg,1) # clip to image
    if size:
        nw,nh=get_scale_size(simg,size[0],size[1])
        scale_image(simg,nw,nh)
    savefunc(simg,ofpath,opt)
    pdb.gimp_image_delete(simg)
    if os.path.exists(ofpath):
        return ofpath # export success 
    return None # export failed(maybe insufficient disk space,lost connection,device failure,etc)
     
#-------------------------------------------------------------------------------
# layer related


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

def copy_layer_into_other_image(other_image,layer,position):
    """
    copy outside layer into other_image.

    Arguments:
        other_image -- this can be Image object or layer group.

        position -- this can be 
                    str(layer name)
                    int(index of priority,at toplevel layers),0 means (place this top) 
                                                             -1 means (place this last : same as None)
                    layer object(copied layer placed at above this)
                    NoneType (add to last)

    Returns:
        the copied layer which belongs to other_image
    """
    if hasattr(other_image,'image'):
        # other_image is actually layer group!!
        parent=other_image
        other_image=other_image.image
    else:
        parent=None
         
    nl=pdb.gimp_layer_new_from_drawable(layer, other_image)

    if type(position)==str:
        # position is name
        idx=get_layer_index(position)
    elif type(position)==int:
        # position is idx
        idx=position
    elif isinstance(position,gimp.Layer):
        # position is layer,which should be contained in other_image
        idx=get_layer_index(position)
        parent=position.parent
    elif position==None:
        # simply add
        idx=len(other_image.layers)

    if idx > len(other_image.layers) or idx < 0:
        idx=len(other_image.layers)


    pdb.gimp_image_insert_layer(other_image,nl,parent,idx)
    return nl

def snap_layer_position(layer_base,layer_snapped,priority=0):
    """
    snap layer_snapped position to layer_base.

    Arguments:
    priority -- 0 or 1 or -1
                0 means no priority changed.
                1 means layer_snapped placed below the layer_base
                -1 means layer_snapped placed over(prior to) the layer_base

    """
    bx,by=layer_base.offsets 
    layer_snapped.set_offsets(bx,by)
    if priority in (-1,1):
        idx=get_layer_index(layer_base)
        move_layer_priority(layer_snapped,layer_base.parent,idx+priority)
       #layer_base.image.insert_layer(layer_snapped,layer_base.parent,idx+priority)

def move_layer_priority(layer,parent,idx):
    """
    move(change) layer priority with index.

    Note:
        pdb and gimp has no way to change layers prioriry with index,for now.
        so I write this wrapper funciton.
    """

    nl=layer.copy()
    img=layer.image

    if parent==None:
        cnt=len(img.layers)
    else:
        cnt=len(parent.layers)

    if idx > cnt:
        idx=cnt

    oldname=layer.name
    img.remove_layer(layer)
    img.insert_layer(nl,parent,idx)
    nl.name=oldname

def get_layer_index(layer):
    """
    get layer index,within its parent(image or layer group)'s layers attribute.

    Arguments:
        layer -- layer object or name of layer
    Returns:
        priority index of layer
    """
         
    if layer.parent==None:
        layers=layer.image.layers
    else:
        layers=layer.parent.layers

    for idx,cl in enumerate(layers):
        if is_equal_layer(layer,cl):
            return idx
       #if type(layer)==str and layer==cl.name:
       #    return idx
       #elif cl==layer:
       #    return idx
    return -1 # should not happen...

def find_layer(img,name,walk_group=True):
    """
    find layer from image(or layer group)

    Arguments:
    img -- image or layer group
    name -- string(layer name) or regular-expression object
    walk_group -- when layergroup found,walk into it.
                  if this flag is False,then return the layergroup as return value.

    Returns:
        a tuple of
        ( layer priority index within its parent, the found layer)
        parent can get from layer.parent attribute.

    Note:
        layer names should be unique...
    """

    for idx,cl in enumerate(img.layers):
        if walk_group and hasattr(cl,'layers'): # this is layer group!!
            tpl=find_layer(cl,name)
            if tpl[1]!=None:
                return tpl
        elif is_equal_layer(cl,name):
                return (idx,cl)


    return (-1,None)

def scale_layer(layer,w,h,method,scale_itself=False):
    """
    method is 
    INTERPOLATION-NONE (0), 
    INTERPOLATION-LINEAR (1), 
    INTERPOLATION-CUBIC (2), 
    INTERPOLATION-LANCZOS (3) 
    """
    if not scale_itself:
        layer=duplicate_layer(layer)

    old_method=pdb.gimp_context_get_interpolation()
    pdb.gimp_context_set_interpolation(method)
    pdb.gimp_layer_scale(layer,w,h,1)
    pdb.gimp_context_set_interpolation(old_method)
    return layer

def set_layers_visiblity(image,layer,above,visible):
    """
    set layers visiblity,when after(or until) met the assigned layer.

    Arguments:
    layer --    the destination layer.this can be string or layer object.
    above --    boolean, if this is true,layer's visiblity should be changed 
                until the dest layer is found.
    visible --  boolean, the visiblity of layers.


    Returns:
    None
    """

    do_change=above

    for cl in image.layers:
        if do_change==False: 
            if is_equal_layer(cl,layer):
                do_change=not above
        else:
            cl.visible=visible


LAYER_TYPES=("<type 'gimp.Layer'>", "<type 'gimp.GroupLayer'>")    
def is_equal_layer(layerA,layerB):
    """
    uniformed utility wrapper function,to check layers equality.

    Arguments:
    layerA,layerB - these arguments can be either of 
                    strings,layer object,regular expression object

    Returns:
    return true when layerA equal (or presumably equal) to layerB
    when both of them are not layer object,exception should be raised.
    """

    if str(type(layerA)) in LAYER_TYPES  or str(type(layerB)) in LAYER_TYPES:
         
        if type(layerA)==str:
            return layerA==layerB.name
        elif isinstance(layerA,re._pattern_type):
            m=layerA.search(layerB.name)
            return m!=None
        else:
            # this case,we assume layerA is layer object.
            if type(layerB)==str:
                return layerA.name==layerB
            elif isinstance(layerB,re._pattern_type):
                m=layerB.search(layerA.name)
                return m!=None
            else: # both of them are layer.
                return layerA==layerB

    raise TypeError

def duplicate_layer(layer,pos=0):
    """
    Utility function,to automatically insert copied layer to its image.
    """
    nl=pdb.gimp_layer_copy(layer,0)
    pdb.gimp_image_insert_layer(layer.image,nl,None,pos)
    return nl
        

#-------------------------------------------------------------------------------
# others

def get_option_value(opt,d,dvalue):
    """
    will be used when get option value
    """
    try:
        return opt[d]
    except KeyError:
        return dvalue
    except TypeError:
        return dvalue

def ask_yesno(msg):
    """
    ask user interraction by gtk dialog.

    Arguments:
    msg -- the message to be shown

    Returns:
    0 when yes selected.
    1 when no selected.
    2 when cancel selected.
    """

    dialog = gtk.Dialog(msg, None, 0,
    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
    gtk.STOCK_NO, gtk.RESPONSE_NO,
    gtk.STOCK_YES, gtk.RESPONSE_YES))

    response = dialog.run()
    dialog.destroy()

    if response==gtk.RESPONSE_CANCEL:
        return 2
    elif response==gtk.RESPONSE_NO:
        return 1
    else:
        return 0

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


if __name__ == '__main__':
    print("TESTING...")
    class Image:
        def __init__(self,w,h):
            self.width=w
            self.height=h
            self.layers=[]
        def add_layer(self,l):
            self.layers.append(l)

    class Layer:
        def __init__(self,name,w,h):
            self.name=name
            self.width=w
            self.height=h

    t=Image(1000,400)
    t.add_layer(Layer('test1',100,100))
    t.add_layer(Layer('find_this',100,100))
    t.add_layer(Layer('test2',100,100))

    idx,l=find_layer(t,'find_this')
    print "%d:%s" % (idx,l.name)


