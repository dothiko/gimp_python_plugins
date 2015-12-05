#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] layerjump
#[desc] 
#あらかじめ設定されたプリセットに従い、アクティブレイヤを移動する
#[version]
#0.1 初期リリース
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
import re

# do not change this UUID / このUUIDを変更してはいけません(parasiteを追尾できなくなる)
LAYER_JUMP_UUID="1af44cde-aa9e-4445-98de-e629fb731ecf"

# presets 
PRESETS=(
        ('主線',re.compile('^-+$')), 
        ('背景', ('background','背景')) ,
        ('パレット','palette'),
        (None,0),# ユーザー定義 0
        (None,1),
        (None,2),
        (None,3),# ユーザー定義 3
        ('戻る',None)
        )

# (ラベル, オブジェクト) のタプルを格納するタプルで、
# オブジェクトには文字列・正規表現オブジェクト・それらを格納したタプルが指定できる。
# オブジェクトがNoneである場合、「直前のレイヤジャンプ実行前のアクティブレイヤ」に戻ることになる。
# backquoteキーで「戻る」を指定したいため、常に「戻る」プリセットは最後にしなくてはならない。

import gimpplugin
import pygtk
pygtk.require("2.0")
import gtk
import gobject
import pickle


class Dothiko_plugin_layerjump(gimpplugin.plugin):
    def init(self):
        # [CAUTION] this is not python constructor __init__. this is gimp plugin init.
        pass

    def quit(self):
        pass

    def query(self):
        gimp.install_procedure(
                "python_fu_layerjump",
                "layerjump",
               #"jump to predefined named layer", # for English
                "登録されているレイヤにアクティブフォーカスを素早く移動する",
                "dothiko",
                "kakukaku world",
                "jan 2014", 
                "<Image>/Python-Fu/layer/layerjump", 
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
        self.thiswindow.set_title("LAYERJUMP for GIMP")
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

        self.user_defines=[]
        self.userdef_start=-1
        self.userdef_end=-1
        self.return_layer_name=None

    @staticmethod
    def generate_userdefine_listmodel(idx,name):
        return ("ユーザー定義 %d:%s" % (idx+1,name),)


    def init_window(self):
        newbut = gtk.Button("ユーザー定義に登録")
        newbut.connect("clicked",self.register_userdefine)
        newbut.show()
        self.hbuttonbox.add(newbut)

        newbut = gtk.Button("OK",gtk.STOCK_OK)
        newbut.connect("clicked",self.on_okbutton)
        newbut.show()
        self.hbuttonbox.add(newbut)
        self.okbutton=newbut

        newbut = gtk.Button(None,gtk.STOCK_CANCEL)
        newbut.connect("clicked",self.quitbutton)
        newbut.show()
        self.hbuttonbox.add(newbut)


        tbox = gtk.HBox(False,8)
        tbox.show()
        t_label= gtk.Label("移動先：")   
       #t_label= gtk.Label("blur radius:")    # for English
        t_label.show()
        tbox.add(t_label)

        lmdl=gtk.ListStore(gobject.TYPE_STRING)
        self.listmodel=lmdl
        for idx,pst in enumerate(PRESETS):
            label,contents=pst
            if label:
                lmdl.append((label,))
            else:
                # ユーザー定義テーブル
                if self.userdef_start==-1:
                    self.userdef_start=idx

                self.userdef_end=idx#-self.userdef_start

                try:
                    tn=self.user_defines[contents]
                except IndexError:
                    self.user_defines.append(None)
                    tn="空"
                lmdl.append(Dothiko_plugin_layerjump.generate_userdefine_listmodel(idx-self.userdef_start,tn))
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

        helplabel= gtk.Label("フルキーの1ー%d : 対象レイヤにジャンプ\nバッククオートで「戻る」\nCTRL同時押下でユーザー定義を設定(%d-%d)" % (len(PRESETS),self.userdef_start+1,self.userdef_end+1))   
       #helplabel= gtk.Label("key of 1ー%d : direct jump to the assigned layer\nbackquote key to return the previous active layer\nregister user-defined jump layer with CTRL+(%d-%d)" % (len(PRESETS),self.userdef_start+1,self.userdef_end+1))   
        helplabel.show()
        self.basebox.add(helplabel)


    def python_fu_layerjump(self,run_mode,image,drawable):
        self.image = image
        self.drawable = drawable
        active=image.active_layer
        self.get_parasite()

        if active:
            self.init_window()
            gtk.main()
            # when OK button pressed,self.okbutton() should be called. 
            # so main processing should be executed at self.okbutton()


    def destroy(self, widget, data=None):
        self.quitbutton(widget)


    def find_layer_from_preset(self,preset):
        name,content=preset
        return self.find_layer_from_content(content) 

    def find_layer_from_content(self,content):
        if type(content)==str:
            for cl in self.image.layers:
                if cl.name==content:
                    return cl
        elif type(content)==tuple:
            for cc in content:
                cl=self.find_layer_from_content(cc)
                if cl:
                    return cl
        elif hasattr(content,'match') and hasattr(content,'pattern'): #isinstance(content,re._pattern_type):
            for cl in self.image.layers:
                m=content.search(cl.name)
                if m:
                    return cl
        elif type(content)==int:
            # ユーザー定義テーブル
            if self.user_defines[content]!=None:
                # basically, find_layer_from_content can process None argument
                # but it is for 'return' functionary,so ignore None here.
                return self.find_layer_from_content(self.user_defines[content])

        elif content==None:
            # return previous
            if self.return_layer_name:
                return self.find_layer_from_content(self.return_layer_name)

        return None

    def do_jump(self,idx):
       #pdb.gimp_image_undo_group_start(self.image)
        try:
            cl=self.find_layer_from_preset(PRESETS[idx])
            if cl:
                old_active=self.image.active_layer.name
                pdb.gimp_image_set_active_layer(self.image,cl)
                gimp.message('レイヤ %sに移動' % cl.name)
                self.return_layer_name=old_active # return-layer set here,because setting active layer may fail.
                self.set_parasite()
            else:
                gimp.message('移動先レイヤ(%s)は、見つかりませんでした' % PRESETS[idx][0])

        except Exception,e:
            import traceback
            print(traceback.format_exc())
        finally:
           #pdb.gimp_image_undo_group_end(self.image)
            pass

    def set_parasite(self):
        self.image.parasite_detach(LAYER_JUMP_UUID)
        try:
            curdata=(self.return_layer_name,self.user_defines)
            cp=gimp.Parasite(LAYER_JUMP_UUID,PARASITE_PERSISTENT,pickle.dumps(curdata))
            self.image.parasite_attach(cp)
        except Exception,e:
            print str(e)

    def get_parasite(self):
        try:
            cp=pdb.gimp_image_get_parasite(self.image,LAYER_JUMP_UUID)
            curdata=pickle.loads(cp.data)
            self.return_layer_name=curdata[0]
            self.user_defines=curdata[1]
        except Exception,e:
            print("[INFO] layerjump.py@get_parasite failed.(this is not error)")
            self.return_layer_name=None

    def mark_userdefine(self,idx):
        uidx=idx-self.userdef_start
        if PRESETS[idx][0]==None:
            # ユーザー定義テーブル
            self.user_defines[uidx]=self.image.active_layer.name
            self.listmodel[idx]=Dothiko_plugin_layerjump.generate_userdefine_listmodel(uidx,self.user_defines[uidx])
            self.set_parasite()
            gimp.message('ユーザー定義アイテム %dを登録しました' % uidx+1)
                              
    #------------------------------------------------------------ 
    # handlers
    
    def register_userdefine(self, widget):

        idx=self.combo.get_active()
        if idx>=self.userdef_start and idx<=self.userdef_end:
            self.mark_userdefine(idx)
        else:
            gimp.message('ユーザー定義アイテムが選択されていません')


    
    def on_okbutton(self, widget):
        idx=self.combo.get_active()

        if idx >= 0:
            self.do_jump(idx)

        gtk.main_quit()


    def quitbutton(self, widget):
        gtk.main_quit()

    def key_released(self,widget,data):
        if data.keyval==gtk.keysyms.Escape:
            self.quitbutton(widget)
        elif data.keyval==gtk.keysyms.Return:
            self.on_okbutton(widget)
        else:
           #print data.keyval
            if data.keyval==ord('`'):# backquote key.
                self.do_jump(-1)
                self.quitbutton(widget)
            else:
                idx=data.keyval-ord('1') # keyvalue 49 means the '1' key of keyboard
                if idx>=0 and idx < len(PRESETS):
                    if not (data.state & gtk.gdk.CONTROL_MASK == gtk.gdk.CONTROL_MASK):
                        # no ctrl pressed
                        self.do_jump(idx)
                    else:
                        # ctrl pressed - SET MARK IT!!
                        self.mark_userdefine(idx)


                    self.quitbutton(widget)




if __name__ == '__main__':
    Dothiko_plugin_layerjump().start()


