import pandas as pd
import numpy as np
from os import listdir
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy
from scipy import signal
import os
import math
from plotnine import *
import patchworklib as pw




class Figure_heatmap:
    def __int__(self,data,x,y,fill="percentage",):
        self.data=data
        self.x=x
        self.y=y
        self.fill=fill

    def _scale_fill_gradient2(self,low="#a8d5e6", mid="#fcba03", high="#d41c34",midpoint=30,name='figure',breaks=None):
        Figure_scale_fill_gradient2=scale_fill_gradient2(low=low, mid=mid, high=high,
                             midpoint=midpoint,
                             name=name,
                             breaks=breaks)
        return Figure_scale_fill_gradient2


    def _theme(self,subplots_adjust={'wspace': 0.05, "hspace": 0.05},
            panel_border=element_blank(),
            panel_background=element_rect(fill="#FFFFFF"),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            strip_background=element_blank(),

            axis_text_y=element_blank(),
            axis_ticks=element_blank(),
            legend_position="top",
            legend_direction="horizontal",
            legend_background=element_blank(),

            legend_title_align=("center"),
            legend_key=element_blank(),
            legend_key_size=(8),
            legend_box_spacing=(0)):

        Figure_theme=theme(
            subplots_adjust=subplots_adjust,
            panel_border=panel_border,
            panel_background=panel_background,
            panel_grid_major=panel_grid_major,
            panel_grid_minor=panel_grid_minor,
            strip_background=strip_background,
            strip_text=element_text(colour="#000000", size=8),
            axis_text=element_text(colour="#000000", size=8),
            axis_text_y=axis_text_y,
            axis_text_x=element_text(angle=90, vjust=1),
            axis_title_x=element_text(colour="#000000", size=10),
            axis_title_y=element_text(colour="#000000", size=10),
            axis_ticks=axis_ticks,
            legend_position=legend_position,
            legend_direction=legend_direction,
            legend_background=legend_background,
            legend_title=element_text(colour="#000000", size=8),
            legend_title_align=legend_title_align,
            legend_key=legend_key,
            legend_key_size=legend_key_size,
            legend_text=element_text(colour="#000000", size=8),
            legend_box_spacing=legend_box_spacing)

        return Figure_theme
    def _facet_grid(self,facets="cell_line ~ cell_cycle",space="free_y",labeller_cols={"Sub-G1": "\nSub-G1", "G1": "\nG1", "S": "\nS", "G2/M": "\nG2/M",
                             "Polyploid": "\nPolyploid",
                             "Polyploid (replicating)": "Polyploid\n(replicating)"}):
        """

        :param facets:
        :param space:
        :param labeller_cols:
        :return:
        """
        def _labeller():
            return labeller(labeller_cols)

        return facet_grid(facets=facets, space=space,
                   labeller=_labeller())


        return Figure_facet_grid

    def _labs(self,x="Greatwall inhibitor (??M)",y="Experiment"):
        """

        :param x:
        :param y:
        :return:
        """

        return labs(x=x,y=y)

    def _guides(self,barwidth=3, barheight=20, ticks=False):
        """

        :param barwidth:
        :param barheight:
        :param ticks:
        :return:
        """
        def _fill():
            """

            :return:
            """
            return guide_colourbar(barwidth=barwidth, barheight=barheight, ticks=ticks)
        return guides(_fill())

    def _geom_title(self,size=0.4,colour="#FFFFFF"):
        """

        :param size:
        :param colour:
        :return:
        """
        return geom_tile(size=size, colour=colour)



    def _heatmap(self,):
        """

        :return:
        """
        return (ggplot(self.data) +aes(x=self.x, y=self.y, fill=self.fill) +
                                 self._geom_tile +
                                 self._facet_grid() +
                                 self._scale_fill_gradient2() +
                                 self._labs() +
                                 self._guides() +
                                 self._theme())


    def ggsave(self,filename,path,width,height):
        """

        :param filename:
        :param path:
        :param width:
        :param height:
        :return:
        """
        return ggsave(plot=self._heatmap(), filename=filename, path=path,
                   width=width, height=height)

def _geom_title(self,size=0.4,colour="#FFFFFF"):
    return geom_tile(size=size, colour=colour)




    """
    generate the figure of heatmap based on the input data frame

    :param data: A pandas DataFrame (pd.DataFrame) A DataFrame with the data you want to plot
    :param x: x-axis value. Can be used for continuous (point, line) charts and for discrete (bar, histogram) charts.
    :param y: y-axis value.  Can be used for continuous charts onlycolor (colour) : color of a layer
             Can be continuous or discrete. If continuous, this will be
             given a color gradient between 2 colors.
    :return:

    DEFAULT_kwargs = {size='0.4', colour = "#FFFFFF", facets= "cell_line ~ cell_cycle",
                   space= "free_y", cols={"Sub-G1" : "\nSub-G1", "G1" : "\nG1", "S" : "\nS", "G2/M" : "\nG2/M", "Polyploid" : "\nPolyploid",
                    "Polyploid (replicating)" : "Polyploid\n(replicating)"},
                    low = "#a8d5e6", mid = "#fcba03", high = "#d41c34",
                    midpoint = 30,
                    name = "Proportion of all cells (%)",
                    breaks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                    labsX = "Greatwall inhibitor (??M)",
                    labsY = "Experiment"
                    barwidth = '3', barheight = '20', ticks = 'False'
                    }
    """


