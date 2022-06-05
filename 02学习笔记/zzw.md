- [数据库](#数据库)
  * [1. mysql](#1-mysql)
  * [2. pgsql](#2-pgsql)
  * [3. es](#3-es)
  * [4. redis](#4-redis)
  * [5. kafka](#5-kafka)
- [网络协议](#网络协议)
  * [1. 网络基础](#1-网络基础)
  * [2. TCP UDP](#2-tcp-udp)
  * [3. http](#3-http)
  * [4. https](#4-https)
- [开发工具](#开发工具)
  * [1. git](#1-git)
  * [2. docker](#2-docker)
  * [3. nginx](#3-nginx)
- [Linux系统](#linux系统)
  * [1. IO模型](#1-io模型)
  * [2. 常用命令](#2-常用命令)
  * [3. 启动流程](#3-启动流程)
- [数据结构和算法](#数据结构和算法)
  * [1. 数据结构](#1-数据结构)
  * [2. 常用算法](#2-常用算法)
- [开发框架](#开发框架)
  * [1. flask](#1-flask)
  * [2. django](#2-django)
  * [3. spring boot](#3-spring-boot)

# 数据库
## 1. mysql
### 1.1 设计原则
  + 数据类型按照实际情况，范围或者占用空间更小的通常更好
  + 尽量避免NUll
  + datetime 能存储1001年到9999年，精度为秒。与时区无关，使用8个字节。
  + timestamp 保存1970年至今的秒数，只使用4个字节，范围是1970-2038，显示依赖时区。
  + 满足三大范式：
    + 第一范式：属性不可再分；
    + 第二范式：为了减少冗余，所有列都只和其中一列（主键）相关；如果有和多个列相关的可以拆开多个表；
    
      | 学号 |  姓名  |  专业名 | 专业主任 | 课程名称 | 分数 |
      | ---- |  ----  |  ---- | ---- | ---- | ---- |
      
      表可以拆为：
      
      | 学号 |   课程名称 | 分数 |
      | ---- | ---- | ---- |
      
      | 学号 |  姓名  |  专业名 | 专业主任 |
      | ---- |  ----  |  ---- | ----  |
    + 第三范式：每列都需要与主键直接相关，不能间接相关
    
      | 学号 |   课程名称 | 分数 |
      | ---- | ---- | ---- |
      
      | 学号 |   姓名 | 专业名 |
      | ---- | ---- | ---- |
      
      | 专业名 | 专业主任 |
      | ---- | ---- |
### 1.2 事务
  + 事务的四个基本特性：
    + 原子性（Atomicity）：一个事务是一个整体，要么全部执行成功，要么都不执行。
    + 一致性（Consistency）：执行前后所有事务对一个数据的读取结果都是相同的。
    + 隔离性（Isolation）：多个并发事务之间相互隔离，一个不影响另一个。
    + 持久性（Durablity）：事务执行完后，对数据库修改是永久的，没法回滚。
  + 事务并发常见问题
    + 脏读：A事务执行过程中，B事务修改了数据，导致A事务读取了修改后的数据，但是B最后又回退了，所以让A读取了错误的数据。
    + 不可重复读：A执行过程中，B修改了数据，导致A前后读取的数据不一致。
    + 幻读：A执行过程中，B增加了数据，导致A前后读取不一致。
  + 针对事务并发隔离的4个级别：MYSQL默认可重复读，设置隔离级别：SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
    + 读未提交：能读到未提交的事务中所做的修改，这种会产生脏读。性能不会好太多，问题很多，很少用。
    + 读已提交：只能获取已经提交事务后的结果，也就是说事务中所做的修改对其他事务是不可见的。解决的脏读问题。
    + 可重复读：读取一个数据前给数据加共享行锁，更新时加排它行锁，这样就避免在事务中数据被其他事务修改，解决了不可重复读问题。innodb通过MCVV快照方式实现可重复读并减少锁的使用。
    + 可串行化：加表锁防止事务并行。
  + innodb处理死锁是将持有最少行级拍他锁的事务进行回滚
### 1.3 索引
  + 为什么用b+树
    + 列表等有序数据：数据量大了不能全部加载到内存来查找
    + 二叉树：可以保存树的前几层，但是极端情况，二叉树就和有序列表一样。
    + 平衡二叉树：没法范围查询
    + B树：
      1. 所有节点都存数据，B+树只有叶子节点存数据，读写磁盘B+树就相对能读的节点多；
      2. B树可能在父节点就查到数据，有可能在子节点，查询效率不稳定，B+树每次都需要查询到子节点；
      3. B+树数据都在叶子节点并且相连，分支都是索引，方便扫库，适合范围查询，而B树只能遍历整个树；
  + 最左原则：联合索引创建时索引是按照从左到右的顺序排列的，比如（a, b）则是先按照a排序，a相同时按照b排序。
  比如a>1 and b=4 只有a走索引，因为在a>1的情况下b是无序的。最左原则就是：最左优先，从左边开始任何连续索引能匹配上，遇到范围查询就回停止匹配。
  + 聚簇索引和非聚簇索引：  
    聚集索引：数据和主键聚集在一起，聚簇索引只能有一个，就是表本身的一种排列方式，类似新华字典正文内容本身就是一种按照一定规则排列的目录。  
    非聚集索引：就是主键和数据分离，主键指向数据，索引是纯粹主键的索引，可以有多个，这种目录纯粹是目录，正文纯粹是正文的排序方式。
    ```
    1）直接创建CREATE INDEX indexName ON mytable(username(length)); 
    2）修改表结构：CREATE INDEX indexName ON mytable(username(length)); 
    3）创建表时创建索引：
    CREATE TABLE mytable(  
    ID INT NOT NULL,   
    username VARCHAR(16) NOT NULL,  
    INDEX [indexName] (username(length))  
    );
    1.添加PRIMARY KEY（主键索引）
    ALTER TABLE `table_name` ADD PRIMARY KEY ( `column` )
    2.添加UNIQUE(唯一索引)
    ALTER TABLE `table_name` ADD UNIQUE ( `column` )
    3.添加INDEX(普通索引)
    ALTER TABLE `table_name` ADD INDEX index_name ( `column` )
    4.添加FULLTEXT(全文索引)
    ALTER TABLE `table_name` ADD FULLTEXT ( `column`)
    5.添加多列索引
    ALTER TABLE `table_name` ADD INDEX index_name ( `column1`, `column2`, `column3` )
    ```

### 1.4 引擎
  + 存储结构  
    MyISAM ：每个MyISAM在磁盘上存储成三个文件。分别： .frm文件存储表定义   .MYD是数据文件的扩展名   .MYI是索引文件的扩展名。(默认)  
    InnoDB ：所有的表都保存在同一个数据文件中。Innodb表的大小只受限于操作系统文件的大小，一般为2GB。（需要制定）  
    所以如果备份、迁移或者删除时，MyISAM比较方便。
  + 存储空间  
    MyISAM：可被压缩，存储空间小。支持三种不同的存储格式：静态表、动态表、压缩表。  
    Innodb：需要更多的内存和存储，它会在主内存中建立专用的缓冲池用于高速缓冲数据和索引。
  + 事务支持  
    MyISAM ：强调的是性能 但不提供事务支持。  
    Innodb：提供事务支持、外部键等高级数据库功能，有事务、回滚、崩溃修复能力。
  + GURD操作  
    MyISAM：不支持行级锁，在增删时会锁定整个表格，效率不如Innodb.  
    Innodb：支持行级锁，在增删时效率更高。
### 1.5 查询和优化
  + 查询步骤
    ```
    (1) FROM <left_table>
    (2) <join_type> JOIN <right_table>
    (3) ON <join_condition>
    (4) WHERE <where_condition>
    (5) GROUP BY <group_by_list>
    (6) WITH {CUBE | ROLLUP}
    (7) HAVING <having_condition>
    (8) SELECT
    (9) DISTINCT
    (9) ORDER BY <order_by_list>
    (10) <TOP_specification> <select_list>
    ```  
     每个步骤都会产生一个虚拟表，作为下一个步骤的输入。
  + 数据库优化  
    ```
      1.优化索引、SQL 语句、分析慢查询; 
      2.设计表的时候严格根据数据库的设计范式来设计数据库;
      3.使用缓存，把经常访问到的数据而且不需要经常变化的数据放在缓存中，能节约磁盘 IO 
      4.优化硬件;采用 SSD，使用磁盘队列技术(RAID0,RAID1,RDID5)等
      5.采用 MySQL 内部自带的表分区技术，把数据分层不同的文件，能够提高磁盘的读取效率; 
      6.垂直分表;把一些不经常读的数据放在一张表里，节约磁盘 I/O; 
      7.主从分离读写;采用主从复制把数据库的读操作和写入操作分离开来; 
      8.分库分表分机器(数据量特别大)，主要的的原理就是数据路由; 
      9.选择合适的表引擎，参数上的优化
      10.进行架构级别的缓存，静态化和分布式;
      11.不采用全文索引;
    ```
  + 查询分析  
  EXPLAIN：可以显示SQL的执行计划。
    ```
    MySQL [rules]> explain select rule from ac_rule;
    +----+-------------+---------+------------+------+---------------+------+---------+------+------+----------+-------+
    | id | select_type | table   | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra |
    +----+-------------+---------+------------+------+---------------+------+---------+------+------+----------+-------+
    |  1 | SIMPLE      | ac_rule | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 2274 |   100.00 | NULL  |
    +----+-------------+---------+------------+------+---------------+------+---------+------+------+----------+-------+
    1 row in set, 1 warning (0.01 sec)
    ```
    id：select执行顺序标识符，从大到小执行。如果在语句中没子查询或关联查询，只有唯一的 SELECT，每行都将显示 1。否则，内层的 SELECT 语句一般会顺序编号，对应于其在原始语句中的位置。id相同表示为一组，执行顺序由上至下。  
    select_type：有很多，如：    
      + SIMPLE：表示简单select，不使用关联或者自查询。
      + PRIMARY：查询中若包含任何复杂的子部分,最外层的select被标记为PRIMARY
      + UNION：UNION中的第二个或后面的SELECT语句 
       
    table：表示引用那个表  
    type：重要指标，表示数据访问类型，从好到坏：system > const > eq_ref > ref > fulltext > ref_or_null > index_merge > unique_subquery > index_subquery > range > index > ALL。一般来说，得保证查询至少达到 range 级别，最好能达到 ref（使用了索引，但不是唯一索引）。  
    possible_keys：显示查询使用了哪些索引，表示该索引可以进行高效地查找，但是列出来的索引对于后续优化过程可能是没有用的。  
    key：显示 MySQL 实际决定使用的键（索引）。如果没有选择索引，键是 NULL。要想强制 MySQL 使用或忽视 possible_keys 列中的索引，在查询中使用 FORCE INDEX、USE INDEX 或者 IGNORE INDEX。  
    key_len：显示 MySQL 决定使用的键长度。如果键是 NULL，则长度为 NULL。使用的索引的长度。在不损失精确性的情况下，长度越短越好。  
    ref： 列显示使用哪个列或常数与 key 一起从表中选择行。  
    rows： 列显示 MySQL 认为它执行查询时必须检查的行数。注意这是一个预估值。  
    filtered：给出了一个百分比的值，这个百分比值和 rows 列的值一起使用。(5.7才有)  
    Extra： 是 EXPLAIN 输出中另外一个很重要的列，该列显示 MySQL 在查询过程中的一些详细信息，MySQL 查询优化器执行查询的过程中对查询计划的重要补充信息。
    
### 1.6 表关联
  + 关联查询：关联数据结构相同的数据表  
  UION：去重重复行
  UION ALL：保留所有行
    ```
    SELECT cust_name, cust_contact, cust_email
    FROM Customers
    WHERE cust_state IN ('IL','IN','MI')
    UNION
    SELECT cust_name, cust_contact, cust_email
    FROM Customers
    ```
  + 内连接：将两个表都满足条件的行所有列组合起来  
  SELECT 列名表 FROM 表名1 [INNER可以省略] JOIN 表名2 ON或WHERE 条件表达式
  + 左连接（LEFT JOIN）：以左表为基础，按照连接条件将右表相关数据和左表组合，右表无法关联的数据，左表补充null
  + 右连接（RIGHT JOIN）：以右表为基础，按照连接条件将左表相关数据和右表组合，左表无法关联的数据，右表补充null
### 1.7 SQL语句
  + 创建表：
    ```
    CREATE TABLE IF NOT EXISTS `runoob_tbl`(
    `runoob_id` INT UNSIGNED AUTO_INCREMENT,
    `runoob_title` VARCHAR(100) NOT NULL,
    `runoob_author` VARCHAR(40) NOT NULL,
    `submission_date` DATE,
    PRIMARY KEY ( `runoob_id` )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    ```
  + 修改表：
    ```
    ALTER TABLE testalter_tbl MODIFY c CHAR(10);
    ALTER TABLE testalter_tbl DROP i;
    ALTER TABLE testalter_tbl ADD i INT FIRST;
    ALTER TABLE testalter_tbl DROP i;
    ALTER TABLE testalter_tbl ADD i INT AFTER c;
    ALTER TABLE testalter_tbl RENAME TO alter_tbl;
    ```
  + 查数据：
    ```
    MySQL 的 WHERE 子句的字符串比较是不区分大小写的。 你可以使用 BINARY 关键字来设定 WHERE 子句的字符串比较是区分大小写的。
    SELECT * from runoob_tbl WHERE BINARY runoob_author='runoob.com';
    更新：UPDATE table_name SET field1=new-value1, field2=new-value2 [WHERE Clause]
    删除：DELETE FROM table_name [WHERE Clause]
    排序：SELECT field1, field2,...fieldN table_name1, table_name2...
    ORDER BY field1, [field2...] [ASC [DESC]]
    分组：SELECT column_name, function(column_name)
    FROM table_name
    WHERE column_name operator value
    GROUP BY column_name;
    分组后的条件使用 HAVING 来限定，WHERE 是对原始数据进行条件限制。几个关键字的使用顺序为 where 、group by 、having、order by ，例如：
    SELECT name ,sum(*)  FROM employee_tbl WHERE id<>1 GROUP BY name  HAVING sum(*)>5 ORDER BY sum(*) DESC;
    ```
## 2. pgsql

  | 区别点 |   mysql | pg |
  | ---- | ---- | ---- |
  | cpu | 最多使用128 | 无限制 |
  | 版本 | 版本分支多，之间不兼容 | 版本统一只有社区版本，开源免费 |
  | 索引 | 索引类型少 | 多 |
  | 插件 | 不支持 | 丰富 |
  | 数据类型 | 少 | 多，如 数组、ip |
  | 跨库 | 支持跨库 | 不支持跨库查询 |
  | 迭代 | 慢，2-3年 | 快，1年 |
## 3. es
+ 解决问题：
  + 数据库字段太多，查询太慢，索引没有办法再做优化；
  + 数据量大
  + 全文检索
+ 概念：开源搜索引擎，可以处理pb级结构或者非结构数据。
  + Cluster&Node：ES是一个分布式数据库，每台服务器可以运行多个es实例，单个实例称为一个Node，一组实例对外提供服务称为一个集群（cluster）。  
  + index（索引）：一类数据的集合，相当于关系数据库的一个数据库。
  + type（逻辑分组）：类似表，最新默认_doc，我理解type就相当于一个类，这个类下面的数据都是这个类的实例，也就是说type下数据格式都相似。
  + document（文档）：类似行，一组json数据。es是存储一个个文档（json数据）
+ 操作：
  + 添加和更新：
    ```
    curl -H "Content-Type: application/json" -X POST http://localhost:9200/project/person/1 -d '{"name":"James","age":35}'
    ```
    POST是插入数据，可以指定id，不指定会自动生成。  
    PUT是更新数据，必须指定，指定后会覆盖数据。上述命令中project是index,person是type，1是id。  
    服务器返回如下：
    ```
    {
        "_index": "project",
        "_type": "person",
        "_id": "1",
        "_version": 2,
        "result": "updated",
        "_shards": {
            "total": 2,
            "successful": 1,
            "failed": 0
        },
        "_seq_no": 1,
        "_primary_term": 1
    }
    ```
    服务器返回的 JSON 对象，会给出 Index、Type、Id、Version 等信息。其中result的值为updated，说明这条id的数据已经存在，所以这次再插入就是更新。
  + 删除数据：
    ```
    curl -X DELETE http://localhost:9200/project/person/1
    ````
  + 查询数据：
    ```
    curl http://localhost:9200/project/person/1
    ```
    后面可以加参数, 
    ?pretty=true 表示以易读格式返回
    返回的易读格式如下：

    ```
    {
      {
      "_index" : "project",
      "_type" : "person",
      "_id" : "1",
      "_version" : 1,
      "_seq_no" : 4,
      "_primary_term" : 1,
      "found" : true,
      "_source" : {
        "name" : "James",
        "age" : 35
      }
    }
    ```
  + 检索：
      ```
      curl -H "Content-Type: application/json" http://localhost:9200/project/person/_search?pretty=true -d '{"query":{"match":{"age":35}}}'
      ```
    默认一次返回10条结果，可以通过size字段改变这个设置：
    参数{"query":{"match":{"age":35}},"from":10, "size":1}表示从第10条结果开始返回一条。
+ 倒排索引
  + 字段：es默认会自动根据数据类型生成字段类型，同时可以设置mapping指定字段类型。一个字段可以同时拥有多种类型，可以在mapping中通过field指定。
    ```
    PUT my_index
    {
      "mappings": {
        "_doc": {
          "properties": {
            "cityName": {
              "type": "text",
              "fields": {
                "raw": { 
                  "type":  "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        }
      }
    }
    ```
    text会分词后存储，keyword不分词。
    cityName字段拥有text类型，也可以通过cityName.raw来使用，此时是keyword类型。对超过 ignore_above 的字符串，analyzer 不会进行处理；所以就不会索引起来。导致的结果就是最终搜索引擎搜索不到了。
  + 索引：如果要是实现搜到包含某个字段得数据，关系数据库需要遍历全表，效率低。ES使用倒排索引解决上面问题。  
    关系数据库中索引为正向索引，通过key，找value。
    倒排索引也是反向索引，通过value找key。
    1. 先将数据分词
    2. 保存各个分词和数据之间关系，如：  
    
    | 单词ID | 单词 | 文档出现频率 | 倒排信息(docID;TF;<POS>) |
    | ---- | ---- | ---- | ---- |
    | 1 | 谷歌 | 5 | (1;1;<1>), (2;2;<4;7>), (3;1;<4>), (4;1;<1>), (5;1;<1>)|
    | 2 | 地图 | 4 | (1;1;<1>), (2;2;<1;8>), (4;1;<4>), (5;1;<1>) |
    | 3 | 之父 | 4 | (2;2;<1;5>), (3;1;<4>), (4;1;<1>), (5;1;<1>) |
    | 4 | 特斯拉 | 2 | (2;2;<1;6>), (5;1;<1;4>) |
    | 5 | 离开 | 1 | (4;3;<1;4;5>) |
    比如单词ID5，表示‘离开’有一个文档包含此单词，在ID为4的文档中，出现了3次，位置分别为1、4、5
+ 各种查询关键字区别
  + term：不分词,所以查询keyword时查询内容需要和数据完全一致；查询text时需要查询内容和分词后的数据某个词一致。
  + match：会分词，所以查询keyword时查询内容需要和数据完全一致；查询text时只要查询的数据分词中有一个和分词后的数据某个词一致。
  + match_phrase：也分词，所以查询keyword时查询内容需要和数据完全一致；查询text时需要查询的数据分词结果必须再数据分词结果中都包含，并且顺序相同，也必须连续。
  + query_string：分词，但是查不出keyword；查询text时需要查询的数据分词结果必须再数据分词结果中都包含，不需要顺序。
## 4. redis
+ 基础数据类型，指的都是数据值的类型，key都是string
  + string：是二进制安全的，也就是可以存数字、字符串、图片或者序列化的对象。
    1. 命令使用：
    
        | 命令 | 简介 | 使用 | 
        | ---- | ---- | ---- | 
        | GET | 获取存储在指定key的值 | GET name |
        | SET | 设置存储在指定key的值 | SET name James |
        | DEL | 删除存储在指定key的值 | DEL name |
        | INCR | key的值+1 | INCR name |
        | DECR | key的值-1 | DECR name |
        | INCRBY | key的值+n | INCRBY name n|
        | DECRBY | key的值-n| DECRBY name n|
    2. 使用场景：
          + 缓存：经典使用场景，把常用信息，字符串，图片或者视频等信息放到redis中，redis作为缓存层，mysql做持久化层，降低mysql的读写压力。
          + 计数器：redis是单线程，一个命令结束才会执行另一个
          + session：一般web用来保存登录信息
    3. 数据结构：
        + SDS：{len:数据长度，alloc:申请的空间大小，flags:SDS类型（8位、16位等），buf[]:二进制数组}
  + List：双向链表结构
    1. 命令使用：
    
        | 命令 | 简介 | 使用 | 
        | ---- | ---- | ---- | 
        | RPUSH | 在列表右边添加值 | RPUSH key value |
        | LPUSH | 在列表左边添加值 | LPUSH key value |
        | RPOP | 从列表右边弹出一个值并返回 | RPOP key |
        | LPOP | 从列表左边弹出一个值并返回 | LPOP key |
        | LRANGE | 获取列表中指定范围的值 | LRANGE key 0 -1 |
        | LINDEX | 获取列表中指定索引的值.0是第一个，-1是最后一个 | LINDEX key -1|
    2. 使用场景：
          + 微博TimeLine: 有人发布微博，用lpush加入时间轴，展示新的列表信息。
          + 消息队列
    3. 数据结构：
        + 双向链表，数据多时用：{head:链表头，tail:链表尾，len:节点数量，dup:节点值复制，free:节点值释放，match:节点值比较}
        + 压缩列表，数据少时使用，省内存,每个数据用的大小不一样：{zlbytes:整个ziplist占用内存字节数，zltail:最后一个entry偏移量，zllen:entry数量，entry：[{prevlen:前一个entry长度，encoding：数据类型和长度，entry-data：数据}]，zlend:结束标识}；
  + Set：通过hash实现，值无序，不重复
    1. 命令使用：
    
        | 命令 | 简介 | 使用 | 
        | ---- | ---- | ---- | 
        | SADD | 向集合添加一个或者多个成员 | SADD key value1,value2...  |
        | SCARD | 获取集合的成员数 | SCARD key |
        | SMEMBER | 返回集合的所有成员 | SMEMBER key |
        | SISMEMBER | 判断集合是否存在该成员，存在返回1 | SISMEMBER key merber |
    2. 使用场景：
          + 标签: 给一个用户打标签，标签不会重复，也无序。
          + 点赞：文章中的那些用户点赞或者收藏
    3. 数据结构
        + intset，数据都是整数且数据不多时使用：{encoding:编码方式，length:整数个数，contents:数组保存数据}
        + 使用hash：值存放在hash的key中，值为空
  + Hash：类似python中字典
    1. 命令使用：
    
        | 命令 | 简介 | 使用 | 
        | ---- | ---- | ---- | 
        | HSET | 添加键值对 | HSET name key value  |
        | HGET | 获取指定键的值 | HGET name key |
        | HGETALL | 获取所有的键值对 | HGETALL name |
        | HDEL | 判断集合是否存在该成员，如果有则删除 | HGETALL name key |
    2. 使用场景：
        + 缓存: 比String节省空间
        + 用户信息：姓名为key，内容可以存放用户各种信息
    3. 数据结构：
        + 使用哈希:{table:哈希数组，size：hash表大小，used:已有节点数量}；table中保存数据{key:value}
  + Zset：有序集合的成员是唯一的,但分数(score)却可以重复。集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是 O(1)。
    1. 命令使用：
    
        | 命令 | 简介 | 使用 | 
        | ---- | ---- | ---- | 
        | ZADD | 添加成员及其对应的分数 | ZADD name 98 小明  |
        | ZSCORE | 获取成员的分数 | ZSCORE name 小明 |
        | ZRANGE | 按照分数从小到大返回start-stop之间的成员[带分数] | ZRANGE name 0-1 [withccores] |
        | ZREVRANGE | 按照分数从大到小返回start-stop之间的成员[带分数] | ZRANGE name 0-1 [withccores] |
        | ZREM | 判断集合是否存在该成员，如果有则删除 | ZREM name key |
    2. 使用场景：
       + 排行榜: 榜单可以按照用户关注数，更新时间，字数等打分，做排行。
    3. 数据结构：
        + 双向链表，数据少时
        + 跳跃表：有序列表增加多级索引，减少检索次数{ele:保存数据，score:保存分数，backward：节点的上一个节点，level(最多32个)：[{forward:指向后面分高的节点，span：表示forward指向节点的距离},]}
     
+ 事务：Redis 事务的本质是一组命令的集合。事务支持一次执行多个命令，一个事务中所有命令都会被序列化。在事务执行过程，会按照顺序串行化执行队列中的命令，其他客户端提交的命令请求不会插入到事务执行命令序列中。

    | 命令 | 简介 | 说明 | 
    | ---- | ---- | ---- | 
    | MULTI  | 开启一个事务 | 后面所有命令会被加入一个执行队列，除非遇到结束命令  |
    | EXEC | 执行事务中所有命令 | 开始顺序执行队列中所有命令，失败后也会接着执行其他命令 |
    | DISCARD | 取消事务 | 清空当前事务中命令，不再执行，后续命令也不加入队列 |
    | WATCH | 监视一个或多个key,如果事务在执行前，这个key(或多个key)被其他命令修改，则事务被中断，不会执行事务中的任何命令。 | 事务执行结束后WATCH会被自动取消 |
    | UNWATCH | 主动放弃监视 | 取消监视后不管监视后是否有修改都不会影响事务 |
+ 缓存问题：数据库大多数情况都是用户并发访问最薄弱的环节。所以，就需要使用redis做一个缓冲操作，让请求先访问到redis，而不是直接访问Mysql等数据库。这样可以大大缓解数据库的压力。
  
  | 问题 | 原因 | 方案 | 
  | ---- | ---- | ---- | 
  | 缓存穿透 | 缓存和数据库中都没有的数据，而用户不断发起请求。比如查询id为-1，会每次都查询数据库，频繁的攻击会导致数据库压力过大。 | 1. 参数校验；2. 数据库没查到就缓存为null,过期时间设置小点；3. 布隆过滤器让查询快速 | 
  | 缓存击穿 | 某条缓存过期导致缓存没有该数据，数据库中有。大量并发时导致请求都去数据库层，引起数据库压力增大。 | 1. 热点数据不过期；2. 接口限流 | 
  | 缓存雪崩 | 缓存中数据大批量到过期时间，而查询数据量巨大，引起数据库压力过大甚至down机。和缓存击穿不同的是，缓存击穿指并发查同一条数据，缓存雪崩是不同数据都过期了，很多数据都查不到从而查数据库。  | 1. 缓存数据过期时间随机避免同时过期；2. 热点数据不过期 | 
  | 缓存污染 | 缓存的数据只被用了几次就不用了，浪费资源  | 1. 数据设置过期时间；2. 合理的数据淘汰策略 | 
  | 数据一致 | 数据库和缓存更新，就容易出现缓存(Redis)和数据库（MySQL）间的数据一致性问题  | 1. 先删除缓存再删除数据库场景采用延时双删：先删除缓存，再更新数据库，更新后sleep（时间需要大于其他线程读写缓存时间）后再删除缓存；2. 先删除数据库再缓存场景：为了保证删除缓存成功，采用消息队列重试机制 | 
+ 分布式锁：
  1. 加锁：SET lock_key random_value NX PX 5000   如果lock_key不存在，则添加一个5000ms过期的值（表示当前加锁的标识），添加成功代表加锁成功
  2. 解锁：获取lock_key的值，如果是自己设置的，就删除，标识释放了锁。
+ 为什么快：
    1. 高效的数据结构
    2. 基于内存
    3. io模型：文件驱动io多路复用
    4. 单线程：处理连接操作
+ 持久化
    1. RDB(快照)：bgsave：自动触发，由子进程完成，如果数据变化则生成该数据副本，将副本写入rdb,当前数据可以修改。快但是实时性不够
    2. AOF：记录操作日志，采用日志还原，先修改数据后写日志。后台子进程可以优化AOF日志。

## 5. kafka
  + 生产者：
    + 常用参数：  
    
        | 参数 | 简介 | 
        | ---- | ---- | 
        | bootstrap.servers | broker地址  |
        | acks | 多少个副本接收到消息服务端才会向生产者发送响应 |
        | buffer.memory | 生产者的内存缓冲区大小。如果生产者发送消息的速度 >消息发送到kafka的速度，那么消息就会在缓冲区堆积，导致缓冲区不足。这个时候，send()方法要么阻塞，要么抛出异常。 |
        | max.block.ms | 表示send()方法在抛出异常之前可以阻塞多久的时间，默认是60s |
        | retries | 发送失败后重试次数 | 
        | retry.backoff.ms | 重试之间时间间隔 | 
        | batch.size | 存多少数据一起发 | 
        | max.in.flight.requests.per.connection | 一个消息发送到收到响应之间，还能发多少个 | 
        | request.timeout.ms | 生产者在发送消息之后，到收到服务端响应时，等待的时间限制 | 
    + 分区策略：配置参数值
         1. 指定分区
         2. 指定对应的key值
         3. 都没有指定，会随机选区分区，之后数据轮询发送。
    + 数据一致性：一个分区有多个副本，其中有一个leader和多个follower。发送者通过ack（确认已收到）来保持发送数据一致问题。  
    ack有一个应答机制：  
    0 ：生产者只管发送数据 不接受ack，会造成数据丢失 因为我都不知道这个leader的死活 有可能在网络连接的时候就挂掉了。  
    1 ：生产者发送数据leader写入成功后，返回ack，这个里面还是会丢数据，如果这个时候leader挂了，他的follower没有同步完数据然后提升为leader之前未同步数据就会丢失。  
    -1：(ALL) 生产者发送数据到leader写入成功后再 等follower也写入成功后返回ack给生产者，这个里面有一个问题就是数据重复，什么样的时候会造成数据重复呢就是follower写入成功后刚要回传ack leader就挂了，这个时候生产者认为数据并没有发送成功，kafka这面会把follower晋升为leader 这个时候的leader已经同步完了但是生产者不知道，又重新发送一个一遍数据，就重复了。
    + 故障处理：  
    A 为leader 数据为1-10  
    B 为follower 已同步数据为 1-6  
    C 为follower 已同步数据为 1-8  
    假如leader挂掉了，B选举为leader了 c再去同步发现数据不一样一个是1-8 一个 是1-6 假如这个时候A恢复了 为1-10，这个时候他们的消息不等 消费者消费消息就会出现问题，kefka是用两个标识来处理的一个是HW（在所有消息队列里面最短的一个LEO）为HW，LEO（log end office）最后一个消息的偏移量，HW在选举为B的时候 他为1-6 他会发送命令 所有人给我截取到6 其余的数据都扔掉，消费者来消费消息也只会消费到HW所在对应的那一个偏移量，假如这个时候选取的是C同步数据为1-8，他的HW为6的数据上面 会发送指定 都给我截取到6，再给我A和B再去询问是否有新数据 发现有 7-8 就会同步上去
    
  + 消费者
    + 常用参数：  
    
        | 参数 | 简介 | 
        | ---- | ---- | 
        | fetch.min.bytes | consumer一次拉取中拉取的最小数据量，默认值为1B  |
        | fetch.max.bytes | 一次最大拉的数据量默认50mb |
        | fetch.max.wait.ms | 等待时间，默认值为500ms，如果消息不够多满足不了最小的拉取量，则等待该时间 |
        | max.partition.fetch.bytes | 配置从每个分区返回给消费者最大数据量 |
        | max.poll.records | 最大拉去数据条数默认500 | 
        | connections.max.idle.ms | 空链接超时限制 | 
        | reconnect.backoff.ms | 尝试连接主机之间的等待时间 | 
        | isolation.level | 事务隔离级别，默认读未提交，可以消费到hw | 
    + 消费者和消费者组：一个topic的消息分为几个分区，每个消费者组之间消费topic是互不干扰，都是完整的数据，比如A组消费到10，B组可以从0开始消费；消费者组可以有多个消费者，多个消费者共同消费一个完整的topic消息，每个消费者是一个线程，连接一个分区进行消费，消费者多于分区，则多的消费者是没用的。
  + 数据存储机制  
  同一个topic有多个不同的分区，每个分区是一个目录，文件夹是topic名_分区序号，从0开始；  
  每个分区目录中文件被平均分割为大小相等（默认500mb）的数据文件  
  每个数据文件被称为一个段（segment），每段消息数量不一定相等，主要是方便旧数据清除，默认7天清除旧的。  
  Segment文件命名的规则：partition全局的第一个segment从0（20个0）开始，后续的每一个segment文件名是上一个segment文件中最后一条消息的offset值。
  段文件包含索引（*.index）和数据文件（*.log），索引文件保存消息在数据文件中编号（第几条），编号不一定连续，因为没必要为每条数据都建立索引，隔一定量数据建立避免索引太大。
  如：*.index中1，0：1表示在数据文件中从上至下第一条消息，0表示消息的物理偏移地址（前面所有消息总长度）。
  + 为什么快：
    1. 顺序IO：顺序写入磁盘
    2. 页缓存和零拷贝
    3. 批量发送和压缩
# 网络协议
## 1. 网络基础  

  | OSI分层 | 简介 | TCP/IP | 五层 |
  | ---- | ---- | ---- | ---- |
  | 应用层 | 封装好的应用服务，ssh,ftp,smtp,dns | 应用层 | 应用层 |
  | 表示层 | 不同系统通信，传输时数据处理及接收后处理，如加密解密、压缩解压缩等 | 应用层 | 应用层 | 
  | 会话层 | 数据传输到电脑，多个程序通过端口区分，将数据从一个端口传输到另一台台电脑指定的端口。 | 应用层 | 应用层 |  
  | 传输层 | 怎么传，确保整个数据传输正确，可靠性。协议：TCP、UDP、SPX等。 | 传输层 | 传输层 | 
  | 网络层 | 多台设备通信，传输给谁。协议：IP、IPX、RIP、OSPF等。 | 网络层 | 网络层 | 
  | 数据链路层 | 输出传输格式定义，传输帧，纠错。协议：SDLC、HDLC、PPP、STP、帧中继等。 | 网络接口层 | 数据链路层 |
  | 物理层 | 定义物理设备接口，网线接口类型，传输速率等，传输数据为比特。（8bite=1B=1字节） | 网络接口层 | 物理层 |
## 2. TCP UDP  
  UDP：无连接;不可靠;效率高;多对多:视频会议等场景  
  TCP：需要建立连接;可靠;只能一对一:文件传输等场景  
  三次握手：因为双方要确保双方发送和接收功能都正常
  1. 客户端发送SYN报文，请求建链。SYN报文：flag中SYN标识为1，随机产生一个序列号，seq=X；
  2. 服务端收到SYN后，发送SYN+ACK报文：flag中SYN和ACk标识为1，ack=X+1,随机产生序列号，seq=Y；服务端知道了客户端发送，服务端接收
  3. 客户端收到回复后，发送确认包ACK：flag中ACK标识为1，ack=Y+1；客户端知道客户端发送，接收，服务端发送接收正常，服务端接收到ack后知道了服务端发送和客户端接收正常
  
  四次挥手：由于全双工，需要两边都确认断链  
  1. 客户端发送FIN报文,表示数据发送完成，请求断链：flag中FIN标识为1
  2. 服务端收到后发送ACK报文关闭本端，
  3. 服务端数据发送完成后，发送FIN报文
  4. 客户端收到后发送ACk报文，等待2*MSL（报文最大存活时间）,没有收到回复表示服务端已经关闭，则客户端关闭。等待2*MSL是为了防止最后一个ACK报文丢失，如果丢失服务端需要等待1个MSL确认丢失，然后会重发FIN报文，所以需要等待2*MSL。
   
  + TCP可靠实现方式：
    + 重传机制
        1. 超时重传：统计RTT（数据包往返时间）设置合理的RTO（超时重传时间），发送数据RTO时间后还未收到则再次发送。
        2. 快速重传：如果RTO很大，数据包重传就会很慢。如果连续收到三次相同ACK，还没到RTO就回重发。
        3. SACK：开启后会在TCP头部添加一个stack(收到的数据信息),这样发送方就知道那些数据没发。重传时只会发送未发送的TCP段
    + 滑动窗口:如果只发送一个接收到返回才能发送下一个，通信效率低
        1. 窗口大小是服务端在TCP头的window中说明自己还有多少缓存可以接收，发送端调整窗口来发送
        2. SND.WND表示发送方窗口大小，
        3. SND.UNA表示已发送但是未收到确认的第一个消息字节序列号，
        4. SND.NXT表示未发送但是可以发送的第一个消息字节序列号
        5. 窗口后第一个不能发送的序列号等于SND.UNA+SND.WND，可用窗口等于SND.UNA+SND.WND-SND.NXT
        6. RCV.WND表示接收窗口大小，发给发送方
        7. RCV.NXT保存期望发送方发送来的下一个数据字节的序列号 
    + 流量控制：避免「发送方」的数据填满「接收方」的缓存
        1. 当对方窗口未0时会启动计时器发送窗口探测报文，确保不会一直为0死锁
        2. 为避免一直发送小数据，发送方等到接收方可用窗口大小大于总窗口1/2或者当前数据大于总窗口1/2；接收方可用窗口小于1/2就告知发送方可用窗口为0
    + 拥塞控制：避免「发送方」的数据填满整个网络，发送方」没有在规定时间内接收到 ACK 应答报文，也就是发生了超时重传，就会认为网络出现了用拥塞
        1. 慢启动:建链后拥塞窗口（cwnd）从1逐渐增大，当发送方每收到一个 ACK，拥塞窗口cwnd的大小就会加1
        2. 拥塞避免算法：当拥塞窗口增大到慢启动门限（ssthresh）。之后发送方每收到一个 ACK，拥塞窗口cwnd的大小就会加1/ssthresh
        3. 拥塞发生：拥塞窗口继续增大到出现了重传，如果时超时重传则ssthresh=cwnd/2,cwnd=1;如果时快速重传则表明拥塞不严重cwn =cwnd/2，ssthresh=cwnd
        4. 快速恢复：当快速重传触发后，拥塞窗口和慢启动门限调整。再将cwnd+3（收到了3个应答）；重传丢失包后如果收到应答cwnd+1,如果收到新的应答，cwnd=ssthresh进入拥塞避免算法来缓慢增长
## 3. http
  + 请求方法：
  
      | 方法 | 描述 |
      | ---- | ---- | 
      | GET | 获取资源 |
      | HEAD | 获取报文首部 |
      | POST | 传输数据 |
      | PUT | 上传文件或者修改资源 |
      | PATCH | 修改部分数据 |
      | DELETE | 删除资源 |
     GET和POST区别：
     1. GET数据一般在url中，POST一般数据放在body中，GET参数会暴露在地址栏
     2. 收到URL长度限制，传输数据大小一般不同
     3. POST相对安全，URL可能在历史记录被别人看到，GET可能导致跨站攻击
     4. 请求效率不同，GET三次握手直接发送数据，POST握手完先发请求头，服务器返回100后才开始发送数据。
  + 状态码
  
      | 状态码 | 描述 |
      | ---- | ---- | 
      | 100 Continue | 正常，客户端可以继续发送请求或者忽略这个响应 |
      | 200 OK | 正常 |
      | 204 No Content  | 请求已经处理，但是响应只有头。一般用于客户端发送服务端消息，不需要服务端返回 |
      | 301 Moved Permanently  | 永久重定向 |
      | 302 Found  | 临时重定向 |
      | 400 Bad Request | 请求报文中存在语法错误 |
      | 401 Unauthorized | 未认证通过 |
      | 403 Forbidden | 请求被拒绝 |
      | 404 Not Found | 未找到资源 |
      | 500 Internal Server Error | 服务器正在执行请求时发生错误 |
      | 503 Service Unavailable | 服务器停机等，无法处理请求 |
  + 请求头字段
    1. 通用字段
    
        | 字段 | 说明 |
        | ---- | ---- | 
        | Date | 报文创建时间，Tue, 15 Feb 2022 07:22:18 GMT |
        | Connection | 管理持久连接 |
        | Transfer-Encoding	 | 报文主体的传输编码方式，chunked |
    2. 请求首部
    
        | 字段 | 说明 |
        | ---- | ---- | 
        | Accept | 可处理的数据类型，application/json, text/plain, */* |
        | Accept-Encoding | 优先的内容编码，gzip, deflate, br |
        | Accept-Language	 | 优先的语言，h-CN,zh;q=0.9 |
        | Host	 | 请求资源所在服务器，10.10.190.10 |
        | Referer	 | 对请求中URI的原始获取方，从哪跳过来的 |
        | User-Agent	 | 客户端程序的信息，Mozilla/5.0 (Windows NT 10.0; Win64; x64) |
    3. 响应首部
    
        | 字段 | 说明 |
        | ---- | ---- | 
        | Accept-Ranges | 是否接受字节范围请求， |
        | Age | 推算资源创建经过时间 |
        | Server | HTTP 服务器的安装信息，nginx |
  + cookie、session和token  
    1. cookie:浏览器的一种功能，cookie能帮助web站点保存信息。服务端设置，客户端每次请求会带着服务器保存的cookie,其中包括了key,value,过期时间,路径和域。
    2. session：一种服务端的机制，如果只用服务端给客户端分配一个ID，保存在cookie中来区分用户是否登录或者有权限，就很容易被伪造cookie。服务端一般会保存用户数据，每一个用户数据有个对应的key，把这个key放在客户端cookie中。客户端携带cookie访问，服务端会用cookie中的值去查找保存在服务中的用户数据判断用户信息。比较安全。
    3. token：由于使用session服务端要保存用户会话信息，如果用户量大，服务端压力大。可以将用户信息在服务端加密返回，用户拿到后每次请求带上token参数，服务端直接解密校验token就可以获得用户数据。
  + CSRF（跨站点请求伪造）：
    1. 原理
        ```
           1. 用户C打开浏览器，访问受信任网站A，输入用户名和密码请求登录网站A；
           2. 在用户信息通过验证后，网站A产生Cookie信息并返回给浏览器，此时用户登录网站A成功，可以正常发送请求到网站A；
           3. 用户未退出网站A之前，在同一浏览器中，打开一个TAB页访问网站B；
           4. 网站B接收到用户请求后，返回一些攻击性代码(包含一个访问第三方网站A的请求)；
           5. 用户C就在自己不知情的情况下，被偷偷请求了A网站（上次自己登录的Cookie还未过期）
        ```
    2. 防御
        ```
           1. 验证Reffer，判断用户是从那个网站跳过来的，
           2. 使用token，因为token是不存在Cookie中无法自动携带
        ```
    3. 前后端分离怎么解决CSRF：浏览器才会产生，因为浏览器访问的页面是80或者443，后端端口比如是8080，所以在页面中请求后端API会产生跨域问题  
      nginx中配置：   
          add_header 'Access-Control-Allow-Origin' '*'; //允许的请求源
          add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS'; //允许的请求方式
          add_header 'Access-Control-Allow-Headers' //允许的请求头
  + url请求过程
    1. DNS域名解析获取IP：浏览器缓存 -> 系统缓存 -> hosts文件 -> 本地DNS服务器缓存
    2. 三次握手进行连接
    3. 使用http协议发送数据
    4. web服务收到请求后处理数据并返回
    5. 浏览器拿到数据后渲染页面
    6. 浏览器关闭TCP连接
## 4. https
  + 为什么有HTTPS，因为http不安全，安全就是传输过程中只有客户端和服务端可以看到通信内容。
    1. 对称加密：数据加密发送，服务端解密，但是一般多个客户端和一个服务端通信，如果服务器端对所有的客户端通信都使用同样的对称加密算法，无异于没有加密。
    2. 非对称加密：公钥加密只有对应私钥才能解，私钥加密只有对应公钥才能解。服务器将 公钥发给所有客户端，服务器发送消息使用私钥加密后发送，客户端有公钥可以解密数据。
    3. 加密算法确定：为了保证不同客户端使用不同加密算法，通信使用随机数来确定，所以只有交互时才能确定加密算法。
    4. 公钥传输掉包：客户端怎么获取服务器的公钥，客户端没法保存所有网站的公钥，只能每次请求前去服务端请求。如果A去请求C获取公钥，被中间B拦截，B将自己的公钥发送给A，A每次发送数据使用B的公钥加密发送，B收到后使用自己私钥解密，再用C公钥加密（可以篡改数据）发送给C，C返回数据给B，B再返回给A，A和C都不知道自己通信数据已经泄密。主要由于客户端无法区分返回公钥的是服务器还是中间人。
    5. 数字证书：服务器让第三方机构管理公钥，第三方机构用自己的私钥加密公钥和服务器相关信息，加密后的信息称为数字证书，将数字证书发给服务端，服务端本地存储证书和自己的私钥。
    6. 数字签名：如果A去请求服务器证书，B同样有第三方公钥，可以拦截修改公钥。所有需要数字签名，第三方机构制作证书时，将所有服务器信息和公钥计算出摘要（MD5或者hash码），然后再用自己的私钥加密摘要生成一个签名，和证书一起颁发给服务器。即使中间B截获了证书并解密，但是无法修改其内容，因为修改后要用私钥加密摘要生成签名，B是没有第三方机构的私钥，所有保证了证书不被篡改。
  + SSL/TLS协议: https中加密信息，就是上述流程
    1. 客户发起请求时，除了说明自己支持的HASH算法，还会附加一个客户端随机数。
    2. 服务器回复请求时，会确定哈希函数，并附上证书（包含网站地址，加密公钥，以及证书的颁发机构等信息）。此外，服务器端还会在此次通信中附加一个服务器端随机数
    3. 客户端会产生第三个随机数(Premaster secret)，客户端验证证书（浏览器保存了第三方机构信息和公钥，可以解密第三方机构颁发的证书，验证签名，验证信息等），获取服务端发送的信息，然后利用服务器确定的非对称加密算法和公钥来加密这个随机数，再发送给服务器端。
    4. 服务端用私钥解密第三个随机数
    5. 客户端和服务器端都知道了三个随机数。双方各自用商量好的哈希函数从三个随机数获得对称加密的密钥。
# 开发工具
## 1. git
  + 四个部分：
    + 工作区：开发修改都在工作区，工作区的修改执行add 命令可以提交到暂存区
    + 暂存区：暂存区的修改可以commit到本地仓库，也可以checkout到工作区
    + 本地仓库：可以push到远端仓库，也可以reset还原到暂存区
    + 远端仓库：可以pull远程修改到本地仓库，也可以clone远端仓库到本地仓库
  + 基本命令：
    + 添加修改提交
        ```
        git init   #建立一个本地仓库
        git add 文件1 文件2   #将工作区文件添加到暂存区
        git add -u #添加所有被tracked文件（git status可以看到）的修改删除到暂存区，不包含untracked文件
        git add -A #添加所有被tracked文件（git status可以看到）的修改删除到暂存区，包含untracked文件
        git add . #将当前工作区所有文件添加到暂存区
        git add -i #进入交互界面，按需添加文件到暂存区
        git commit [-a] -m "提交说明" #将暂存区[跳过暂存区，将工作区直接]内容提交到本地仓库
        git commit --amend -m "提交说明" #修改最近一次的提交信息，会将最后一次提交记录替换
        git commit --amend --no-edit #在最后一次提交记录中再提交修改，不修改message不产生提交记录
        git push -u origin master #提交master到远程 
        ```
    + 查看
        ```
        git status #查看仓库状态
        git diff #工作区和暂存区差异
        git diff 分支名 #工作区和该分支差别，远端分支：remote/origin/分支名
        git diff HEAD #工作区与HEAD指向的内容差异
        git diff 提交id 文件名 #工作区某文件和某次历史版本该文件差别
        git diff 版本tag #从某个版本后都修改了啥
        git diff 分支1 分支2 #比较两个分支差别
        git log #查看所有提交记录
        git log -p -n #查看最近n提交记录
        git log filename #查看某个文件的提交记录
        ```
    + 回滚撤销
        ```
        git reset HEAD^ #恢复到上次提交的版本
        git reset HEAD^^ #恢复到上上次提交的版本，或者~n，恢复到前n次
        git reset --hard commit号 #恢复到指定版本
        git revert HEAD #撤销最近一次提交
        git revert commit号 #撤销某次commit
        ```    
    + 分支
        ```
        git checkout [-b] 分支 #【创建并切】换到分支
        git branch #查看分支
        git branch -d #删除分支，-D强制删除
        
        git仓库过大，git clone --depth=1 可以拉去一个分支，之后每次拉去一个分支可以使用：
            $ git remote set-branches origin remote_branch_name  设置一个远端分支管理
            $ git fetch origin remote_branch_name   拉取远端分支
            $ git checkout remote_branch_name  切换分支
        ```
    + merge和rebase：
       + rebase：变基，在当前分支rebase开发分支，相当于把当前分支的修改依次放在了开发分支后面，整个开发分支是一条线；但是rebase后没法追踪是从按个提交拉出来的
       + merge：合并，在开发分支merge自己分支，相当于将开发分支的修改和自己的修改再生成一次commit记录，然后让开发分支指向最新的这个提交
## 2. docker
  + 基础：
    + 镜像：就是一个装有软件的环境，启动后就可以使用
    
        | 命令 | 说明 |
        | ---- | ---- | 
        | docker images | 查看本机docker中所有镜像 |
        | docker search mysql | 在远端dockerhub仓库搜索镜像 |
        | docker pull mysql | 将远端仓库mysql拉去到本地 |
        | docker rmi mysql | 删除本地mysql镜像 |
        | docker save > 文件名 镜像ID | 导出指定镜像 |
        | docker load < 文件名 | 导入镜像 |
    + 容器：运行镜像并提供服务
    
        | 命令 | 说明 |
        | ---- | ---- | 
        | docker run -it 镜像ID/镜像名 /bin/bash | 启动一个容器并打卡一个终端允许交互 |
        | docker ps | 查看容器 |
        | docker stop/start/restart 容器ID | 停止/启动/重启一个容器 |
        | docker exec -it 容器ID /bin/bash| 进入容器交互 |
        | docker rm [-f] 容器ID | 删除[强制]容器 |
        | docker logs 容器ID | 查询容器日志 |
        | docker load < 文件名 | 导入镜像 |
    + dockerfile：用来构建docke镜像的文件

        | 命令 | 说明 |
        | ---- | ---- | 
        | FROM | 基础镜像 |
        | RUN | 构建镜像时执行的命令 |
        | CMD | 运行容器时执行的命令 |
        | VOLUME | 指定容器挂载点到宿主机自动生成的目录或其他容器 |
        | USER | 为RUN、CMD、和 ENTRYPOINT 执行命令指定运行用户 |
        | EXPOSE | 声明容器的服务端口（仅仅是声明） |
        | ENV | 设置容器环境变量 | 
        | ADD | 拷贝文件或目录到容器中，如果是URL或压缩包便会自动下载或自动解压 | 
        | COPY | 拷贝文件或目录到容器中，跟ADD类似，但不具备自动下载或解压的功能 | 
        ```
        docker build -t test:10.1 . #使用当前目录的Dockerfile 文件生成镜像
        docker save ubuntu:latest |gzip filename #保存镜像为zip文件
        docker load -i  filename # 导入镜像
        docker run  -v $PWD/myapp:/usr/src/myapp  -w /usr/src/myapp python:3.5 python helloworld.py  
        -v $PWD/myapp:/usr/src/myapp :将主机中当前目录下的myapp挂载到容器的/usr/src/myapp
        -w /usr/src/myapp :指定容器的/usr/src/myapp目录为工作目录
        python helloworld.py :使用容器的python命令来执行工作目录中的helloworld.py文件
        ```
    + docker-compose:批量管理容器，docker-compose.yml 定义构成应用程序的服务
        ```
        # docker-compose.yml
        version: '3'  // 指定本 yml 依从的 compose 哪个版本制定的。
        services:
          es:  //服务
            container_name: es  //容器名称
            image: es  //使用的镜像名
            environment:  //容器环境变量设置
              - "ES_JAVA_OPTS=-Xms32G -Xmx32G"
              - cluster.name=es_cluster
              - bootstrap.memory_lock=true
              - xpack.security.transport.ssl.enabled=true
              - xpack.security.enabled=true
              - ELASTIC_USERNAME=elastic
              - ELASTIC_PASSWORD=123
            ulimits:  //资源限制
              memlock:
                soft: -1
                hard: -1
              nofile:
                soft: 655360
                hard: 655360
            volumes:  //目录挂在
              - /data/es:/usr/share/elasticsearch/data
              - /lib/log4j-core-2.11.1.jar:/usr/share/elasticsearch/lib/log4j-core-2.11.1.jar
            networks:  //网络配置
              - net
            ports:  //端口映射
              - "127.0.0.1:9200:9200"
            tty: true //运行容器内部建立shell
            stdin_open: true
            restart: always //支持restart
        networks:
          net:
            driver: bridge 
        ```    
## 3. nginx
  1. 特点：低内存、高可靠性、高可扩展、高并发（50000）、单master多works模式支持热部署
  2. 场景：静态文件服务器、反向代理、负载均衡
  3. 常用命令：
      ```
      nginx -t   # 检查配置语法
      nginx # 启动
      nginx -s reload # 重启
      nginx -s stop # 停止
      nginx -c 文件 # 使用指定文件启动nginx
      ```
  4. 配置解析
      ```
      user nginx;   # 运行的用户，可以不设置默认nginx
      worker_processes auto; # work进程数量，一般和cpu核数一致
      error_log /var/log/nginx/error.log; # 错误日志路径
      pid /run/nginx.pid; # 进程pid保存路径
        
      include /usr/share/nginx/modules/*.conf; # 导入其他地方的配置
        
      events {
          worker_connections 1024; # 单个work进程最大并发数
          #use epoll;      #事件驱动模型，select|poll|kqueue|epoll|resig|/dev/poll|eventport
          multi_accept on;  #设置一个进程是否同时接受多个网络连接，默认为off
      }
        
      http {
          log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                              '$status $body_bytes_sent "$http_referer" '
                              '"$http_user_agent" "$http_x_forwarded_for"';  # 自定义日志格式
        
          access_log  /var/log/nginx/access.log  main;  # 使用自定义个的日志格式
        
          sendfile            on; #允许sendfile方式传输文件，默认为off，可以在http块，server块，location块。
          tcp_nopush          on; #有数据就发
          tcp_nodelay         on; #缓存一部分一起发
          keepalive_timeout   65; #tcp连接结束后，保留连接65s，下次连接就不用重新建立了
          types_hash_max_size 2048; #该参数指定了存储MIME type与文件扩展名的散列的最大大小，该值越大，散列的key就越稀疏，检索速度越快，但是会占用更多的内存；该值越小，占用的内存越小，但是冲突率就会上升，检索越慢。
        
          server_tokens off;  # 返回错误页面时是否在Server头部中返回具体的nginx版本
        
          include             /etc/nginx/mime.types; #文件扩展名和类型映射表
          default_type        application/octet-stream; #默认的文件类型

          include /etc/nginx/conf.d/*.conf; #包含的子配置项的位置和文件,子配置文件可以只包含下面一部分
        
          server{
            listen 443 ssl;  #配置监听端口，开启ssl协议
            server_name 0.0.0.0; //配置域名
        
            root /opt/static; #服务默认启动目录
            index index.html; #默认访问文件
            client_max_body_size 1024M; #用户上传数据大小限制
            set $outdated N;  
        
            ssl_protocols TLSv1.2; #协议版本
            ssl_certificate "/etc/nginx/ssl/server.crt"; 证书路径，包含公钥
            ssl_certificate_key "/etc/nginx/ssl/server.key"; 私钥路径
            ssl_session_cache shared:SSL:1m; #储存SSL会话的缓存类型和大小
            ssl_session_timeout  10m; #会话过期时间
            ssl_ciphers HIGH:!aNULL:!MD5; #选择的加密套件，前面叹号的是废弃的
            ssl_prefer_server_ciphers on; #设置协商加密算法时，优先使用我们服务端的加密套件，而不是客户端浏览器的加密套件
        
            gzip on; #开启gzip压缩模式
            gzip_types application/x-javascript text/css application/javascript text/javascript text/plain text/xml application/json application/vnd.ms-fontobject application/x-font-opentype application/x-font-truetype application/x-font-ttf application/xml font/eot font/opentype font/otf image/svg+xml image/vnd.microsoft.icon;
        
            access_log  /var/log/nginx/web_access.log;
            error_log  /var/log/nginx/web_error.log;
            
            upstream servers{
            # 配置负载均衡服务器
            server 1.1.1.1 weight=10
            server 1.1.1.2 weight=20
            }
            
            location /api { #匹配请求
              proxy_pass http://servers:8888; 转发到负载均衡配置中的服务器
              proxy_set_header Host $host;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Real-IP $remote_addr;
            }
          }
        }

      ```
  5. 负载均衡对比
  
      | 工具 | 优点 | 缺点 |
      | ---- | ---- | ---- |
      | nginx | 简单；7层可以针对http应用做分流策略；高负载稳定；静态文件服务器 | 只支持http、https和email协议；对后端服务器只能通过端口健康检查 |
      | lvs | 负载能力强；在4层资源消耗低；应用范围广支持协议多；相当于一个请求过来，只修改目的ip端口 | 不能动静分离；只能基于端口转发，不能基于url等转发 |
      | haproxy | 负载均衡策略多；支持session保持；支持通过指定url检查后端服务状态 | 修改配置需要重启进程，不支持http cache；不支持pop/smtp |

# Linux系统
## 1. IO模型
+ 同步：（注意同步和异步只是针对于I/O操作来讲的）提交一个任务之后要等待这个任务执行完毕
+ 异步：　只管提交任务，不用等待任务执行完毕就可以去做其他事情
+ 阻塞：  recv\accept等 运行状态会被阻塞，不会立即返回
+ 非阻塞：  指调用函数的时候，当前线程不会被挂起，而是立即返回。

+ 一个线程的IO模型：针对IO操作发生时会经历等待数据准备和将数据从内核copy到程序种两个阶段
  + 阻塞IO：当用户进程调用系统得recv时，内核开始准备数据，如果数据还没有准备OK，内核就要等待数据。用户进程被阻塞一直到数据准备OK，拷贝数据到用户进程内存，拷贝时也时阻塞的。直到拷贝完才解除阻塞。优点：简单；缺点：线程被阻塞，在此期间线程无法执行任何运算或者网络请求，多线程模型可以解决小规模服务请求，但是大规模服务请求场景会遇到瓶颈。
  + 非阻塞IO：当用户进程调用系统得recv时，如果内核种数据没有准备好则直接返回error，进程返回后线程可以做别的事情，此模式中用户进程需要不断主动询问内核数据是否OK。优点：能够利用等待时间干其他活；缺点：不断询问将大幅度提高CPU占用率，任务完成响应也增大，因为每过一段时间才去轮询一次，可能再两次轮询之间数据已经准备OK。
  + 多路复用IO（事件驱动IO）:I/O多路复用就是通过一种机制，可以监视多个描述符，一旦某个描述符就绪（一般是读就绪或者写就绪），能够通知应用程序进行相应的读写操作。
    + select（水平触发）:fd_r_list, fd_w_list, fd_e_list = select.select(rlist(等待读), wlist（等待写）, xlist（等待异常）, [timeout])
        select函数会阻塞，直到rlist中的套接字被触发  
        优点：占用资源少，同时能监听多个客户端  
        缺点：保存文件描述符的fd_set结构体的定义实际包含的是fds_bits位数组，当前系统大小1024，当等待读的数据多时，select接口需要大量时间去轮询各个句柄
    + poll机制（水平触发）： select监听机制一样，但是对监听列表里面的数量没有限制（链表），select默认限制是1024个，但是他们两个都是操作系统轮询每一个被监听的文件描述符（如果数量很大，其实效率不太好），看是否有可读操作。
    + epoll机制（水平触发-默认，边缘触发）： 也没有监听数量限制（使用红黑树），它的监听机制和上面两个不同，他给每一个监听的对象绑定了一个回调函数，你这个对象有消息，那么触发回调函数给用户，用户就进行系统调用来拷贝数据，并不是轮询监听所有的被监听对象，这样的效率高很多。  
    水平触发：epoll中当监听的文件描述符有读写事件发生时，会通知处理程序。如果处理程序没有处理完，下次还会通知你接着上次进度处理。如果这个读写事件自己不关心，它们会每次都通知。  
    边缘触发：epoll中当监听的文件描述符有读写事件发生时，会通知处理程序。只会通知一次，直到下次产生新的读写事件。
## 2. 常用命令
  + 快捷键
    ```
    Ctrl + a/Home 切换到命令行开始
    Ctrl + e/End 切换到命令行末尾
    Ctrl + l 清除屏幕内容，效果等同于 clear
    Ctrl + u 清除剪切光标之前的内容
    Ctrl + k 剪切清除光标之后的内容
    Ctrl + y 粘贴刚才所删除的字符
    Ctrl + r 在历史命令中查找
    Ctrl + c 终止命令
    ctrl + o 重复执行命令
    Ctrl + d 退出 shell，logout
    !! 重复执行最后一条命令
    !$ 显示系统最近的一条参数，如果刚才是cat /opt/test,接下来要vim 这个文件，可以直接 vim !$
    ```
  + 磁盘文件
    ```
    df -h 查看磁盘挂载和使用情况
    du -sh * 查看当前文件夹下每个目录大小
    ln –sf 源文件 目标文件
    mount –n –o remount,rw / 重新挂载根目录，设置为可读
    umount /aixi 用挂载点来卸载
    ll(ls -lh) 查看目录中文件信息：
    # drwxr-xr-x  3 root root 17 Jan 24 11:07 work
    # 第一个字符表示文件类型d(目录文件)；
    # 后面表示权限后面三个是读写执行，表示该用户的，接着是文件组的权限，最后是other用户权限，
    chmod 777 文件名： 修改文件权限，4-读，2-写，1-执行。u 表示该档案的拥有者，g 表示与该档案的拥有者属于同一个群体(group)者，o 表示其他以外的人，a 表
    示这三者皆是。所以chmod ug=rwx,o=x file 和 chmod 771 file 效果相同。  
    umask 022：系统权限掩码，用777减去就是默认创建文件的权限
    chown user:group 文件：修改文件所有者和群组
    cat: 获取文件内容，-n：展示行号
    tac:cat相反操纵，从最后一行开始倒序输出
    more:一页一页读取
    less：可以向上翻页
    head:取前几行 -n
    tail:取后几行 -n
    grep -rn "hello,world!" *
        * : 表示当前目录所有文件，也可以是某个文件名
        -r 是递归查找
        -n 是显示行号
        -R 查找所有文件包含子目录
        -i 忽略大小写
        -v 反向查找，排除
        # grep '20:[1-5][0-9]:' *.log  匹配当前目录下搜索log日志中，20点的日志
        # grep '20:[1-5][0-9]:' 1.log 2.log  指定文件中查找
        
    find   path   -option   [   -print ]   [ -exec   -ok   command ]   {} \;
    # find /home/midou/logs// -mtime +30 -name "*.log.gz" -exec rm -rf {} \; 删除30天前满足格式的文件
        -print find命令将匹配的文件输出到标准输出。
        -name 按照文件名查找文件。
        -perm  按照文件权限来查找文件。
        -prune 使用这一选项可以使find命令不在当前指定的目录中查找。
        -user  按照文件属主来查找文件。
        -mtime -n +n 按照文件的更改时间来查找文件， - n表示文件更改时间距现在n天以内，+ n表示文件更改时间距现在n天以前。
        -mmin n  查找系统中最后N分钟被改变文件数据的文件
        -ctime n 查找系统中最后n*24小时被改变文件状态的文件
        -cmin n  查找系统中最后N分钟被改变文件状态的文件
        -atime n 查找系统中最后n*24小时访问的文件
        -amin n  查找系统中最后N分钟访问的文件
        -size n：[c] 查找文件长度为n块的文件，带有c时表示文件长度以字节计。-depth：在查找文件时，首先查找当前目录中的文件，然后再在其子目录中查找。
    ```
  + 目录结构
    ```
    /usr 目录包含所有的命令、程序库、文档和其它文件。
    /usr/local 本地管理员安装的应用程序
    /usr/local/bin 可能是用户安装的小的应用程序，和一些在/usr/local 目录下大应用程序的符号连接。
    /proc/cpuinfo 关于处理器的信息，如类型、厂家、型号和性能等。
    /proc/devices 当前运行内核所配置的所有设备清单
    /var 目录包含在正常操作中被改变的文件：下系统的日志文件就在/var/log 目录中
    /home 目录包含用户的文件：参数设置文件、个性化文件、文档、数据、EMAIL、缓存数据等。
    /bin 系统启动时需要的执行文件（二进制），这些文件可以被普通用户使用。
    /sbin 系统执行文件（二进制），这些文件不打算被普通用户使用。（普通用户仍然可以使用它们，但要指定目录。）
    /etc 操作系统的配置文件目录。
    /root 系统管理员（也叫超级用户或根用户）的 Home 目录。
    /dev 设备文件目录。
    /lib 根文件系统目录下程序和核心模块的共享库。
    /boot 用于自举加载程序（LILO 或 GRUB）的文件。计算机启动时这些文件首先被装载。
    /opt 可选的应用程序。
    /tmp 临时文件。该目录会被自动清理干净。
    # 用户应该将文件存在/home/user_name 目录下
    # 本地管理员大多数情况下将额外的软件安装在/usr/local 目录下并符号连接在/usr/local/bin 下的主执行程序
    # 系统的所有设置在/etc 目录下
    ```
  + 资源管理
  
    + 任务状态：Linux内核里，进程有时候也叫做任务，状态定义如下：  
        ```
        R运行状态（running）: 并不意味着进程一定在运行中，它表明进程要么是在运行中要么在运行队列里。
        S睡眠状态（sleeping): 意味着进程在等待事件完成（这里的睡眠有时候也叫做可中断睡眠（interruptible sleep））。
        D磁盘休眠状态（Disk sleep）有时候也叫不可中断睡眠状态（uninterruptible sleep），在这个状态的进程通常会等待IO的结束。
        T停止状态（stopped）： 可以通过发送 SIGSTOP 信号给进程来停止（T）进程。这个被暂停的进程可以通过发送 SIGCONT 信号让进程继续运行。
        X死亡状态（dead）：这个状态只是一个返回状态，你不会在任务列表里看到这个状态。
        Z僵死状态（zombie）
        ```
      僵尸进程（有害）：当子进程退出但是父进程并没有调用wait或waitpid获取子进程的状态信息，内核就无法从内存中释放已结束的子进程的PCB。
      孤儿进程（无害）：当一个父进程退出，而它的一个或多个子进程还在运行，那么那些子进程将成为孤儿进程。孤儿进程将被init进程(进程号为1)所收养，并由init进程对它们完成状态收集工作。
    + 查看管理:
        ```
        ps aux 最常用:显示进程信息
            l 长格式输出；
            u 按用户名和启动时间的顺序来显示进程；
            j 用任务格式来显示进程；
            f 用树形格式来显示进程；
            a 显示所有用户的所有进程（包括其它用户）；
            x 显示无控制终端的进程；
            r 显示运行中的进程
        top : 显示系统当前的进程状况
            d：指定更新的间隔，以秒计算。
            q：没有任何延迟的更新。如果使用者有超级用户，则 top 命令将会以最高的优先序执行。
            c：显示进程完整的路径与名称。
            S：累积模式，会将已完成或消失的子进程的 CPU 时间累积起来。
            s：安全模式。
            i：不显示任何闲置（Idle）或无用（Zombie）的进程。
            n：显示更新的次数，完成后将会退出 top
        top命令界面执行参数：
            P：根据 CPU 使用大小进行排序。
            T：根据时间、累计时间排序。
            q：退出 top 命令。
            m：切换显示内存信息。
            t：切换显示进程和 CPU 状态信息。
            c：切换显示命令名称和完整命令行。
            M：根据使用内存大小进行排序
        free：查看系统内存情况
        service 服务 start|stop|reload|restart :service可以管理/etc/rc.d/init.d/中的服务（该目录的服务都是system服务）
        ```
  + 网络管理
    ```
    netstat:查询网络信息
        -a 所有信息
        -t：只查询显示tcp进程
        -u：只查询显示udp进程
        -n：将别名转化为数字，结果中将全部显示端口号
        -l：只显示监听中的服务状态
        -p：显示端口相关的应用进程名称
        
    ifconfig：查看网络信息
    配置静态路由：
    sudo ip route add 192.168.55.20/32 via 192.168.27.1 dev eth0
    
    配置静态IP：
    vi /etc/sysconfig/network-scripts/ifcfg-eth0
    
    DEVICE=eth0
    ONBOOT=yes
    HWADDR=ec:f4:bb:c3:e9:a4
    TYPE=Ethernet
    BOOTPROTO=static
    IPADDR=10.16.190.185
    NETMASK=255.255.254.0

    配置好后就重启网口：/usr/sbin/ifdown eth0 && /usr/sbin/ifup eth0
    
    tcpdump:抓包
        -nn，直接以 IP 及 Port Number 显示，而非主机名与服务名称。
        -i，后面接要「监听」的网络接口，例如 eth0, lo, ppp0 等等的接口。
        -w，如果你要将监听所得的数据包数据储存下来，用这个参数就对了。后面接文件名。
        -c，监听的数据包数，如果没有这个参数， tcpdump 会持续不断的监听，
         直到用户输入 [ctrl]-c 为止。
        -A，数据包的内容以 ASCII 显示，通常用来捉取 WWW 的网页数据包资料。
        -e，使用资料连接层 (OSI 第二层) 的 MAC 数据包数据来显示。
        -q，仅列出较为简短的数据包信息，每一行的内容比较精简。
        -X，可以列出十六进制 (hex) 以及 ASCII 的数据包内容，对于监听数据包内容很有用
    如：tcpdump -i eth0 -nn port 21
        tcpdump -i eth0 -nn port 22 and src host 192.168.1.100  # 监听来自 eth0 适配卡且通信协议为 port 22，目标来源为 192.168.1.100 
        tcpdump -i eth0 dst 172.168.70.35 and tcp port 9080 # 访问 eth0 适配卡且访问端口为 tcp 9080
    ```
  + 定时任务：
    ```
    crontab -e 编辑当前用户的 cron 表
    crontab -l 查看当前用户的 cron 表
    crontab -r 删除当前用户的 cron 进程 
    crontab 内容：* * * * * wall hello everyone
    第一个*星号代表个小时的第几分钟：minute 范围是从 0-59
    第二个*星号代表每天的第几个小时：hour 范围是从 0-23
    第三个*星号代表每月的第几个日：day-of-month 范围从 1-31
    第四个*星号代表每年的第几个月：month-of-year 范围从 1-12
    第五个*星号代表每周的星期几：day-of-week 范围从 0-6，其中 0 表示星期日 
    如：25 * 10 9 * ls   #9 月 10 日 25 分执行 ls
      */1 * * * 0     # 每周日每分钟执行一次，*/代表每多少分钟执行一次
      10 1 * * 6,0     # 每周六日1：10分执行
      * 23-7/1 * * *   #每天23点到早上7点，每小时执行一次
    ```
  + 文件编辑
    ```
    Ctrl+f 向下翻页
    Ctrl+b 向上翻页
    G 移动到文件最后一行
    gg 移动到文件第一行
    N+回车 N 为数字，向下移到到 N 行
    /关键字 向下寻找关键字
    ?关键字 向上寻找关键字
    # 从光标向后查找光标所在关键词
    * 从光标向前查找光标所在关键词
    n 向下重复上一次查找操作
    N 与 n 相反，反向重复上一次查找操作
    dd 删除整行
    ndd n 为数字，删除光标所在向下 n 行。
    yy 复制光标所在行
    nyy n 为数字，复制光标所在向下 n 行
    p,P 小 p 将复制的数据在光标下一行粘贴，大 P 将复制的数据在光标上一行粘贴
    u 撤消前一个操作
    Ctrl+r 重做上一个操作
    . 将会重复上一个命令
    i：在当前字符的左边插入
    I：在当前行首插入
    a：在当前字符的右边插入
    A：在当前行尾插入
    o：在当前行下面插入一个新行
    O：在当前行上面插入一个新行
    :w 保存数据
    :wq 保存退出
    :q! 不保存退出
    :w 文件名 相当于另存为
    ``` 
  + 打包压缩
    ```
    tar命令参数
    -c: 建立压缩档案
    -x：解压
    -t：查看内容
    -r：向压缩归档文件末尾追加文件
    -u：更新原压缩包中的文件
    这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的。
    
    -z：有gzip属性的
    -j：有bz2属性的
    -Z：有compress属性的
    -v：显示所有过程
    -O：将文件解开到标准输出
    
    -f是必须的
    -f: 使用文件名字，这个参数是最后一个参数，后面只能接文件名。
    
    解压：tar zxvf /bbs.tar.zip -C /zzz/bbs
    压缩：tar zcvf /zzz.tar.gz ./zzz
    ```        
## 3. 启动流程
  ```
  1. BIOS自检：BIOS 检测（硬件检测、引导顺序等）
  2. 读取并运行装置内 MBR（isolinux/isolinux.bin） 的 boot Loader（就是在操做系统内核运行以前运行的一段小程序，初始化硬件设备、建内存
立内存空间的映射图，从而将系统的软硬件环境带到一个合适的状态，以便为最终调用操做系统内核作好一切准备。）
  3. 加载系统引导文件： isolinux/isolinux.cfg（ isolinux.bin的配置文件） 这个文件就是启动菜单；自定义启动菜单可以修改此文件，可以修改文件让操作系统根据ks文件安装
  4. 根据系统引导文件（isolinux/isolinux.cfg）定义调用内核文件：加载内核： isolinuz/vmlinuz（内核镜像）；向内核传递参数： append initrd=initrd.img
  5. systemd: 硬件驱动成功后，Kernel 会主动呼叫 systemd 程序，并以 default.target 流程开机
  6. 执行anaconda：default.target 会启动很多服务，其中anaconda是一个python脚本，会判断ks文件，根据文件设置安装
  ```

# 数据结构和算法
## 1. 数据结构
   + 数组:一种连续存储线性结构，元素类型相同，大小相等，数组是多维的，通过使用整型索引值来访问他们的元素。插入删除效率低
   + 链表：一个节点保存数据外还有其他节点的指针，每个节点只有一个前驱节点，每个节点只有一个后续节点，首节点没有前驱节点，尾节点没有后续节点。确定一个链表我们只需要头指针，通过头指针就可以把整个链表都能推出来。插入删除快
   + 栈和队列：栈先进后出，队列先进先出
   + 树：相对于链表，链表节点是一对一，树是一对多。
     + 二叉树：最多有两颗子树
     + 满二叉树：所有非叶子结点的度（子树数量）都是2，且叶子结点都在同一层次上
     + 完全二叉树：一个二叉树与满二叉树前m个节点的结构相同，这样的二叉树被称为完全二叉树
     + 二叉查找树(二叉搜索树): 左节点小于根节点，右节点大于跟节点，不存在相等的节点。
     + 平衡二叉树：左右子树层级相差不超过1的二叉查找树
     + 红黑树：一种含有红黑结点并能自平衡的二叉查找树。黑色完美平衡二叉树。
        1. 每个节点要么是黑色，要么是红色。
        2. 根节点是黑色。
        3. 每个叶子节点（NIL）是黑色。
        4. 每个红色结点的两个子结点一定都是黑色。
        5. 任意一结点到每个叶子结点的路径都包含数量相同的黑结点。  
        左旋转：右子树深，右子树根节点变为根节点，根节点右子树不变，左子树由原来根节点及原来左子树+根节点左子树（变为右子树）组成  
        右旋转：左子树深，左子树根节点变为跟节点，根节点左子树不变，右子树由原来根节点及原来右子树+根节点右子树（变为左子树）组成  
     + B树：
        1. 根结点至少有两个子女。
        2. 每个中间节点都包含k-1个元素和k个孩子，其中 m/2 <= k <= m。
        3. 每一个叶子节点都包含k-1个元素，其中 m/2 <= k <= m。
        4. 所有的叶子结点都位于同一层。
        5. 每个节点中的元素从小到大排列，节点当中k-1个元素正好是k个孩子包含的元素的值域分划。  
     + B+树：能够保持数据稳定有序，其插入与修改拥有较稳定的对数时间复杂度。B+ 树元素自底向上插入，这与二叉树恰好相反。
        与B树区别：  
        1. b+树的中间节点不保存数据，所以磁盘页能容纳更多节点元素，更“矮胖”；
        2. b+树查询必须查找到叶子节点，b树只要匹配到即可不用管元素位置，因此b+树查找更稳定（并不慢）；
        3. 叶子节点增加了指向相邻叶子节点的链表，对于范围查找来说，b+树只需遍历叶子节点链表即可，b树却需要重复地中序遍历。
   + 堆：如果对于每个父节点的值都大于等于（或者小于等于）其两个孩子的值，那么就称这种特殊的数据结构为堆，又称为优先队列。二叉堆就是二叉树形式的堆。
     ```angular2
        """
                2
            5       8
          6   10  9   20
        """
        heap = [2, 5, 8, 6, 10, 9, 20]
     ```
## 2. 常用算法
  + 排序
    + 冒泡排序：
    ```
    def bubble_sort(arr, n):
        if n <= 1:
            return
        for i in range(n):
            # 提前退出标志位
            flag = False
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]  # 交换
                    flag = True  # 此次冒泡有数据交换
            if not flag:
                break
    ```
    + 快速排序：
    ```
    def quick_sort(src_l, l, r):
        if l >= r:
            return
        start = l
        end = r
        x = src_l[l]
    
        while l < r:
    
            while l < r and src_l[r] >= x:
                r -= 1
            src_l[l] = src_l[r]
            while l < r and src_l[l] <= x:
                l += 1
            src_l[r] = src_l[l]
            src_l[l] = x
        quick_sort(src_l, start, l - 1)
        quick_sort(src_l, l + 1, end)
    ```    
  + 链表操作
    + 链表反转：
    ```
    def reverse(root):
        pre = None
        while root:
            tmp = root.next
            root.next = pre
            pre = root
            root = tmp
        return pre
    ```
    + 链表重排：
    ```
    给定head链表1->2->3->4->5, 重新排列为 1->5->2->4->3
    class Solution:
    def reverse(self, root):
        pre = None
        while root:
            tmp = root.next
            root.next = pre
            pre = root
            root = tmp
        return pre

    def reorderList(self, head):

        if not head or not head.next:
            return head
        # 快慢指针，将链表分为两半
        slow_head = head
        fast_head = head
        while fast_head and fast_head.next:
            fast_head = fast_head.next.next
            slow_head = slow_head.next

        # 后半段链表
        last_haed = slow_head.next
        slow_head.next = None
        # 反转后半段链表
        last_haed = self.reverse(last_haed)

        # 合并链表
        left_head = head
        while left_head and last_haed:
            tmp_left = left_head.next
            tmp_right = last_haed.next
            left_head.next = last_haed
            last_haed.next = tmp_left
            left_head = tmp_left
            last_haed = tmp_right
        return head
    ``` 
    + 合并有序链表：
    ```
    给定head链表1->2->3,4->5->6 合并为为 1->2->3->4->5->6
    def Merge(self, pHead1: ListNode, pHead2: ListNode) -> ListNode:

    head = p = ListNode(None)
    while pHead1 and pHead2:
        if pHead1.val <= pHead2.val:
            p.next = pHead1
            pHead1 = pHead1.next
        else:
            p.next = pHead2
            pHead2 = pHead2.next
        p = p.next
    if pHead1:
        p.next = pHead1
    if pHead2:
        p.next = pHead2
    return head
    ```
  + 二叉树
    + 前序遍历：
    ```
    def pre_print(tree_node):
        if not tree_node:
            return
        print(tree_node.val)
        pre_print(tree_node.left)
        pre_print(tree_node.right)

    ```
    + 根节点到叶子节点路径和为某值：
    ```
    class Solution:
        def __init__(self):
            self.ret = []
    
        def FindPath(self, root: TreeNode, target: int):
    
            if not root:
                return self.ret
    
            def find(node, n, tmp):
                if not node.left and not node.right:
                    if node.val == n:
                        tmp.append(node.val)
                        self.ret.append(tmp)
                        return
                tmp.append(node.val)
                if node.left:
                    find(node.left, n - node.val, tmp.copy())
                if node.right:
                    find(node.right, n - node.val, tmp.copy())
    
            find(root, target, [])
            return self.ret
    ``` 
    + 二叉树最大路径和：可以从子节点经过父节点到子节点，但是一个节点只能路过一次
    ```
         -20
        8   20
           15  6
     最大路径是：15->20->6=41
     
    class Solution:
        def __init__(self):
            self.ret = None
    
        def MaxPath(self, root):
            def get_path_num(node):
                l, r = 0, 0
                if node.left:
                    l = max(get_path_num(node.left), l)
                if node.right:
                    r = max(get_path_num(node.right), r)
                curl_val = node.val + l + r
                if not self.ret:
                    self.ret = curl_val
                else:
                    self.ret = max(self.ret, curl_val)
                return node.val + max(l, r)
    
            if not root:
                return 0
            get_path_num(root)
            return self.ret
    ```
  + 动态规划
    + 最小路径和
    ```
    def uniquePaths(arr):
        """
        从左上角走到右下角最小路径
        :param arr = [
          [1,3,1],
          [1,5,1],
          [4,2,1]
        ]
        :return:
        """
        # 定义数组元素：从左上角走到(i, j) 这个位置时，最小的路径和是 dp[i][j]
        n = len(arr)
        if n == 0:
            return 0
        m = len(arr[0])
    
        if m == 0:
            return 0
        # 初始化dp
        dp = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                # 确定边界和各节点状态转移方程
                if j == 0 and j == 0:
                    dp[i][j] = arr[i][j]
                elif j == 0:
                    dp[i][j] = dp[i - 1][j] + arr[i][j]
                elif i == 0:
                    dp[i][j] = dp[i][j - 1] + arr[i][j]
                else:
                    dp[i][j] = min(dp[i][j - 1], dp[i - 1][j]) + arr[i][j]
        return dp[-1][-1]
    ```
    + 编辑距离
    ```
    def minEditCost(self, str1: str, str2: str, ic: int, dc: int, rc: int) -> int:
        """
        给定两个字符串str1和str2，再给定三个整数ic，dc和rc，分别代表插入、删除和替换一个字符的代价，请输出将str1编辑成str2的最小代价。
        """
        # 定义数组元素的含义:dp[i][j]的含义为：当字符串word1的长度为i,字符串word2的长度为j 时，将word1转化为word2所使用的最少操作次数为 dp[i][j]
        # 定义dp
        dp = [[0] * (len(str1) + 1) for _ in range(len(str2) + 1)]
        for i in range(len(str2) + 1):
            for j in range(len(str1) + 1):
                if i == 0 and j == 0:
                    continue
                elif i == 0:
                    dp[i][j] = dp[i][j - 1] + dc
                elif j == 0:
                    dp[i][j] = dp[i - 1][j] + ic
                elif str1[j - 1] == str2[i - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # 状态转移方程
                    dp[i][j] = min(dp[i - 1][j - 1] + rc, dp[i][j - 1] + dc, dp[i - 1][j] + ic)
        return dp[-1][-1]
    ```
    + 买卖股票最大利润
    ```
    有一个数组prices，长度为n，其中prices[i]是股票在第i天的价格，总共只能买入和卖出一次，且买入必须在卖出的前面的某一天，求最大利润
     
    class Solution:  # 使用一次遍历
        def maxProfit(self , prices):
            ret = 0
            min_prices = None
    
            for price in prices:
                if min_prices is None:
                    min_prices = price
                min_prices = min(min_prices, price)
                ret = max(price-min_prices, ret)
            return ret
    ```
    + 连续子数组的最大和
    ```    
    class Solution:
        def FindGreatestSumOfSubArray(self, array) -> int:
            if not array:
                return 0
            max_ret = array[0]
            # 只保存当前连续的，不需要dp保存全部
            cur_sum = 0
            for item in array:
                cur_sum += item
                max_ret = max(max_ret, cur_sum)
                if cur_sum < 0:
                    cur_sum = 0
            return max_ret
    ```
# 开发框架
## 1. flask
+ 项目结构
    ```
    |-flasky  
        |-app/
            |-templates/ 
            |-static/
            |-main/
                |-__init__.py
                |-common/
                |-controllers/
                |-exception/
                |-service/
            |-__init__.py
            |-scripts/
            |-email.py
            |-models.py
    |-migrations/
    |-tests/
        |-__init__.py
        |-test*.py
    |-venv/
    |-requirements.txt
    |-config.py
    |-manage.py  #启动程序
    ```
    common:常用公共函数  
    controllers：主要是视图路由过来解析处理并返回合适结果。
    ```
    *controller.py
    
    from flask import Blueprint, Response
    blueprint = Blueprint('auto', __name__, url_prefix="/api") #定义蓝图
    ExceptionHandler(blueprint).handler()  #注册异常处理
    
    // 视图函数
    @blueprint.route("/auto/index", methods=["GET"])
    @login_required
    def index():
        return Response("hello world", mimetype='application/json')
    ```
    exception：定义异常处理，blueprint.register_error_handler(异常类型，处理函数)。  
    service：业务实现代码，主要供controller调用。  
    scripts：保存一些脚本。  
    models：定义数据库类。  
    config：配置类，保存一些配置项。  
    app/__init__.py:一般在该文件中使用工厂方法创建实例，并初始化一些配置。
    ```
    app/__init__.py
    
    from flask import Flask
    from flask.ext.sqlalchemy import SQLAlchemy
    from config import config
    
    db = SQLAlchemy()
    def create_app(config_name):
        app = Flask(__name__)
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)
        db.init_app(app)
        
        # 配置日志等
        # 附加路由
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        
        return app
    ```           
    manage：启动类。  
    ```
    import os
    from app import create_app, db
    from app.models import *
    from flask_script import Manager
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    manager = Manager(app)

    if __name__ == '__main__':
        manager.run()
    ```    
+ 上下文全局变量:  
    LocalStack是flask实现的线程隔离栈，LocalProxy是从LocalStack中获取对象，同一个线程只能获取该线程保存的数据。
    + current_app（app上下文，保存在_app_ctx_stack）：当前激活程序的程序实例,用于获取当前APP的一些配置信息等.当前程序实例还在运行，都不会失效。
    + g（app上下文,保存在_app_ctx_stack）：应用上下文上的对象。处理请求时用作临时存储的对象，一般保存用户信息.一次请求期间，当请求处理完成后，生命周期也就完结了
    + request（请求上下文，保存在_request_ctx_stack）：一般用来保存一些请求的变量。比如method、args、form等。一次请求期间，当请求处理完成后，生命周期也就完结了
    + session（请求上下文，保存在_request_ctx_stack）：一般用来保存一些会话信息。只要它还未失效（用户未关闭浏览器、没有超过设定的失效时间），那么不同的请求会共用同样的session。
+ 蓝图:
  + 作用：类似django中app,可以将项目通过蓝图分为几个模块分别管理路由等
  + 创建：
    ```
    from flask import Blueprint
    blueprint = Blueprint('auto', __name__, url_prefix="/api") #定义蓝图
    // 视图函数注册路由
    @blueprint.route("/auto/index", methods=["GET"])
    @login_required
    def index():
        return Response("hello world", mimetype='application/json')
    
    //flask 实例中注册路由    
    app.register_blueprint(blueprint)
    ```   
+ session配置：
  + 第三方扩展的session可以将信息存储在服务器，浏览器只保存sessionid
  + flask请求上下文session是将信息加密后保存在浏览器cookie中：
    1. session操作和字典一样：session['username']="aaa"
    2. session的有效期:app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hour=2);SECRET_KEY来设置加密密钥
+ 请求钩子：通过装饰器实现的
  + before_first_request:在处理第一个请求前运行
  + before_request:在每次请求前运行
  + after_request(response):如果没有未处理的异常抛出，在每次请求后运行
  + teardown_request(response):在每次请求后运行，即使有未处理的异常
+ SQLAlchemy:
  + 配置
  
  | 参数 | 说明 |
  | ---- | ---- |
  | SQLALCHEMY_DATABASE_URI | "sqlite:///data/test.db":连接数据库的URI |
  | SQLALCHEMY_POOL_SIZE | 连接池的大小 |
  | SQLALCHEMY_POOL_TIMEOUT | 连接池的超时时间 |
  | SQLALCHEMY_POOL_RECYCLE | 自动回收连接的秒数 |
  | SQLALCHEMY_MAX_OVERFLOW | 控制连接池达到最大大小后还可以创建的连接数 |
  + falsk中操作
  ```
    table1 = Table(name='zx',age=13) # 创建
    session.add(table1) #添加
    
    table = Table.query.get(1) #修改
    table.name = '小李'
    
    table = Table.query.get(2) #删除
    session.delete(table)
  ```
  查询：
  
  | 参数 | 说明 | 示例 |
  | ---- | ---- | ---- |
  | all | 查询所有，返回列表，没有则空列表 | Table.query.all() |
  | get(id) | id查询，返回一个对象，没有返回None | table = Table.query.get(1) |
  | filter | 过滤筛选，不支持组合查询，全局查询，参数需要指定表名 |  Table.query.filter(Table.age <= 14).filter(Table.name=aaa).all() |
  | filter_by | 过滤筛选，支持组合查询,表内查询，参数可以直接用属性 |  Table.query.filter_by(age=16, name=aaa).all() |
  | like | 模糊查询 （%匹配0或多个，_ 匹配一个） |  Table.query.filter(Table.name.like("%李%")).all() |
  | order_by | 排序 |  Table.query.filter(Table.name.like("%李%")).order_by(Table.name.desc()).all() |
  | offset|limit | 查询起始位置，以下标进行偏移|返回的条数 |  Table.query.filter(Table.name.like("%李%")).order_by(Table.name.desc()).offset(offset).limit(page_size).all().all() |
  | count | 统计查询的条数 |  Table.query.count() |
+ 请求到返回过程
  1. 客户端-----> wsgi server，__call__调用 wsgi_app
  2. wsgi_app-----> requests对象和上下文环境
  3. dispatch_requests-----> 进行url到view转发获取返回值
  4. make_response函数-----> 将返回值转成response_class对象
  4. response对象传入environ和start_response参数-----> 服务器
## 2. django
+ 目录结构
    ```
    建立django项目：django-admin startproject mysite
    创建一个app:python manage.py startapp polls
    mysite/  
    manage.py  管理Django的交互脚本
    polls/
        __init__.py
        admin.py  后台用户配置
        apps.py  定义app
        migrations/ 数据库迁移文件
            __init__.py
        models.py 数据库模型定义
        tests.py
        views.py 视图处理
    mysite/
        __init__.py
        settings.py 项目的配置文件。
        urls.py 路由文件
        wsgi.py 一个基于WSGI的web服务器进入点，提供底层的网络通信功能
    ```
+ ORM和querySet
    
     ```
    Entry.objects.all()   查询全部
    Entry.objects.get(pk=1)   查询pk为1的
    
    filter(**kwargs)：返回一个根据指定参数查询出来的QuerySet
    exclude(**kwargs)：返回除了根据指定参数查询出来结果的QuerySet
    
    Entry.objects.get(headline__contains='Lennon') 查询标题包含Lennon,区分大小写
    ```
    每次查询出来的QuerySet返回的都是一个QuerySet，只有在必须返回具体结果时才查询数据库。
    数据库执行实际的查询操作后会将数据缓存在这个QuerySet中.
    
    | 参数 | 说明 |
    | ---- | ---- | 
    | exact | 精确匹配 | 
    | iexact | 不区分大小写的精确匹配 | 
    | contains | 包含匹配 | 
    | icontains | 不区分大小写的包含匹配 | 
    | in | 在..之内的匹配 | 
    | gte | 大于等于 | 
    | startswith | 开头 | 
    | regex | 区分大小写的正则匹配 | 
    F表达式：获取模型字段的值，可以用于比较或者模型字段值修改后比较
    ```
    Entry.objects.filter(comments__gt=F('pingbacks')) comments值等于pingbacks值的列
    Entry.objects.filter(authors__name=F('blog__name')) 跨表
    Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3)) 加值后比较
    ```
    Q表达式：Q用于封装关键字参数的集合，可以实现or逻辑。可以使用&或者|或~来组合Q对象，分别表示与、或、非逻辑。它将返回一个新的Q对象。
    ```
    Poll.objects.get(Q(question__startswith='Who'), Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))
    Poll.objects.get(Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)), question__startswith='Who') 当关键字参数和Q对象组合使用时，Q对象必须放在前面
    ```    
+ restful:django使用rest-framework
  + 序列化：请求数据和模型数据转换
    + ModelSerializers：json对象和模型对象转换
    + HyperlinkedModelSerializer：使用超链接来表示关系而不是主键
    ```
    from .models import Student
    from rest_framework import serializers
        
    class StudentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Student
            fields = ('id', 'name', 'age', 'group')
    ```
  + 视图：
    + 可以自己实现各种请求函数
    ```
    def article_list(request):
        if request.method == 'GET':
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
            return JSONResponse(serializer.data)
    
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = ArticleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.errors, status=400)
    ```  
    + 可以继承APIView使用类视图
    ```
    class UserDetail(APIView):
        def get_user(self, id):
            try:
                user = User.objects.get(id=id)
                return user
            except User.DoesNotExist:
                raise Http404
    
        def get(self, request, *args, **kwargs):
            user = self.get_user(kwargs.get('id'))
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
    
        def put(self, request, *args, **kwargs):
            user = self.get_user(kwargs.get('id'))
            serializer = UserSerializer(user, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        def detete(self, request, *args, **kwargs):
            user = self.get_user(kwargs.get('id'))
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    ```   
    + 可以直接用viewsets的ModelViewSet，自动生成增删改查
    ```
    from .models import Student
    from rest_framework import viewsets
    from .serializers import StudentSerializer
    
    class StudentViewSet(viewsets.ModelViewSet):
        queryset = Student.objects.all()
        serializer_class = StudentSerializer
    ```
  + 路由：
    + 自定义和映射：
    ```
    game_list = views.GameView.as_view({
        'get': 'list',
        'post': 'create'
    })
    game_detail = views.GameView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })
    
     path('games/', game_list, name='game-list'),  # 获取或创建
     path('games/<int:pk>/', game_detail, name='game-detail'),  # 查找、更新、删除
    ```
    + Router类自动生成路由
    ```
    from rest_framework.routers import DefaultRouter
    
    # 创建路由器并注册我们的视图。
    router = DefaultRouter()
    router.register('games', views.GameView)
    
    path('', include(router.urls)),
    ```
  + 筛选：
    + 过滤：
    ```
    class GameView(CustomModelViewSet):
        queryset = Game.objects.all()
        serializer_class = GameSerializer
        filter_backends = (DjangoFilterBackend,)
        filter_fields = ('name', 'status')  直接设置支持筛选的字段，但是可能有限制，需要自定义筛选类
        
    自定义筛选类
    from django_filters import rest_framework as filters
    class GameFilter(filters.FilterSet):
        min_status = filters.NumberFilter(field_name='status', lookup_expr='gte')
        max_status = filters.NumberFilter(field_name='status', lookup_expr='lte')
        #根据名字过滤忽略大小写
        name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    
        class Meta:
            model = Game
            fields = ('min_status', 'max_status')  # 允许精准查询的字段
            search_fields = ('name',)  # 允许模糊查询的字段
            
    class GameView(CustomModelViewSet):
        queryset = Game.objects.all()
        serializer_class = GameSerializer
    
        filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
        # filter_fields = ('name', 'status') 
        filterset_class = GameFilter 视图中直接使用
        # 搜索
        search_fields = ("name", "status")
        #排序
        ordering_fields = ['status', "id", "name"]
    ```      
+ celery
  1. setting中配置CELERY_BROKER_URL参数
  2. setting中配置CELERY_QUEUES、CELERY_ROUTES、CELERYBEAT_SCHEDULE等参数
  3. 定义异步任务使用@app.task(queue='async_apis')装饰器 def task1(*args, **kargs)
  4. 在接口中使用：task1.delay(*args, **kargs)
+ session
  1. setting 中配置过期时间，保存为数据库/缓存/文件等等
  2. request.session：session类似字典，可以通过key，也可以get,delete.
+ 中间件
  1. setting MIDDLEWARE 中添加
  2. 定义中间件，类继承MiddlewareMixin    
  process_request(self,request)  视图函数之前执行  
  process_view(self, request, view_func, view_args, view_kwargs)  视图函数之前，process_request之后  
  process_exception(self, request, exception)  视图函数中出现异常了才执行，按照 settings 的注册倒序执行  
  process_response(self, request, response)  视图函数之后执行
+ 生命周期
  1. uWSGI处理：监听到端口消息将http转为WSGI,封装request等
  2. WSGIHandler处理:加载django的settings，控制整个请求过程
  3. middleware中间件处理：process_request
  4. url路由匹配
  5. middleware中间件处理：process_view方法预处理
  6. views处理request，model->数据库
  7. middleware中间件处理：process_response
  8. WSGIHandler处理:获取到response后调用 start_response 返回http协议的 响应行和响应头 到uWSGI
  9. uWSGI处理:response内容包装成http协议的内容后，通过uwsgi协议返回
## 3. spring boot
  + 项目结构
    ```
    web/
        src/ 源码文件
            main/
                assembly/ maven 使用assembly打包的相关文件
                java/
                    com.***.web/ 项目代码目录
                        constan/ 常量配置
                        controller/ 表示层，web层，DTO转VO对象，主要是对访问控制进行转发，各类基本参数校验，或者不复用的业务简单处理等。
                        dao/ 数据访问层，与底层MySQL、Oracle、Hbase等进行数据交互，返回DO对象，此对象与数据库表结构一一对应
                        domain/ 实体类，定义各种对象如DTO，DO，VO等
                        mapper/ mapper接口，
                        mapping/ 实现mapper接口的mybatis xml配置文件
                        service/ 业务逻辑层，DO返回DTO
                        util/ 一些通用方法等
                        WebApplication  启动类文件
                resources/ 资源配置，环境变量等
            test/ 测试代码       
        target/ 编辑生成文件
        pom.xml  项目依赖管理  
    ```
  + Maven：项目管理工具，可以对 Java 项目进行构建、依赖管理
    + POM：POM文件是一个xml文件，是maven管理的基本工作单元，结构如下：
        ```
        <project xmlns = "http://maven.apache.org/POM/4.0.0"
            xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation = "http://maven.apache.org/POM/4.0.0
            http://maven.apache.org/xsd/maven-4.0.0.xsd">
         
            <!-- 模型版本 -->
            <modelVersion>4.0.0</modelVersion>
            <!-- 公司或者组织的唯一标志，并且配置时生成的路径也是由此生成， 如com.companyname.project-group，maven会将该项目打成的jar包放本地路径：/com/companyname/project-group -->
            <groupId>com.companyname.project-group</groupId>
         
            <!-- 项目的唯一ID，一个groupId下面可能多个项目，就是靠artifactId来区分的 -->
            <artifactId>project</artifactId>
         
            <!-- 版本号 -->
            <version>1.0</version>
        </project>
        ```
    + 构建生命周期：  
        1. clean（项目清理的处理）  
          pre-clean：执行一些需要在clean之前完成的工作  
          clean：移除所有上一次构建生成的文件
          post-clean：执行一些需要在clean之后立刻完成的工作
        2. Default (Build) 生命周期  
          validate（校验）、initialize（初始化）、generate-sources（生成源代码）、...compile（编译）、...、test（测试）、...package（打包）、...verify （验证）、install（安装）、deploy（部署）  
        3. Site 生命周期：一般用来创建新的报告文档、部署站点等
          pre-site：执行一些需要在生成站点文档之前完成的工作  
          site：生成项目的站点文档
          post-site： 执行一些需要在生成站点文档之后完成的工作，并且为部署做准备
          site-deploy：将生成的站点文档部署到特定的服务器上
    + 命令：格式为 mvn [plugin-name]:[goal-name] 会执行plugin-name所在周期前面所有plugin直到plugin-name，如mvn clean package 先执行clean生命周到,并运行到clean这个phase;接着运行default生命周期,并运行到package。  
    -D 指定参数，如 -Dmaven.test.skip=true 跳过单元测试；  
    -P 指定 Profile 配置，可以用于区分环境；  
    -e 显示maven运行出错的信息；  
    -o 离线执行命令,即不去远程仓库更新包；  
    -X 显示maven允许的debug信息；  
    -U 强制去远程更新snapshot的插件或依赖，默认每天只更新一次  
      ```
        命令 描述
        mvn –version 显示版本信息
        mvn clean 清理项目生产的临时文件,一般是模块下的target目录
        mvn compile 编译源代码，一般编译模块下的src/main/java目录
        mvn package 项目打包工具,会在模块下的target目录生成jar或war等文件
        mvn test 测试命令,或执行src/test/java/下junit的测试用例.
        mvn install 将打包的jar/war文件复制到你的本地仓库中,供其他模块使用
        mvn deploy 将打包的文件发布到远程参考,提供其他人员进行下载依赖
        mvn site 生成项目相关信息的网站
        mvn eclipse:eclipse 将项目转化为Eclipse项目
        mvn dependency:tree 打印出项目的整个依赖树
        mvn archetype:generate 创建Maven的普通java项目
        mvn tomcat:run 在tomcat容器中运行web应用
        mvn jetty:run 调用 Jetty 插件的 Run 目标在 Jetty Servlet 容器中启动 web 应用
      ```
  + MyBatis：半自动ORM，java的持久层框架，它内部封装了jdbc，使开发者只需要关注sql语句本身，而不需要花费精力去处理加载驱动、创建连接、创建statement等繁杂的过程。  
    1. 引入maven依赖
    2. 增加yml配置：指定mapper文件等
    3. 定义mapper.xml文件，写sql获取数据
    4. 定义dao层，与mapper方法和返回参数对应
    5. service中调用获取数据
  + 常用注解：
    + 项目配置层：  
    1、@SpringBootApplication：复合注解，包含了@SpringBootConfiguration，@EnableAutoConfiguration，@ComponentScan这三个注解。  
        @SpringBootConfiguration:标注当前类是配置类，这个注解继承自@Configuration。并会将当前类内声明的一个或多个以@Bean注解标记的方法的实例纳入到srping容器中，并且实例名就是方法名。  
        @EnableAutoConfiguration:是自动配置的注解，这个注解会根据我们添加的组件jar来完成一些默认配置，我们做微服时会添加spring-boot-starter-web这个组件jar的pom依赖，这样配置会默认配置springmvc 和tomcat。  
        @ComponentScan:扫描当前包及其子包下被@Component，@Controller，@Service，@Repository注解标记的类并纳入到spring容器中进行管理。等价于<context:component-scan>的xml配置文件中的配置项。  
    2、@ServletComponentScan:Servlet、Filter、Listener 可以直接通过 @WebServlet、@WebFilter、@WebListener 注解自动注册，这样通过注解servlet ，拦截器，监听器的功能而无需其他配置
    3、@MapperScan:spring-boot支持mybatis组件的一个注解，通过此注解指定mybatis接口类的路径，即可完成对mybatis接口的扫描，和mapper一样@mapper需要加在每一个mapper接口类上面。
    4、@import注解是一个可以将普通类导入到spring容器中做管理
    + controller层：  
    1、@Controller:处理http请求，用于标记这个类是⼀一个控制器器，返回⻚面的时候使用;如果要返回JSON,则需 要在接口上使用@ResponseBody才可以  
    2、@RestController:Spring4之后添加，返回json，@RestController = @Controller+@ResponseBody
    3、@RequestMapping:配置URL映射用于类上做1级路径，最新可以使用getMapping('/api')；@GetMapping = @RequestMapping(method = RequestMethod.GET)  
    4、@GetMapping(value =“”) = @RequestMapping(value=“”,method = RequestMethod.GET)  
    5、@Autowired：对象的创建交给了Spring容器，是spring的自动装配。
    + servcie层  
    1、@Service：这个注解用来标记业务层的组件  
    2、@Override：检测方法覆写的正确性
    + 持久层：  
    1、@Repository：注解类作为DAO对象，管理操作数据库的对象。  
    2、@JsonIgnore：指定字段不不返回  
    3、@Data：自动添加getset，equals()、hashCode()、toString()
  + Swagger：通过注解可以生成接口说明文档，作用  
    1、将项目中所有的接口展现在页面上，这样后端程序员就不需要专门为前端使用者编写专门的接口文档；  
    2、接口更新之后，只需要修改代码中的 Swagger 描述就可以实时生成新的接口文档了，从而规避了接口文档老旧不能使用的问题；   
    3、Swagger页面，可以直接进行接口调用，降低了项目开发阶段的调试成本。   
  + 定时任务：
    ```
    @Scheduled
    如：@Scheduled(cron = "0 0 */1 * * ?")
    cron：cron表达式，指定任务在特定时间执行； 
    fixedDelay：表示上一次任务执行完成后多久再次执行，参数类型为long，单位ms； 
    fixedDelayString：与fixedDelay含义一样，只是参数类型变为String； 
    fixedRate：表示按一定的频率执行任务，参数类型为long，单位ms； 
    fixedRateString: 与fixedRate的含义一样，只是将参数类型变为String； 
    initialDelay：表示延迟多久再第一次执行任务，参数类型为long，单位ms； 
    initialDelayString：与initialDelay的含义一样，只是将参数类型变为String； 
    zone：时区，默认为当前时区，一般没有用到。
    ```