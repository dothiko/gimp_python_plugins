#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class HSV:

    def __init__(self,rgb=None):
        if rgb:
            r,g,b=rgb
            self.set(r,g,b)

    def set(self,r,g,b):
        """
        hue  0.0 - 360.0
        saturation  0.0 - 1.0
        value       0.0 - 1.0
        """
        MAX=float(max(max(r,g),b))
        MIN=float(min(min(r,g),b))

        # hue
        if r==g==b:
            self.h=0
        elif r==MAX:
            self.h=(g-b)/(MAX-MIN)+0
        elif g==MAX:
            self.h=(b-r)/(MAX-MIN)+2.0
        elif b==MAX:
            self.h=(r-g)/(MAX-MIN)+4.0

        if self.h<0:
            self.h+=6.0

        self.h/=6.0 # justfying Hue into 0.0 - 1.0


       #elif r==MAX:
       #    self.h=60.0*(g-b)/(MAX-MIN)+0
       #elif g==MAX:
       #    self.h=60.0*(b-r)/(MAX-MIN)+120
       #elif b==MAX:
       #    self.h=60.0*(r-g)/(MAX-MIN)+240
       #
       #if self.h<0:
       #    self.h+=360
       #
        # saturation
        if MAX!=0:
            self.s=(MAX-MIN)/MAX
        else:
            self.s=0

        # value
        self.v=MAX/255.0

    def set_hue_from_angle(self,a):
        self.h=((a  % 360.0) / 360.0)

    def justify(self):
        if self.h > 1.0 or self.h < 0.0:
            self.h%=1.0

        if self.s < 0:
            self.s=0
        elif self.s > 1.0:
            self.s=1.0

        if self.v < 0:
            self.v=0
        elif self.v > 1.0:
            self.v=1.0

    def get_rgb(self):
        self.justify()
        r=g=b=self.v
       #hf=self.h/60.0
        hf=self.h*6.0
        hi=int(hf) % 6
        f=hf-float(hi)
        ts=1.0-self.s
        trf=1.0 - self.s * (1.0 - f)
        tf=1.0 - self.s * f
        if hi==0:
            g*=trf
            b*=ts
        elif hi==1:
            r*=tf
            b*=ts
        elif hi==2:
            r*=ts
            b*=trf
        elif hi==3:
            r*=ts
            g*=tf
        elif hi==4:
            r*=trf
            g*=ts
        elif hi==5:
            g*=ts
            b*=tf

        return (int(r*255.0),int(g*255.0),int(b*255.0))



if __name__ == '__main__':

    h=HSV()
    r,g,b=(242,201,172)
    h.set(r,g,b)
    print "input:%d,%d,%d" % (r,g,b)
    print (h.h,h.s,h.v)
    print h.get_rgb()

    pass


