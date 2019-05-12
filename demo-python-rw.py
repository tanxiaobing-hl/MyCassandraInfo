# coding=utf-8

import tbl_model as modelMgmt

#------------------------- 如何从 ModelQuerySet 中获取结果 ------------------------------------------
# 语句 q = modelMgmt.tbl_hello_world.objects(**perfRawDict).limit(None) 中， 返回的结果 q 表示 ModelQuerySet 对象；
# 如何从 q 中获取结果呢？
# 1. 迭代操作  for ts in q:
# 2. List索引操作
#    q[0] #returns the first result
#    q[1] #returns the second result
# 3. list 分割提取
#    q[1:] #returns all results except the first
#    q[1:9] #returns a slice of the results
# 4. 调用 first()
#    ts = q.first()
# 5. 调用 get() --- 只有当结果只有一个对象，也就是查询结果只有一行时才可用。
#    ts = q.get()

#------------------------- 常用的查询 -----------------------------
# 1. 不限制查询结果的条数
#   q = modelMgmt.tbl_hello_world.objects(**perfRawDict).limit(None)
# 2. 限制查询结果最多为 100 条
#   q = modelMgmt.tbl_hello_world.objects(**perfRawDict).limit(100)
# 3. 设置超时，单位为秒
#   q = modelMgmt.tbl_hello_world.objects(**perfRawDict).timeout(120)
# 4. 选择列
#   q = modelMgmt.tbl_hello_world.objects(**perfRawDict).only(['mc', 'perftime', 'task_id'])
# 5. 排除列，反选
#   q = modelMgmt.tbl_hello_world.objects(**perfRawDict).defer(['ne_type'])
# 6. 设置 consistency
#   q = modelMgmt.tbl_hello_world.objects(**perfRawDict).consistency(CL.ONE)
# 7. 设置 fetch_size
#   q = modelMgmt.tbl_hello_world.objects(**perfRawDict).fetch_size(5000)
# 8. 使能 allow_filtering
#   q = modelMgmt.tbl_hello_world.objects(**perfRawDict).allow_filtering()

#--------------- Batch: only for create/update/delete ------------
# b = BatchQuery()
# now = datetime.now()
# em1 = ExampleModel.batch(b).create(example_type=0, description="1", created_at=now)
# em2 = ExampleModel.batch(b).create(example_type=0, description="2", created_at=now)
# em3 = ExampleModel.batch(b).create(example_type=0, description="3", created_at=now)
# b.execute()

############## 往表 tbl_hello_world 中写入一行数据 ##############
perfRawDict = {"task_id":7171686, "dev_id_str":"", "mc_id":1234567, "moi":"0", "period":15}
# 先读一下，证明DB中没有这条数据
q = modelMgmt.tbl_hello_world.objects(**perfRawDict)
print("q.count %s" %q.count())
# 插入这条数据
modelMgmt.tbl_hello_world(**perfRawDict).save() # modelMgmt.tbl_hello_world.create(**perfRawDict) 也可以
# 再从数据库中这一条数据
q = modelMgmt.tbl_hello_world.objects(**perfRawDict)
print("q.count %s" %q.count())
for row in q:
    print("ts_len is:%s" %row.ts_len)


############## 采用过滤的方式进行查询 ###########
perfRawDict = {"task_id":612, "dev_id_str":"", "moi":"metfone"}
q = modelMgmt.tbl_hello_world.objects(**perfRawDict)
# 这个操作会超时，因为没有指定完整的PartitionKey，会触发全表扫描, 所以在filter中增加过滤条件
# print("q.count %s" %q.count())
q2 = q.filter(mc_id=138418018)
# 这个操作不会超时，因为已经指定完整的PartitionKey
print("q2.count %s" %q2.count())
# for循环取所有的结果
for row in q2:
    print(row.mc)
    print(row.perftime)

# 只取第一个
firstRow = q2[0]

