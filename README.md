# Awesome Agentic RL Infrastructure

A curated reading list on **infrastructure for agentic reinforcement learning**: multi-turn agent training, rollout execution, distributed optimization, environment management, and algorithm-system co-design.

**34 papers** · **17 official project entries** · **Source review: 2026-10-12** · **English and Chinese paper summaries**

[Contents](#table-of-contents) · [Reading guide](docs/READING_GUIDE.md) · [Source audit](docs/SOURCE_AUDIT.md) · [Search record](docs/SEARCH_LOG.md) · [BibTeX](references.bib) · [Contributing](CONTRIBUTING.md)

## Scope and Terminology

The core scope is **LLM agents trained through repeated interaction with tools or environments**. Infrastructure includes the agent harness, trajectory collection, inference services, environments, rewards, experience storage, policy optimization, weight synchronization, and resource scheduling.

The catalog separates direct agent-training systems from general RLHF/RLVR foundations, environment/data pipelines, optimization methods, and embodied extensions. A code-generation benchmark alone does not establish multi-turn agent support. Likewise, an environment dataset is not a distributed trainer, and asynchronous execution alone does not guarantee learning stability.

- **Rollout:** a sampled sequence of model actions and environment observations; its length and runtime can vary across tasks.
- **Agent harness:** the program managing tools, context, and interaction control flow around model calls.
- **Disaggregation:** separate components or resource pools for training, inference, environments, or rewards; the exact separation differs by system.
- **Policy staleness:** the lag between the policy used to generate a sample and the policy being optimized.
- **Partial rollout:** interruption or staged processing of an unfinished trajectory; version and probability handling must follow the specific algorithm.
- **Training-inference mismatch:** different probabilities produced by training and inference implementations, distinct from policy-version lag.

## Reading the Entries

- **First submitted** comes from the arXiv submission history, not the identifier month, repository announcement, conference date, or latest revision.
- **A** means the primary-source abstract, metadata, and submission history were inspected. **M** additionally requires a cited method-section review. All initial entries are **A**; no experiment reproduction is implied.
- The **Source** cell links to the paper and, when verified, its official project. A missing code link means no official implementation was verified in this review, not that no code exists.
- **Checked** links to the exact reviewed version, full title, authors, and scope notes in the audit. Summaries describe that paper version; current repositories can contain later features.
- English and Chinese summaries carry the same mechanism and scope. Tags are editorial navigation aids. Entries have one primary section and are sorted by first submission within it.
- This is a curated starting collection, not an exhaustive survey or a cross-paper performance leaderboard.

## Start Here

Suggested sequence: **HybridFlow → AReaL → AgentRL → Agent Lightning / v1.0 → RollArt**. Read the original Lightning paper for the abstraction and its separate v1.0 report for harness integration. Then branch toward scheduling, environment costs, or algorithm-system correctness using the [reading guide](docs/READING_GUIDE.md).

## Table of Contents

- [Direction Overview](#direction-overview)
- [Agent Training Frameworks](#agent-training-frameworks)
- [Rollout Execution and Scheduling](#rollout-execution-and-scheduling)
- [General RL Training Systems](#general-rl-training-systems)
- [Environments and Data Pipelines](#environments-and-data-pipelines)
- [Algorithm-System Co-design](#algorithm-system-co-design)
- [Multimodal and Embodied Systems](#multimodal-and-embodied-systems)
- [Online Learning Architecture](#online-learning-architecture)
- [Official Projects](#official-projects)
- [Contributing](#contributing)

## Direction Overview

| Direction | Papers | Systems question |
| --- | --- | --- |
| [Agent Training Frameworks](#agent-training-frameworks) | 9 | Agent loops, harness integration, trajectory abstractions, and multi-agent execution. |
| [Rollout Execution and Scheduling](#rollout-execution-and-scheduling) | 9 | Asynchronous pipelines, synchronous long-tail mitigation, policy synchronization, cache placement, and heterogeneous resources. Reasoning-only systems are identified in the summaries. |
| [General RL Training Systems](#general-rl-training-systems) | 5 | Distributed RLHF and RLVR foundations. Inclusion here does not imply that the original paper implements multi-turn agents. |
| [Environments and Data Pipelines](#environments-and-data-pipelines) | 5 | Executable tasks, sandbox measurements, environment construction, and verification. These are complementary to the optimizer and trainer. |
| [Algorithm-System Co-design](#algorithm-system-co-design) | 3 | Optimization and diagnostics that constrain how asynchronous samples, policy versions, and training signals should be handled. |
| [Multimodal and Embodied Systems](#multimodal-and-embodied-systems) | 2 | Visual web interaction and VLA training, where screenshots, rendering, or simulators add different resource demands. |
| [Online Learning Architecture](#online-learning-architecture) | 1 | Trajectory protocols, data governance, and control-plane proposals for learning from deployed agents. |

## Agent Training Frameworks

Agent loops, harness integration, trajectory abstractions, and multi-agent execution.

| Paper and direction | First submitted | English | 中文 | Source | Checked |
| --- | --- | --- | --- | --- | --- |
| **RAGEN**<br>trajectory optimization · training stability | 2025-04-24 | Introduces a modular agent-training system and trajectory-level StarPO optimization. Studies unstable multi-turn learning and stabilizes it through trajectory filtering, a critic, and gradient stabilization in the reviewed revision. | 提出模块化智能体训练系统和轨迹级 StarPO 优化。研究多轮学习不稳定问题，并在所核验版本中通过轨迹过滤、评价网络及梯度稳定化进行改进。 | [arXiv 2504.20073](https://arxiv.org/abs/2504.20073)<br>[Code](https://github.com/mll-lab-nu/RAGEN) | [A · v2](docs/SOURCE_AUDIT.md#paper-2504-20073) |
| **AgentFly**<br>resource lifecycle · backpressure | 2025-07-20 | The reviewed revision manages sandboxes, model services, and APIs as typed resources in one scheduling engine. Its agent, rollout, context, and resource layers support multi-turn reuse, asynchronous backpressure, and scoped resource lifecycles. | 所核验版本将沙箱、模型服务与 API 作为类型化资源，交由统一引擎调度。智能体、采样、上下文和资源四层设计支持多轮复用、异步背压及分作用域的资源生命周期。 | [arXiv 2507.14897](https://arxiv.org/abs/2507.14897)<br>[Code](https://github.com/Agent-One-Lab/AgentFly) | [A · v2](docs/SOURCE_AUDIT.md#paper-2507-14897) |
| **Agent Lightning**<br>agent integration · trajectory interface | 2025-08-05 | Decouples agent execution from RL training through a unified transition interface. LightningRL assigns credit within agent trajectories, supporting existing agent implementations and dynamic workflows. | 通过统一转移接口，将智能体执行与 RL 训练解耦。LightningRL 在智能体轨迹内分配信用，支持已有智能体实现和动态工作流。 | [arXiv 2508.03680](https://arxiv.org/abs/2508.03680)<br>[Code](https://github.com/microsoft/agent-lightning) | [A · v1](docs/SOURCE_AUDIT.md#paper-2508-03680) |
| **AgentGym-RL**<br>interactive environments · horizon curriculum | 2025-09-10 | Offers a modular, decoupled framework for multi-turn RL across interactive environments. ScalingInter-RL gradually increases interaction horizons to manage exploration, exploitation, and optimization stability. | 提供跨交互环境的模块化、解耦多轮 RL 框架。ScalingInter-RL 逐步增加交互时域，以平衡探索、利用和优化稳定性。 | [arXiv 2509.08755](https://arxiv.org/abs/2509.08755)<br>[Code](https://github.com/WooooDyy/AgentGym-RL) | [A · v1](docs/SOURCE_AUDIT.md#paper-2509-08755) |
| **AgentRL**<br>multi-turn · multi-task · asynchronous | 2025-10-05 | Combines fully asynchronous generation and training with a unified function-call API, containerized environments, and a central controller. Cross-policy sampling and task advantage normalization address exploration and multi-task optimization. | 将全异步生成与训练、统一函数调用接口、容器化环境和集中控制器结合。通过跨策略采样与任务优势归一化，处理探索及多任务优化问题。 | [arXiv 2510.04206](https://arxiv.org/abs/2510.04206)<br>[Code](https://github.com/THUDM/AgentRL) | [A · v1](docs/SOURCE_AUDIT.md#paper-2510-04206) |
| **SkyRL-Agent**<br>agent integration · asynchronous dispatch | 2025-11-20 | Provides an agent layer with asynchronous pipeline dispatch, lightweight tool integration, and interoperability with multiple training backends. Demonstrates long-horizon training through software-engineering, research, computer-use, and memory agents. | 提供包含异步流水线调度、轻量工具接入和多训练后端互操作的智能体层。通过软件工程、研究、计算机操作及记忆智能体展示长时域训练。 | [arXiv 2511.16108](https://arxiv.org/abs/2511.16108)<br>[Code](https://github.com/NovaSky-AI/SkyRL) | [A · v1](docs/SOURCE_AUDIT.md#paper-2511-16108) |
| **FlexMARL**<br>multi-agent · resource allocation | 2026-02-10 | Coordinates LLM-based multi-agent rollout and training through an experience store and micro-batch asynchronous pipeline. Uses hierarchical rollout balancing and agent-centric allocation with training-state swapping. | 通过经验存储和微批次异步流水线，协调基于 LLM 的多智能体采样与训练。采用分层采样负载均衡，以及结合训练状态换入换出的智能体级资源分配。 | [arXiv 2602.09578](https://arxiv.org/abs/2602.09578) | [A · v1](docs/SOURCE_AUDIT.md#paper-2602-09578) |
| **Molt**<br>PyTorch native · experience storage | 2026-07-22 | Combines PyTorch and Hugging Face models with compatible agent interfaces, context-compaction handling, fully asynchronous training, and distributed experience storage. Targets experimentation with large policies and long multimodal trajectories. | 结合 PyTorch 与 Hugging Face 模型、兼容的智能体接口、上下文压缩处理、全异步训练和分布式经验存储。面向大规模策略及长多模态轨迹上的研究迭代。 | [arXiv 2607.21653](https://arxiv.org/abs/2607.21653)<br>[Code](https://github.com/NVIDIA-NeMo/labs-molt) | [A · v3](docs/SOURCE_AUDIT.md#paper-2607-21653) |
| **Agent Lightning v1.0**<br>agent harness · token consistency | 2026-08-18 | Keeps the deployment harness in control of tools, context, and interaction while the trainer observes model requests and responses. Studies retokenization, sample merging, advantage calculation, loss normalization, and backend scheduling. | 由部署时使用的 harness 控制工具、上下文和交互，训练器观测模型请求与响应。研究重新分词、样本合并、优势计算、损失归一化和后端调度。 | [arXiv 2608.17528](https://arxiv.org/abs/2608.17528)<br>[Code](https://github.com/microsoft/agent-lightning) | [A · v1](docs/SOURCE_AUDIT.md#paper-2608-17528) |

## Rollout Execution and Scheduling

Asynchronous pipelines, synchronous long-tail mitigation, policy synchronization, cache placement, and heterogeneous resources. Reasoning-only systems are identified in the summaries.

| Paper and direction | First submitted | English | 中文 | Source | Checked |
| --- | --- | --- | --- | --- | --- |
| **StreamRL**<br>disaggregation · long-tail scheduling | 2025-04-22 | Separates generation and training resources, then uses stream generation to overlap stages. An output-length ranker guides skewness-aware dispatch to reduce long-tail stalls, including heterogeneous deployment settings. | 分离生成与训练资源，并通过流式生成重叠不同阶段。利用输出长度排序模型指导长尾感知调度，减少长尾停顿，并研究异构部署场景。 | [arXiv 2504.15930](https://arxiv.org/abs/2504.15930) | [A · v1](docs/SOURCE_AUDIT.md#paper-2504-15930) |
| **AReaL**<br>asynchronous · policy staleness | 2025-05-30 | Decouples continuous rollout generation from batched policy updates. Controls data staleness through workload balancing and a staleness-enhanced PPO variant; the paper evaluates language reasoning rather than a general environment API. | 将持续采样生成与批次策略更新解耦。通过工作负载平衡和考虑陈旧度的 PPO 变体控制数据陈旧度；论文评测聚焦语言推理，而非通用环境接口。 | [arXiv 2505.24298](https://arxiv.org/abs/2505.24298)<br>[Code](https://github.com/areal-project/AReaL) | [A · v5](docs/SOURCE_AUDIT.md#paper-2505-24298) |
| **AsyncFlow**<br>streaming · distributed data | 2025-07-02 | Uses distributed storage and transfer to stream RL data between components with fine-grained scheduling. A producer-consumer workflow overlaps tasks and defers parameter updates within staleness limits while decoupling backend engines. | 通过分布式存储和传输，以细粒度调度在组件间流式传递 RL 数据。生产者—消费者工作流重叠执行任务，在陈旧度限制内推迟参数更新，并解耦底层引擎。 | [arXiv 2507.01663](https://arxiv.org/abs/2507.01663) | [A · v2](docs/SOURCE_AUDIT.md#paper-2507-01663) |
| **RollPacker**<br>synchronous · tail batching | 2025-09-25 | Groups prompts that produce long responses into designated long rounds while keeping most synchronous rollout rounds short. Combines this tail-batching strategy with elastic rollout parallelism, reward scheduling, and streaming training. | 将易产生长回答的提示集中到指定长轮次，使多数同步采样轮次保持较短。将这种尾部批处理与弹性采样并行、奖励调度和流式训练结合。 | [arXiv 2509.21009](https://arxiv.org/abs/2509.21009)<br>[Code](https://github.com/alibaba/ROLL) | [A · v1](docs/SOURCE_AUDIT.md#paper-2509-21009) |
| **ROLL Flash**<br>asynchronous · environment execution | 2025-10-13 | Extends ROLL with fine-grained parallelism and rollout-training separation. Queue scheduling and asynchronous environment execution support RLVR and agentic training, paired with evaluation of off-policy optimization methods. | 通过细粒度并行与采样训练分离扩展 ROLL。队列调度和异步环境执行支持 RLVR 及智能体训练，并配合对离策略优化方法的评估。 | [arXiv 2510.11345](https://arxiv.org/abs/2510.11345)<br>[Code](https://github.com/alibaba/ROLL) | [A · v1](docs/SOURCE_AUDIT.md#paper-2510-11345) |
| **RollArt**<br>heterogeneous hardware · reward services | 2025-12-27 | Maps prefill, decoding, and environments to suitable hardware and separates rollout components at trajectory granularity. Stateless reward computation uses serverless infrastructure, while bounded-staleness weight synchronization overlaps rollout and training. | 将预填充、解码和环境执行映射到适合的硬件，并在轨迹粒度分离采样组件。无状态奖励计算使用无服务器基础设施，通过有界陈旧度的权重同步重叠采样与训练。 | [arXiv 2512.22560](https://arxiv.org/abs/2512.22560)<br>[Code](https://github.com/alibaba/ROLL) | [A · v2](docs/SOURCE_AUDIT.md#paper-2512-22560) |
| **DORA**<br>multi-version policies · consistency | 2026-04-29 | Uses multi-version streaming rollout to overlap generation and training under long-tailed workloads. Frames system design around intra-trajectory policy consistency, data integrity, and bounded staleness. | 使用多版本流式采样，在长尾工作负载下重叠生成与训练。围绕轨迹内策略一致性、数据完整性和有界陈旧度设计系统。 | [arXiv 2604.26256](https://arxiv.org/abs/2604.26256) | [A · v2](docs/SOURCE_AUDIT.md#paper-2604-26256) |
| **WAR**<br>synchronous · KV cache | 2026-07-19 | Optimizes synchronous agentic rollout according to runtime load: suffix-based speculative decoding at low load and cache-aware placement at high load. The scheduler considers cache locality, trajectory progress, and replica load. | 根据运行负载优化同步智能体采样：低负载使用基于后缀的推测解码，高负载采用缓存感知放置。调度器综合缓存局部性、轨迹进度及副本负载。 | [arXiv 2607.17299](https://arxiv.org/abs/2607.17299) | [A · v1](docs/SOURCE_AUDIT.md#paper-2607-17299) |
| **VenusRL**<br>group scheduling · sandbox memory | 2026-10-02 | Prioritizes sample groups likely to unblock the next update across admission, KV-cache residency, and worker placement. Combines memory-aware sandbox admission with template-based page sharing and copy-on-write. | 在准入、KV 缓存驻留和工作节点放置中，优先处理更可能推动下一次更新的样本组。结合内存感知的沙箱准入、基于模板的页面共享和写时复制。 | [arXiv 2610.03286](https://arxiv.org/abs/2610.03286) | [A · v1](docs/SOURCE_AUDIT.md#paper-2610-03286) |

## General RL Training Systems

Distributed RLHF and RLVR foundations. Inclusion here does not imply that the original paper implements multi-turn agents.

| Paper and direction | First submitted | English | 中文 | Source | Checked |
| --- | --- | --- | --- | --- | --- |
| **OpenRLHF**<br>Ray · training and inference backends | 2024-05-20 | Provides a scalable RLHF and RLVR framework built on Ray, vLLM, DeepSpeed, and Hugging Face Transformers. The reviewed paper emphasizes coordinating training and inference with an accessible implementation. | 提供基于 Ray、vLLM、DeepSpeed 和 Hugging Face Transformers 的可扩展 RLHF 与 RLVR 框架。所核验论文强调训练推理协调，以及便于使用的实现。 | [arXiv 2405.11143](https://arxiv.org/abs/2405.11143)<br>[Code](https://github.com/OpenRLHF/OpenRLHF) | [A · v6](docs/SOURCE_AUDIT.md#paper-2405-11143) |
| **ReaL / ReaLHF**<br>parameter reallocation · execution planning | 2024-06-20 | Changes parallelization and resource allocation across RLHF workloads by redistributing model parameters. Searches for execution plans using a runtime estimator and executes the chosen plan with a distributed runtime. | 通过重新分配模型参数，在不同 RLHF 工作负载之间调整并行策略与资源分配。利用运行时间估计器搜索执行计划，再由分布式运行时执行所选计划。 | [arXiv 2406.14088](https://arxiv.org/abs/2406.14088)<br>[Code](https://github.com/openpsi-project/ReaLHF) | [A · v2](docs/SOURCE_AUDIT.md#paper-2406-14088) |
| **HybridFlow / verl**<br>control plane · resharding | 2024-09-28 | Combines single-controller and multi-controller execution to express RLHF dataflow with distributed models. Its hybrid engine reshards actor parameters between training and generation; this is foundational RL infrastructure. | 结合单控制器与多控制器执行，表达包含分布式模型的 RLHF 数据流。其混合引擎在训练与生成之间重分片策略模型参数，属于基础 RL 训练设施。 | [arXiv 2409.19256](https://arxiv.org/abs/2409.19256)<br>[Code](https://github.com/verl-project/verl) | [A · v2](docs/SOURCE_AUDIT.md#paper-2409-19256) |
| **ROLL**<br>worker abstraction · sample lifecycle | 2025-06-06 | Uses a single controller and parallel-worker abstraction to compose RL pipelines. Sample-lifecycle scheduling, environment and reward workers, data transfer, and flexible device mapping support agentic experimentation. | 使用单控制器和并行工作单元抽象组织 RL 流水线。通过样本生命周期调度、环境与奖励工作单元、数据传输和灵活设备映射，支持智能体实验。 | [arXiv 2506.06122](https://arxiv.org/abs/2506.06122)<br>[Code](https://github.com/alibaba/ROLL) | [A · v1](docs/SOURCE_AUDIT.md#paper-2506-06122) |
| **RLinf**<br>workflow transformation · elastic pipelining | 2025-09-19 | Transforms high-level RL workflows into optimized temporal and spatial execution flows. Adaptive communication, context switching, elastic pipelining, and profiling-guided scheduling support reasoning and embodied RL. | 将高层 RL 工作流转换为在时间与空间维度优化的执行流。通过自适应通信、上下文切换、弹性流水线和性能剖析引导的调度，支持推理及具身 RL。 | [arXiv 2509.15965](https://arxiv.org/abs/2509.15965)<br>[Code](https://github.com/RLinf/RLinf) | [A · v2](docs/SOURCE_AUDIT.md#paper-2509-15965) |

## Environments and Data Pipelines

Executable tasks, sandbox measurements, environment construction, and verification. These are complementary to the optimizer and trainer.

| Paper and direction | First submitted | English | 中文 | Source | Checked |
| --- | --- | --- | --- | --- | --- |
| **AgentGym**<br>environment interfaces · trajectory data | 2024-06-06 | Provides diverse interactive environments with a unified format and concurrent exploration, together with trajectories and benchmarks. Supplies environment infrastructure and an agent-evolution method rather than a distributed RL trainer. | 提供统一格式、支持并发探索的多种交互环境，以及轨迹数据和评测基准。贡献环境基础设施与智能体演化方法，而非分布式 RL 训练器。 | [arXiv 2406.04151](https://arxiv.org/abs/2406.04151)<br>[Code](https://github.com/WooooDyy/AgentGym) | [A · v1](docs/SOURCE_AUDIT.md#paper-2406-04151) |
| **SWE-Gym**<br>executable tasks · verification | 2024-12-30 | Packages software-engineering tasks with repositories, executable environments, and unit tests. Supports training agents and trajectory verifiers; it supplies task infrastructure rather than an asynchronous RL execution engine. | 将软件工程任务与代码仓库、可执行环境和单元测试打包。支持训练智能体及轨迹验证器；提供任务基础设施，而非异步 RL 执行引擎。 | [arXiv 2412.21139](https://arxiv.org/abs/2412.21139)<br>[Code](https://github.com/SWE-Gym/SWE-Gym) | [A · v2](docs/SOURCE_AUDIT.md#paper-2412-21139) |
| **SWE-smith**<br>environment construction · task synthesis | 2025-04-30 | Builds execution environments from Python repositories and synthesizes task instances that break existing tests. Scales software-engineering training data and associated runtime environments rather than introducing an RL optimizer. | 从 Python 仓库构建执行环境，并合成使现有测试失败的任务实例。扩展软件工程训练数据及配套运行环境，而非提出 RL 优化器。 | [arXiv 2504.21798](https://arxiv.org/abs/2504.21798)<br>[Code](https://github.com/SWE-bench/SWE-smith) | [A · v2](docs/SOURCE_AUDIT.md#paper-2504-21798) |
| **SWE-Factory**<br>environment construction · test validation | 2025-06-12 | Automates issue-resolution dataset construction through binary-test recovery, multi-agent environment setup, and exit-code-based fail-to-pass validation. Supports training-data and evaluation-environment preparation. | 通过二进制测试恢复、多智能体环境搭建，以及基于退出码的失败到通过验证，自动构建问题修复数据集。支持准备训练数据和评测环境。 | [arXiv 2506.10954](https://arxiv.org/abs/2506.10954)<br>[Code](https://github.com/DeepSoftwareAnalytics/swe-factory) | [A · v3](docs/SOURCE_AUDIT.md#paper-2506-10954) |
| **Rollout Infrastructure Tax**<br>sandbox overhead · measurement | 2026-07-01 | Compares containers, hosted sandboxes, Kubernetes-managed containers, and cloud VMs as coding-agent execution substrates. Measures startup overhead and projects rollout worker costs; this is a measurement study, not a new trainer. | 比较容器、托管沙箱、Kubernetes 管理的容器和云虚拟机作为编码智能体执行底座的表现。测量启动开销并估算采样工作成本；属于测量研究，而非新训练框架。 | [arXiv 2607.01415](https://arxiv.org/abs/2607.01415) | [A · v1](docs/SOURCE_AUDIT.md#paper-2607-01415) |

## Algorithm-System Co-design

Optimization and diagnostics that constrain how asynchronous samples, policy versions, and training signals should be handled.

| Paper and direction | First submitted | English | 中文 | Source | Checked |
| --- | --- | --- | --- | --- | --- |
| **RAGEN-2**<br>online diagnostics · sample filtering | 2026-04-07 | Diagnoses input-agnostic reasoning templates that can persist despite stable entropy using mutual-information proxies. Uses reward-variance-based filtering to retain stronger training signals; included for online observability and sample-selection implications. | 利用互信息代理指标，诊断在熵稳定时仍可能存在的、与输入无关的推理模板。通过基于奖励方差的过滤保留较强训练信号；因其对在线观测和样本选择的启示而收录。 | [arXiv 2604.06268](https://arxiv.org/abs/2604.06268)<br>[Code](https://github.com/mll-lab-nu/RAGEN) | [A · v1](docs/SOURCE_AUDIT.md#paper-2604-06268) |
| **Missing Old Logits**<br>policy versions · training-inference mismatch | 2026-05-12 | Distinguishes training-inference distribution mismatch from policy staleness when historical training-side logits are missing. Analyzes version snapshots, a dedicated old-policy model, partial-rollout synchronization, and approximate correction. | 在缺少历史训练侧 logits 时，区分训练推理分布差异与策略陈旧度。分析版本快照、专用旧策略模型、部分轨迹同步，以及近似校正方案。 | [arXiv 2605.12070](https://arxiv.org/abs/2605.12070) | [A · v3](docs/SOURCE_AUDIT.md#paper-2605-12070) |
| **SAO**<br>single-rollout sampling · off-policy optimization | 2026-07-08 | Replaces group-wise sampling with one rollout per prompt, combined with value-model training and double-sided token clipping. Studies the stability and off-policy implications of asynchronous agent training; primarily an optimization method. | 以每个提示采样一条轨迹替代分组采样，结合价值模型训练与词元级双侧裁剪。研究异步智能体训练的稳定性及离策略影响，主要贡献是优化方法。 | [arXiv 2607.07508](https://arxiv.org/abs/2607.07508) | [A · v1](docs/SOURCE_AUDIT.md#paper-2607-07508) |

## Multimodal and Embodied Systems

Visual web interaction and VLA training, where screenshots, rendering, or simulators add different resource demands.

| Paper and direction | First submitted | English | 中文 | Source | Checked |
| --- | --- | --- | --- | --- | --- |
| **RLinf-VLA**<br>embodied agents · simulator scheduling | 2025-10-08 | Unifies VLA architectures, RL algorithms, and heterogeneous simulators. Coordinates rendering, inference, and training with flexible resource allocation and a hybrid fine-grained pipeline; an embodied extension of the main scope. | 统一 VLA 架构、RL 算法和异构模拟器。通过灵活资源分配与混合细粒度流水线协调渲染、推理及训练，属于本目录主题的具身扩展。 | [arXiv 2510.06710](https://arxiv.org/abs/2510.06710)<br>[Code](https://github.com/RLinf/RLinf) | [A · v3](docs/SOURCE_AUDIT.md#paper-2510-06710) |
| **AsyncWebRL**<br>visual web agents · asynchronous | 2026-06-04 | Overlaps rollout, gradient updates, and policy refresh using a persistent rollout pool and lightweight screenshot handling. Also changes multi-step GRPO normalization to address inefficient trajectories and token usage. | 通过持续采样池与轻量截图处理，重叠轨迹采样、梯度更新和策略刷新。还调整多步 GRPO 归一化，以处理轨迹和词元使用效率问题。 | [arXiv 2606.05597](https://arxiv.org/abs/2606.05597) | [A · v3](docs/SOURCE_AUDIT.md#paper-2606-05597) |

## Online Learning Architecture

Trajectory protocols, data governance, and control-plane proposals for learning from deployed agents.

| Paper and direction | First submitted | English | 中文 | Source | Checked |
| --- | --- | --- | --- | --- | --- |
| **AReaL 2.0 / Self-Evolving Agent Systems**<br>trajectory protocol · learning control plane | 2026-07-01 | Argues for step-level trajectory protocols, governed data proxies, and a control plane for agent evolution. Instantiates policy-weight updates through AReaL 2.0; a systems position and architecture paper, not proof of every proposed evolution mechanism. | 主张建设步骤级轨迹协议、受治理的数据代理及智能体演化控制平面。通过 AReaL 2.0 实现策略权重更新；属于系统立场与架构论文，不代表所有提议的演化机制均已得到验证。 | [arXiv 2607.01120](https://arxiv.org/abs/2607.01120)<br>[Code](https://github.com/areal-project/AReaL) | [A · v2](docs/SOURCE_AUDIT.md#paper-2607-01120) |

## Official Projects

Repository identities, README paper links, and archive flags were checked on **2026-10-12**. These are navigation entries, not feature-parity or maintenance-quality rankings. Multiple papers may share one codebase. README blob identifiers are recorded in [projects.json](data/projects.json).

| Official repository | Related catalog entries | Repository status at review |
| --- | --- | --- |
| [Agent-One-Lab/AgentFly](https://github.com/Agent-One-Lab/AgentFly) | AgentFly | Not archived |
| [alibaba/ROLL](https://github.com/alibaba/ROLL) | ROLL Flash; RollArt; RollPacker; ROLL | Not archived |
| [areal-project/AReaL](https://github.com/areal-project/AReaL) | AReaL; AReaL 2.0 / Self-Evolving Agent Systems | Not archived |
| [DeepSoftwareAnalytics/swe-factory](https://github.com/DeepSoftwareAnalytics/swe-factory) | SWE-Factory | Not archived |
| [microsoft/agent-lightning](https://github.com/microsoft/agent-lightning) | Agent Lightning; Agent Lightning v1.0 | Not archived |
| [mll-lab-nu/RAGEN](https://github.com/mll-lab-nu/RAGEN) | RAGEN; RAGEN-2 | Not archived |
| [NovaSky-AI/SkyRL](https://github.com/NovaSky-AI/SkyRL) | SkyRL-Agent | Not archived |
| [NVIDIA-NeMo/labs-molt](https://github.com/NVIDIA-NeMo/labs-molt) | Molt | Not archived |
| [openpsi-project/ReaLHF](https://github.com/openpsi-project/ReaLHF) | ReaL / ReaLHF | Archived |
| [OpenRLHF/OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) | OpenRLHF | Not archived |
| [RLinf/RLinf](https://github.com/RLinf/RLinf) | RLinf; RLinf-VLA | Not archived |
| [SWE-bench/SWE-smith](https://github.com/SWE-bench/SWE-smith) | SWE-smith | Not archived |
| [SWE-Gym/SWE-Gym](https://github.com/SWE-Gym/SWE-Gym) | SWE-Gym | Not archived |
| [THUDM/AgentRL](https://github.com/THUDM/AgentRL) | AgentRL | Not archived |
| [verl-project/verl](https://github.com/verl-project/verl) | HybridFlow / verl | Not archived |
| [WooooDyy/AgentGym](https://github.com/WooooDyy/AgentGym) | AgentGym | Not archived |
| [WooooDyy/AgentGym-RL](https://github.com/WooooDyy/AgentGym-RL) | AgentGym-RL | Not archived |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for inclusion criteria, bilingual summaries, evidence requirements, and validation. Edit [catalog.json](data/catalog.json), then regenerate the README, source audit, and bibliography.

## Organization Reference

This repository follows the English navigation, bilingual paper tables, explicit scope boundaries, submission dates, and source-audit style of [Awesome-OPD](https://github.com/kissshhot/Awesome-OPD). Its taxonomy and summaries are written specifically for agentic RL infrastructure.
