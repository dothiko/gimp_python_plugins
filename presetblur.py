#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] presetblur
#[desc] 
#あらかじめ設定されたプリセットでplug_in_gaussを用いてぼかす
#[version]
#0.1 初期リリース
#0.2 プリセットを増やす
#0.3 キーボードでの実行に対応。これでより素早い操作が可能になった
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
#   Copyright (C) 2014 dothiko(http://dothiko.blog.fc2.com/) 


from gimpfu import *


# presets are pixel-size and method(0=IIR, 1=RLE)
PRESETS=((8,0), (16,0), (24,0) , (32,0), (48,0), (64,0),(128,0),(256,0))

import gimpplugin
import pygtk
pygtk.require("2.0")
import gtk
import gobject

class Dothiko_plugin_presetblur(gimpplugin.plugin):
    def init(self):
        pass

    def quit(self):
        pass

    def query(self):
        gimp.install_procedure(
                "python_fu_presetblur",
                "presetblur",
               #"executing plug_in_gauss with preset value,for faster operation.", # for English
                "ガウスぼかしをプリセットされた値で素早く実行する",
                "dothiko",
                "kakukaku world",
                "jan 2014", 
                "<Image>/Python-Fu/others/presetblur", 
                "RGB*,GRAY*",
                PLUGIN,
                [
                    ((PDB_INT32),"run_mode","RUN mode"),
                    ((PDB_IMAGE),"image","Image"),
                    ((PDB_DRAWABLE),"drawable","Drawable")
                ],
                []
                )
                
        pass


    def __init__(self):
        self.thiswindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.thiswindow.set_title("TITLE")
        self.thiswindow.set_resizable(False)
        self.thiswindow.show()
        self.thiswindow.connect("destroy",self.destroy)
        outervbox = gtk.VBox(False,8) # this 'outerbox' is to form entire dialog
        outervbox.show()
        self.thiswindow.add(outervbox)
        self.basebox = gtk.VBox(False,8) # this 'self.basebox' is to contain plugin widgets
        self.basebox.show()
        outervbox.add(self.basebox)
        self.hbuttonbox = gtk.HButtonBox()
        self.hbuttonbox.props.layout_style=gtk.BUTTONBOX_END
        self.hbuttonbox.show()
        outervbox.add(self.hbuttonbox)

        self.thiswindow.resize(200,50) # size should be customizeable
        # for now, other initilizations are executed at self.init_window()
        # which called from self.python_fu_presetblur()

        self.thiswindow.connect("key-release-event",self.key_released)
        self.thiswindow.add_events(gtk.gdk.KEY_RELEASE_MASK)


    def init_window(self):
        newbut = gtk.Button("OK",gtk.STOCK_OK)
        newbut.connect("clicked",self.okbutton)
        newbut.show()
        self.hbuttonbox.add(newbut)
        self.okbutton=newbut

        newbut = gtk.Button(None,gtk.STOCK_CANCEL)
        newbut.connect("clicked",self.quitbutton)
        newbut.show()
        self.hbuttonbox.add(newbut)

        tbox = gtk.HBox(False,8)
        tbox.show()
        t_label= gtk.Label("ぼかしサイズ：")   
       #t_label= gtk.Label("blur radius:")    # for English
        t_label.show()
        tbox.add(t_label)

        lmdl=gtk.ListStore(gobject.TYPE_STRING)
        for ci in PRESETS:
            lmdl.append(("%dピクセル" % ci[0],))
           #lmdl.append(("%d pixel" % ci[0],)) # for English

        cell=gtk.CellRendererText()
             
        combo=gtk.ComboBox(lmdl)
        combo.pack_start(cell,True)
        combo.add_attribute(cell,'text',0)
        combo.set_active(0)
        combo.show()
        tbox.add(combo)
        self.basebox.add(tbox)
        self.combo=combo
        self.model=lmdl


        # sample codes
       #txtbuf=gtk.TextBuffer()
       #self.txtbuf=txtbuf
       #
       #t_frame=gtk.Frame()
       #t_frame.set_shadow_type(gtk.SHADOW_IN)
       #t_frame.show()
       #
       #txtview=gtk.TextView(txtbuf)
       #txtview.set_wrap_mode(gtk.WRAP_CHAR)
       #txtview.show()
       #t_frame.add(txtview)
       #self.basebox.add(t_frame)
       #self.txtview=txtview


    def python_fu_presetblur(self,run_mode,image,drawable):
        self.image = image
        self.drawable = drawable
        active=image.active_layer

        if active:
            self.init_window()
            gtk.main()
            # when OK button pressed,self.okbutton() should be called. 
            # so main processing should be executed at self.okbutton()


    def destroy(self, widget, data=None):
        self.quitbutton(widget)



    def do_blur(self,idx):
        pdb.gimp_image_undo_group_start(self.image)
        try:
            size,method=PRESETS[idx]
            pdb.plug_in_gauss(self.image,
                              self.image.active_layer,
                              size,size,
                              method)
            pdb.gimp_displays_flush()
            gimp.message('プリセット %d (%dピクセル)のガウスぼかしを実行' % (idx,size))
           #gimp.message('gauss-blur operation of preset %d (%dpixel) has done.' % (idx,size)) # for English
        except Exception,e:
            print(str(e))
        finally:
            pdb.gimp_image_undo_group_end(self.image)
    #------------------------------------------------------------ 
    # handlers
    
    def okbutton(self, widget):
        idx=self.combo.get_active()

        if idx >= 0:
            self.do_blur(idx)

        gtk.main_quit()


    def quitbutton(self, widget):
        gtk.main_quit()

    def key_released(self,widget,data):
        if data.keyval==gtk.keysyms.Escape:
            self.quitbutton(widget)
        else:
            idx=data.keyval-49 # keyvalue 49 means the '1' key of keyboard
            if idx>=0 and idx < len(PRESETS):
                self.do_blur(idx)
                if not (data.state & gtk.gdk.CONTROL_MASK == gtk.gdk.CONTROL_MASK):
                    self.quitbutton(widget)

if __name__ == '__main__':
    Dothiko_plugin_presetblur().start()


