from sense_file import S3File
import sense_core as sd


def test_content():
    sd.log_init_config('s3_file', '/tmp/logs')
    s3_file = S3File('aws')
    conetnt = s3_file.get_obj_content('news/news_post/2020/07/04/22ArPS7wn6Xd2PvoRSRiHN/20200416.txt','sdai-alg')
    sd.log_info(conetnt)
    import pdb
    pdb.set_trace()