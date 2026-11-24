# 堂音 · 曲艺驻演会堂听感分组

南棚曲艺馆维护一间小堂和一间分场，驻演由两位制作人轮值。原先用曲目音轨与纸质席位图配对，混用说、唱段，难复现实测组，且临时吸声板容易选错座席。系统接收前后排监听读数与素材引用，给驻演场务固定布置。

## 一天的工作顺序

1. 08:30 核对南棚小堂与西厢分场的座席图。
2. 09:00 读入说段-B1.wav 的清晰度 64、回声 660 ms。
3. 09:25 复核唱段-B1.wav 和同排 B2，凑齐双段。
4. 10:00 用 0.6 最大距离切出三组。
5. 11:10 S1 额度不够，拒签 B1 / B2。
6. 11:35 C1 位于通道，拒绝临时板。
7. 13:10 用中区软面板 S2 签入 N-28，锁定 B1 / B2 试听。
8. 13:40 收到迟到的试听更正，补录后重算整堂分组，再签 N-29。

## 迟到更正与重算

试听数值始终可以补录，包括已签场次用到的座席。签核时写入的座席与吸声板数即为该场次的固定布置，后续补录不会改动已签场次。

每次试听数值真正变化，会为该会堂开启新的试听版本。分组计算带版本标记存档，从不覆盖旧结果：

- 分组页同时给出「当前分组」与「过期结果」；过期结果折叠供查阅，但仍可追溯阈值、试听版本与完成时间。
- 只有按最新试听算完的整套分组才可签核；过期分组即使座席完全相同也会被拒绝，复核员须重新确认新分组。
- 若重算期间又补录了试听，旧任务算完也只会作为过期结果留存，不会成为当前分组，也不解锁签核。
- 重算失败不留下半套结果，可直接重试。

## 算法口径

以说、唱段的中位清晰度、回声和声级构成向量。两座席距离为绝对差分别除以 18、200、8 后取最大。完全联结按组内最远距离合并，并限定同一个区、相邻连续座号。回声中位达到 550 与 850 ms 时分别建议一块和两块吸声板。

## 上手

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
docker compose down --remove-orphans
```

前端走本机 **18447**，API 走 **19447**，PostgreSQL 走 **17947**。本地开发可在安装 Python 3.11、PostgreSQL 和 Redis 后配置与 Compose 相同的环境变量，在 backend 运行 `uvicorn app:app --reload`，前端以 Nginx 同源代理启动。

| 角色 | 邮箱 | 业务权限 |
|---|---|---|
| 录入员 | operator@demo.local | 录入试听、计算座席组 |
| 复核员 | reviewer@demo.local | 核对通道与布置额度并签核 |
| 查阅员 | viewer@demo.local | 查座席、音源凭证与方案 |

三个演示账号默认密码均为 `Demo2026!`。使用本地合成样本，seed 只插入缺失的自然键。关闭 `SEED_DEMO` 可跳过自动 seed。使用自己的 `JWT_SECRET`、`POSTGRES_PASSWORD` 和 `DEMO_PASSWORD` 部署。

| 目录 | 技术与职责 |
|---|---|
| backend | Python 3.11 / FastAPI，使用 PostgreSQL 16；Worker 轮询持久化队列，Redis 为登录限流及健康检查提供支持 |
| frontend | Nginx、HTML、CSS、JavaScript ES modules，HTTP 同源代理 |
| docker-compose.yml | 5 服务及健康检查、独立卷；Redis 与 worker 无宿主端口 |

角色、作业状态在 `backend/core.py`、`frontend/base.js` 定义，在 `backend/core.py`（鉴权、队列）与 `backend/worker.py` 使用。领域阶段由数据库约束与业务服务维护，`frontend/view.js` 负责显示。试听版本与分组计算的对应关系在 `backend/hearing_runs.py` 维护，接口输出当前与过期分组供前端区分。

试听源只保存参考名称与观察数值，演示没有分发曲艺录音。

MIT License
