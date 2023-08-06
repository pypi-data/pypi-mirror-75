import time
from sense_core import log_info, now_time


def upload_db_logs(function):
    def inner(self, file_name, origin_path, bucket_name):
        start = time.time()
        _success, _msg = function(self, file_name, origin_path, bucket_name)
        end = time.time()
        key = file_name.split('/')[-1]
        deal_time = now_time()
        log_info(msg='action: {}, msg: {}'.format(_success, _msg), project='s3-service', module='upload',
                 key=key, bucket_name=bucket_name, origin_path=origin_path, deal_time=deal_time, cost_time=end-start)
        return _success, _msg
    return inner


def upload_pdf_logs(function):
    def inner(self, file_name, origin_path, bucket_name, publish_time=None, url=None, stock_code=None):
        start = time.time()
        _success, _msg = function(self, file_name, origin_path, bucket_name, publish_time, url, stock_code)
        end = time.time()
        key = file_name.split('/')[-1]
        deal_time = now_time()
        log_info(msg='action: {}, msg: {}'.format(_success, _msg), project='s3-service', module='upload',
                 stock_code=stock_code, key=key, bucket_name=bucket_name, publish_time=publish_time,
                 url=url, origin_path=origin_path, deal_time=deal_time, cost_time=end-start)
        return _success, _msg
    return inner


def upload_model_logs(function):
    def inner(self, file_name, origin_path, bucket_name, alg):
        start = time.time()
        _success, _msg = function(self, file_name, origin_path, bucket_name, alg)
        end = time.time()
        deal_time = now_time()
        log_info(msg='action {}'.format(_success), project='s3-service', module='upload_model',
                 bucket_name=bucket_name, alg=alg, origin_path=origin_path, deal_time=deal_time, cost_time=end-start)
        return _success, _msg
    return inner


def delete_db_logs(function):
    def inner(self, file_name, bucket_name):
        start = time.time()
        _success, key = function(self, file_name, bucket_name)
        end = time.time()
        deal_time = now_time()
        log_info(msg='action {}'.format(_success), project='s3-service', module='delete',
                 key=key, bucket_name=bucket_name, deal_time=deal_time, cost_time=end-start)
        return _success, key

    return inner
