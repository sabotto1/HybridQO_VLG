from datetime import datetime

from ltr_db_optimizer.model.model_interface import create_model
import pickle
import os

from ltr_db_optimizer.ext.ptranking.ltr_adhoc.listwise.listnet import ListNet
from ltr_db_optimizer.ext.ptranking.ltr_adhoc.listwise.listmle import ListMLE

from ltr_db_optimizer.ext.ptranking.ltr_adhoc.listwise.lambdaloss import LambdaLoss
from ltr_db_optimizer.ext.ptranking.ltr_adhoc.listwise.lambdarank import LambdaRank
from ltr_db_optimizer.ext.ptranking.ltr_adhoc.listwise.rank_cosine import RankCosine

from ltr_db_optimizer.ext.ptranking.ltr_adhoc.listwise.approxNDCG import ApproxNDCG
from ltr_db_optimizer.ext.ptranking.ltr_adhoc.listwise.softrank import SoftRank
from argparse import ArgumentParser
from ltr_db_optimizer.ext.ptranking.ltr_adhoc.pairwise.ranknet import RankNet


from ltr_db_optimizer.extra_utils import get_the_split_of_training_data


parser = ArgumentParser()

parser.add_argument("--mn", type=str, default='HM', help="model's name to indicate model's architecture")

parser.add_argument("--score_func", type=str, default='linearR')
parser.add_argument("--score_n", type=int, default=50)
parser.add_argument("--score_bord", type=int, default=97)

parser.add_argument("--loss_func", type=str, default="lambdaloss")
parser.add_argument("--loss_type", type=str, default="NDCG_Loss2++", help="NDCG_Loss2++")
parser.add_argument("--sigma", type=float, default=0.5)
parser.add_argument("--ll_k", type=int, default=5)
parser.add_argument("--mu", type=float, default=1.0)
parser.add_argument("--presort", type=bool, default=False)

parser.add_argument("--iter", type=str, default="None")

parser.add_argument("--train_wk", type=str, default="", help="training workload/data")
parser.add_argument("--postfix", type=str, default="")





args = parser.parse_args()
model_name = args.mn

if args.loss_func == "lambdaloss":
    loss_func = LambdaLoss
elif args.loss_func == "listmle":
    loss_func = ListMLE
elif args.loss_func == "rankcosine":
    loss_func = RankCosine
elif args.loss_func == "listnet":
    loss_func = ListNet
elif args.loss_func == "lambdarank":
    loss_func = LambdaRank
elif args.loss_func == "softrank":
    loss_func = SoftRank
elif args.loss_func == "approxndcg":
    loss_func = ApproxNDCG
elif args.loss_func == "ranknet":
    loss_func = RankNet



score_func = args.score_func
score_n = args.score_n
score_bord = args.score_bord
iter = args.iter

training_workload = args.train_wk
postfix = args.postfix


directory = "./LTR4QO"

root_path = f"{directory}/Data"

