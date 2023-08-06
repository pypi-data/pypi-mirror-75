# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 12:42:20 2020

@author: Mark
"""


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation

import warnings


def frame_number(frame, speed, particles):
    pos = frame*speed
    return f"Position: {pos},  Frame: {frame}"
    

def combine(step, *cords):
    if step == 0:
        step = 1
    n_cords = np.array(cords).T
    new_c = []
    for i in range(0, len(cords[0]), step):
        Temp = n_cords[i]
        new_c.append(Temp)
    return np.array(new_c)

class c_plot():
    def __init__(self, ax, size=2, text="", colour_axis=False, is_point=False, cmap=0, norm=0, max_dots=300):
        self.ax = ax
        self.x = []
        self.y = []
        self.z = []
        self.size = size
        self.colour_axis = colour_axis
        self.text = text
        self.cmap = cmap
        self.norm = norm
        self.max_dots = max_dots

        if self.colour_axis:
            self.me = self.ax.scatter([], [], c=[], s=self.size**2)
            self.init_data = self.init_data_col
            if is_point:
                self.set_data = self.set_data_col_point
            if is_point is False:
                self.set_data = self.set_data_col_track

        if self.colour_axis is False:
            if is_point:
                self.me, = self.ax.plot([], [], 'bo', ms=self.size)
            if is_point is False:
                self.me, = self.ax.plot([], [], lw=self.size)

            self.init_data = self.init_data_no_col
            self.set_data = self.set_data_no_col

    def init_data_col(self):
        self.me.set_offsets([[]])
        self.me.set_color(self.cmap([]))

    def set_data_col_point(self, x, y, z):
        data = combine(1, x, y)
        self.me.set_offsets(data)
        self.me.set_color(self.cmap(self.norm(z)))

    def set_data_col_track(self, x, y, z):

        step = int(np.ceil(len(x)/self.max_dots))

        data = combine(step, x, y)
        self.me.set_offsets(data)
        self.me.set_color(self.cmap(self.norm(combine(step,z).reshape(1,-1)[0])))

    def init_data_no_col(self):
        self.me.set_data([], [])

    def set_data_no_col(self, x, y, z):
        self.me.set_data(x, y)


class Particle():
    def __init__(self, x, y, z, Size, Particle_Color, Track_Length, Track_Size, Mass = 1):# Track_Color):
        self.x = x
        self.y = y
        self.z = z
        self.size = Size
        self.m = Mass 
        
        
        self.color = Particle_Color
        self.tl = Track_Length
        self.ts = Track_Size
        #self.tc = Track_Color
        
        
        self.track_line = None  # to be a line
        self.point = None  # to be a point



class trajectory():
    def __init__(self, name = "My_Trajectory", cmap = mpl.cm.winter):
        self.name = name
        self.cmap = cmap
        self.Particles = [] 
        
    def plot3D(self, x,y,z = [], Size = 10, Particle_Color = "blue",
               Track_Length = 500, Track_Size = 0):
        if Track_Size == 0:
            Track_Size = Size/5
           
        if len(z) == 0:
            z = [0]*len(x)
            
        #Check all same length
        if ((len(x)==len(y)) and (len(y)==len(z))) is False:
            
            raise ValueError(f'x,y,z do not have correct length(x={len(x)}, y={len(y)}, z={len(z)})')
            
        if len(self.Particles) != 0:
            if len(x) != len(self.Particles[0].x):
                warnings.warn("Incorrect numbers of cords entered, only has impact on frame pos in Animation")
        
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
                plt.scatter(Part.x, Part.y, c = Part.z, cmap = self.cmap,
                            vmin = z_axis[0], vmax = z_axis[1], s = s)

            else:
                plt.plot(Part.x, Part.y)
                    
        if with_color:
            plt.colorbar()
                
            if save:
                plt.savefig("Static_" + self.name + "_with_color.png", dpi = 270)
                
        else:
            if save:
                plt.savefig("Static_" + self.name + ".png", dpi = 270)
        
    def Clear(self):
        self.Particles = []
        
    
    def ShowAnimation(self, size=15, follow_mass=-1, save=False, link_data=[], z_axis=[-15, 15],
                      with_color=False, max_dots=150, speed = 4, setup = False,
                      text = [frame_number]):
        '''

        follow_mass
        -3 : The camera remains static
        -2 : The camera follows the largest mass
        -1 : The camera follows the center of mass of the system
        0,1,2, n-1 : The camera follows that particle


        link_data
        links particles together with a line.
        0 means origin
        i means particle i

        examples
        [[0,0]] line drawn between origin and orign(thus no line)

        [[0,1],[1,2]]
        a line drawn from origin to particle 1 
        and a line drawn from 1 to 2

        z_axis
        the colour range of the z axis

        with_color
        uses colour as a 3rd axis

        max_dots
        since the track length is made out of lots of dots to get different colours
        The number of dots can't exceed this, to help combat slow animaitons,
        doesn't matter if saving animation.
        '''
        if setup:
            plt.style.use('dark_background')
        
        
        if follow_mass == -2:
            # Follow largest mass
            max_val = 0
            max_pos = -1
            for index in range(0, len(self.Particles)):
                current_mass = self.Particles[index].m
                if current_mass > max_val:
                    max_val = current_mass
                    max_pos = index

            follow_mass = max_pos

        num_of_frames = (len(self.Particles[0].x)-1)//speed
        # The limits on the colour bar, Z limits
        my_norm = mpl.colors.Normalize(vmin=z_axis[0], vmax=z_axis[1])

        if with_color:
            fig, [ax, cax] = plt.subplots(
                1, 2, gridspec_kw={"width_ratios": [50, 1]})
        else:
            fig, ax = plt.subplots(1, 1)

        if with_color:
            cmap = self.cmap  # Colour you want to use as scale

            cb1 = mpl.colorbar.ColorbarBase(
                cax, cmap=cmap, norm=my_norm, orientation='vertical')
            # The actual color bar
        else:
            cmap = 0

        ax.set_xlim(-size, size)
        ax.set_ylim(-size, size)

        # Get total track length
        total_track_length = 0
        for Part in self.Particles:
            total_track_length += Part.tl

        for Part in self.Particles:
            # Main Body
            Part.point = c_plot(
                ax=ax, size=Part.size, colour_axis=with_color, is_point=True,
                cmap=cmap, norm=my_norm)

            # Track
            dots_in_track = int((Part.tl/total_track_length)*max_dots)
            Part.track_line = c_plot(ax=ax, size=Part.size/5, colour_axis=with_color,
                                     is_point=False, cmap=cmap, norm=my_norm,
                                     max_dots=dots_in_track)

        my_links = []
        for link_pos in link_data:
            temp_link, = ax.plot([], [], lw=3)
            my_links.append(temp_link)
            
            
        #Setting Up Text
        my_text = []
        y_pos_text = 0.95
        x_pos_text = 0.02
        
        for text_index in range(len(text)):
            my_text.append(ax.text(x_pos_text, y_pos_text, '', transform=ax.transAxes))
            y_pos_text -= 0.05

        def my_init():

            Points = []
            Tracks = []
            Texts = []
            
            #Text
            for the_text in my_text:
                the_text.set_text('')
                Texts.append(the_text)
            

            links_lines = []

            for Part in self.Particles:
                # Main Body
                Part.point.init_data()
                Points.append(Part.point.me)

                # Track
                Part.track_line.init_data()
                Tracks.append(Part.track_line.me)

            # Set up links/bonds
            for my_link in my_links:
                my_link.set_data([], [])
                links_lines.append(my_link)

            return [*Points, *Tracks, *links_lines, *Texts]

        def my_animate(i):
            # i represents the frame number
            pos = i*speed
            
            Texts = []
            
            #Text
            for text_index in range(len(text)):
                Func = text[text_index]
                the_text = my_text[text_index]
                the_text.set_text(Func(frame = i, speed = speed, particles = self.Particles))
                Texts.append(the_text)
                

            Points = []
            Tracks = []

            links_lines = []
            link_line = None

            for Part in self.Particles:
                # Main Body
                Part.point.set_data(
                    Part.x[pos:pos+1], Part.y[pos:pos+1], Part.z[pos:pos+1])
                Points.append(Part.point.me)

                # Track
                start_pos = max(0, pos-Part.tl)
                Part.track_line.set_data(
                    Part.x[start_pos:pos], Part.y[start_pos:pos], Part.z[start_pos:pos])
                Tracks.append(Part.track_line.me)

            # Draw links
            for link_index in range(len(link_data)):
                my_link = my_links[link_index]
                link_pos = link_data[link_index]
                start_pos = None
                end_pos = None
                elements = len(self.Particles[0].x)
                #link_line = None

                if link_pos[0] == 0:
                    # means origin
                    start_pos = np.zeros([elements, 2])

                else:
                    start_part = self.Particles[link_pos[0]-1]
                    start_pos = combine(1, start_part.x, start_part.y)

                if link_pos[1] == 0:
                    # means origin
                    end_pos = np.zeros([elements, 2])

                else:
                    end_part = self.Particles[link_pos[1]-1]
                    end_pos = combine(1, end_part.x, end_part.y)

                my_link.set_data([start_pos[pos][0], end_pos[pos][0]], [
                                 start_pos[pos][1], end_pos[pos][1]])
                links_lines.append(my_link)

            # Set center of camera
            if follow_mass >= 0:
                # Follow specific mass
                x_mass = self.Particles[follow_mass].x[pos]
                y_mass = self.Particles[follow_mass].y[pos]
                ax.set_xlim(x_mass-size, x_mass+size)
                ax.set_ylim(y_mass-size, y_mass+size)

            if follow_mass == -1:
                # Follows centre of mass of system
                total_mass = 0
                total_x_mass = 0
                total_y_mass = 0
                for Part in self.Particles:
                    total_mass += Part.m
                    total_x_mass += Part.m*Part.x[pos]
                    total_y_mass += Part.m*Part.y[pos]
                x_cen = total_x_mass/total_mass
                y_cen = total_y_mass/total_mass
                ax.set_xlim(x_cen-size, x_cen+size)
                ax.set_ylim(y_cen-size, y_cen+size)

            return [*Points, *Tracks, *links_lines, *Texts]

        self.anim = animation.FuncAnimation(fig, my_animate, init_func=my_init,
                                            frames=num_of_frames, interval=40, blit=False)

        if save:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=25, metadata=dict(
                artist='Mark Pearson'), bitrate=1800)
            self.anim.save(self.name + ".mp4", writer=writer, dpi=300)
        
        
        
        