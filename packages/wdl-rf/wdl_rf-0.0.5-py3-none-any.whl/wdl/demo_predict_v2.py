import pickle
import numpy as np
from wdl.build_wdl_fp_v2 import build_wdl_fingerprint_fun
from wdl.run_utils import read_csv, save_result_to_csv, save_result_to_csv2

def predict_fp_and_pvalue(input_file,weights_file,model_file):
    """
    输出分子指纹和预测的生物活性
    :param input_file: 待预测的配体分子的SMILES分子式csv文件
    :param weights_file: 训练好的wdl网络的权重值pkl文件
    :param model_file: 训练好的RF模型pkl文件
    :return:
    """
    print("Loading data...")
    print('读取待预测文件：',input_file)
    input_smiles = read_csv(input_file)
    #print(input_smiles)
    model_params = dict(fp_length=50,
                        fp_depth=4,
                        hidden_width=20,
                        h1_size=100,
                        n_estimators=100,
                        max_features='log2',
                        L2_reg=np.exp(-2))

    def build_weight_fp_experiment(input_smiles,init_weight):
        conv_layer_sizes = [model_params['hidden_width']] * model_params['fp_depth']  # [20,20,20,20].
        conv_arch_params = {'num_hidden_features': conv_layer_sizes,
                            'fp_length': model_params['fp_length'], 'normalize': 1}
        conv_fp_func, conv_parser = build_wdl_fingerprint_fun(**conv_arch_params)
        input_fp = conv_fp_func(init_weight, input_smiles)
        return input_fp

    print("读取权重文件:",weights_file)
    with open(weights_file, 'rb') as fr:
        trained_weights = pickle.load(fr)
    fp = build_weight_fp_experiment(input_smiles,trained_weights)

    print('读取模型文件',model_file)
    with open(model_file, 'rb') as fr:
        rf_model = pickle.load(fr)
    p_value = rf_model.predict(fp)

    return fp,p_value

if __name__ == "__main__":
    input_file = 'E:\\keti_data\\A1.csv'
    temp = input_file.split('\\')[-1].split('.')[0]
    trained_weights_file = 'model\\'+temp+'_weights.pkl'
    model_file = 'model\\'+temp+'_rf.pkl'
    fp, pvalue = predict_fp_and_pvalue(input_file, trained_weights_file, model_file)
    save_result_file = 'result\\'+temp+'_pvalue_result.csv'
    save_result_to_csv(input_file, save_result_file, pvalue, 'predict_pvalue')
