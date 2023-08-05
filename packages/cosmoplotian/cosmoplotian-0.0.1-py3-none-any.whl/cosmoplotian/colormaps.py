#
# Copyright (C) 2012-2020  Ben Thorne
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""
Colormaps for plotting of cosmological image. This module deals with providing
customizable colormaps implemented with
:class:`matplotlib.colors.LinearSegmentedColormap`. The colormaps are
implemented individually, rather than being able to choose colors
'on-the-fly', as it results in a simpler interface. Once ``cosmoplotian``
has been implemented, the colormap names will be available thorugh the
``cmap`` keyword argument.

Examples
--------

Divergent colormap

.. plot::
   :context: reset
   :include-source:
   :align: center

    import cosmoplotian
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(figsize=(6, 0.3), dpi=100, sharey=True)
    fig.subplots_adjust(
        wspace=0, right=0.99, top=0.99, bottom=0.00, left=0.01, hspace=0.0
    )
    plt.yticks([])
    arr = np.tile(np.arange(1000), 100).reshape(100, 1000)
    plt.imshow(arr, cmap='div yel grn')

Linear colormap

.. plot::
   :context: reset
   :include-source:
   :align: center

    import cosmoplotian
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(figsize=(6, 0.3), dpi=100, sharey=True)
    fig.subplots_adjust(
        wspace=0, right=0.99, top=0.99, bottom=0.00, left=0.01, hspace=0.0
    )
    plt.yticks([])
    arr = np.tile(np.arange(1000), 100).reshape(100, 1000)
    plt.imshow(arr, cmap='lin blu')

"""
import matplotlib
import matplotlib.cm
from matplotlib.colors import LinearSegmentedColormap

aitetsu = "#003A47"
azuki = "#A04940"
shironeri = "#FCFAF2"
sabinando = "#406F79"
ominaeshi = "#F2F2B0"
seiheki = "#478384"
koiai = "#002E4E"

# Now register some of the sensible defaults with matplotlib
matplotlib.cm.register_cmap(
    name="div yel grn",
    cmap=LinearSegmentedColormap.from_list("", [ominaeshi, seiheki, koiai]),
)
matplotlib.cm.register_cmap(
    name="lin blu", cmap=LinearSegmentedColormap.from_list("", [shironeri, aitetsu])
)
# matplotlib.cm.register_cmap(name='lin blu shp', cmap=tri('shironeri', 'sabinando', 'black'))

del azuki, shironeri, sabinando, ominaeshi, seiheki, koiai

__all__ = []
