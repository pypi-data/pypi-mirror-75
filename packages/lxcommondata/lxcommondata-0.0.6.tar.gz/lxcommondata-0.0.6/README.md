# Common Data gRPC API client

灵犀公共数据微服务接口

### 配置

settings配置指定server

```
COMMON_DATA_SERVER = 'host:port'

```

### 使用

```
# 导入查询接口
from commondata.apis import do_query

# 定义查询对象
query_obj = {
    'model': 'CompanyModify',		# model名（必须）
    'operate': {		# 操作（必须）
        'filter': "entid_id=363248",		# 方法、参数
        'order_by': "'-ALTDATE'",
    },
    'paging': '[0:5]'		# 分页（可选）
}

# 查询并接收结果

status, data = do_query(query_obj)

```

