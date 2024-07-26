import time
import cortisol_decades
import create_plots
import multiprocessing
import argparse

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("days", default=7, nargs="?", type=int)
simulation_days: int = parser.parse_args().days

simulation_gender = "F"

cortisol_exp_F = [2.32, 2.24, 2.25, 2.43, 2.55, 2.80]
cortisol_exp_M = [2.32, 2.25, 2.55, 2.62, 2.84, 3.13]
cortisol_exp_use = cortisol_exp_F if simulation_gender == "F" else cortisol_exp_M

gluc_intake_decade_multiplier = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]

# todozao: Fazer o teste mantendo o valor do cortisol fixo e testar da glucose fixa
# tb pra ver a variação das citocinas com os 7 dias por decada

processes = [
    multiprocessing.Process(
        target=cortisol_decades.cortisolDecadesOneWeek,
        args=(simulation_gender, cortisol_exp_use[i], gluc_intake_decade_multiplier[i], simulation_days),
    )
    for i in range(6)
]

for process in processes:
    process.start()

for process in processes:
    process.join()

end = time.time()

print(f"Time: {int(end - start)}s")

print("Simulation done. Starting post-processing.")

create_plots.create_plots(
    simulation_gender="female" if simulation_gender == "F" else "male",
    days=simulation_days,
    cortisol_exp=cortisol_exp_use,
)
