import pickle
import numpy
from wdl.build_wdl_fp_v0 import build_wdl_fingerprint_fun
from wdl.run_utils import read_csv
from wdl.run_utils import save_result_to_csv2, save_result_to_csv


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
                        layer_weight=0.5,
                        n_estimators=100,
                        max_features='sqrt',
                        L2_reg=numpy.exp(-2))

    def build_single_weight_fp_experiment(input_smiles, init_weights, x=0):
        fp_depth = x
        hidden_layer_sizes = [model_params['hidden_width']] * fp_depth
        hidden_arch_params = {'num_hidden_features': hidden_layer_sizes,
                              'fp_length': model_params['fp_length'], 'normalize': 1}
        fp_func, conv_parser = build_wdl_fingerprint_fun(**hidden_arch_params)
        datafp = fp_func(init_weights, input_smiles)
        return datafp

    def build_weight_fp_experiment(input_smiles,init_weight):
        train_x0 = build_single_weight_fp_experiment(input_smiles,init_weight, 0)
        train_x = model_params['layer_weight'] * train_x0
        for i in range(1, model_params['fp_depth']):
            train_x1 = build_single_weight_fp_experiment(input_smiles,init_weight, i)
            train_x = train_x + model_params['layer_weight'] * (train_x1 - train_x0)
            train_x0 = train_x1
        train_xx = build_single_weight_fp_experiment(input_smiles,init_weight, model_params['fp_depth'])
        train_x = train_x + train_xx - train_x0
        return train_x

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
    trained_weights_file = 'E:\\wdl_rf_package\\wdl_rf\\model\\'+temp+'_trained_weights.pkl'
    model_file = 'E:\\wdl_rf_package\\wdl_rf\\model\\'+temp+'_RF.pkl'
    fp, pvalue = predict_fp_and_pvalue(input_file, trained_weights_file, model_file)
    save_result_file = 'E:\\wdl_rf_package\\wdl_rf\\result\\'+temp+'_result.csv'
    save_result_to_csv2(input_file, save_result_file, pvalue, fp)
