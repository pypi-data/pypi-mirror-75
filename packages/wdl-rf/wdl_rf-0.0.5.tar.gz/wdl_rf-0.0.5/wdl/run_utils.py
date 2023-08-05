import csv
import numpy as np
from wdl.util import wdl_lose_fun, rmse
from sklearn.model_selection import KFold


def file_split(filename):
    """
    将数据集切分为训练集、验证集、测试集
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        num = len(f.readlines()) - 1
    N_val = int(round(num / 5.0))
    N_test = int(round(num / 5.0))
    N_train = num - N_val - N_test
    return (N_train, N_val, N_test)


def file_split2(filename):
    """
    将数据集按3：1切分为训练集、测试集
    :param filename:
    :return:（训练集的个数，测试集的个数）
    """
    with open(filename, 'r') as f:
        num = len(f.readlines()) - 1
    N_test = int(round(num / 4.0))
    N_train = num - N_test
    return (N_train, N_test)


def save_experiment(filename, c1, c2, c3, c4, c5):
    """
    记录训练的结果
    :param filename: 保存的文件
    :param c1: input_File
    :param c2: num_iters
    :param c3: batch_size
    :param c4: RMSE
    :param c5: R2
    :return:
    """
    if len(filename) != 0:
        print("实验结果保存到：", filename)
        with open(filename, 'a', newline='') as fw:
            writer = csv.writer(fw)
            writer.writerow([c1, c2, c3, c4, c5])


def read_csv(filename):
    """从输入的文件中获取smiles分子式,输入文件的第一行是列名"""
    res = []
    with open(filename, 'r') as fr:
        reader = csv.DictReader(fr)
        for line in reader:
            res.append(line['smiles'])
    return res


def write_csv(filename, data):
    """将结果data存到filename文件中"""
    with open(filename, 'w', newline='') as fw:
        writer = csv.writer(fw)
        for i in data:
            writer.writerow([i])


def save_result_to_csv(inputfile, outputfile, data, column_name):
    """
    保存结果
    :param inputfile: 原始输入的待预测配体分子的文件，作为保存结果文件的模板
    :param outputfile: 输出结果所保存的文件
    :param data: 预测得到的结果
    :param column_name: 保存文件中当前列的列名
    :return:
    """
    print('得出', column_name, '存放在', outputfile)
    with open(inputfile, 'r') as fr:
        lines = csv.reader(fr)
        with open(outputfile, 'w', newline='') as fw:
            writer = csv.writer(fw)
            i = 0
            for l in lines:
                if i == 0:
                    l.append(column_name)
                    writer.writerow(l)
                else:
                    l.append(data[i - 1])
                    writer.writerow(l)
                i += 1


def save_result_to_csv2(inputfile, outputfile, pvalue, fp):
    """
    保存预测得到的活性和分子指纹,文件第一行都是列名
    :param inputfile: 原始输入的待预测配体分子的文件
    :param outputfile: 输出结果所保存的文件
    :param pvalue: 预测得到的配体分子与gpce的结合活性
    :param fp: 生成的分子指纹
    :return:
    """
    print('输出的分子指纹和生物活性所保存的文件：', outputfile)
    with open(inputfile, 'r') as fr:
        lines = csv.reader(fr)
        with open(outputfile, 'w', newline='') as fw:
            writer = csv.writer(fw)
            i = 0
            for l in lines:
                if i == 0:
                    l.append('predict_value')
                    l.append('fp')
                    writer.writerow(l)
                else:
                    l.extend([pvalue[i - 1], fp[i - 1]])
                    writer.writerow(l)
                i += 1


def divide_data(file, k=1):
    """
    读取file文件，按k折交叉验证拆分数据集。当k=1时不做交叉验证，直接按3：1切分训练集和测试集
    :param file:
    :param k:
    :return:
    """
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = -1
        smiles, value, res = [], [], []
        for row in csv_reader:
            line_count += 1
            if line_count != 0:
                """去除第一行列名"""
                smiles.append(f'{row[2]}')
                value.append(float(f'{row[1]}'))
        X = np.asarray(smiles)
        Y = np.asarray(value)
    if k > 1:
        kf = KFold(n_splits=k, shuffle=True, random_state=1)
        # kf = KFold(n_splits=k)
        for train_index, test_index in kf.split(X, Y):
            train_x = X[train_index]
            train_y = Y[train_index]
            test_x = X[test_index]
            test_y = Y[test_index]
            res.append((train_x, train_y, test_x, test_y))
            # print('test:\n',test_index,test_index.shape)
    else:
        """不做交叉验证，直接将数据按3：1切分为训练集和验证集"""
        N_test = int(round(line_count / 4.0))
        N_train = line_count - N_test
        train_index = range(N_train)
        test_index = range(N_train, line_count)
        train_x = X[train_index]
        train_y = Y[train_index]
        test_x = X[test_index]
        test_y = Y[test_index]
        res.append((train_x, train_y, test_x, test_y))
        # print('train:\n',list(train_index))
        # print('test:\n', list(test_index))
        # print(test_y)
    return res


class InitParam():
    """wdl_rf训练所需要的参数类"""
    file_params = {'target_name': 'STANDARD_VALUE',
                   'input_file': 'E:\keti_data\A1.csv', }

    train_params = dict(num_iters=200,
                        batch_size=5,
                        init_scale=np.exp(-4),
                        step_size=0.01)

    model_params = dict(fp_length=50,
                        fp_depth=4,
                        hidden_width=20,
                        h1_size=100,
                        layer_weight=0.5,
                        n_estimators=100,
                        max_features='sqrt',
                        L2_reg=np.exp(-2))
    vanilla_net_params = dict(
        layer_sizes=[model_params['fp_length'], model_params['h1_size']],
        normalize=True, L2_reg=model_params['L2_reg'], nll_func=rmse)

    save_params = dict(flag=False, weights_file="weights.pkl", model_file="model.pkl")
    record_file = ""
    source_domain_weights_file = ""

    def __init__(self, filename, n_iters, batch_size):
        self.file_params['input_file'] = filename
        self.train_params['num_iters'] = n_iters
        self.train_params['batch_size'] = batch_size

    def set_save_model_file(self, weights_file, model_file):
        """
        设置保存模型的文件
        :param weights_file: wdl部分的权重，文件路径写全路径
        :param model_file: rf模型
        :return:
        """
        self.save_params['flag'] = True
        self.save_params['weights_file'] = weights_file
        self.save_params['model_file'] = model_file

    def set_save_record_file(self, filename):
        """
        设置训练结果的记录文件
        :param filename: 存放训练结果的文件
        :return:
        """
        self.record_file = filename

    def set_source_domain_weights_file(self, filename):
        """
        运用迁移学习，设置源域训练得到的权重文件
        :param filename:
        :return:
        """
        self.source_domain_weights_file = filename


class InitParam2():
    """wdl_rf2训练模型的一些必要参数类"""
    task_params = {'target_name': 'STANDARD_VALUE',
                   'data_file': ''}

    model_params = dict(fp_length=50,
                        fp_depth=4,
                        hidden_width=20,
                        h1_size=100,
                        n_estimators=100,
                        max_features='log2',
                        L2_reg=np.exp(-2))

    train_params = dict(num_iters=500,
                        batch_size=30,
                        init_scale=np.exp(-4),
                        step_size=0.01)

    # Define the architecture of the network that sits on top of the fingerprints.
    vanilla_net_params = dict(
        layer_sizes=[model_params['fp_length'], model_params['h1_size']],
        normalize=True, L2_reg=model_params['L2_reg'], nll_func=wdl_lose_fun)

    save_params = dict(flag=False, weights_file="", model_file="")
    record_file = ""
    source_domain_weights_file = ""

    def __init__(self, filename, n_iters, batch_size):
        self.task_params['data_file'] = filename
        self.train_params['num_iters'] = n_iters
        self.train_params['batch_size'] = batch_size

    def set_save_model_file(self, weights_file, model_file):
        """
        设置保存模型的文件
        :param weights_file: wdl部分的权重，文件路径写全路径
        :param model_file: rf模型
        :return:
        """
        self.save_params['flag'] = True
        self.save_params['weights_file'] = weights_file
        self.save_params['model_file'] = model_file

    def set_save_record_file(self, filename):
        """
        设置训练结果的记录文件
        :param filename: 存放训练结果的文件
        :return:
        """
        self.record_file = filename

    def set_source_domain_weights_file(self, filename):
        """
        运用迁移学习，设置源域训练得到的权重文件
        :param filename:
        :return:
        """
        self.source_domain_weights_file = filename


if __name__ == "__main__":
    print(InitParam.file_params['input_file'].split('\\')[-1].split('.')[0] + '.pkl')

