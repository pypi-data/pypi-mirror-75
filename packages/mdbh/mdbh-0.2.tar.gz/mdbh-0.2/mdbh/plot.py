# -*- coding: utf-8 -*-1.3
# Copyright (C) 2020  The MDBH Authors
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

from pathlib import Path
from typing import Optional, List

import numpy as np
import matplotlib.pyplot as plt

from pymongo.database import Database

from mdbh import get_metric


def plot_metric(db: Database,
                ids: List[int],
                label_y,
                label_x: Optional[str] = None,
                plot_norm: Optional[str] = None,
                avg: Optional[str] = None,
                avg_arg: Optional[float] = None,
                id_avg: bool = False,
                y_min: float = None,
                y_max: float = None,
                plt_show: bool = True,
                plt_kwargs: dict = {}):
    """Plot metrics of one or multiple run IDs.

    Args:
        db: Database instance.

        ids: List of run IDs to plot.

        label_y: Metric label of y-axis.

        label_x: Optional metric label of x-axis. If None, epoch number is used.

        plot_norm: Optional plotting norm.
                   Either "semilogx", "semilogy", or "loglog".
                   If None, regular plot is used.

        avg: Averaging of data.
             Either "MA" (moving average), "Gauss" (Gauss filtering) or
             "exp" (exponential weighting).

        avg_arg: Optional average parameter. For moving average, specifies
                   filter length, for Gauss filter, specifies sigma,
                   for exponential weighting, specifies exponential factor.

        id_avg: Whether to also average over the multiple run IDs.

        plt_show: Whether to show the plot.

    Returns:
        Matplotlib figure instance.
    """
    ma = None
    sigma = None
    beta = None
    if avg is not None:
        if avg.lower() == "ma":
            ma = avg_arg if avg_arg is not None else 5
        elif avg.lower() == "gauss":
            sigma = avg_arg if avg_arg is not None else 3
        elif avg.lower() == "exp":
            beta = avg_arg if avg_arg is not None else 3

    mpl_p = plt.semilogx if plot_norm == "semilogx" \
        else plt.semilogy if plot_norm == "semilogy" \
        else plt.loglog if plot_norm == "loglog" \
        else plt.plot

    y_dicts = [get_metric(db, id, label_y) for id in ids]
    y = [y_dict['values'] for y_dict in y_dicts]
    y_name = [y_dict['name'] for y_dict in y_dicts]

    if label_x is not None:
        x_dicts = [get_metric(db, id, label_x) for id in ids]
        x = [x_dict['values'] for x_dict in x_dicts]
        x_name = [x_dict['name'] for x_dict in x_dicts]
    else:
        x = [y_dict['steps'] for y_dict in y_dicts]
        x_name = ["Steps" for _ in y_dicts]

    lim_x = slice(0, -1)
    lim_y = lim_x
    if ma is not None and ma != 0:
        y = [np.convolve(tmp, (1 / ma) * np.ones(ma), 'same') for tmp in y]
        lim_x = slice(ma, -ma)
        lim_y = lim_x

    elif sigma is not None:
        from scipy.ndimage import gaussian_filter1d
        y = [gaussian_filter1d(tmp, sigma) for tmp in y]

    elif beta is not None:
        # Exponential weighting of values
        if len(ids) > 1:
            raise ValueError("Exponentially weighted smoothing only available "
                             "for single ID metrics.")

        avg = np.zeros(len(y))
        avg[0] = y[0]
        for i in range(1, len(avg)):
            avg[i] = beta * avg[i - 1] + (1 - beta) * y[i]

        norm = np.asarray([1 - beta**(i + 1) for i in range(len(avg))])
        y = (avg / norm).tolist()

    # Calculate avarage/std across multiple IDs
    y_std = None
    if id_avg and len(ids) > 1:
        # Check that all runs have the same x length
        x_lens = [len(i) for i in x]
        if len(set(x_lens)) != 1:
            raise ValueError("Cannot average runs with different lenghths of x axis.")
        y = np.asarray(y)
        y_std = np.std(y, axis=0, ddof=1)
        y = np.mean(y, axis=0)
        x = x[0]

    fig = plt.figure()
    if y_std is not None:
        mpl_p(x[lim_x], y[lim_y], label="ID average", **plt_kwargs)
        plt.fill_between(x[lim_x], (y - y_std)[lim_y], (y + y_std)[lim_y], alpha=0.2)
    else:
        for i, id in enumerate(ids):
            mpl_p(x[i][lim_x], y[i][lim_y], label=id, **plt_kwargs)
    plt.title(f"Metric plot for ID {ids}")
    plt.xlabel(x_name)
    plt.ylabel(y_name[0])

    if y_min is not None and y_max is not None:
        plt.ylim([y_min, y_max])

    if len(ids) > 1:
        plt.legend()

    if plt_show:
        plt.show()

    return fig
