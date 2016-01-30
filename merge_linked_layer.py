#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from gimpfu import *

def python_fu_merge_linked_layer(a_img,a_drawable):

    pdb.gimp_image_undo_group_start(a_img)

    try:

        # visible states saved into a dict. 
        vstates={}

        for cl in a_img.layers:
            vstates[cl.name]=cl.visible
           #print "%s : %s" % (cl.name, str(cl.visible))
            cl.visible=False

        for cl in a_img.layers:
            if cl.linked:
                cl.visible=True

        merged_layer=pdb.gimp_image_merge_visible_layers(a_img,0)

        for cl in a_img.layers:
            if vstates[cl.name] or cl.ID==merged_layer.ID:
               #print "%s to show" % cl.name
                cl.visible=True

    except ValueError:
        pass
    finally:
        pdb.gimp_image_undo_group_end(a_img)


    
    pass


register(
        "python_fu_merge_linked_layer",
        "merge linked layers",
        "merge linked layers",
        "dothiko",
        "dothiko",
        "2013",
        "<Image>/Python-Fu/linked/merge-linked-layer",
        "RGB*,GRAY*",
        [
        ],
        [],
        python_fu_merge_linked_layer)


main()






if __name__ == '__main__':

    pass


