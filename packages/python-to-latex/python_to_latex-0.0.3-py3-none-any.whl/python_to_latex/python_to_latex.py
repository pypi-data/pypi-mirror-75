#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Sonja Stuedli
"""
This module gives several method to process data within python to use in latex.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import linalg as la
import itertools

def mat2lat(matrix,matrix_style='ownmatrix',save_name=None,style=dict()):
    """
    Takes a vector or two dimensional array into a string that produces a latex matrix or vector for printing.

    Parameters
    ----------

    matrix_style (String:ownmatrix): Selects the latex environment that is used. 

    save_name (String:None): give the file name that the output should be saved to. If None the string is printed instead.

    style (dict:{'decimal_points':0,'cell_width':3}): formating style for all numbers in the matrix. Currenlty, the formatting will be done using: 
               :<cell_width>.<decimal_points>f
    """
    s = f"\\begin{{{ matrix_style}}}\n"
    decimal_points = f".{style.get('decimal_points',0)}f"
    cell_width = str(style.get('cell_width',3+style.get('decimal_points',0)))
    for l in matrix: 
        s += " & ".join([f"{n:{cell_width}{decimal_points}}" for n in l]) 
        s += "\\\\ \n" 
    s += f"\end{{{matrix_style}}}\n"

    if save_name:
        file_name = str(save_name)
        if (file_name.endswith('.dat')) or (file_name.endswith('.tab')) or (file_name.endswith('.tex')):
            f = open(file_name,'w')
        else:
            f = open(file_name +'.tab','w')
        f.write(s)
        f.close()
    else:
        print(s)
    return s


def numeric_list_to_tabularx(data,heading=None,exponent=0,row_heading=None,save_name=None):
    """
    Transforms two dimensional array into a string that produces a latex tabularx using siunitx for printing. 

    For exaple:
    [[1,2,3],[4,5,6]] is transformed to a string that if printed yields:
    \begin{tabularx}{\linewidth}{S[table-auto-round,table-omit-exponent,fixed-exponent=0]S[table-auto-round,table-omit-exponent,fixed-exponent=0]S[table-auto-round,table-omit-exponent,fixed-exponent=0]} \toprule
    1 & 2 & 3\\
    4 & 5 & 6\\\bottomrule 
    \end{tabularx}

    Parameters
    ----------

    heading (list:None): This is an optional parameter that will be included in the tabularx environment and assumes strings. For example heading=['A','B','c'] in the above yields
    \begin{tabularx}{\linewidth}{S[table-auto-round,table-omit-exponent,fixed-exponent=0]S[table-auto-round,table-omit-exponent,fixed-exponent=0]S[table-auto-round,table-omit-exponent,fixed-exponent=0]} \toprule
    {A} & {B} & {C}\\ \midrule
    1 & 2 & 3\\
    4 & 5 & 6\\\bottomrule 
    \end{tabularx}

    exponent (int: 0): is an optional parameter used in the definition of the S column for fixed-exponent=<exponent>. Default is 0, to not use a fixed exponent use exponent=None

    row_heading (list:None): is an optional parameter that allows to include a row heading.

    save_name (String:None): give the file name that the picture should be saved. If None the string is printed instead.

    """
    # Add input checking that data is 2D array like; row_heading is either None or a list; heading is either None or a list, exponent is int or None
    
    s='\\begin{tabularx}{\linewidth}{'
    init = True
    if row_heading is not None:
        for row,row_start in zip(data,row_heading):
            if init:
                s += 'X'
                if exponent:
                    s += f'S'*len(row) + '} \\toprule'
                else:
                    s += f'S[table-auto-round,table-omit-exponent,fixed-exponent={exponent}]'*len(row) + '} \\toprule'
                if heading:
                    s += '\n' + ' & ' + ' & '.join(['{'+str(entry)+'}' for entry in heading]) +'\\\\ \midrule'
                init = False
            s += '\n' + row_start + ' & ' + ' & '.join([str(entry) for entry in row]) + '\\\\'
    else:
        for row in data:
            if init:
                if exponent:
                    s += f'S'*len(row) + '} \\toprule'
                else:
                    s += f'S[table-auto-round,table-omit-exponent,fixed-exponent={exponent}]'*len(row) + '} \\toprule'
                if heading:
                    s += '\n' + ' & '.join(['{'+str(entry)+'}' for entry in heading]) +'\\\\ \midrule'
                init = False
            s += '\n' + ' & '.join([str(entry) for entry in row]) + '\\\\'

        s += '\\bottomrule \n \end{tabularx}'

    if save_name:
        file_name = str(save_name)
        if (file_name.endswith('.dat')) or (file_name.endswith('.tab')) or (file_name.endswith('.tex')):
            f = open(file_name,'w')
        else:
            f = open(file_name +'.tab','w')
        f.write(s)
        f.close()
    else:
        print(s)
    return s


plot_linestyles = {'-':"solid",'None':"only marks","--":'dashed',"-.":'dashdotted',":":"dotted"}
plot_markers = {'None':'no marks','.':"mark=*",'x':'mark=x','o':'mark=o','s':'mark=square'}

def fig2pgf(fig,save_name=None,retain_color = False, retain_linestyle = False, retain_marker = True,plot_as_table=True,figure_options="grid",plot_options=None,line_options=None,add_labels=None):
    """
    Convert a figure to a pgf plot.

    Parameters
    ----------

    save_name (String:None): give the file name that the picture should be saved. If None the string is printed instead.
    retain_color (Bool:False):  keep the color given in the plot in the pgf plot as well
    retain_linestyle (Bool:False): keep the line style chosen in plot in the pgf plot
    retain_marker (Bool:True): keep the markers chosen in the plot in the pgf plot
    plot_as_table (Bool:True): use the table input in the pgf plot. Sometimes this does not work then you can set it to false to force coordinate input, if the x or y coordinates are strings plot_as_table is set to False to avoid issues
    figure_options (String:'grid') : give additional options that apply for the complete figure. This will be overwritten by plot and line options.
    plot_options (Dict:None): give additional options that hold for a single subplot. Set a plot label such as <plt_1.set_label('label')> when drawing the plot. Then, options can be given as dictionary having the given label as key (String) and the options as value (String)
    line_options (Dict:None): give additional options that hold for this line. Set a label for the line while plotting such as <plt_2[1].plot(x,y2,label="line 1")>. Then, options can be given as dictionary having the given label as key (String) and the options as value (String)
    
   add_labels (String: None): if not None a label is printed included for each plot. This can be references as \ref{pgfplot:<add_labels><line_number>}

    Example usage: 
    x = np.arange(15)
    y1 = 2*x
    y2 = x+5
    y3 = x

    fig1,plt1 = plt.subplots(nrows=1,ncols=2)
    plt1[0].plot(x,y1)
    plt1[0].plot(x,y2,'.',label="line a")
    plt1[1].plot(x,y3,label="line 1")
    plt1[0].set_ylabel('$\lambda_2$')
    plt1[1].set_xlabel('$b$')
    plt1[1].set_ylabel('$\lambda_N$')
    plt1[1].set_xlabel('$N$')
    plt1[0].legend(loc=1)
    plt1[0].set_label("test")
    fig1.show()

    fig2pgf(fig1,"test",retain_color=True,retain_linestyle=True,line_options={"line a":"black,dashed"},plot_options={"test":"dashed"})
   
 
    The main idea is to let pgfplot take care of most plotting styles. It relies on the following latex packages:
    - pgfplots (load also library groupplots)
    - xcolor 
    
    To set some common features use pgfplotsset, for example:
    \pgfplotsset{
    every axis plot post/.style={
      line join=round, % make the corners nicer: possible round,bevel,miter
      thick,
    }
    To select a color, linestyle, and marker cycling automatically. Use a cycle list, for example:
    }
    \pgfplotsset{
    % initialize colors
    % cycle list/Paired,
    cycle list/Set1,
    cycle list/.define={my lines}{solid, dotted, dashed, dashdotted, dashdotdotted},
    cycle list/.define={my marks}{*,x,asterisk,o},
    % combine it with marks and line styles:
    cycle multiindex* list={
    linestyles*\nextlist
    mark list*\nextlist
    Set1\nextlist
    },
    }

    """
    # implement input checking:
    # check whether fig is a figure todo
    # check plot/line_options are dictionaries
    # check figure_options is string
    # retain_* is bool

    # get all axes from the figure
    ax = fig.axes

    # define some options that are used identically for all plots
    global_options = "    width=\\figurewidth,height=\\figureheight,\n    at={(0\\figurewidth,0\\figureheight)},\n"
    # allow nan +inf or -inf in plots
    global_options += "    unbounded coords=jump,\n"
    # add user provided options
    if figure_options:
        global_options += "    " + str(figure_options) + ",\n"
    
    if len(ax) == 1:
        s_init = "\\begin{axis}[\n" + global_options
        s_start = ""
        s_exit = "\end{axis}\n"
    else:
        row_number,column_number,index = ax[0].get_geometry()
        s_init = "\\begin{groupplot}[group style={group size="+str(column_number) + " by " + str(row_number) +"},\n" + global_options + "    ]\n"

        s_exit = "\end{groupplot}\n"
        s_start = "\\nextgroupplot[\n"

    # start string that makes figure
    s = "%This file was created by python_to_latex. \n\\begin{tikzpicture} \n"
    if retain_color:
        color_definitions = list()
        s += " REPLACE_COLORS \n"
    s += s_init
    
    # add each subplot
    for axis in ax:
        
        s += s_start
        # todo logarithmic scale for x or y using tikz options below
        # "xmode=log|normal,ymode=log|normal"


        # set label, min, max and check whethere the ticks are symbolic for x and y axis
        s += f"    xlabel = {axis.get_xlabel()},\n"
        if True in [i.get_xdata().dtype.num in [19] for i in axis.lines]:
            symbolic_x_coordinates = [str(0)]
            s += "    xtick = data,\n    symbolic x coords = {REPLACE_SYMBOLIC_COORDS_X},\n"
            plot_as_table = False
        else:
            symbolic_x_coordinates = None
            s += f"    xmin={axis.get_xlim()[0]}, xmax={axis.get_xlim()[1]},\n"

        s += f"    ylabel = {axis.get_ylabel()},\n"
        if True in [i.get_ydata().dtype.num in [19] for i in axis.lines]:
            symbolic_y_coordinates = [str(0)]
            s += "    ytick = data,\n    symbolic y coords = {REPLACE_SYMBOLIC_COORDS_Y},\n"
            plot_as_table = False
        else:
            symbolic_y_coordinates = None
            s += f"    ymin={axis.get_ylim()[0]}, ymax={axis.get_ylim()[1]},\n"
        # todo add other options from figure
        # add user options if available
        if plot_options:
            option = plot_options.get(axis.get_label(),None)
            if option:
                s += "    " + str(option) + "\n"
        s += "    ]\n"

        # make legend_entries
        if axis.get_legend():
            legend_labels = [i.get_text() for i in axis.get_legend().texts]
            s+= "\legend{" + ','.join(legend_labels) + "}\n"

        # add line plots
        for line_number,line in enumerate(axis.lines):
            s += "\\addplot +["
            # add necessary options
            if retain_linestyle:
                linestyle = plot_linestyles.get(line.get_linestyle(),None)
                if linestyle:
                    s += f"{linestyle},"
            if retain_color:
                color_definitions.append("\definecolor{color"+str(len(color_definitions))+"}{RGB}{"+" , ".join([str(int(line.get_color().lstrip('#')[i:i+2], 16)) for i in (0, 2, 4)])+"} ")
                s += f"color{str(len(color_definitions)-1)},"
            if retain_marker:
                markers = plot_markers.get(line.get_marker(),None)
                if markers:
                    s += f"{markers},"
            # add additional user options
            if line_options:
                s += str(line_options.get(line.get_label(),'')) 
            s += "]\n"

            if plot_as_table :
                s+= " table{%\n" +"\n".join([f"  {x} {y}" for (x,y) in zip(line.get_xdata(),line.get_ydata())]) + "\n};\n"
            else:
                if symbolic_x_coordinates:
                    [symbolic_x_coordinates.append(str(label)) for label in line.get_xdata() if label not in symbolic_x_coordinates]
                if symbolic_y_coordinates:
                    [symbolic_y_coordinates.append(str(label)) for label in line.get_ydata() if label not in symbolic_y_coordinates]
                s+= " coordinates{%\n" +"\n".join([f"  ({x},{y})" for (x,y) in zip(line.get_xdata(),line.get_ydata())]) + "\n};\n"

            if add_labels:
                  s += f"\label{{pgfplot:{add_labels}{line_number}}}"

    if retain_color:
        s=s.replace("REPLACE_COLORS","\n ".join(color_definitions)) + "\n"

    if symbolic_x_coordinates:
        s=s.replace("REPLACE_SYMBOLIC_COORDS_X",",".join(symbolic_x_coordinates)) 
    if symbolic_y_coordinates:
        s=s.replace("REPLACE_SYMBOLIC_COORDS_Y",",".join(symbolic_y_coordinates)) 


    # finish string
    s += s_exit + "\end{tikzpicture} \n"

    if save_name:
        file_name = str(save_name)
        if (file_name.endswith('.tikz')) or (file_name.endswith('.pgf')) or (file_name.endswith('.tex')):
            f = open(file_name,'w')
        else:
            f = open(file_name +'.tikz','w')
        f.write(s)
        f.close()
    else:
        print(s)
    return s