def figure_heatmap(data,x,y,fill,**kwargs):
    """
    generate the figure of heatmap based on the input data frame

    :param data: A pandas DataFrame (pd.DataFrame) A DataFrame with the data you want to plot
    :param x:  x-axis value. Can be used for continuous (point, line) charts and for discrete (bar, histogram) charts.
    :param y: y-axis value.  Can be used for continuous charts onlycolor (colour) : color of a layer
    :param fill:
    :param kwargs: parameters for adjust the figure,
    # All  themes are initiated with these params.
    DEFAULT_kwargs = {size='0.4', colour = "#FFFFFF", facets= "cell_line ~ cell_cycle",
                   space= "free_y", cols={"Sub-G1" : "\nSub-G1", "G1" : "\nG1", "S" : "\nS", "G2/M" : "\nG2/M", "Polyploid" : "\nPolyploid",
                    "Polyploid (replicating)" : "Polyploid\n(replicating)"},
                    low = "#a8d5e6", mid = "#fcba03", high = "#d41c34",
                    midpoint = 30,
                    name = "Proportion of all cells (%)",
                    breaks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                    labsX = "Greatwall inhibitor (??M)",
                    labsY = "Experiment"
                    barwidth = '3', barheight = '20', ticks = 'False'
                    }
    :return: A heatmap figure
    """
    Figure_heatmap=(ggplot(data)+aes(x=x, y=y, fill=fill)+geom_tile(size=kwargs['size'], colour=kwargs['color'])+
                   facet_grid(facets=kwargs['facets'], space=kwargs['space'],
                   labeller=labeller(cols=kwargs['cols'])) +
                   scale_fill_gradient2(low=kwargs['low'], mid=kwargs['mid'], high=kwargs['high'],
                   midpoint=kwargs['midpoint'],
                   name=kwargs['name'],
                   breaks=kwargs['breaks']) +
                   labs(x=kwargs['labsX'],y=kwargs['labsY']) +
                   guides(fill = guide_colourbar(barwidth = kwargs['barwidth'], barheight = kwargs['barheight'], ticks = kwargs['ticks'])) +
                   _theme(legend_position='top',legend_direction="horizontal",colour="#000000",
                   subplots_adjust={'wspace': 0.05, "hspace": 0.05},angle=90,vjust=1 )
                    )
    return Figure_heatmap

def _theme(legend_position,legend_direction,**kwargs):
    """
    Set and adjust the theme to the figure
    :param legend_position:
    :param legend_direction:
    :param kwargs:
    :return:theme og figure
    # All  themes are initiated with these params.
    DEFAULT_Parameters = {
                   panel_border=element_blank(),
                   panel_background=element_rect(fill="#FFFFFF"),
                   panel_grid_major=element_blank()
                   panel_grid_minor=element_blank(),
                   strip_background=element_blank(),
                   strip_text=element_text(colour="#000000", size=8),
                   axis_text=element_text(colour="#000000", size=8),
                   axis_text_y=element_blank(),
                   axis_text_x=element_text(angle=90, vjust=1),
                   axis_title_x=element_text(colour="#000000", size=10),
                   axis_title_y=element_text(colour="#000000", size=10),
                   axis_ticks=element_blank(),
                   legend_background=element_blank(),
                   legend_title=element_text(colour="#000000", size=8),
                   legend_title_align=("center"),
                   legend_key=element_blank(),
                   legend_key_size=(8),
                   legend_text=element_text(colour="#000000", size=8),
                   legend_box_spacing=(0))
                    }
    """

    _theme=theme(
        subplots_adjust=kwargs['subplots_adjust'],
        panel_border=element_blank(),
        panel_background=element_rect(fill="#FFFFFF"),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        strip_background=element_blank(),
        strip_text=element_text(colour=kwargs['colour'], size=8),
        axis_text=element_text(colour=kwargs['colour'], size=8),
        axis_text_y=element_blank(),
        axis_text_x=element_text(angle=kwargs['angle'], vjust=kwargs['vjust']),
        axis_title_x=element_text(colour=kwargs['colour'], size=10),
        axis_title_y=element_text(colour=kwargs['colour'], size=10),
        axis_ticks=element_blank(),
        legend_position=legend_position,
        legend_direction=legend_direction,
        legend_background=element_blank(),
        legend_title=element_text(colour=kwargs['colour'], size=8),
        legend_title_align=("center"),
        legend_key=element_blank(),
        legend_key_size=(8),
        legend_text=element_text(colour=kwargs['colour'], size=8),
        legend_box_spacing=(0))
    return _theme

def  _ggsave(plot,filename, path,**kwargs):
    """
    Calling the function to save the plot
    :param plot: Plot to save, defaults to last plot displayed.
    :param filename:File name to create.
    :param path: Path of the directory to save plot to: path and filename are combined to create the fully qualified file name.
    :param kwargs: the size of plot, can adjust the width adn height of figure.
    :return: A file include the saved plot.
    """
    return ggsave(plot=plot, filename=filename, path=path,
                      width=kwargs['width'], height=kwargs['height'])


































