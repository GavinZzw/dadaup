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
    + 一致性（Consistency）：事务执行前后，数据从一个状态到另一个状态必须是一致的（本来应该+，结果出来成-了）。
    + 隔离性（Isolation）：多个并发事务之间相互隔离，一个不影响另一个。
    + 持久性（Durablity）：事务执行完后，对数据库修改是永久的，没法回滚。
  + 事务并发常见问题
    + 脏读：A事务执行过程中，B事务修改了数据，导致A事务读取了修改后的数据，但是B最后又回退了，所以让A读取了错误的数据。
    + 不可重复读：A执行过程中，B修改了数据，导致A前后读取的数据不一致。
    + 幻读：A执行过程中，B增加了数据，导致A前后读取不一致。
  + 针对事务并发隔离的4个级别：MYSQL默认可重复读，设置隔离级别：SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
    + 读未提交：能读到未提交的事务中所做的修改，这种会产生脏读。性能不会好太多，问题很多，很少用。
    + 读已提交：只能获取已经提交事务后的结果，也就是说事务中所做的修改对其他事务是不可见的。解决的脏读问题。
    + 可重复读：读取一个数据前给数据加共享行锁，更新时加排它行锁，这样就避免在事务中数据被其他事务修改，解决了不可重复读问题。
    + 可串行化：加表锁防止事务并行。innodb通过MCVV快照方式解决幻读问题。
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
    ```angular2
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
  | 数据一致 | 数据库和缓存更新，就容易出现缓存(Redis)和数据库（MySQL）间的数据一致性问题  | 1. 读的时候缓存没有就读数据库，读到数据存入缓存并返回响应；2. 更新数据先更新数据库然后让缓存失效。如果先让缓存失效可能导致一个线程让缓存失效了，还没更新完数据库，另一个查询又把脏数据缓存了。 | 
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
    假如leader挂掉了，B选举为leader了 c再去同步发现数据不一样一个是1-8 一个 是1-6 假如这个时候A恢复了 为1-10，这个时候他们的消息不等 消费者消费消息就会出现问题，kefka是用两个标识来处理的一个是HW（在所有消息队列里面最短的一个LEO）为HW，LEO（log end office）最后一个消息的偏移量，HW在选举为B的时候 他为1-6 他会发送命令 所有人给我截取到6 其余的数据都扔掉，消费者来消费消息也只会消费到HW所在对应的那一个偏移量，假如这个时候选取的是C同步数据为1-8，他的HW为6的数据上面 会发送指定 都给我截取到6 卡卡卡都截取了，再给我A和B再去询问是否有新数据 发现有 7-8 就会同步上去
    
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
  如：*.index：1，0 表在数据文件中从上倒下第一条消息，0表示消息的物理偏移地址（前面所有消息总长度）。
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
## 2. TCP/UDP  
  UDP：无连接;不可靠;效率高;多对多:视频会议等场景  
  TCP：需要建立连接;可靠;只能一对一:文件传输等场景  
  三次握手：
  1. 客户端发送SYN报文，请求建链。SYN报文：flag中SYN标识为1，随机产生一个序列号，seq=X
  2. 服务端收到SYN后，发送SYN+ACK报文：flag中SYN和ACk标识为1，ack=X+1,随机产生序列号，seq=Y
  3. 客户端收到回复后，发送确认包ACK：flag中ACK标识为1，ack=Y+1 
  
  四次挥手：由于全双工，需要两边都确认断链  
  1. 客户端发送FIN报文,表示数据发送完成，请求断链：flag中FIN标识为1
  2. 服务端收到后发送ACK报文关闭本端，
  3. 服务端数据发送完成后，发送FIN报文
  4. 客户端收到后发送ACk报文，等待2*MSL,没有收到回复表示服务端已经关闭，则客户端关闭
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
## 4. https加密
  + 为什么有HTTPS，因为http不安全，安全就是传输过程中只有客户端和服务端可以看到通信内容。
    1. 对称加密：数据加密发送，服务端解密，但是一般多个客户端和一个服务端通信，如果服务器端对所有的客户端通信都使用同样的对称加密算法，无异于没有加密。
    2. 非对称加密：公钥加密只有对应私钥才能解，私钥加密只有对应公钥才能解。服务器将 公钥发给所有客户端，服务器发送消息使用私钥加密后发送，客户端有公钥可以解密数据。
    3. 加密算法确定：为了保证不同客户端使用不同加密算法，通信使用随机数来确定，所以只有交互时才能确定加密算法。
    4. 公钥传输掉包：客户端怎么获取服务器的公钥，客户端没法保存所有网站的公钥，只能每次请求前去服务端请求。如果A去请求C获取公钥，被中间B拦截，B将自己的公钥发送给A，A每次发送数据使用B的公钥加密发送，B收到后使用自己私钥解密，再用C公钥加密（可以篡改数据）发送给C，C返回数据给B，B再返回给A，A和C都不知道自己通信数据已经泄密。主要由于客户端无法区分返回公钥的是服务器还是中间人。
    5. 数字证书：服务器让第三方机构管理公钥，第三方机构用自己的私钥加密公钥和服务器相关信息，加密后的信息称为数字证书。客户端将数字证书发给服务端，服务端本地存储好第三方机构的公钥，使用该公钥解密数字证书，可以解密就说明没有被掉包。
    6. 数字签名：如果A去请求服务器证书，B同样有第三方公钥，可以拦截修改公钥。所有需要数字签名，第三方机构制作证书时，将所有服务器信息和公钥计算出摘要（MD5或者hash码），然后再用自己的私钥加密摘要生成一个签名，和证书一起颁发给服务器。即使中间B截获了证书并解密，但是无法修改其内容，因为修改后要用私钥加密摘要生成签名，B是没有第三方机构的私钥，所有保证了证书不被篡改。
  + SSL/TLS协议: https中加密信息，就是上述流程
    1. 客户发起请求时，除了说明自己支持的非对称加密算法，还会附加一个客户端随机数。
    2. 服务器回复请求时，会确定非对称加密算法和哈希函数，并附上公钥。此外，服务器端还会在此次通信中附加一个服务器端随机数
    3. 客户端会产生第三个随机数(Premaster secret)，客户端验证公钥，获取服务端发送的信息，然后利用服务器确定的非对称加密算法和公钥来加密这个随机数，再发送给服务器端。
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
        git reset HEAD^ #恢复到上次提交的版本
        git reset HEAD^^ #恢复到上上次提交的版本，或者~n，恢复到前n次
        git reset --hard commit号 #恢复到指定版本
        git revert HEAD #撤销最近一次提交
        git revert commit号 #撤销某次commit
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
              - cluster.name=aisa_es_cluster
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
              - /opt/work/nta/lib/log4j-core-2.11.1.jar:/usr/share/elasticsearch/lib/log4j-core-2.11.1.jar
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
            ssl_certificate "/etc/nginx/ssl/aisa/server.crt"; 证书路径，包含公钥
            ssl_certificate_key "/etc/nginx/ssl/aisa/server.key"; 私钥路径
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
    + select:fd_r_list, fd_w_list, fd_e_list = select.select(rlist(等待读), wlist（等待些）, xlist（等待异常）, [timeout])
        select函数会阻塞，直到rlist中的套接字被触发  
        优点：占用资源少，同时能监听多个客户端  
        缺点：当等待读的数据多时，select接口需要大量时间去轮询各个句柄
    + poll机制： Linux    #和lselect监听机制一样，但是对监听列表里面的数量没有限制，select默认限制是1024个，但是他们两个都是操作系统轮询每一个被监听的文件描述符（如果数量很大，其实效率不太好），看是否有可读操作。
    + epoll机制： Linux    #它的监听机制和上面两个不同，他给每一个监听的对象绑定了一个回调函数，你这个对象有消息，那么触发回调函数给用户，用户就进行系统调用来拷贝数据，并不是轮询监听所有的被监听对象，这样的效率高很多。
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
        R运行状态（running）: 并不意味着进程一定在运行中，它表明进程要么是在运行中要么在运行队列 里。
        S睡眠状态（sleeping): 意味着进程在等待事件完成（这里的睡眠有时候也叫做可中断睡眠 （interruptible sleep））。
        D磁盘休眠状态（Disk sleep）有时候也叫不可中断睡眠状态（uninterruptible sleep），在这个状态的 进程通常会等待IO的结束。
        T停止状态（stopped）： 可以通过发送 SIGSTOP 信号给进程来停止（T）进程。这个被暂停的进程可 以通过发送 SIGCONT 信号让进程继续运行。
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
   + 数组
   + 链表
   + 堆
   + 栈
   + 队列
   + 二叉树
   + 红黑树
   + B树
   + b+树
## 2. 常用算法

# 开发框架
## 1. flask
## 2. django
## 3. spring boot