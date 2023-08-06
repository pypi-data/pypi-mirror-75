# TI SDK

## 了解TI SDK
1. TI SDK 是腾讯云智能钛机器学习平台 TI-ONE 提供的SDK训练任务构建包。用户可以使用TI SDK 提交机器学习和深度学习训练任务到 TI-ONE 中。
2. TI-ONE 支持 CPU、GPU 等多种算力类型，利用对象存储 COS、容器服务 TKE、日志服务 CLS等腾讯云上成熟的组件作为支撑，帮助用户在云上快速搭建自己的机器学习和深度学习训练任务。
3. TI-ONE 内置了深度优化过的 Tensorflow、PyTorch 等多种流行的机器学习框架，用户只需要少量的适配即可使用 TI Python SDK 提交运行自己的训练代码。

### 主要功能
1. 支持提交TensorFlow单机训练任务、分布式PS训练任务、分布式MPI训练任务
1. 支持提交PyTorch单机训练任务、分布式MPI训练任务
1. 支持提交MXNet单机训练任务、分布式PS训练任务、分布式MPI训练任务
1. 支持提交Scikit-Learn单机训练任务
1. 支持提交自定义镜像训练任务
1. 支持提交自定义环境变量训练任务
1. 支持Tensorboad查看训练任务模型
1. 支持提交CFS文件系统作为数据源的训练任务
1. 支持CLS查看训练任务日志
1. 支持本地环境调试训练任务

## 安装 TI SDK
### 环境要求
Python3.6及以上

### 源码安装
```
python setup.py install
```


### 配置TI SDK环境
若用户的TI SDK环境为非腾讯云Jupyter Noteboo环境时，用户需要配置TI SDK环境。
TI SDK配置的环境目录为~/.ti/config.yaml，用户需要提供的配置信息如下：
1. region: 训练任务提交的腾讯云资源的地域，目前支持ap-guangzhou,ap-shanghai
2. uin: 腾讯云账号ID，可在腾讯云控制台-账号信息中查看
3. app_id: 腾讯云账号APPID，可在腾讯云控制台-账号信息中查看
4. secret_id：腾讯云账号API密钥ID，可在腾讯云控制台-访问管理-用户详情中查看
5. secret_key: 腾讯云账号API密钥KEY，可在腾讯云控制台-访问管理-用户详情中查看 

~/.ti/config.yaml的内容格式如下：
```yaml
basic:
    region: 你的腾讯云地域
    uin: 你的uin
    app_id:  你的appid
    secret_id:  你的secret_id
    secret_key:  你的secret_key
```

## 使用 TI SDK
TI SDK 使用以下几个核心类实现 TI 的模型训练
- Estimators： 对训练任务的抽象，包括Tensorflow、Pytorch、MXNet、Scikit-Learn
- Session：使用TI SDK 资源的方法集合

使用TI SDK训练模型需要以下三个简单步骤
1. 准备一个训练脚本
2. 构造一个Estimator
3. 调用Estimator的fit方法

### 准备训练脚本
训练脚本必须在 Python2.7 或3.6环境下执行。TI 提供了很高的兼容性，只需要少部分改动就可以将外部环境运行的训练脚本适配到 TI 中，同时 TI 提供了训练环境各种资源和参数环境变量定义，在训练脚本中可以直接访问这些环境变量获取相关属性，包括：

