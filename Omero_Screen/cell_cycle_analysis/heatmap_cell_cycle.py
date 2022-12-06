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

    def _labs(self,x="Greatwall inhibitor (µM)",y="Experiment"):
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

