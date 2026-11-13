# 澄翼研修 · 故障证据概率推理

在给定的二元DAG与不可变CPT版本中，计算证据后的精确后验，并比较候选观测的期望信息增益。每份底稿保留证据分母、对数概率、消元操作和分支依据。

## 研修场景

澄翼技术研修组是15人的模拟培训团队，使用 `CY-07_evidence_202611.json` 讨论故障假设与表征之间的概率关系。原先依赖经验排查清单与电子表格：先验常被当成后验，互相矛盾的零概率证据容易被忽略，下一项观察的信息价值也缺少可追溯计算。

上游是课程作者给定的DAG、完整CPT与练习证据；本系统替代概率汇总、精确消元、候选分支推演与签批整理；下游是课程主管与研究助理。这里的结构和概率都是模拟输入，不从数据发现因果，也不输出真实检查或维修指令。

|角色|权限|典型动作|
|---|---|---|
|analyst 分析师|读取六页；创建网络、CPT修订、证据案例、运行和复核|核对父配置，执行联合证据推理|
|admin 研修主管|分析师权限；批准、归档、查看审计|签署模型版本、证据分母与研修边界|
|viewer 研究助理|只读六页与批准报告CSV|下载锁定后验与候选分支|

### 一天的演练

1. 09:00 打开「CY-07 研修证据图」，核对Fault、Power、Heat、Vibration、Alarm、Indicator、Lock共7个二元节点。Heat有Fault/Power两个父节点，Indicator是弱指示表征。
2. 09:05 核对「CY-07 研修证据图 / CPT r1」的16个父配置行。Lock为确定性演练标记，严格零概率被明确保留。
3. 09:10 新建「温升与告警联合证据」，锁定r1，查询Fault，证据Heat=1、Alarm=1，候选自动限定为未观测非目标节点。
4. 09:15 Redis worker执行log域精确因子消元。给定模型后验P(Fault=1|E)约0.660806，logZ约−1.848945，不能读成现实故障率。
5. 09:20 点选Vibration，核对两分支权重、条件后验和熵；其IG约0.393832 bit，原始IG和基准分母一起保留。
6. 09:25 查看词典序消元Indicator→Lock→Power→Vibration的真实因子作用域与单元数。
7. 09:30 运行「两项1e-200证据仍可行」：logZ约−921.034037，exp下溢为0但证据仍可行。再运行Fault=0、Lock=1的零概率反例，应明确失败。
8. 09:40 分析师提交说明，主管批准并生成不可变快照；助理下载后验/候选/分支CSV，连同版本和SHA256归档。

## 六聚合与页面

|聚合|职责|页面|
|---|---|---|
|BayesNetwork|给定DAG、节点标签与有序父节点列表|给定网络|
|CptRevision|不可变网络版本与完整条件概率|概率版本|
|EvidenceCase|绑定版本、证据、查询目标与候选集合|证据案例|
|InferenceRun|异步状态、快照、后验、候选分支与VE留痕|推理底稿|
|EvidenceReview|分析师说明与主管批准状态|研修归档|
|Report|批准后的不可变报告与CSV|研修归档|

「证据总览」使用真实基线结果；另有登录与管理员审计页。总览/网络/运行共用DAG图，总览/运行共用候选信息排行，概率摘要也用于批准底稿。

## 输入与版本

网络节点JSON为 `[{"node_id":"F","label":"故障假设","parents":[]},{"node_id":"S","parents":["F"]}]`。1–10个二元节点，最多4个父节点；ID唯一、ASCII字母起始，最长32字符。父节点已知、不可重复、自环和有向环均拒绝。parents原顺序被保留，用于解释CPT配置。

CPT行JSON为 `[{"node_id":"F","parent_values":[],"p0":0.8,"p1":0.2},...]`。每个节点、每种完整父配置恰有一行；parent_values按parents顺序使用0/1。p0/p1有限、在[0,1]，行和1的绝对容差1e−12；原始概率和行和均保留，不擅自填缺失配置。未知、重复或缺失配置拒绝。

同一网络/版本号具有数据库复合唯一约束，重复创建返回409；CPT没有更新接口。新知识创建新修订。网络PATCH只允许说明字段，DAG、概率、证据和目标都通过新实体版本修改，既有研究结果不被覆盖。

证据JSON为已知节点的0/1映射，布尔值不替代二元整数。候选JSON为null（所有未观测非目标节点）或不重复的节点数组；观测节点和目标不能混入候选。

## 两个Python算法

### log因子消元精确后验

`services.variable_elimination.infer(nodes,cpt,evidence,target)` 创建真实CPT因子，限制证据，并按隐藏节点ID词典序执行：收集包含该变量的因子→log域乘积（相加）→用logsumexp边缘化→回收缩减因子。最后乘积给出目标未归一质量，logsumexp产生logZ。实现没有建立全状态联合枚举表；独立验收脚本另用枚举作为oracle。

对数使用自然log；内部严格0用−∞表示。**只有logZ=−∞才是不可能证据**。有限logZ代表正概率，即使exp(logZ)已下溢为0，仍返回可行后验并标注 `evidence_probability_underflow=true`。查询变量已观测时，也必须先算出可行Z，随后才返回one-hot。

后验每个状态包含probability、log_probability及下溢标记；API的log_probability=null只表示严格零概率，避免将非有限JSON数值冒充普通数字。有限log概率但exp为0仍有独立下溢标记。概率与logZ是float64数值计算，数学上精确推理不代表无限精度算术，极小概率场景可能有约1e−14的归一舍入差。

