import os
import time
from roshambo.api import get_similarity_scores

st = time.perf_counter()

database_dir = '/dbpath'
ref_lig = 'ref.sdf'
wd = os.getcwd()

for db in os.listdir(database_dir):
    db_name = os.path.splitext(os.path.basename(f"{database_dir}/{db}"))[0]
    print(db_name)
    get_similarity_scores(
        ref_file=f"{ref_lig}",
        dataset_files_pattern=f"{db}",
        ignore_hs=True,
        n_confs=0,
        use_carbon_radii=True,
        color=True,
        sort_by="ComboTanimoto",
        write_to_file=True,
        gpu_id=0,
        working_dir=f"{wd}",
    )
    os.rename('hits.sdf', f'{db_name}_hits.sdf')
    os.rename('roshambo.csv', f'{db_name}_hits.csv')
    print(f'Roshambo run for {db_name}: Complete')

et = time.perf_counter()
print(f"Roshambo took: {(et - st) / 60} min to complete.")
