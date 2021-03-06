#### PCC

[TOC]

##### 实现facebook中的like功能，需要：

* 可以对一个对象（一条feed、文章、或者url）进行like操作，禁止like两次，第二次like返回错误码
* 有isLike接口，返回参数指定的对象有没有被当前用户like过
* 需要看到一个对象的like总数
* 可以看到一个对象的like用户列表；
* 数据量：每天新增的like对象数为1千万，每秒like计数器查询量为30万次/秒。
* 加分项：优先显示我的好友列表(social list)。

##### 一些具体的要求为：

1. 有架构设计文档；
2. RESTful接口，压测数据；
3. 最好有优缺点分析，说明权衡点；

##### 数据量

- 用户数量级1000万，好友数量级1000，正态分布

##### 技术选型：

- 要求必须用关系数据库持久化
- 不能用云服务
- 其它技术栈随意
- 语言随意
- 一共三台机器
- 部署方式自己定
- 分布式或单块应用自己定

==要求qps  占用的系统资源  数据一致性级别  扩展性综合评分最高者获胜==

---

##### 奖励

既然是championship，那么就要要有champion，我们想到的奖励是：

1. PCC奖杯；
2. Top3获得后花园讲师晚宴资格；
3. 可选职业规划辅导交流一小时，可选Tim或者一乐

##### 评分标准：

- 性能分数 60 + 架构设计 40

##### review

- 由于是三周的Project，一乐会每周组织大家一起来线上来review进度，并讨论系统，三周后我们会有一次线下的跑分比赛。

##### 一乐的一些建议

- 第一周，注重需求分析、架构设计和代码实现；
- 第二周，性能测试和优化，解决瓶颈；
- 第三周，完善系统，往分布式或者更高规模扩展；
- 具体要求一乐会在每周review时提醒大家，并视各位进度情况来调整下周要求。

