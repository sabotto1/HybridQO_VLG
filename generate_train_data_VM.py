
import ltr_db_optimizer.model.featurizer_graph_train as feature_extraction

import pickle


from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument("--workload", type=str, default='None', help="training queries: job_part/tpch1000/stats1000")

parser.add_argument("--nr_jobs", type=int, default=1000)

parser.add_argument("--postfix", type=str, default="")

parser.add_argument("--score_func", type=str, default="linearR")


# workload = "job_part"
# workload = "tpch1000"
# workload = "stats1000"

args = parser.parse_args()
workload = args.workload
nr_jobs = args.nr_jobs
postfix = args.postfix
score_func = args.score_func
root_path = f"./LTR4QO/Data/subplans_{workload}"


training_data_path = "./LTR4QO/Data/"


vectors, plans, labels = feature_extraction.featurize_with_labels_Random(f"{root_path}", f"{root_path}",
                                                                    f"{root_path}/all_cost_labels.csv", workload=workload, nr_jobs=nr_jobs,
                                                                  score_function=score_func,  postfix=postfix)

print(f'{score_func}: number of query samples, plan samples, and label samples', len(vectors.keys()), len(plans.keys()), len(labels.keys()))


with open(f"{training_data_path}/training_data/{score_func}_{workload}{postfix}_query_enc_norm.pickle", "wb") as f:
    pickle.dump(vectors, f)

with open(f"{training_data_path}/training_data/{score_func}_{workload}{postfix}_plan_enc_norm.pickle", "wb") as f:
    pickle.dump(plans, f)

with open(f"{training_data_path}/training_data/{score_func}_{workload}{postfix}_labels_norm.pickle", "wb") as f:
    pickle.dump(labels, f)
















