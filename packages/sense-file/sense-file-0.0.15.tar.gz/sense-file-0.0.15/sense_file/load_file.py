import os
import configparser
from sense_core import config, log_warn, log_error
from sense_file import S3File
import tarfile


def log_alg_exec(function):
    def inner(mode):
        if mode == 'TestEnv':
            return function(mode)
        s3_file = S3File('aws')
        # 加载conf配置
        aim_conf_path = config('conf_path')
        conf_file = config('s3', 'config')
        conf_bucket = config('s3', 'conf_bucket')
        _code, _msg = s3_file.download(conf_file, aim_conf_path, conf_bucket)
        try:
            # 将s3 bucket中的s3_model_tar下载到本地model_tar位置，并解压到model_path下
            s3_model_tar = config('s3', 'model_tar')
            s3_bucket = config('s3', 'model_bucket')
            model_tar = config('model_tar')
            model_path = config('model_path')
            if not os.path.exists(model_tar):
                _code, _msg = s3_file.download(s3_model_tar, model_tar, s3_bucket)
                if not _code:
                    return None
            t = tarfile.open(model_tar)
            t.extractall(path=model_path)
        except configparser.NoOptionError:
            log_warn('no model load')
        except Exception as ex:
            _msg = 'load model error {}'.format(ex.__str__())
            print(_msg)
            log_error(_msg)
            return None
        return function(mode)
    return inner


@log_alg_exec
def serve(mode):
    print('end')


if __name__ == '__main__':
    serve('TestEnv')
    # 加载conf配置
    # _code, _msg = s3_file.download('alg_access_config/all.ini', './all1.ini', 'sdai-conf')
    # s3_model_tar = config('s3_model_tar')