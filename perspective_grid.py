#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#[license] GPLv3
#[plugin]
#[name] perspective-grid-layer
#[desc] 
#透視法に基づくグリッドの描かれたレイヤを選択されたパスに基づいて生成
#[version]
#0.1 初期リリース
#0.2 背景色塗りつぶし機能追加、バグフィックス
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
#   Copyright 2014 dothiko(http://dothiko.hatenablog.com/) 


from gimpfu import *
from vector2d import *
import random


class Perspective_grid:

    def __init__(self,image,thick_size,mid_size,thin_size):
        self.BD=vector2d()
        self.AB=vector2d()
        self.BC=vector2d()
        self.AC=vector2d()
        self.img=image
        self.id=random.random() * 2147483647
        self.sizes=(thick_size,mid_size,thin_size)
        

    def main(self,raw_stroke,recursive_max,fill_bg):
        margin=32


        # the gridpt contains 4 lists,they are list of vectors to represent grid startpoints
        # that index should be...
        #  
        #  A---0---B
        #  |       |
        #  3   c   1
        #  |       |
        #  D---2---C
        #  
        #  the each number of ridges is the index of grid startpoint list(self.gridpt).

        self.m_gridpt=([],[],[],[])
        
        self.m_basevectors=[]
        for i in range(0,4):
            cv=vector2d()
            cv.x=raw_stroke[i*6+2]
            cv.y=raw_stroke[i*6+3]
            self.m_basevectors.append(cv)

        # culculate min-max coordinate of assigned vectors
        # and use them for layer dimension.
        min_x=min(self.m_basevectors,key=lambda v:v.x).x
        min_y=min(self.m_basevectors,key=lambda v:v.y).y
        max_x=max(self.m_basevectors,key=lambda v:v.x).x
        max_y=max(self.m_basevectors,key=lambda v:v.y).y

        width=int(max_x - min_x)+margin*2
        height=int(max_y - min_y)+margin*2
        top=int(min_y-margin)
        left=int(min_x-margin)

        # setup vanising points
        self.m_vp=(vector2d(),vector2d())

        self.get_crossed_point(self.m_vp[0],
                           self.m_basevectors[1],
                           self.m_basevectors[0],
                           self.m_basevectors[2],
                           self.m_basevectors[3]);

        self.get_crossed_point(self.m_vp[1],
                          self.m_basevectors[2],
                          self.m_basevectors[0],
                          self.m_basevectors[3],
                          self.m_basevectors[1]);


        self.m_recursive_max=recursive_max
        self.divide_plane()


        layer = gimp.Layer(self.img, "perspective grid layer",
                width, height, RGBA_IMAGE, 100, NORMAL_MODE)
        self.img.add_layer(layer,0)
        
        layer.set_offsets(left,top)
        self.draw_grid(layer,fill_bg)

    def get_crossed_point(self,ov,a,b,c,d):
        """
        get crossed point from vectors.

        Arguments:
        ov -- output vector, to consider recycle and low memory usage.
        a,b,c,d -- the vectors

        Returns:
        the cross-product of vectors,which indicates whether the crossed point actually crossed 
        when that value is positive.when negative,they are not crossed but to be crossed.
        """
        vector2d.sub(self.BD,d,b);
        vector2d.sub(self.AB,b,a);
        vector2d.sub(self.BC,c,b);
        vector2d.sub(self.AC,c,a);
        cross_AB=vector2d.cross(self.BD,self.AB);
        cross_BC=vector2d.cross(self.BD,self.BC);
        try:
            ratio=cross_AB / (cross_AB + cross_BC);
        except ZeroDivisionError:
            # vanising point dose not exist 
            ov.x=None
            ov.y=None
            return None

        ov.x=a.x + ratio*(self.AC.x);
        ov.y=a.y + ratio*(self.AC.y);

        return ratio;


    def divide_plane(self):
        self.divide_recursive(self.m_vp[0],
                         self.m_gridpt[0],self.m_gridpt[2],
                         self.m_basevectors[0],self.m_basevectors[1],
                         self.m_basevectors[2],self.m_basevectors[3],0);

        self.divide_recursive(self.m_vp[1],
                         self.m_gridpt[1],self.m_gridpt[3],
                         self.m_basevectors[1],self.m_basevectors[2],
                         self.m_basevectors[3],self.m_basevectors[0],0);


        # sort all points from base-vector
        tv=vector2d()

        def sort_key_A(cv):
            # get distance from corner "A"
            vector2d.sub(tv,cv,self.m_basevectors[0])
            return tv.get_scalar()

        def sort_key_D(cv):
            # get distance from corner "D"
            vector2d.sub(tv,cv,self.m_basevectors[3])
            return tv.get_scalar()

        def sort_key_B(cv):
            # get distance from corner "B"
            vector2d.sub(tv,cv,self.m_basevectors[1])
            return tv.get_scalar()

        self.m_gridpt[0].sort(key=sort_key_A)
        self.m_gridpt[1].sort(key=sort_key_B)
        self.m_gridpt[2].sort(key=sort_key_D)
        self.m_gridpt[3].sort(key=sort_key_A)

    def divide_recursive(self,vp,gridpt1,gridpt2,a,b,c,d,depth):
        if(depth > self.m_recursive_max):
            return;

        self.divide_single_plane(vp,
                            gridpt1,gridpt2,
                            a,b,
                            c,d);

        hab=gridpt1[-1];
        hcd=gridpt2[-1];

        self.divide_recursive(vp,gridpt1,gridpt2,
                         a,hab,
                         hcd,d,depth+1);

        self.divide_recursive(vp,gridpt1,gridpt2,
                         hab,b,
                         c,hcd,depth+1);

    def divide_line(self,array,targetpt,vp,a,b):
        curpt=vector2d();
        self.get_crossed_point(curpt,
                          vp,
                          a,
                          targetpt,
                          b);

        array.append(curpt); 
        return curpt;

    def divide_single_plane(self,vp,array1,array2,a,b,c,d):
        center=vector2d();
        self.get_crossed_point(center,
                          a,
                          b,
                          c,
                          d);

        if vp.x==None:
            # this means...vanising point does not exist!!(the target ridges are palallel!)
            nvp=a-d
            nvp.normalize_self()
            nvp+=center
            self.divide_line(array1,center,nvp,a,b);
            self.divide_line(array2,center,nvp,c,d);
        else:
            self.divide_line(array1,center,vp,a,b);
            self.divide_line(array2,center,vp,c,d);
        return center

    @staticmethod
    def generate_stroke_list(srcarray):
        """
        generate gimp-stroke array from srcarray.

        Arguments:
        srcarray -- the array of vector

        Returns:
        generated list
        """

        retlst=[]
        for cv in srcarray:
            i=0
            while i<3:
                retlst.append(cv.x)
                retlst.append(cv.y)
                i+=1

        return retlst

    @staticmethod
    def get_control_point_count(stroke):
        return len(stroke)/6


    def draw_grid(self,layer,fill_bg):


        pathes=[]

        def generate_pathobj(dst_size,force):
            if self.sizes[0]==dst_size and force==False:
                return pathes[0]
            else:
                cp=pdb.gimp_vectors_new(self.img,"pg_path_%d_%08x" % (dst_size,self.id))
                pdb.gimp_image_insert_vectors(self.img,cp,None,0)
                return cp


        for i in range(0,3):
            pathes.append(generate_pathobj(self.sizes[i],i==0))


        # setup grid base rectangle
        ts=Perspective_grid.generate_stroke_list(self.m_basevectors)


        # setup grid lines
        def append_CAC_point(ss,cv):
            for r in range(0,3):# to satisfy 'CAC' control point format
                ss.append(cv.x)
                ss.append(cv.y)

        # the original rectangle
        ss=[]
        for i in range(0,4):# m_basevectors index
            append_CAC_point(ss,self.m_basevectors[i])

        sid=pdb.gimp_vectors_stroke_new_from_points(pathes[0],0,
                len(ss),ss,True)

        if fill_bg:
            cursel=pdb.gimp_selection_save(self.img)
            pdb.gimp_image_select_item(self.img,2,pathes[0]) # replace
            pdb.gimp_edit_fill(layer,1) # bg fill
            pdb.gimp_image_select_item(self.img,2,cursel)

        # inner grid
        for i in range(0,2):# m_gridpt index
            for t in range(0,len(self.m_gridpt[i])):
                ss=[]
                append_CAC_point(ss,self.m_gridpt[i][t])
                append_CAC_point(ss,self.m_gridpt[i+2][t])

                if t != int(len(self.m_gridpt[i]) / 2):
                    sid=pdb.gimp_vectors_stroke_new_from_points(pathes[2],0,
                            len(ss),ss,0)
                else:
                    sid=pdb.gimp_vectors_stroke_new_from_points(pathes[1],0,
                            len(ss),ss,0)
        


        # save current contexts        
        pdb.gimp_context_push()

        # now,draw them.
        pdb.gimp_context_set_paint_method("gimp-paintbrush")
        bname="brush_%08x" % self.id
        pdb.gimp_brush_new(bname)
        pdb.gimp_brush_set_shape(bname,0)# 0 Round brush 1=square brush
        pdb.gimp_context_set_brush(bname)
        pdb.gimp_context_set_dynamics("Dynamics Off")
        pdb.gimp_brush_set_radius(bname,self.sizes[0]*2) # i dont know really how it works...
        pdb.gimp_brush_set_hardness(bname,0.7)# blurness
        pdb.gimp_brush_set_spacing(bname,5)

        def draw_single_path(dpath):
            if len(dpath.strokes)==0 or len(dpath.strokes[0].points[0])==0:
                    pass
            else:
                pdb.gimp_edit_stroke_vectors(layer,dpath)

            # deleting path
            pdb.gimp_image_remove_vectors(self.img,dpath)

        for i in range(0,3):
            pdb.gimp_context_set_brush_size(self.sizes[i])
            draw_single_path(pathes[i])

        pdb.gimp_brush_delete(bname)

        # do not forget to pop context.
        pdb.gimp_context_pop()

    def draw_stroke(self,stroke):
        pass

