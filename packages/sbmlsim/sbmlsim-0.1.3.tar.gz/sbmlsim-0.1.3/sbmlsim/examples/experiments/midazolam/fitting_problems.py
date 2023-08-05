"""
Definition of parameter fitting problems
"""
from sbmlsim.fit import FitExperiment, FitParameter
from sbmlsim.fit.optimization import OptimizationProblem

from sbmlsim.examples.experiments.midazolam.experiments.mandema1992 import Mandema1992
from sbmlsim.examples.experiments.midazolam.experiments.kupferschmidt1995 import Kupferschmidt1995

from sbmlsim.examples.experiments.midazolam import MIDAZOLAM_PATH

exp_kwargs = {
    "base_path": MIDAZOLAM_PATH,
    "data_path": MIDAZOLAM_PATH / "data",
}


def op_kupferschmidt1995() -> OptimizationProblem:
    """Factory to get uninitialized optimization problem."""

    KM_BOUNDS = (1E-5, 1E-1)
    VMAX_BOUNDS = (1E-5, 1E3)

    return OptimizationProblem(
        opid="mid1oh_iv",
        base_path=MIDAZOLAM_PATH,
        data_path=MIDAZOLAM_PATH / "data",

        fit_experiments=[
            FitExperiment(experiment=Kupferschmidt1995, mappings=["fm_mid_iv", "fm_mid1oh_iv"]),
        ],
        fit_parameters=[
            # liver
            FitParameter(parameter_id="LI__MIDIM_Vmax", start_value=0.1,
                         lower_bound=VMAX_BOUNDS[0], upper_bound=VMAX_BOUNDS[1],
                         unit="mmole_per_min"),

            FitParameter(parameter_id="LI__MID1OHEX_Vmax", start_value=0.1,
                         lower_bound=VMAX_BOUNDS[0], upper_bound=VMAX_BOUNDS[1],
                         unit="mmole_per_min"),

            FitParameter(parameter_id="LI__MIDOH_Vmax", start_value=100,
                         lower_bound=VMAX_BOUNDS[0], upper_bound=VMAX_BOUNDS[1],
                         unit="mmole_per_min"),

            # does not improve fits
            # FitParameter(parameter_id="LI__MIDX_Vmax", start_value=100,
            #            lower_bound=VMAX_BOUNDS[0], upper_bound=VMAX_BOUNDS[1],
            #            unit="mmole_per_min"),
            #FitParameter(parameter_id="LI__MIDX_Km", start_value=0.1,
            #             lower_bound=KM_BOUNDS[0], upper_bound=KM_BOUNDS[1],
            #             unit="mM"),

            # kidneys (determined via 1-OH fits)
            FitParameter(parameter_id="KI__MID1OHEX_Vmax", start_value=100,
                         lower_bound=VMAX_BOUNDS[0], upper_bound=VMAX_BOUNDS[1]*10,
                         unit="mmole/min"),
            FitParameter(parameter_id="KI__MID1OHEX_Km", start_value=100,
                         lower_bound=KM_BOUNDS[0], upper_bound=KM_BOUNDS[1],
                         unit="mM"),

            # distribution
            FitParameter(parameter_id="ftissue_mid", start_value=50,
                         lower_bound=VMAX_BOUNDS[0], upper_bound=VMAX_BOUNDS[1],
                         unit="liter/min"),
            # FitParameter(parameter_id="fup_mid", start_value=0.1,
            #               lower_bound=0.05, upper_bound=0.3,
            #              unit="dimensionless"),
            FitParameter(parameter_id="ftissue_mid1oh", start_value=1.0,
                         lower_bound=VMAX_BOUNDS[0], upper_bound=VMAX_BOUNDS[1],
                         unit="liter/min"),
            # FitParameter(parameter_id="fup_mid1oh", start_value=0.1,
            #             lower_bound=0.01, upper_bound=0.3,
            #             unit="dimensionless"),
            ],
    )


def op_mid1oh_iv() -> OptimizationProblem:
    """Factory to get uninitialized optimization problem."""
    return OptimizationProblem(
        opid="mid1oh_iv",
        fit_experiments=[
                FitExperiment(experiment=Mandema1992, mappings=["fm4"])
            ],
        fit_parameters=[
                # distribution parameters
                FitParameter(parameter_id="ftissue_mid1oh", start_value=1.0,
                             lower_bound=1, upper_bound=1E5,
                             unit="liter/min"),
                FitParameter(parameter_id="fup_mid1oh", start_value=0.1,
                             lower_bound=0.01, upper_bound=0.5,
                             unit="dimensionless"),
                # mid1oh kinetics
                FitParameter(parameter_id="KI__MID1OHEX_Vmax", start_value=100,
                             lower_bound=1E-1, upper_bound=1E4,
                             unit="mmole/min"),
            ],
        **exp_kwargs
    )


def op_mandema1992() -> OptimizationProblem:
    """Factory to get uninitialized optimization problem."""
    return OptimizationProblem(
        opid="mandema1992",
        fit_experiments=[
            # FitExperiment(experiment=Mandema1992, mappings=["fm1"]),
            FitExperiment(experiment=Mandema1992, mappings=["fm1", "fm3", "fm4"]),
        ],
        fit_parameters=[
            # liver
            FitParameter(parameter_id="LI__MIDIM_Vmax", start_value=0.1,
                         lower_bound=1E-3, upper_bound=1E6,
                         unit="mmole_per_min"),
            FitParameter(parameter_id="LI__MID1OHEX_Vmax", start_value=0.1,
                         lower_bound=1E-3, upper_bound=1E6,
                         unit="mmole_per_min"),
            FitParameter(parameter_id="LI__MIDOH_Vmax", start_value=100,
                         lower_bound=10, upper_bound=200, unit="mmole_per_min"),
            # kidneys
            FitParameter(parameter_id="KI__MID1OHEX_Vmax", start_value=100,
                         lower_bound=1E-1, upper_bound=1E4,
                         unit="mmole/min"),

            # distribution
            FitParameter(parameter_id="ftissue_mid", start_value=2000,
                          lower_bound=1, upper_bound=1E5,
                          unit="liter/min"),
            FitParameter(parameter_id="fup_mid", start_value=0.1,
                          lower_bound=0.05, upper_bound=0.3,
                          unit="dimensionless"),
            # distribution parameters
            FitParameter(parameter_id="ftissue_mid1oh", start_value=1.0,
                         lower_bound=1, upper_bound=1E5,
                         unit="liter/min"),
            FitParameter(parameter_id="fup_mid1oh", start_value=0.1,
                         lower_bound=0.01, upper_bound=0.3,
                         unit="dimensionless"),
        ],
        **exp_kwargs
    )

