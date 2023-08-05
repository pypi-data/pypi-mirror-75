from typing import List, Dict, Iterable, Set, Tuple


from pathlib import Path
import json

import time
import numpy as np
import pandas as pd
import logging
import seaborn as sns
from scipy.optimize import OptimizeResult

from sbmlsim.plot.plotting_matplotlib import plt
from sbmlsim.fit.objects import FitParameter
from sbmlsim.serialization import ObjectJSONEncoder
from sbmlsim.utils import timeit

logger = logging.getLogger(__name__)


class OptimizationResult(ObjectJSONEncoder):
    """Result of optimization problem"""

    def __init__(self, parameters: List[FitParameter], fits: List[OptimizeResult],
                 trajectories: List):
        """Result of an optimization.

        Provides access to the FitParameters, the individual fits, and
        the trajectories of the fits.

        :param parameters:
        :param fits:
        :param trajectories:
        """
        self.parameters = parameters
        self.fits = fits
        self.trajectories = trajectories

        # create data frame from results
        self.df_fits = OptimizationResult.process_fits(self.parameters, self.fits)
        self.df_traces = OptimizationResult.process_traces(self.parameters, self.trajectories)

    def to_dict(self):
        """ Convert to dictionary. """
        d = dict()
        for key in ['parameters', 'fits', 'trajectories']:
            d[key] = self.__dict__[key]
        return d

    @staticmethod
    def from_json(json_info: Tuple[str, Path]) -> 'TimecourseSim':
        """ Load OptimizationResult from Path or str

        :param json_info:
        :return:
        """
        if isinstance(json_info, Path):
            with open(json_info, "r") as f_json:
                d = json.load(f_json)
        else:
            d = json.loads(json_info)
        return OptimizationResult(**d)

    def __str__(self):
        info = f"<OptimizationResult: n={self.size}>"
        return info

    @staticmethod
    def combine(opt_results: List[OptimizeResult]):
        # FIXME: check that the parameters are fitting
        parameters = opt_results[0].parameters
        pids = {p.pid for p in parameters}

        fits = []
        trajectories = []
        for opt_res in opt_results:
            pids_next = {p.pid for p in opt_res.parameters}
            if pids != pids_next:
                logger.error(f"Parameters of OptimizationResults do not match: "
                             f"{pids} != {pids_next}")

            fits.extend(opt_res.fits)
            trajectories.extend(opt_res.trajectories)
        return OptimizationResult(parameters=parameters, fits=fits,
                                  trajectories=trajectories)

    @property
    def size(self):
        """Number of optimizations in result."""
        return len(self.df_fits)

    @property
    def xopt(self):
        """Optimal parameters"""
        return self.df_fits.x.iloc[0]

    @staticmethod
    def process_traces(parameters: List[FitParameter], trajectories):
        """Process the optimization results."""
        results = []
        pids = [p.pid for p in parameters]
        # print(fits)
        for kt, trajectory in enumerate(trajectories):
            for step in trajectory:
                res = {
                    'run': kt,
                    'cost': step[1],
                }
                # add parameter columns
                for k, pid in enumerate(pids):
                    res[pid] = step[0][k]
                results.append(res)
        df = pd.DataFrame(results)
        return df

    @staticmethod
    def process_fits(parameters: List[FitParameter], fits: List[OptimizeResult]):
        """Process the optimization results."""
        results = []
        pids = [p.pid for p in parameters]
        # print(fits)
        for kf, fit in enumerate(fits):
            res = {
                'run': kf,
                # 'status': fit.status,
                'success': fit.success,
                'duration': fit.duration,
                'cost': fit.cost,
                 # 'optimality': fit.optimality,
            }
            # add parameter columns
            for k, pid in enumerate(pids):
                res[pid] = fit.x[k]
            res['message'] = fit.message if hasattr(fit, "message") else None
            res['x'] = fit.x
            res['x0'] = fit.x0

            results.append(res)
        df = pd.DataFrame(results)
        df.sort_values(by=["cost"], inplace=True)
        # reindex
        df.index = range(len(df))

        return df

    def report(self, output_path: Path=None, print_output=True):
        """ Readable report of optimization. """
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)

        info = [
            "\n",
            "-" * 80,
            "Optimization Results",
            "-" * 80,
            str(self.df_fits),
            "-" * 80,
            "Optimal parameters:",
        ]

        xopt = self.xopt
        fitted_pars = {}
        for k, p in enumerate(self.parameters):
            opt_value = xopt[k]
            if abs(opt_value-p.lower_bound)/p.lower_bound < 0.05:
                logger.error(f"Optimal parameter '{p.pid}' within 5% of lower bound!")
            if abs(opt_value-p.upper_bound)/p.upper_bound < 0.05:
                logger.error(f"Optimal parameter '{p.pid}' within 5% of upper bound!")
            fitted_pars[p.pid] = (opt_value, p.unit, p.lower_bound, p.upper_bound)

        for key, value in fitted_pars.items():
            info.append(
                "\t'{}': Q_({}, '{}'),  # [{} - {}]".format(key, value[0], value[1],
                                                            value[2], value[3])
            )
        info.append("-" * 80)
        info = "\n".join(info)
        if print_output:
            print(info)

        if output_path is not None:
            filepath = output_path / "00_fit_report.txt"
            with open(filepath, "w") as fout:
                fout.write(info)

    @timeit
    def plot_waterfall(self, output_path: Path = None, show_plots: bool = True):
        """Creates waterfall plot for the fit results.

        Plots the optimization runs sorted by cost.
        """
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
        ax.plot(range(self.size), 1 + (self.df_fits.cost - self.df_fits.cost.iloc[0]), '-o', color="black")
        ax.set_xlabel("index (Ordered optimizer run)")
        ax.set_ylabel("Offsetted cost value (relative to best start)")
        ax.set_yscale("log")
        ax.set_title("Waterfall plot")
        if show_plots:
            plt.show()

        if output_path is not None:
            filepath = output_path / "01_waterfall.svg"
            fig.savefig(filepath, bbox_inches="tight")

    @timeit
    def plot_traces(self, output_path: Path = None, show_plots: bool = True):
        """Plots optimization traces.
        """
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

        for run in range(self.size):
            df_run = self.df_traces[self.df_traces.run == run]
            ax.plot(range(len(df_run)), df_run.cost, '-', alpha=0.8)
        for run in range(self.size):
            df_run = self.df_traces[self.df_traces.run == run]
            ax.plot(len(df_run)-1, df_run.cost.iloc[-1], 'o', color="black", alpha=0.8)

        ax.set_xlabel("step")
        ax.set_ylabel("cost")
        ax.set_yscale("log")
        ax.set_title("Traces")
        if show_plots:
            plt.show()

        if output_path is not None:
            filepath = output_path / "02_traces.svg"
            fig.savefig(filepath, bbox_inches="tight")

    @timeit
    def plot_correlation(self, output_path: Path = None, show_plots: bool = True,
                         output_format: str="png"):
        """Process the optimization results."""
        df = self.df_fits

        pids = [p.pid for p in self.parameters]
        sns.set(style="ticks", color_codes=True)
        # sns_plot = sns.pairplot(data=df[pids + ["cost"]], hue="cost", corner=True)

        npars = len(pids)
        # x0 =
        fig, axes = plt.subplots(nrows=npars, ncols=npars, figsize=(5*npars, 5*npars))
        cost_normed = (df.cost - df.cost.min())
        cost_normed = 1 - cost_normed/cost_normed.max()
        # print("cost_normed", cost_normed)
        size = np.power(15*cost_normed, 2)

        bound_kwargs = {'color': "darkgrey", 'linestyle': "--", "alpha": 1.0}

        for kx, pidx in enumerate(pids):
            for ky, pidy in enumerate(pids):
                if npars == 1:
                    ax = axes
                else:
                    ax = axes[ky][kx]

                # optimal values
                if kx > ky:
                    ax.set_xlabel(pidx)
                    # ax.set_xlim(self.parameters[kx].lower_bound, self.parameters[kx].upper_bound)
                    ax.axvline(x=self.parameters[kx].lower_bound, **bound_kwargs)
                    ax.axvline(x=self.parameters[kx].upper_bound, **bound_kwargs)
                    ax.set_ylabel(pidy)
                    #ax.set_ylim(self.parameters[ky].lower_bound, self.parameters[ky].upper_bound)
                    ax.axhline(y=self.parameters[ky].lower_bound, **bound_kwargs)
                    ax.axhline(y=self.parameters[ky].upper_bound, **bound_kwargs)

                    # start values
                    xall = []
                    yall = []
                    xstart_all = []
                    ystart_all = []
                    for ks in range(len(size)):
                        x = df.x[ks][kx]
                        y = df.x[ks][ky]
                        xall.append(x)
                        yall.append(y)
                        if 'x0' in df.columns:
                            xstart = df.x0[ks][kx]
                            ystart = df.x0[ks][ky]
                            xstart_all.append(xstart)
                            ystart_all.append(ystart)

                    # start point
                    ax.plot(xstart_all, ystart_all, "^", color="black", markersize=2, alpha=0.5)
                    # optimal values
                    ax.scatter(df[pidx], df[pidy], c=df.cost, s=size, alpha=0.9, cmap="jet"),

                    ax.plot(self.xopt[kx], self.xopt[ky], "s",
                                      color="darkgreen", markersize=30,
                                      alpha=0.7)

                if kx == ky:
                    ax.set_xlabel(pidx)
                    ax.axvline(x=self.parameters[kx].lower_bound, **bound_kwargs)
                    ax.axvline(x=self.parameters[kx].upper_bound, **bound_kwargs)
                    # ax.set_xlim(self.parameters[kx].lower_bound,
                    #            self.parameters[kx].upper_bound)
                    ax.set_ylabel("cost")
                    ax.plot(df[pidx], df.cost, color="black", marker="s", linestyle="None", alpha=1.0)

                # traces (walk through cost function)
                if kx < ky:
                    ax.set_xlabel(pidy)
                    # ax.set_xlim(self.parameters[ky].lower_bound, self.parameters[ky].upper_bound)
                    ax.axvline(x=self.parameters[ky].lower_bound, **bound_kwargs)
                    ax.axvline(x=self.parameters[ky].upper_bound, **bound_kwargs)
                    ax.set_ylabel(pidx)
                    # ax.set_ylim(self.parameters[kx].lower_bound, self.parameters[kx].upper_bound)
                    ax.axhline(y=self.parameters[kx].lower_bound, **bound_kwargs)
                    ax.axhline(y=self.parameters[kx].upper_bound, **bound_kwargs)

                            # ax.plot([ystart, y], [xstart, x], "-", color="black", alpha=0.7)

                    for run in range(self.size):
                        df_run = self.df_traces[self.df_traces.run == run]
                        # ax.plot(df_run[pidy], df_run[pidx], '-', color="black", alpha=0.3)
                        ax.scatter(df_run[pidy], df_run[pidx], c=df_run.cost, cmap="jet",
                                   marker="s", alpha=0.8)

                    # end point
                    # ax.plot(yall, xall, "o", color="black", markersize=10, alpha=0.9)
                    ax.plot(self.xopt[ky], self.xopt[kx], "s", color="darkgreen", markersize=30, alpha=0.7)

                ax.set_xscale("log")
                if kx != ky:
                    ax.set_yscale("log")
                if kx == ky:
                    ax.set_yscale("log")

        # correct scatter limits
        for kx, pidx in enumerate(pids):
            for ky, pidy in enumerate(pids):
                if kx < ky:
                    axes[ky][kx].set_xlim(axes[kx][ky].get_xlim())
                    axes[ky][kx].set_ylim(axes[kx][ky].get_ylim())

        if show_plots:
            plt.show()
        if output_path is not None:
            filepath = output_path / f"04_parameter_landscape.{output_format}"
            fig.savefig(filepath, bbox_inches="tight")
