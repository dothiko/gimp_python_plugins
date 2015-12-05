#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math

class vector2d:

    def __init__(s,x=0.0,y=0.0):    
        s.x=x
        s.y=y

    def __repr__(self):
        return "vector (%f , %f)" % (self.x , self.y)

    def __add__(s,other):
        return vector2d(
                s.x+other.x,
                s.y+other.y
                )

    def __iadd__(s,other):
        s.x+=other.x
        s.y+=other.y
        return s

    def __sub__(s,other):    
        return vector2d(
                s.x-other.x,
                s.y-other.y
                )

    def __isub__(s,other):
        s.x-=other.x
        s.y-=other.y
        return s

    def dot(s,other):
        return s.x*other.x + s.y*other.y
    
    def cross(s,other):
        """
        in math,there is no cross-product in 2D vector.
        cross-product can be in only 3D vector.
        but for convinience,I created cross products
        thats treat 2d vector as virtually 3d vector
        by adding fixed Z axis value(i.e, z=1)
        and this method returns only culculated Z value
        
        if this Z value is NEGATIVE,
        the 'other' vector locates ...
        -> counter-clockwise from this vector @ screen-coordinate(or right-handed-system)
        -> clockwise from this vector @ ordinary-coordinate(left-handed-system)
        """
        return s.x*other.y-other.x*s.y 


    def __mul__(s,other):

        if type(other)==float:
            return vector2d(
                s.x*other,
                s.y*other
                )
        
        elif type(other)==int:
            
            other = float(other)
            return vector2d(
                s.x*other,
                s.y*other
                )
        
        else:
           
            try:
                return s.dot(other)
            except:
                pass

            try:
                # assume to matrix3.otherwise,exception should be raised.
                return s.mult_matrix(other)
            except:
                raise TypeError


    def __imul__(s,other):

        if type(other)==float:
            s.x*=other
            s.y*=other
        
        elif type(other)==int:
            
            other = float(other)
            s.x*=other
            s.y*=other
        

        else:

            # dot product cannot be applied to vector itself
            # because output is scalar.

            try:
                # assume to matrix3.otherwise,exception should be raised.
                s.mult_matrix_self(other)
            except:
                raise TypeError


        return s

    
    def __div__(s,other):

        if type(other)==float:
            return vector2d(
                s.x/other,
                s.y/other
                )

    def get_scalar(s):
        return math.sqrt((s.x*s.x) + (s.y * s.y))
            
    def get_angle(s,other):
        """
            get the angle of 'self' with the 'other' in RADIAN.
            
            for example, when you want to get angle from 
            a base-vector 'bvec'  assigned (0.0 , 1.0)
            to 
            a direction-vector 'dvec' (-128.0,128.0),
            
            (offcouse you MUST normalize direction-vector previously)
            
            you can get angle with following code:

                angle = bvec.get_angle(dvec)


            if the 'other' vector locates in counter-clock wise from 'self' vector,
            return value should be negative.
        """
        cz = s.cross(other)
        dp = s.dot(other)

        
        if dp<=-1.0:
            return math.pi
        elif dp >= 1.0:
            return 0.0

        try:
            if cz > 0.0: 
               return -math.acos(dp)
            else:
               return math.acos(dp)
        except:
               print("vec s.x,s.y %f,%f / other %f,%f / dot %f " % (s.x,s.y,other.x,other.y,s.dot(other)))
        
    def get_angle_abs(s,other):
        """
            get the angle of 'self' with the 'other' in RADIAN.
            this method returns simply angle of two normalized vector with absolute value.
            so,each vector2d objects should be normalized preceding calling this method.
        """
        dp = s.dot(other)

        
        if dp <= -1.0:
            return math.pi
        elif dp >= 1.0:
            return 0.0

        try:
               return math.acos(dp)
        except:
               print("vec s.x,s.y %f,%f / other %f,%f / dot %f " % (s.x,s.y,other.x,other.y,s.dot(other)))
        
    def get_degree(s,other): 
        """
            get the angle of 'self' with the 'other' in degree.
            this method is a wrapper conversion method of 'get_angle()'.
        """
        return s.get_angle(other)*57.295779513082323

    def get_normalized(s):
        sc= s.get_scalar()
        if sc!=0.0:
            return vector2d(s.x / sc,s.y / sc)

    def normalize(s):
        # deprecated,remained for compatibility
        return s.get_normalized()

    def normalize_self(s):
        sc= s.get_scalar()
        if sc!=0.0:
            s.x /= sc
            s.y /= sc

    def rotate(s,angle):
        """
        this rotation is clockwize.in RADIAN(0.0 to pi*2)
        """
        return vector2d( s.x * math.cos(angle) + s.y * math.sin(angle),
                         -s.x * math.sin(angle) + s.y * math.cos(angle))

    def rotate_self(s,angle):
        """
        this rotation is clockwize.in RADIAN(0.0 to pi*2)
        """
        nx=s.x * math.cos(angle) + s.y * math.sin(angle)
        ny=-s.x * math.sin(angle) + s.y * math.cos(angle)
        s.x=nx
        s.y=ny

    def rotate_degree(s,degree):
        return s.rotate(degree / 57.295779513082323)

    def rotate_degree_self(s,degree):
        s.rotate_self(degree / 57.295779513082323)

    
    def tuple(self):
        return (self.x,self.y)

    def set(self,aX,aY):
        self.x=aX
        self.y=aY

    def is_zero(self):
        return ((self.x==0.0) and (self.y==0.0))

    @staticmethod
    def sub(out,a,b):
        out.x=a.x-b.x
        out.y=a.y-b.y
        return out

    @staticmethod
    def add(out,a,b):
        out.x=a.x+b.x
        out.y=a.y+b.y
        return out

    @staticmethod
    def mul(out,a,b):
        out.x=a.x*b
        out.y=a.y*b
        return out

    @staticmethod
    def cross(a,b):
        return a.x*b.y - b.x*a.y

    @staticmethod
    def dot(a,b):
        return a.x*b.x + a.y*b.y

    @staticmethod
    def normalize(out,s):
        sc= s.get_scalar()
        if sc!=0.0:
            out.x=s.x / sc
            out.y=s.y / sc
        else:
            raise ValueError
                 
    @staticmethod
    def rotate(out,s,angle):
        """
        this rotation is clockwize.in RADIAN(0.0 to pi*2)
        """
        out.x=s.x * math.cos(angle) + s.y * math.sin(angle)
        out.y=-s.x * math.sin(angle) + s.y * math.cos(angle)
        return out

    @staticmethod
    def convert_radian_to_degree(rad):
        return rad*57.295779513082323