| 名称  | 含义 |
| --- | --- |
TM_NUM_GPUS | 表示训练实例可用的GPU数目
TM_NUM_CPUS | 表示训练实例可用的CPU数目
TM_HPS |  表示训练任务指定的超参数列表，json表示；例如{"train-steps": 500, "batch-size": 128}
TM_HOSTS | 表示训练任务的Host列表，json表示；例如["algo-host-0"，"algo-host-1"]
TM_CURRENT_HOST | 表示训练任务的Host名称，例如algo-host-0
TM_CHANNELS | 表示通道名称列表，默认为["training"]; <br> 若设置train和test两个通道，则对应的环境变量是["train"、"test"]
TM_CHANNEL_XXX | 表示输入训练数据的路径，XXX对应通道的名称，默认为training；<br>若设置train和test两个通道，则对应的环境变量是TM_CHANNEL_TRAIN和TM_CHANNEL_TEST
TM_MODEL_DIR | 表示训练实例中模型的输出路径，值为/opt/ml/model
TM_OUTPUT_DATA_DIR | 表示训练实例中输出数据的路径，值为/opt/ml/output/data，包括failure等文件
TM_INPUT_CONFIG_DIR | 表示训练实例中输入配置的路径，路径下包括hyperparameters.json、resourceconfig.json、inputdataconfig.json
TM_NETWORK_INTERFACE_NAME | 表示训练实例中使用的网卡设备名称，如eth0


一个典型的训练脚本处理流程如下：
1. 从输入通道加载训练数据
2. 读取超参数配置
3. 开始训练模型
4. 保存模型

TI 会运行用户的训练脚本，建议将启动训练的入口代码放到 main 方法中（if__name__== '__main__'）

### 使用Estimator提交训练任务
Estimator 是对一个训练任务的高级抽象，包含训练镜像、算力资源、安全权限、算法参数、输入输出等一次训练依赖的所有参数。TI 针对 Tensorflow、PyTorch 等多种流行的机器学习框架分别封装了 Estimator 的具体实现。 具体可见 src/tensorflow/estimator.py、src/pytorch/estimator.py等。
用户可直接使用Estimator提交自定义镜像训练任务，具体参见 [使用自定义镜像训练模型](https://cloud.tencent.com/document/product/851/40126)

以下例子展示了一个简单的 Tensorflow Estimator 使用：

```
tf_estimator = TensorFlow(role=role,
                          train_instance_count=1,
                          train_instance_type='TI.SMALL2.1core2g',
                          py_version='py3',
                          script_mode=True,
                          framework_version='1.14.0',
                          entry_point='train.py',
                          source_dir='gpu/code')

tf_estimator.fit('cos://bucket/path/to/training/data')
```

参数说明    
- role：str 用户在云控制台创建的角色，需要传递角色给 TI，授权 TI 服务访问用户的云资源。
- train_instance_count：int 创建的算力实例数量。
- train_instance_type：str 创建的算力类型，目前支持的类型和配额可见 [购买指南](https://cloud.tencent.com/document/product/851/41239)
- train_volume_size：int 附加的云硬盘大小，单位 GB。
- hyperparameters：dict 超级参数，将传递到训练容器中。
- train_max_run：int 最大运行时间，单位秒，超过设定时间若训练未完成，TI 会终止训练任务（默认值：24 * 60 * 60）。
- input_mode：输入类型，默认 File。
- base_job_name：str fit()方法启动的训练任务名称前缀，如果没有指定，会使用镜像名和时间戳生成默认任务名。
- output_path：用于保存模型和输出文件的 COS 路径，如果未指定，会生成默认的存储桶。
- subnet_id：str 子网 ID，如果未指定，将在没有 VPC 配置的情况下创建任务。

### 调用fit方法
fit 方法会创建并启动一个训练任务
```
fit(inputs=None、wait=True、logs=True、job_name=None)
```

参数说明  
- inputs： 存储训练数据集的 COS 路径，可以采用以下两种数据结构。
   str：例如：cos://my-bucket/my-training-data，COS URI，表示数据集的路径。
   dict[str, str]：例如{'train': 'cos://my-bucket/my-training-data/train', 'test': 'cos://my-bucket/my-training-data/test'}，可以指定多个通道的数据集
- wait (bool)：默认为 True，是否在阻塞直到训练完成。如果设置为 False，fit 立即返回，训练任务后台异步执行。
- logs (bool)：默认为 False，是否打印训练任务产生的日志。只有在 wait 为 True 时才生效。
- job_name (str)：训练任务名称。如果未指定，则 Estimator 将根据训练镜像名和时间戳生成默认名字。

更多的关于TI SDK介绍，请见 [TI SDK 简介](https://cloud.tencent.com/document/product/851/40077)