def python_fu_perspective_grid_func(a_img,a_drawable,divcount=2,delete_srcpath=False,thickness=4,same_thickness=False,fill_bg=False):

    # check the current active vector is suitable for later operations.
    v=pdb.gimp_image_get_active_vectors(a_img)
    if v==None:
       #pdb.gimp_message("please select a rectangular path")
        pdb.gimp_message("矩形パスを選択してください。")
        return

    if len(v.strokes)!=1:
       #pdb.gimp_message("the stroke should be a rectangle,and only one at path.")
        pdb.gimp_message("このスクリプトは、ひとつの矩形だけを持つパスにしか対応しません")
        return

    ctl_cnt=len(v.strokes[0].points[0])/6

    if ctl_cnt!=4:
       #pdb.gimp_message("the stroke should be a rectangle.this stroke of path has %d control points." % ctl_cnt)
        pdb.gimp_message("このパスは %d つの制御点を持ち、矩形ではありません。" % ctl_cnt)
        return



    if same_thickness:
        thick_size=mid_size=thin_size=thickness
    else:
        thick_size=thickness
        mid_size=thick_size*0.75
        thin_size=mid_size*0.5

    # start of groping undoable operations
    try:
        pdb.gimp_image_undo_group_start(a_img)

        p=Perspective_grid(a_img,thick_size,mid_size,thin_size)
        p.main(v.strokes[0].points[0],divcount,fill_bg)

        if delete_srcpath:
            pdb.gimp_image_remove_vectors(a_img,v)


    except Exception,e:
        print(str(e))
        import traceback
        print(traceback.format_exc())
    # end of grouping undoable operations
    finally:
        pdb.gimp_image_undo_group_end(a_img)





register(
        "python_fu_perspective_grid_func",
        "perspective-grid-layer",
        "creating perspective grid layer from a rectangular-formed path.",
        "dothiko",
        "kakukaku world",
        "dec 2014", 
        "<Image>/Python-Fu/layer/perspective-grid-layer", 
        "RGB*,GRAY*",
        [
            (PF_OPTION,"divcount","分割数",1,("4分割(2x2)","16分割(4x4)","64分割(8x8)","256分割(16x16)")),
            (PF_BOOL,"delete_srcpath","対象パスを消去する",True),
            (PF_ADJUSTMENT,"thickness","描線の太さ",4,(1,8,1)),
            (PF_BOOL,"same_thickness","全て同じ太さにする",False),
            (PF_BOOL,"fill_bg","背景色で塗りつぶす",False),
        ],
        [],
        python_fu_perspective_grid_func)


main()

