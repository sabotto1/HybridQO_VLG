# from __future__ import print_function  # `__future__` has to be before other imports
import copy

from ltr_db_optimizer.enumeration_algorithm.table_info import TPCHTableInformation
from ltr_db_optimizer.enumeration_algorithm.table_info_5 import TPCHTableInformation5

from ltr_db_optimizer.enumeration_algorithm.table_info_imdb import IMDBTableInformation

from ltr_db_optimizer.enumeration_algorithm.table_info_stats import STATSTableInformation

from pyodbc import ProgrammingError, OperationalError
import os
import pandas as pd
from datetime import datetime
import time
from ltr_db_optimizer.parser import SQLParser
from argparse import ArgumentParser

from ltr_db_optimizer.extra_utils import set_DBMS, enumerate_by_SQL_Server




if __name__ == "__main__":
    parser = ArgumentParser()

    # random.seed(248)
    # np.random.seed(248)
    # torch.manual_seed(248)

    parser.add_argument("--emd", type=str, default='HM')

    parser.add_argument("--db", type=str, default="tpch")

    parser.add_argument('--tq', type=str, default="tpch-o")

    parser.add_argument('--topk', type=int, default=20)

    parser.add_argument('--do_enum', type=bool, default=True)

    parser.add_argument('--do_runtime', type=bool, default=True)

    parser.add_argument('--iter', type=str, default='None')

    parser.add_argument("--mn", type=str, default='special_50_97_MODEL_LTRankModel1_lambdaloss_sigma_0.5_k_5_mu_1.0_NDCG_Loss2++_presort_False')


    print('start time: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Start_time = datetime.now()

    args = parser.parse_args()

    targeted_enum_method = args.emd

    targeted_database = args.db

    targeted_test_query = args.tq

    targeted_model_name = args.mn

    iter = args.iter

    k = args.topk

    db_maxrows = {'tpch': 6001215, "imdb": 36244343, "stats":328064}


    if args.emd not in ["DB", 'Optime']:
        train_wk = targeted_model_name.split('TWL_')[1].split('_')[0]
        train_wk_info =  targeted_model_name.split('TWL_')[1].split('_')[1]
        train_tree_high, train_tree_low = train_wk_info.split('Tree')[1].split('%')
        train_tree_high = int(train_tree_high)
        train_tree_low = int(train_tree_low)

        print('train_wk', train_wk)

        if args.db in train_wk:
            print(111)
            tree_high = copy.copy(train_tree_high)
            tree_low = copy.copy(train_tree_low)

        else:
            print(222)

            if 'tpch' in train_wk:
                source_db = 'tpch'
            elif ("job" in train_wk) or ('imdb' in train_wk):
                source_db = 'imdb'
            elif "stats" in train_wk:
                source_db = 'stats'

            max_rows_source_data = db_maxrows[source_db]
            max_rows_target_data = db_maxrows[args.db]

            tree_high = (max_rows_target_data/max_rows_source_data)*train_tree_high

            tree_low = 1


        print('Training workload: ', train_wk)
        print('Tree info: ', tree_high, tree_low)

    print('Argumments: ', args)

    cursor = set_DBMS(db=targeted_database)


    ### dataset info.
    if targeted_database == "tpch":
        TableInformation = TPCHTableInformation()
    elif targeted_database == "imdb":
        TableInformation = IMDBTableInformation()
    elif targeted_database == "tpch5":
        TableInformation = TPCHTableInformation5()
    elif targeted_database == "stats":
        TableInformation = STATSTableInformation()


    ### enum method info.
    if targeted_enum_method == "Ada":
        from ltr_db_optimizer.enumeration_algorithm.enumeration_algorithm import EnumerationAlgorithm
        print("from ltr_db_optimizer.enumeration_algorithm.enumeration_algorithm_XL import EnumerationAlgorithm")



    ### trained ranking model to rank plans in enumeration process
    # model = f"ltr_db_optimizer/model/saved_models/{targeted_model_name}/best_avg_ndcg.pth"
    print('targeted_model_name:', targeted_model_name)
    if targeted_model_name != None and targeted_model_name != "None":
        model_archi_name = targeted_model_name.split("MODEL_")[1].split("_")[0]

        print('used Model Architecture: ', model_archi_name)
        if model_archi_name  == "HM":
            model = f"ltr_db_optimizer/model/saved_models/{targeted_model_name}/avg_k.pth"
        else:
            model = f"ltr_db_optimizer/model/saved_models/{targeted_model_name}/min_avg_valid_loss.pth"


    ### test queries info.

    if targeted_test_query in ["tpch-d"]:

        query_folder_name = "tpch_test"  # tpch_query
        query_path = f'Data/{query_folder_name}/'

    elif targeted_test_query == "stats-r":
        query_folder_name = "stats_test"
        query_path = f"Data/{query_folder_name}/"
        query_file_names = os.listdir(query_path)
        testquery = []
        for stats_query in query_file_names:
            if stats_query.endswith(".txt") and (stats_query.startswith("qt") or stats_query.startswith("tq")):
                testquery.append(stats_query.split(".")[0])

    elif targeted_test_query == "imdb-r":
        query_folder_name = "imdb_test"
        query_path = f"Data/{query_folder_name}/"
        query_file_names = os.listdir(query_path)
        testquery = []
        for imdb_query in query_file_names:
            if imdb_query.endswith(".sql"):
                testquery.append(imdb_query.split(".")[0])

        testquery = sorted(testquery, reverse=False)


    elif targeted_test_query == "job-c":
        query_folder_name = "job-complex"
        query_path = f"Data/{query_folder_name}/"
        query_file_names = os.listdir(query_path)
        testquery = []
        for imdb_query in query_file_names:
            if imdb_query.endswith(".sql"):
                testquery.append(imdb_query.split(".")[0])

        testquery = sorted(testquery, reverse=False)



    if args.do_enum:
        all_inference_times = []

        for job_index, job in enumerate(testquery):

            if targeted_test_query == "tpch-d" and job in ["Job17v3", "Job1131v3", "Job128v3"]:
                continue

            if targeted_test_query == "tpch-l" and job not in ['Job49v1', 'Job44v3', 'Job25v1', 'Job253v4', 'Job253v0',
                                                               'Job185v3', 'Job185v2', 'Job16v0', 'Job161v0', 'Job1325v3',
                                                               'Job1300v2', 'Job128v4', 'Job128v3', 'Job128v0', 'Job1252v1',
                                                               'Job1103v3', 'Job1034v4', 'Job1034v0', 'Job1033v4', 'Job1028v2',
                                                               'Job1021v1', 'Job1017v3', 'Job1017v1', 'Job1011v2']:


                continue

            if targeted_test_query == "tpch-s" and job in ["Job1300v2"]:
                continue

            # if targeted_test_query == "job-c" and job in ["19", "16"]:
            #     continue

            if targeted_test_query == "job-c" and job in ["12"]:
                continue

            # if targeted_test_query == "job-c" and job not in ["11"]:
            #     continue

            print('enumerate job: ', job_index, job)


            ###load query
            if os.path.exists(f"{query_path}/{job}.txt"):
                with open(f"{query_path}/{job}.txt", "r") as f:
                    sql_full = f.read()
            else:
                with open(f"{query_path}/{job}.sql", "r") as f:
                    sql_full = f.read()

            sql_full = sql_full.replace("tcph", "tpch")
            # sql_full = sql_full.replace("tpch5", "tpch")


            if targeted_enum_method == "DB":
                enum_time = enumerate_by_SQL_Server(job, sql_full, query_folder_name, cursor, iter)
                all_inference_times.append(['DB', job, enum_time, 'ms'])
                continue

            path_out = f"results/enumerated_plans_{targeted_enum_method}_{targeted_model_name}/{query_folder_name}/iter{iter}/{job}/"

            if targeted_test_query in ["job-o", "stats-o"] and os.path.exists(path_out):
                print(f'{job} in {targeted_test_query} alreay enumerated and thus ignored!')
                continue

            ### parse query
            sql_dict, alias_dict = SQLParser.from_sql(sql_full, temp_table_info=TableInformation)
            # print('sql_dict', sql_dict)
            # print('alias_dict', alias_dict)


            ###enumeration
            enum = EnumerationAlgorithm(sql_dict,
                                        TableInformation,
                                        model,
                                        sql_full,
                                        k,
                                        alias_dict=alias_dict, train_wk=train_wk, tree_high=tree_high, tree_low=tree_low)


            best_plans = enum.find_best_plan()

            print('the number of returned best plans', len(best_plans))

            # path_out = f"results/enumerated_plans_{targeted_enum_method}_{targeted_model_name}/{query_folder_name}/iter{iter}/{job}/"

            # os.mkdir(path_out)
            os.system(f"mkdir -p {path_out}")
            # pathlib.Path(path_out).mkdir(parents=True, exist_ok=True)

            for idx, plan in enumerate(best_plans):
                xml = enum.to_xml(plan)

                with open(path_out + str(idx) + ".txt", "w") as f:
                    f.write(xml)
                # with open(path_out + str(idx) + ".pickle", "wb") as f:
                #     pickle.dump(plan, f)



    if args.do_runtime:
        ### get runtime of plans
        print('Enumeration done! Continue to obtain runtime of enumerated plans !!!')
        print('Current time: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        all_runtime_list = []
        for job_index, job in enumerate(testquery):


            if targeted_test_query == "tpch-d" and job in ["Job17v3", "Job1131v3", "Job128v3"]:
                continue

            if targeted_test_query == "tpch-l" and job not in ['Job49v1', 'Job44v3', 'Job25v1', 'Job253v4', 'Job253v0',
                                                               'Job185v3', 'Job185v2', 'Job16v0', 'Job161v0',
                                                               'Job1325v3',
                                                               'Job1300v2', 'Job128v4', 'Job128v3', 'Job128v0',
                                                               'Job1252v1',
                                                               'Job1103v3', 'Job1034v4', 'Job1034v0', 'Job1033v4',
                                                               'Job1028v2',
                                                               'Job1021v1', 'Job1017v3', 'Job1017v1', 'Job1011v2']:
                continue

            # if targeted_test_query == "job-c" and job in ["11", "18"]:
            #     continue

            if targeted_test_query == "job-c" and job in ["12"]:
                continue

            # if targeted_test_query == "job-c" and job in ["19", "16"]:
            #     continue


            # if targeted_test_query == "stats-r" and job in ["tq575"]:
            #     continue

            # if targeted_test_query == "stats-o" and job not in ["q141", "q63", "q58", "q46", "q140", "q65", "q142", "q64", "q139", "q66", "q49"]:  # select *, q66 newly added
            #     continue


            # if targeted_test_query == "stats-o" and job in ["qo57", "qo47", "qo132"]: # select count(*)
            #     continue

            # sort_merge_join_jobs = ["8a", "9a", "9c", "9d", "17c", "17d", '17e', '17f', '20b', '22d']
            # if targeted_test_query == "job-o" and job not in sort_merge_join_jobs:
            #     continue

            # prune_at_end_test_query = ["32a", "23a", "5a", "6a", "2a", "11a", "12a", "13a", "4a", "1a"]
            # if targeted_test_query == "imdb-o" and job not in prune_at_end_test_query:
            #     continue

            print('run job: ', job_index, job)
            print('Job Start time: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            methods_runtime_list = []

            if targeted_enum_method == "DB":
                plan_path = f"results/enumerated_plans_{targeted_enum_method}/{query_folder_name}/iter{iter}/{job}/"
            else:
                plan_folder_postfix = "_".join([targeted_enum_method, targeted_model_name])
                plan_path = f"results/enumerated_plans_{plan_folder_postfix}/{query_folder_name}/iter{iter}/{job}/"


            with open(plan_path + str(0) + ".txt", "r") as f:
                plan_sql = f.read()
            try:
                cursor.execute("SET STATISTICS TIME ON")
                cursor.execute(plan_sql)
                while (cursor.nextset()):
                    mess = cursor.messages
                    # print('results:', mess)
                    if len(mess[0][1].split(",")) == 3:
                        cpu = int(mess[0][1].split(",")[1].split("=")[1][:-3])
                        cpu_unit = mess[0][1].split(",")[1].split("=")[1][-3:]
                        time = int(mess[0][1].split(",")[2].split("=")[1][:-3])
                        time_unit = mess[0][1].split(",")[2].split("=")[1][-3:]
                    elif len(mess[0][1].split(",")) == 2:
                        cpu = int(mess[0][1].split(",")[0].split("=")[1][:-3])
                        cpu_unit = mess[0][1].split(",")[0].split("=")[1][-3:]
                        time = int(mess[0][1].split(",")[1].split("=")[1][:-3])
                        time_unit = mess[0][1].split(",")[1].split("=")[1][-3:]
                    else:
                        print('mess', mess)
                        continue
                result = [job, cpu, time, cpu + time, cpu_unit, time_unit]

            except OperationalError as err:
                print("Timeout")
                print(job, targeted_enum_method, targeted_model_name, err)
                result = [job, -1, -1, -1, 'ms', 'ms']
                print("----")

            except ProgrammingError as err:
                print('WeridError')
                print(job, targeted_enum_method, targeted_model_name, err)
                if targeted_enum_method != "DB":
                    result = [job, -2, -2, -2, 'ms', 'ms']
                    print("----")
                else:
                    pure_sql = plan_sql.split("OPTION")[0] + " OPTION (MAXDOP 1) "
                    ### rerun the pure sql instead of plan
                    cursor.execute("SET STATISTICS TIME ON")
                    cursor.execute(pure_sql)
                    while (cursor.nextset()):
                        mess = cursor.messages
                        # print('results:', mess)
                        if len(mess[0][1].split(",")) == 3:
                            cpu = int(mess[0][1].split(",")[1].split("=")[1][:-3])
                            cpu_unit = mess[0][1].split(",")[1].split("=")[1][-3:]
                            time = int(mess[0][1].split(",")[2].split("=")[1][:-3])
                            time_unit = mess[0][1].split(",")[2].split("=")[1][-3:]
                        elif len(mess[0][1].split(",")) == 2:
                            cpu = int(mess[0][1].split(",")[0].split("=")[1][:-3])
                            cpu_unit = mess[0][1].split(",")[0].split("=")[1][-3:]
                            time = int(mess[0][1].split(",")[1].split("=")[1][:-3])
                            time_unit = mess[0][1].split(",")[1].split("=")[1][-3:]
                        else:
                            print('mess', mess)
                            continue
                    result = [job, cpu, time, cpu + time, cpu_unit, time_unit]
            except Exception as exce:
                print('Exception:', Exception)
                continue

            print('statistic:', result)
            print('Job End time: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            methods_runtime_list.append(result)

            df = pd.DataFrame(methods_runtime_list, index=[targeted_enum_method])
            print('df', df)
            df.columns = "Job,CPU time,Time,Sum,CPU unit,Time unit".split(',')
            all_runtime_list.append(df)

            all_runtime_df = pd.concat(all_runtime_list, axis=0)

            if targeted_enum_method == "DB":
                all_df_path = f"results/dataset_{targeted_database}_workload_{targeted_test_query}_enum_{targeted_enum_method}_iter_{iter}_runtime.csv"
            else:
                all_df_path = f"results/dataset_{targeted_database}_workload_{targeted_test_query}_enum_{targeted_enum_method}_rank_{targeted_model_name}_iter_{iter}_runtime.csv"
                # all_df_path = f"results/dataset_{targeted_database}_workload_{targeted_test_query}_enum_{targeted_enum_method}_rank_{targeted_model_name}_runtime.csv"

            all_runtime_df.to_csv(all_df_path, index=True, header=True)


        ### describe the runtime distributions of test queries
        runtime_desc_list = []
        for method in [targeted_enum_method]:
            method_runtime_df = all_runtime_df[all_runtime_df.index == method]
            method_runtime_desc_df = method_runtime_df['Time'].describe()
            runtime_desc_list.append(method_runtime_desc_df)

        runtime_desc_df = pd.concat(runtime_desc_list, axis=1)
        runtime_desc_df.columns = [targeted_enum_method]
        runtime_desc_df = runtime_desc_df.round(1)

        if targeted_enum_method == "DB":
            runtime_desc_file_path = f"results/dataset_{targeted_database}_workload_{targeted_test_query}_enum_{targeted_enum_method}_iter_{iter}_runtime_descr.csv"
        else:
            runtime_desc_file_path = f"results/dataset_{targeted_database}_workload_{targeted_test_query}_enum_{targeted_enum_method}_rank_{targeted_model_name}_iter_{iter}_runtime_descr.csv"
            # runtime_desc_file_path = f"results/dataset_{targeted_database}_workload_{targeted_test_query}_enum_{targeted_enum_method}_rank_{targeted_model_name}_runtime_descr.csv"

        runtime_desc_df.to_csv(runtime_desc_file_path, index=True, header=True)


    print('end time: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    End_time = datetime.now()

    Elapsed_time = round((End_time - Start_time).total_seconds()/60, 2)
    print('Total Elapsed Time: ', Elapsed_time)





"""
dataset_imdb_workload_imdb-r_enum_Ada_rank_MODEL_LTRankNet0_lambdaloss_sigma_0.5_k_5_mu_1.0_NDCG_Loss2++_presort_False_TWL_imdb39reshuff_Q6D10PrevTree53435600%1_linearR_ITER_334thSamTrain50%FixValid20%SamSize20NoScheduler_iter_None_runtime_descr.csv


MODEL_LTRankNet0_lambdaloss_sigma_0.5_k_5_mu_1.0_NDCG_Loss2++_presort_False_TWL_imdb39reshuff_Q6D10PrevTree53435600%1_linearR_ITER_334thSamTrain50%FixValid20%SamSize20NoScheduler


bash LTR_enumerate_plans_VM.sh Ada imdb-r imdb MODEL_LTRankNet0_lambdaloss_sigma_0.5_k_5_mu_1.0_NDCG_Loss2++_presort_False_TWL_imdb39reshuff_Q6D10PrevTree53435600%1_linearR_ITER_334thSamTrain50%FixValid20%SamSize20NoScheduler hyb

"""







