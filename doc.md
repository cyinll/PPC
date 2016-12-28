### 设计文档

#### 技术选型

    1.mysql
    2.redis(lru策略使用allkeys-lru)

#### 需求分析

1. 1000w用户，1000好友上限，符合正态分布

    也就是说好友越多的人数越少，可以假设平均每个用户有100个好友，则要存储100kw的好友关系。

    建立如下表结构
    <pre><code>
    create table friends(
    from_uid bigint,
    to_uid bigint,
    ctime timestamp,
    index id(from_uid, to_uid)
    );
    </code></pre>
    简单插入数据，每100个用户相互为好友

    1w用户时 表大小为74MB

    10w用户时 表大小为714MB

    基本按比例增长，所以如果为1000w用户，需要70G左右

2. 每天新增的like对象数为1千万

    1000w每天qps大约115/s 不算大

    建立feed like 总数表，按feed_id 1000w区间分表
    <pre><code>
    create table feed_stat(
    feed_id bigint,
    total bigint,
    PRIMARY KEY (feed_id)
    );
    </code></pre>
    其他用户like消息的table，使用唯一组合索引和自增的id用户分页
    <pre><code>
    create table feed_like(
    id bigint  NOT NULL auto_increment,
    feed_id bigint,
    like_uid bigint,
    ctime timestamp,
    PRIMARY KEY  (id),
    unique index id(feed_id, like_uid)
    );
    </code></pre>

3. 每秒like计数器查询量为30万次/秒。会查询like次数，like用户列表

    这个qps很大，采用分页，递增发送，每次发送50个

4. 优先显示我的好友列表

    用空间换时间的做法，有一个人点赞了，把他所有好友的信息都加入表中，新建一张表
    <pre><code>
    create table feed_friend_like(
    id bigint  NOT NULL auto_increment,
    feed_id bigint,
    uid bigint,
    friend_like_uid bigint,
    ctime timestamp,
    PRIMARY KEY  (id),
    unique index id(feed_id, friend_like_uid)
    );
    </code></pre>
    假设平均好友是100，所以每天会新增10亿的数据，是个问题。
    显示的时候，先从此表读取数据，数据量不大，然后再读取feed_like做去重（这个去重我更倾向于在前端完成）

    如果已经请求到非好友用户列表了，就不会把现有的like好友加入进来，除非重新开始请求

6. 重复点赞

    倾向于在前端判断

5. 其他(新增好友，删除好友，取消点赞)

    这些发生频率并不会高，发生时，修改所有相关mysql和redis数据

    总结特征就是写入频率不高，读取频率高

#### RESTful接口

1. 用户like操作
    <pre><code>
    /v1/feed
    POST请求
    参数:
        {
            action: 操作的类型
            feed_id: feed的id值
            user_id: 用户id
        }
    返回: {"status": "Success"}
    </code></pre>

2. 显示like总数和用户列表
    <pre><code>
    /v1/feed/<feed_id>
    GET请求
    参数:
        user_id: 用户的user_id
        max_id: 当前用户列表的最大编号
        is_friend: 最后一个user是否是好友
    返回:
        {
            "status": "Success",
            "total": 100,
            "data": [1, 3, 5, 10]
        }
    </code></pre>

#### 整体架构

1. 单机

    按上面的描述搭建mysql表, redis只用做缓存，因为like总数是变化的，所以redis也要每次更新，好友列表redis也是变化的，所以也要每次更新，非好友用户列表不需要变化，不需要更新，redis的lru策略使用allkeys-lru

2. 分布式

    还是比较容易实现分布式的，feed相关的表按照id range分表，用主从的方式设置读写分离，好友关系暂时按照from_uid range, like操作时总数的redis和好友list都更新所有实例，非好友list不需要更新

#### 优缺点分析
    优点
    1. 易于实现，易于扩展

    缺点
    1. 如果请求点赞list已经到了非好友页，新增的好友点赞就会看不到
    2. 好友关系不容易拆分，feed_friend_like表过大
    3. feed_like, fedd_friend_like都按照id分表，就无法快速取到user是否like feed这个状态，除非再新建一张表
