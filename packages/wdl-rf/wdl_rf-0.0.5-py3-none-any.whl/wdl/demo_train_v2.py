import autograd.numpy.random as npr
import pickle
from wdl.build_wdl_fp_v2 import build_wdl_deep_net, build_wdl_fingerprint_fun
from wdl.optimizers import adam
from wdl.util import build_batched_grad, rmse, Rs2
from sklearn.ensemble import RandomForestRegressor
from autograd import grad
from wdl.run_utils import InitParam2, divide_data, save_experiment


def train_nn(init_weights, pred_fun, loss_fun, num_weights, train_smiles, train_raw_targets, train_params,
             validation_smiles=None, validation_raw_targets=None):
    """loss_fun has inputs (weights, smiles, targets)"""
    print("Total number of weights in the network:", num_weights)
    #init_weights = npr.RandomState(seed).randn(num_weights) * train_params['init_scale']
    train_targets = train_raw_targets
    training_curve = []

    def callback(weights, iter):
        if iter % 50 == 0:
            # print ("max of weights", np.max(np.abs(weights)))
            # train_preds = undo_norm(pred_fun(weights, train_smiles[:num_print_examples]))
            train_preds = pred_fun(weights, train_smiles)
            cur_loss = loss_fun(weights, train_smiles, train_targets)
            training_curve.append(cur_loss)
            print("---------------")
            print("Iteration", iter, "loss", cur_loss)
            print("train RMSE", rmse(train_preds, train_raw_targets), \
                  "train R^2", Rs2(train_preds, train_raw_targets))
            if validation_smiles is not None:
                validation_preds = pred_fun(weights, validation_smiles)
                print("Validation RMSE", iter, ":", rmse(validation_preds, validation_raw_targets))
                print("Validation R^2", iter, ":", Rs2(validation_preds, validation_raw_targets))

    # Build gradient using autograd.
    grad_fun = grad(loss_fun)
    grad_fun_with_data = build_batched_grad(grad_fun, train_params['batch_size'],
                                            train_smiles, train_targets)

    # Optimize weights.
    trained_weights = adam(grad_fun_with_data, init_weights, callback=callback,
                           num_iters=train_params['num_iters'], step_size=train_params['step_size'])

    def predict_func(new_smiles):
        """Returns to the original units that the raw targets were in."""
        return pred_fun(trained_weights, new_smiles)

    return predict_func, trained_weights, training_curve

def train_one(param2,train_inputs,train_targets,test_inputs,test_targets):
    print("Loading data...")
    task_params = param2.task_params
    N_train, N_test = train_targets.shape,test_targets.shape
    model_params = param2.model_params
    train_params = param2.train_params
    vanilla_net_params = param2.vanilla_net_params

    def build_weight_fp_experiment(init_weight):
        conv_layer_sizes = [model_params['hidden_width']] * model_params['fp_depth']  # [20,20,20,20].
        conv_arch_params = {'num_hidden_features': conv_layer_sizes,
                            'fp_length': model_params['fp_length'], 'normalize': 1}
        conv_fp_func, conv_parser = build_wdl_fingerprint_fun(**conv_arch_params)
        train_x_fp = conv_fp_func(init_weight, train_inputs)
        test_x_fp = conv_fp_func(init_weight, test_inputs)
        return train_x_fp, test_x_fp

    def run_weight_fp_experiment():
        hidden_layer_sizes = [model_params['hidden_width']] * model_params['fp_depth']
        hidden_arch_params = {'num_hidden_features': hidden_layer_sizes,
                              'fp_length': model_params['fp_length'], 'normalize': 1}
        loss_fun, pred_fun, wfp_parser = \
            build_wdl_deep_net(hidden_arch_params, vanilla_net_params, model_params['L2_reg'])
        num_weights = len(wfp_parser)
        if len(param2.source_domain_weights_file)!=0:
            with open(param2.source_domain_weights_file,'rb') as fr:
                init_weights = pickle.load(fr,encoding='latin1')
        else:
            init_weights = npr.RandomState(0).randn(num_weights) * train_params['init_scale']
        predict_func, trained_weights, conv_training_curve = \
            train_nn(init_weights, pred_fun, loss_fun, num_weights, train_inputs, train_targets,
                     train_params, validation_smiles=test_inputs, validation_raw_targets=test_targets)
        return trained_weights

    print("Starting weight fingerprint experiment...")
    trained_weights = run_weight_fp_experiment()
    train_x, test_x = build_weight_fp_experiment(trained_weights)
    train_y = train_targets
    test_y = test_targets
    print("*******************WDL_RF2********************")
    print("input_file:", param2.task_params['data_file'])
    print(N_train, N_test)
    print("num_iters:", train_params["num_iters"])
    print("batch_size:", train_params["batch_size"])
    clf = RandomForestRegressor(param2.model_params['n_estimators'])
    clf.fit(train_x,train_y)
    test_predict = clf.predict(test_x)
    Rmse = rmse(test_predict,test_y)
    R2 = Rs2(test_predict,test_y)
    print("rmse:",Rmse)
    print("R2:",R2)
    save_experiment(param2.record_file, param2.task_params['data_file'], param2.train_params['num_iters'],
                   param2.train_params['batch_size'], Rmse, R2)
    if len(param2.source_domain_weights_file)!=0:
        print("使用源域训练得到的权重值做迁移学习,初始化权重为：",param2.source_domain_weights_file)
    if (param2.save_params['flag']):
        print("开启模型保存")
        with open(param2.save_params['weights_file'], 'wb') as fw:
            pickle.dump(trained_weights, fw)
        with open(param2.save_params['model_file'],'wb') as fw:
            pickle.dump(clf,fw)
    print("************************************************")

def train_experiment(param2,k=1):
    """
    训练wdl-rf2模型
    :param param2: 训练模型的一些必要参数类
    :param k: 做k折交叉验证，默认k=1不做交叉验证，直接将数据集按3：1切分为训练集和测试集
    :return:
    """
    for (train_inputs,train_targets,test_inputs,test_targets) in divide_data(param2.task_params['data_file'],k):
        train_one(param2,train_inputs,train_targets,test_inputs,test_targets)

if __name__ == '__main__':
    param2 = InitParam2("E:\\keti_data\\A1.csv", 100, 44)
    param2.set_save_record_file("experiment_record.csv")
    #param2.set_save_model_file("model\\A1_weights.pkl","model\\A1_rf.pkl")
    param2.set_source_domain_weights_file("E:\\keti_data\\trained_weights1AS1.pkl")
    train_experiment(param2)