### 候选期望后验熵与信息增益

`services.information_gain.information_gain(nodes,cpt,evidence,target,candidates=None,negative_tolerance=1e-10)` 先算基准后验，再为每个合法候选X求P(X|E)。对两个状态分别追加证据并调用同一精确VE：

`IG(X)=H(Q|E)−Σ_x P(X=x|E)*H(Q|E,X=x)`，熵使用log₂，单位bit。

严格零概率分支跳过；若分支log概率有限而exp权重下溢，仍计算该分支后验并标注，浮点加权贡献可能为0。仅[−1e−10,0)的数值微负IG截为0，原始值与标记保留；更严重负值失败，不能隐藏异常。每个候选保留基准熵、期望熵、原始/展示IG、边缘后验与两分支的完整推理结果/联合logZ。

IG是给定模型内的期望不确定性下降，不等于维修收益、风险降低或观测的现实可实施性。模型依赖给定DAG的条件独立结构和人工CPT；不拟合参数，不学习因果，不构造现实诊断保证。

### 手算与极小概率

F先验0.2；P(S=1|F=1)=0.8、P(S=1|F=0)=0.1，则P(S=1)=0.24，S=1后P(F=1)=2/3。无证据时观测S的IG约0.2754581855 bit。两个独立事件各1e−200同时为1时logZ=2*ln(1e−200)≈−921.034037，证据可行；不能因浮点乘积变0而报不可能。

NumPy使用float64；CPT、行和、概率、log概率、熵、原始/展示IG等SQL标量全部为MySQL DOUBLE。严格零log概率使用可空DOUBLE；完整DAG/CPT/证据/目标/候选/版本及所有推理留存JSON快照与SHA256。相同锁定案例可复跑并得到相同结果。

## 快速启动

```sh
cp .env.example .env
docker compose config --quiet
docker compose up -d --build --wait
docker compose exec backend python scripts/seed_demo.py
```

前端 http://localhost:18235；后端 http://localhost:19235/docs；健康检查 `/health`。MySQL端口17735，库/用户名evidence，演示密码evidence_demo。

账号 `admin@evidence.demo`、`analyst@evidence.demo`、`viewer@evidence.demo`，统一密码 `EvidenceDemo2026!`。首次启动 `SEED_DEMO=true` 自动seed；固定自然ID只补缺，不覆盖用户说明。seed包括7节点主图、F/S手算图、极小正证据图与5个练习案例。基线由seed直接计算以便首次打开，新建运行真实经过Redis worker。

```sh
docker compose ps
docker compose logs worker
docker compose down -v --remove-orphans
```

最后一条删除本项目演示数据卷。

## 技术与结构

|部分|实现|
|---|---|
|前端|Vue3.5.13 / TypeScript5.7.2 / Vite6，原生SVG，轻量hash路由|
|API与任务|Python3.12 / FastAPI0.115.6 / SQLAlchemy2 / Redis列表worker|
|数值|NumPy2.2.1 / SciPy1.14.1 logsumexp|
|存储|MySQL8.4，实际验收8.4.11；Redis7.4|
|五服务|frontend/Nginx1.28、backend、worker、db、redis|

`backend/src/{models,schemas,services,controllers,routes}`贯穿六聚合；`middlewares`处理审计与全局错误，`utils`负责JWT/PBKDF2/队列；`backend/scripts/seed_demo.py`及demo_data定义自然键演示数据。新库按SQLAlchemy metadata建表，已有生产库需审查增量迁移。

`frontend/src/{api,stores,types,components/common,hooks,pages,router,utils,constants}`拆分职责。Python完成全部概率计算、业务校验与持久化，前端只输入、选择与展示结果。

前端本地：`cd frontend && npm ci && npm run dev`，Vite代理 `/api` 至localhost:19235。后端本地创建Python3.12虚拟环境，安装 `backend/requirements.txt`，设置DATABASE_URL、REDIS_URL、JWT_SECRET，在backend目录运行 `uvicorn src.main:app --reload` 及单独的 `python -m src.worker`；数据库/Redis可用Compose。

|环境变量|默认/用途|
|---|---|
|COMPOSE_PROJECT_NAME|fault-evidence，隔离容器、卷与网络|
|FRONTEND_PORT/BACKEND_PORT/DB_PORT|18235/19235/17735|
|JWT_SECRET|本地演示值，部署替换|
|SEED_DEMO|true，自动补齐演示数据|
|DATABASE_URL/REDIS_URL|Compose内服务地址，本地开发按实际地址设置|

JWT缺失/无效401，权限不足403，缺实体404，重复名称/版本或状态冲突409，非法输入422；全局错误提供重试提示。审计记录写入路径、方法、响应码与认证账号，不写密码、Token或模型正文。worker失败保留原因，可重新运行；单worker无分布式故障恢复保证。

共享枚举定义在 `backend/src/constants/enums.py` 与 `frontend/src/constants/enums.ts`：角色admin/analyst/viewer、运行queued/running/completed/failed、复核submitted/approved。认证、worker/复核和前端权限/状态显示使用这些取值。

源码与证据分离，同批 `test-artifacts/gb-2406/TESTING.md`提供可复跑测试与截图。依赖使用npm ci，`.env`、node_modules、构建产物、上传、截图与日志被忽略。

## License

MIT，见LICENSE。客户、DAG和概率均为模拟。
