#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] layermove
#[desc] 座標指定でのレイヤ移動用スクリプト
#[version]
#0.1 初期リリース
#0.2 ウィジェット作成を自作ユーティリティモジュールを利用することに変更
#0.3 ウィンドウをバツ印クリック(destroy)時にアンドゥ状態がおかしくなるバグを修正
#[end]

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
#   Copyright (C) 2013 dothiko(http://dothiko.cocolog-nifty.com/) 

from gimpfu import *
import gimpplugin
import pygtk
pygtk.require("2.0")
import gtk
import dothikoutil # need this for creating widgets

class dothiko_layermove_plugin(gimpplugin.plugin):
    def init(self):
        pass

    def quit(self):
        pass

    def query(self):
        gimp.install_procedure(
                "python_fu_layermove",
                "layer move script for gimp",
                "",
                "dothiko",
                "kakukaku world",
                "jan 2013", 
                "<Image>/Python-Fu/layer/layermove", 
                "*",
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
        self.lines = 0
        self.tableX = 4
        self.tableY = 1
        self.theWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.theWindow.set_title("python-fu layermove")
        self.theWindow.set_resizable(False)
        self.theWindow.show()
        self.theWindow.connect("destroy",self.destroy)
        self.vbox = gtk.VBox(False,8)
        self.vbox.show()
        self.theWindow.add(self.vbox)
        self.mainTable = gtk.Table(self.tableY,self.tableX,True)
        self.mainTable.show()
        self.vbox.add(self.mainTable)
        self.basebox = gtk.VBox(False,8)
        self.basebox.show()
        self.vbox.add(self.basebox)
        self.hbuttonbox = gtk.HButtonBox()
       #self.hbuttonbox.set_proerty("layout-style",gtk.BUTTONBOX_END)
        self.hbuttonbox.props.layout_style=gtk.BUTTONBOX_END
        self.hbuttonbox.show()
        self.vbox.add(self.hbuttonbox)
        self.checkboxes = []
        self.labels = []
        self.entries = []
        self.combos = []
        self.theWindow.resize(200,50)

    def okbutton(self, widget):
        if self.destlayer:
            x=int(self.spin_x.get_value())
            y=int(self.spin_y.get_value())

            if self.x_right_check.get_active():
                x=self.image.width - (self.destlayer.width + x)
            if self.y_bottom_check.get_active():
                y=self.image.height - (self.destlayer.height + y)

            self.destlayer.set_offsets(x,y)
            pdb.gimp_displays_flush()

        gtk.main_quit()

    def quitbutton(self, widget):
        gtk.main_quit()

    def init_window(self,name,x,y):
        newbut2 = gtk.Button(None,gtk.STOCK_OK)
        newbut2.connect("clicked",self.okbutton)
        newbut2.show()
        self.hbuttonbox.add(newbut2)
        newbut3 = gtk.Button(None,gtk.STOCK_CANCEL)
        newbut3.connect("clicked",self.quitbutton)
        newbut3.show()
        self.hbuttonbox.add(newbut3)

        t_label= gtk.Label("layer name:" + str(name))
        t_label.show()
        self.basebox.add(t_label)

        def setup_input_block(name,init_val):
            t_hbox = gtk.HBox(False,1)
            t_hbox.show()
            t_label= gtk.Label(name)
            t_label.props.justify=gtk.JUSTIFY_RIGHT
            t_label.show()
            t_hbox.add(t_label)
            t_adj=gtk.Adjustment(init_val,-100000,100000,1,100)
            t_spin=gtk.SpinButton(t_adj,1.0,0)
            t_spin.show()
            t_hbox.add(t_spin)
            self.basebox.add(t_hbox)
            return t_spin

        self.spin_x=setup_input_block("x:",x)
        self.x_right_check= dothikoutil.create_checkbutton(self.basebox,"右端からのオフセット値として指定")
        self.spin_y=setup_input_block("y:",y)
        self.y_bottom_check= dothikoutil.create_checkbutton(self.basebox,"下端からのオフセット値として指定")


    def python_fu_layermove(self,run_mode,image,drawable):
        self.image = image
        self.drawable = drawable
        active=image.active_layer
        pdb.gimp_image_undo_group_start(self.image)
        try:
            if active:
                x,y=active.offsets
                self.init_window(active.name,x,y)
                self.destlayer=active
                gtk.main()
        except Exception,e:
            print str(e)
        finally:
            pdb.gimp_image_undo_group_end(self.image)


    def destroy(self, widget, data=None):
        # Ending undo group should be done in the finally block at python_fu_layermove()
        gtk.main_quit()

if __name__ == '__main__':
    dothiko_layermove_plugin().start()






