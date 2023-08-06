# sense-file

sense-file目前包含的功能主要有：

1) aws s3 操作（包括文件的上传，下载，删除）
2) 从s3中加载配置和模型文件到制定位置

注意：

1) 上传和删除时会写日志到固定日志表中，需要在settings.ini中添加mysql配置
2) 下载时只需要配置s3的key和secret
