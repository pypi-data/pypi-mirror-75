from typing import TypedDict, Union


class ConfigGAInterface(TypedDict):
    XMatrix: str
    yvector: str
    varcut: float
    corrcut: float
    max_latent_model: Union[int, None]
    min_vars_model: int
    max_vars_model: int
    population_size: int
    migration_rate: float
    crossover_rate: float
    mutation_rate: float
    generations: int
    yrand: float
    lno: float
    output_matrix: str
    output_cv: str
    output_q2: str
    output_selected: str
    autoscale: bool
    lj_transform: bool
    autocorrcut: float


class ConfigOPSInterface(TypedDict):
    XMatrix: str
    yvector: str
    varcut: float
    corrcut: float
    latent_vars_ops: int
    latent_vars_model: int
    ops_window: int
    ops_increment: int
    vars_percentage: float
    models_to_save: int
    yrand: float
    lno: float
    output_matrix: str
    output_cv: str
    output_models: str
    lj_transform: bool
    autoscale: bool
    autocorrcut: float
    ops_type: str
