import os
import matplotlib.pyplot
import pandas
import numpy
from pydoc import locate
from pandas.core.computation.ops import Literal
from dataclasses import dataclass


def create_plots(simulation_gender: Literal["female", "male"], days: int, cortisol_exp: list[float]):
    folder_path = "Output/week_post_processing"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # --- Generate Cortisol Plot by paper ---
    decades = ["30-40", "40-50", "50-60", "60-70", "70-80", "80-90"]
    headers = ["index", "avg", "max", "min", "std"]
    x = [30, 35, 45, 55, 65, 75, 85]

    @dataclass
    class plot_information:
        substance_name: str
        substance_name_on_file: str
        description: str

    plot_informations = [
        plot_information(
            substance_name="IL-6", substance_name_on_file="il6", description="IL-6 concentrations \n (relative values)"
        ),
        plot_information(
            substance_name="IL-8", substance_name_on_file="il8", description="IL-8 concentrations \n (relative values)"
        ),
        plot_information(
            substance_name="IL-10",
            substance_name_on_file="il10",
            description="IL-10 concentrations \n (relative values)",
        ),
        plot_information(
            substance_name="TNF", substance_name_on_file="TNF", description="TNF concentrations \n (relative values)"
        ),
        plot_information(
            substance_name="Cortisol",
            substance_name_on_file="cortisol",
            description="Cortisol concentrations \n (relative values)",
        ),
        plot_information(
            substance_name="Macrophage",
            substance_name_on_file="ma",
            description="Macrophage concentrations \n (relative values)",
        ),
    ]

    for information in plot_informations:
        figure, (ax2) = matplotlib.pyplot.subplots(1, 1)

        for i in range(6):
            file_name = (
                f"Output/{simulation_gender}_{cortisol_exp[i]}_week/{days}_{information.substance_name_on_file}.csv"
            )

            value = pandas.read_csv(file_name, header=None)
            value_transposed = value.T

            plot_label = f"Decade {decades[i]}"
            x_axis = numpy.linspace(0, days, days * 1000)

            y_axis = value_transposed[0]

            ax2.plot(x_axis, y_axis, ".", label=plot_label)

        ax2.legend(bbox_to_anchor=(0.5, -0.15), loc="upper center", fontsize=18, fancybox=True, shadow=True, ncol=5)
        ax2.set_ylabel(information.description, fontsize=18)
        ax2.set_xlabel("Time (days)", fontsize=18)
        figure.set_figwidth(15)
        figure.set_figheight(6)
        figure.tight_layout()

        matplotlib.pyplot.savefig(
            f"Output/week_post_processing/{information.substance_name_on_file}_{simulation_gender}.png",
            bbox_inches="tight",
        )