print("Start Time =", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

Start_time = datetime.now()

optimizer = "adam"


# workload = "job_part"

with open(f"{root_path}/training_data/{score_func}_{training_workload}{postfix}_query_enc_norm.pickle", "rb") as f:
    vectors = pickle.load(f)
with open(f"{root_path}/training_data/{score_func}_{training_workload}{postfix}_plan_enc_norm.pickle", "rb") as f:
    plans = pickle.load(f)
with open(f"{root_path}/training_data/{score_func}_{training_workload}{postfix}_labels_norm.pickle", "rb") as f:
    labels = pickle.load(f)


assert len(plans.keys()) == len(vectors.keys()) == len(labels.keys()), "the number of plan encoding, query encoding, and labels does not match!!"

split_valid, split_test = get_the_split_of_training_data(plan_keys=list(plans.keys()), valid_ratio=0.2, test_ratio=0.0, workload=training_workload)

print('split_valid detail: ',  len(split_valid), split_valid[:10])

print('split_test detail: ',  len(split_test), split_test[:10])


sorted_plans = {}
sorted_vecs = {}

for plan_key in plans.keys():
    # job_nr = plan_key.split("_")[0]
    job_nr = "_".join(plan_key.split("_")[:-1])

    if not job_nr in sorted_plans.keys():
        sorted_plans[job_nr] = {}
    sorted_plans[job_nr][plan_key] = plans[plan_key]
    if not job_nr in sorted_vecs.keys():
        sorted_vecs[job_nr] = {}
    sorted_vecs[job_nr][plan_key] = vectors[plan_key]

print('total number of jobs: ', len(list(sorted_plans.keys())))


X_test_tree = {}
X_test_vecs = {}
y_test = {}

X_train_tree = {}
X_train_vecs = {}
y_train = {}

X_valid_tree = {}
X_valid_vecs = {}
y_valid = {}
control_dict = {}

for key in sorted_plans.keys():
    # if key.split("_")[0] in split_test:
    if key in split_test:
        X_test_tree[key] = {}
        X_test_vecs[key] = {}
        for subkey in sorted_plans[key].keys():
            y_test[subkey] = labels[subkey]
            X_test_tree[key][subkey] = sorted_plans[key][subkey]
            X_test_vecs[key][subkey] = sorted_vecs[key][subkey]
    elif key in split_valid:
        X_valid_tree[key] = {}
        X_valid_vecs[key] = {}
        for subkey in sorted_plans[key].keys():
            y_valid[subkey] = labels[subkey]
            X_valid_tree[key][subkey] = sorted_plans[key][subkey]
            X_valid_vecs[key][subkey] = sorted_vecs[key][subkey]
    else:
        X_train_tree[key] = {}
        X_train_vecs[key] = {}
        for subkey in sorted_plans[key].keys():
            y_train[subkey] = labels[subkey]
            X_train_tree[key][subkey] = sorted_plans[key][subkey]
            X_train_vecs[key][subkey] = sorted_vecs[key][subkey]


print('the number of X_train vecs:', len(X_train_vecs.keys()))
print('the number of X_valid vecs:', len(X_valid_vecs.keys()))
print('the number of X_test vecs:', len(X_test_vecs.keys()))



if args.score_func == "special":
    score_info = args.score_func
else:
    score_info = args.score_func


if args.loss_func == "lambdaloss":
    model_info = '_'.join(['MODEL', model_name, args.loss_func, 'sigma', str(args.sigma), 'k', str(args.ll_k), 'mu', str(args.mu), args.loss_type, 'presort', str(args.presort)])
else:
    model_info = '_'.join(['MODEL', model_name, args.loss_func])


print("Begin training with ", score_info + '###' + model_info)

model_save_name =  model_info + "_" + "TWL" + "_" + training_workload + "_" + postfix + "_" + score_info + "_" + "ITER" + "_" + iter

folder = f"./ltr_db_optimizer/model/saved_models"

os.system(f"mkdir -p {folder}")

print('model saving name: ', f"{folder}/{model_save_name}")

if os.path.exists(f"{folder}/{model_save_name}"):
    print('Model file already exists and needs to be deleted first!!!')
    os.system(f'rm -rf {folder}/{model_save_name}')
    print('after deleting, check if the model file still exists: ', os.path.exists(f"{folder}/{model_save_name}"))
else:
    print("Model file not exists!")


if args.loss_func == "lambdaloss":
    model = create_model(loss_func, folder=folder, name=model_save_name, workload=training_workload, model_para_dict={"sigma": args.sigma, 'k': args.ll_k, 'mu': args.mu, 'loss_type': args.loss_type})
elif args.loss_func in ["listmle", "rankcosine", "lambdarank", "softrank", "approxndcg"]:
    model = create_model(loss_func, folder=folder, name=model_save_name, workload=training_workload, model_para_dict={"sigma": args.sigma, 'k': args.ll_k, 'mu': args.mu, 'loss_type': args.loss_type})
elif args.loss_func == "ranknet": ### for lero model
    model = create_model(loss_func, folder=folder, name=model_save_name, workload=training_workload, model_para_dict={"sigma": 1.0})
else:
    model = create_model(loss_func, folder=folder, name=model_save_name, workload=training_workload)


model.fit(X_train_vecs, X_train_tree, y_train, X_valid_vecs, X_valid_tree, y_valid, use_presort=args.presort, optimizer=optimizer)
print('training is done!!!')
print("End Time =", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
End_time = datetime.now()
elapsed_time = round((End_time - Start_time).total_seconds()/60, 2)
print('total elapsed time for training: (mins)', elapsed_time)


# print('Model Test!!')
# avg_test_loss, avg_test_ndcg, avg_test_ndcg_new = model.test(X_test_vecs, X_test_tree, y_test)
# print('test ndcg: ', avg_test_ndcg)
# print('test ndcg sk: ', avg_test_ndcg_new)
# print('test loss: ', avg_test_loss)
# print("Finish testing", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))





