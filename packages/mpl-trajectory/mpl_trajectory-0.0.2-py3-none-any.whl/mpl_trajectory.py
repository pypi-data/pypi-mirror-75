# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 12:42:20 2020

@author: Mark
"""


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

class Particle():
    def __init__(self, x, y, z, Size, Particle_Color, Track_Length, Track_Size):# Track_Color):
        self.x = x
        self.y = y
        self.z = z
        self.size = Size
        self.color = Particle_Color
        self.tl = Track_Length
        self.ts = Track_Size
        #self.tc = Track_Color
        
        
        self.track_line = None  # to be a line
        self.point = None  # to be a point



class trajectory():
    def __init__(self, name = "My_Trajectory"):
        self.name = name
        self.Particles = [] 
        
    def plot3D(self, x,y,z = [], Size = 10, Particle_Color = "blue",
               Track_Length = 500, Track_Size = 0):
        if Track_Size == 0:
            Track_Size = Size/5
           
        if z == []:
            z = [0]*len(x)
            
        #Check all same length
        if ((len(x)==len(y)) and (len(y)==len(x))) is False:
            
            raise ValueError(f'x,y,z do not have correct length(x={len(x)}, y={len(y)}, z={len(z)})')
        
        self.Particles.append(Particle(x=x,y=y,z=z, Size=Size,
                                       Particle_Color=Particle_Color,
                                       Track_Length = Track_Length,
                                       Track_Size = Track_Size))
        
    def ShowStatic(self, with_color = False, z_axis = [-15,15], save = False,
                   s = 12, setup = False):   
        if setup:
            plt.style.use('dark_background')
            plt.figure(figsize=(7,7))
        for Part in self.Particles:
            if with_color:
                plt.scatter(Part.x, Part.y, c = Part.z, cmap = mpl.cm.winter,
                            vmin = z_axis[0], vmax = z_axis[1], s = s)
                plt.colorbar()
                
                if save:
                    plt.savefig("Static_" + self.name + "_with_color.png")
            else:
                plt.plot(Part.x, Part.y)
                if save:
                    plt.savefig("Static_" + self.name + ".png")





        
    def Clear(self):
        self.Particles = []