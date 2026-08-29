# # -*- coding: utf-8 -*-
# """
# 运行后在当前目录生成 talk/ 文件夹，内含 18 个 .json 文件。
# 每个文件是对应 PPT 页面的「逐句中英对照」讲稿，结构为:
#     {"page": 1, "topic": "标题",
#      "sentences": [{"en": "...", "zh": "..."}, ...]}

# 设计要点:
#   * 以「句」为对齐单位 —— 同一份句子列表同时驱动 TTS 配音与字幕，
#     因此「英文语音 / 英文字幕 / 中文字幕」三者天然一一对应。
#   * 英文逐句保持与 PPT 旁白完全一致(保证配音不变)，中文为对应翻译。
# 直接运行: python generate_talk.py
# """
# import os
# import json

# # (页码, 主题, [(英文句, 中文句), ...])
# pages = [
#     (1, "标题", [
#         ("Hi everyone.",
#          "大家好。"),
#         ("Today I'll walk you through one of the most talked-about papers from NVIDIA this year — OmniDreams.",
#          "今天，我将带大家了解英伟达今年最受热议的论文之一——OmniDreams。"),
#         ("The title is ambitious: a real-time, generative world model for closed-loop autonomous-vehicle simulation.",
#          "它的标题颇具野心：一个面向闭环自动驾驶仿真的实时生成式世界模型。"),
#         ("Three words carry the whole story — closed-loop, real-time, and generative.",
#          "三个词概括了整个故事——闭环、实时、生成式。"),
#         ("Let's unpack them, one by one.",
#          "让我们逐一拆解。"),
#     ]),

#     (2, "闭环仿真工作流", [
#         ("Let's begin with the core idea: what does closed-loop simulation actually mean?",
#          "先从核心概念说起：闭环仿真到底意味着什么？"),
#         ("The easiest way in is to look at its opposite — open-loop.",
#          "最简单的切入方式，是看看它的反面——开环。"),
#         ("Open-loop is like replaying a recording — the footage is fixed in advance.",
#          "开环就像回放一段录像——画面是预先固定好的。"),
#         ("So no matter what your policy decides, the world simply never reacts.",
#          "所以无论你的策略做出什么决定，世界都不会做出任何反应。"),
#         ("Closed-loop, by contrast, is genuine interaction.",
#          "相比之下，闭环是真正的交互。"),
#         ("On the left is the policy model, Alpamayo — and you could just as easily put a human here.",
#          "左边是策略模型 Alpamayo——这里同样可以换成一个人。"),
#         ("It outputs an action — steering, throttle, brake — and feeds it into the runtime, AlpaSim.",
#          "它输出一个动作——转向、油门、刹车——并送入运行时 AlpaSim。"),
#         ("AlpaSim updates the abstract state of the whole scene, then passes it to the world model, OmniDreams.",
#          "AlpaSim 更新整个场景的抽象状态，再交给世界模型 OmniDreams。"),
#         ("OmniDreams renders the next photorealistic frame and sends it right back to the policy.",
#          "OmniDreams 渲染出下一帧逼真画面，并立刻回传给策略。"),
#         ("The policy decides again — and round and round it goes.",
#          "策略再次做出决策——如此往复，循环不息。"),
#         ("The loop is closed.",
#          "闭环就此形成。"),
#         ("And this matters: only a closed loop reveals how a policy's small mistakes snowball over time.",
#          "这一点很关键：只有闭环，才能揭示策略的小失误如何随时间滚雪球般放大。"),
#     ]),

#     (3, "控制视频与训练数据", [
#         ("Any powerful world model stands on a mountain of data.",
#          "任何强大的世界模型，都建立在海量数据之上。"),
#         ("These four images reveal OmniDreams' input logic.",
#          "这四张图揭示了 OmniDreams 的输入逻辑。"),
#         ("Panels (a) and (c) are real camera views — front-wide and rear-tele.",
#          "图 (a) 和 (c) 是真实的相机视角——前视广角与后视长焦。"),
#         ("Panels (b) and (d) are their matching abstract states.",
#          "图 (b) 和 (d) 是与之对应的抽象状态。"),
#         ("Think of an abstract state as the game-engine blueprint: colored boxes for cars, thin lines for lanes.",
#          "可以把抽象状态想象成游戏引擎的蓝图：彩色方框代表车辆，细线代表车道。"),
#         ("The model's job is to take that crude sketch and imagine the photorealistic world on the right.",
#          "模型的任务，就是把这张粗糙的草图，想象成右侧那个逼真的世界。"),
#         ("Now the numbers — and they're striking.",
#          "再看数据——着实惊人。"),
#         ("Sixteen thousand six hundred raw driving hours, and nearly five thousand hours of curated, high-quality data.",
#          "一万六千六百小时的原始驾驶数据，以及近五千小时经过精选的高质量数据。"),
#         ("That's over 1.1 million clips, at 704 by 1280, across fifteen countries.",
#          "总计超过 110 万个片段，分辨率 704×1280，覆盖十五个国家。"),
#         ("Scale and diversity are what earn the name \"world model.\"",
#          "正是规模与多样性，才配得上“世界模型”这个名字。"),
#     ]),

#     (4, "条件与输入", [
#         ("So what exactly does OmniDreams take in, and what does it produce?",
#          "那么，OmniDreams 究竟接收什么、又产出什么呢？"),
#         ("On the left are its conditioning inputs.",
#          "左侧是它的条件输入。"),
#         ("First, a text prompt — weather, time of day, the high-level context.",
#          "第一，文本提示——天气、时段，以及高层语境。"),
#         ("Second, the next-step abstract state — that sketch again, and this is the core control signal.",
#          "第二，下一步的抽象状态——又是那张草图，这是核心的控制信号。"),
#         ("It's how a driving action turns into a picture.",
#          "正是它，把一个驾驶动作转化成一幅画面。"),
#         ("Third, a history cache — the last few frames, keeping everything temporally coherent.",
#          "第三，历史缓存——最近的若干帧，用以保持时间上的连贯。"),
#         ("In the middle, OmniDreams is, at heart, an autoregressive, causal video generator.",
#          "居中的 OmniDreams，本质上是一个自回归的因果视频生成器。"),
#         ("It fuses these conditions into the next photorealistic frame on the right.",
#          "它将这些条件融合，生成右侧下一帧逼真画面。"),
#         ("Now watch the dashed line at the bottom — this is the key.",
#          "现在看底部那条虚线——这是关键所在。"),
#         ("The frame it just made is fed back into the cache, becoming input for the next step.",
#          "它刚生成的这一帧会被送回缓存，成为下一步的输入。"),
#         ("Each frame feeds the next, so the world keeps dreaming forward, indefinitely.",
#          "每一帧喂给下一帧，于是这个世界不断向前“做梦”，永不停歇。"),
#         ("Only the first frame gets a real image, to anchor the scene.",
#          "只有第一帧使用真实图像，用来锚定整个场景。"),
#     ]),

#     (5, "多视角DiT架构", [
#         ("Let's zoom inside the model.",
#          "让我们深入模型内部。"),
#         ("OmniDreams uses a DiT — a diffusion transformer.",
#          "OmniDreams 采用 DiT——扩散 Transformer。"),
#         ("That's today's mainstream backbone for video generation.",
#          "这是当下视频生成的主流骨干网络。"),
#         ("But driving adds a twist: a car carries several cameras — front, rear, sides — and these views all have to agree with each other.",
#          "但自动驾驶带来一个难点：一辆车装有多个相机——前、后、侧——而这些视角必须彼此一致。"),
#         ("You can't have sunshine on the left and an overcast sky on the right.",
#          "你不能左边阳光明媚，右边却阴云密布。"),
#         ("NVIDIA's answer is the red dashed line here: cross-view attention.",
#          "英伟达的答案，就是这里的红色虚线：跨视角注意力。"),
#         ("It lets each view glance at the others while generating — guaranteeing multi-camera consistency.",
#          "它让每个视角在生成时都能瞥见其他视角——从而保证多相机的一致性。"),
#         ("Each DiT block actually runs three kinds of attention, each with a job.",
#          "每个 DiT 模块其实运行着三种注意力，各司其职。"),
#         ("Self-attention handles coherence within one view, across time.",
#          "自注意力负责单一视角内、跨时间的连贯。"),
#         ("Cross-attention absorbs the text condition.",
#          "交叉注意力负责吸收文本条件。"),
#         ("And cross-view attention ties the cameras together.",
#          "而跨视角注意力，则把各个相机绑在一起。"),
#         ("But the real star is that little staircase, top-right — the causal mask.",
#          "但真正的主角，是右上角那个小小的阶梯——因果掩码。"),
#         ("It lets each frame see only itself and the past — never the future.",
#          "它让每一帧只能看到自己和过去——永远看不到未来。"),
#     ]),

#     (6, "双向vs因果自回归", [
#         ("That tiny mask matters enormously.",
#          "这个小小的掩码，意义重大。"),
#         ("Here are the two paradigms, side by side — and this contrast is the key to the whole paper.",
#          "这里并列着两种范式——而这一对比，正是整篇论文的关键。"),
#         ("On the left, traditional bidirectional generation.",
#          "左边是传统的双向生成。"),
#         ("A five-second clip is denoised all at once, every frame attending to every other frame.",
#          "一段五秒的片段被一次性去噪，每一帧都关注其他所有帧。"),
#         ("The quality is excellent — but you wait minutes, and it simply can't interact.",
#          "质量很高——但你要等上几分钟，而且根本无法交互。"),
#         ("The future is baked in from the very start.",
#          "未来从一开始就被写死了。"),
#         ("On the right, causal, autoregressive generation.",
#          "右边是因果的自回归生成。"),
#         ("Like writing text, it emits frames left to right, each depending only on the past.",
#          "就像写文字一样，它从左到右逐帧生成，每一帧只依赖过去。"),
#         ("And here's the elegant part — it borrows the KV-cache from large language models.",
#          "精妙之处在于——它借用了大语言模型的 KV 缓存。"),
#         ("Everything computed for past frames is cached, never recomputed.",
#          "过去帧的所有计算都被缓存起来，绝不重复计算。"),
#         ("Add one-step or few-step denoising, and it finally runs in real time.",
#          "再配合单步或少步去噪，它终于能够实时运行。"),
#         ("And real-time speed is the hard prerequisite for closed-loop.",
#          "而实时的速度，正是闭环的硬性前提。"),
#         ("No speed, no loop.",
#          "没有速度，就没有闭环。"),
#     ]),

#     (7, "三阶段训练", [
#         ("Now, the heart of the paper.",
#          "现在，进入全文的核心。"),
#         ("Causal models have a notorious disease — error accumulation.",
#          "因果模型有个臭名昭著的顽疾——误差累积。"),
#         ("In training, the model is fed real, ground-truth history; that's called teacher forcing.",
#          "训练时，模型被喂入真实的历史帧，这叫作教师强制。"),
#         ("But at inference, it must feed on its own generated frames, which carry tiny flaws.",
#          "但推理时，它只能依赖自己生成的帧，而这些帧带着微小的瑕疵。"),
#         ("This train-test gap is exposure bias — and those flaws snowball.",
#          "这种训练与测试之间的鸿沟就是曝光偏差——而那些瑕疵会滚雪球般累积。"),
#         ("Within seconds, the picture drifts and collapses.",
#          "几秒之内，画面就会漂移、崩坏。"),
#         ("OmniDreams cures this with a three-stage pipeline.",
#          "OmniDreams 用一条三阶段流水线来根治它。"),
#         ("Stage A: the bidirectional teacher — easy to train, top quality, but slow and non-interactive.",
#          "阶段 A：双向教师模型——易于训练、质量顶尖，但速度慢、不可交互。"),
#         ("Stage B turns it causal, with two clever tricks.",
#          "阶段 B 用两个巧妙的技巧，把它变为因果模型。"),
#         ("First, Diffusion Forcing: give each frame its own noise level — past clean, future noisy.",
#          "其一，扩散强制：给每一帧各自的噪声水平——过去干净，未来含噪。"),
#         ("So the model naturally learns to predict the future from the past.",
#          "于是模型自然学会了从过去预测未来。"),
#         ("Second, Self Forcing: in training, let the model roll out and feed on its own imperfect frames.",
#          "其二，自强制：训练中让模型自行推演，并依赖它自己生成的不完美帧。"),
#         ("Exactly like inference — so it meets its own mistakes early, and learns to fix them, cutting error accumulation at the root.",
#          "这与推理时如出一辙——让它尽早直面自己的错误，学会纠正，从根源上斩断误差累积。"),
#         ("Stage C, DMD distillation: compress the slow teacher into the fast student, matching their output distributions.",
#          "阶段 C，DMD 蒸馏：把慢速教师压缩成快速学生，并对齐二者的输出分布。"),
#         ("The result — fast, stable, and high-quality at once.",
#          "结果就是——快速、稳定、高质量，三者兼得。"),
#     ]),

#     (8, "多卡推理性能", [
#         ("Great algorithms aren't enough — to hit real time, the engineering has to be ruthless.",
#          "光有好算法还不够——要做到实时，工程必须做到极致。"),
#         ("These two tables show OmniDreams measured on NVIDIA's GB300.",
#          "这两张表格展示了 OmniDreams 在英伟达 GB300 上的实测数据。"),
#         ("The top one is single-view.",
#          "上面这张是单视角。"),
#         ("The pipeline splits into four stages: scene encoding, the diffusion DiT, the RGB decoder, and the KV-cache update.",
#          "流水线分为四个阶段：场景编码、扩散 DiT、RGB 解码器，以及 KV 缓存更新。"),
#         ("From one GPU to eight, total latency falls from 118 milliseconds to 78.",
#          "从一块 GPU 到八块，总延迟从 118 毫秒降到 78 毫秒。"),
#         ("Effective frame rate climbs to 103 — comfortably past real time.",
#          "有效帧率攀升到 103——轻松越过实时门槛。"),
#         ("The bottom is the heavier four-view case.",
#          "下面这张是更重的四视角情形。"),
#         ("On one GPU it needs 1,289 milliseconds — basically unusable.",
#          "单块 GPU 需要 1289 毫秒——基本无法使用。"),
#         ("But with sixteen GPUs in parallel, that drops to 151 milliseconds — frame rate jumps from 12 to 105.",
#          "但十六块 GPU 并行后，延迟降到 151 毫秒——帧率从 12 跃升到 105。"),
#         ("Notice one clever choice: the KV-cache update runs on a separate thread, off the critical path.",
#          "注意一个巧妙的设计：KV 缓存更新跑在独立线程上，脱离关键路径。"),
#         ("This millisecond-level obsession turns \"real-time\" from a slogan into a fact.",
#          "正是这种对毫秒的执着，把“实时”从口号变成了事实。"),
#     ]),

#     (9, "端到端推理流水线", [
#         ("Now let's assemble every piece into the full end-to-end pipeline.",
#          "现在，把每个部件拼装成完整的端到端流水线。"),
#         ("The top row is the macro, three-way handshake.",
#          "上面一行是宏观的三方握手。"),
#         ("AlpaSim holds the scene state and agents, and emits N abstract states.",
#          "AlpaSim 维护场景状态与各个智能体，并输出 N 个抽象状态。"),
#         ("The Video Model Server, running OmniDreams, turns abstract states, text, and a first frame into photorealistic video.",
#          "运行 OmniDreams 的视频模型服务器，把抽象状态、文本和首帧转化为逼真视频。"),
#         ("Those frames go to Alpamayo — or a human — who returns an N-frame trajectory to AlpaSim.",
#          "这些帧送给 Alpamayo——或一个人——再由其向 AlpaSim 回传一条 N 帧的轨迹。"),
#         ("The bottom row zooms into OmniDreams itself.",
#          "下面一行，则放大到 OmniDreams 自身。"),
#         ("On the far left, initialization: text and the first frame warm up the DiT caches.",
#          "最左侧是初始化：用文本和首帧预热 DiT 的缓存。"),
#         ("And that happens just once, before the very first rollout.",
#          "这一步只发生一次，在最初的推演之前。"),
#         ("After that it's rollout after rollout: states encoded, run through the DiT, decoded to RGB, cache updated.",
#          "此后便是一轮接一轮的推演：状态编码、经过 DiT、解码为 RGB、更新缓存。"),
#         ("And that cache is handed along the arrow to the next rollout.",
#          "而这份缓存，会沿着箭头传递给下一轮推演。"),
#         ("That continually-forwarded cache is what stitches separate chunks into one endless world.",
#          "正是这份不断前传的缓存，把一个个独立片段缝合成一个无尽的世界。"),
#     ]),

#     (10, "训练阶段对比", [
#         ("Does all this training actually pay off?",
#          "这么多训练，真的值得吗？"),
#         ("This page answers with hard numbers.",
#          "这一页用硬数据给出回答。"),
#         ("The top table compares the three stages — and here's the counterintuitive part.",
#          "上面的表格对比了三个阶段——而反直觉之处就在这里。"),
#         ("The middle row — pure causal, multi-step Diffusion Forcing — is the worst, red X's almost everywhere.",
#          "中间一行——纯因果、多步扩散强制——表现最差，几乎满是红叉。"),
#         ("That confirms something key: going causal without the right tricks actually hurts.",
#          "这印证了一个关键点：没有正确的技巧，贸然转向因果反而有害。"),
#         ("But the bottom row — after Self Forcing and distillation — sweeps the gold medals.",
#          "但最下面一行——经过自强制与蒸馏之后——几乎包揽了所有金牌。"),
#         ("Its FVD is 24.8, beating even the slow bidirectional teacher at 26.8.",
#          "它的 FVD 为 24.8，甚至超过了慢速双向教师的 26.8。"),
#         ("Faster and better — you really can have both.",
#          "更快又更好——你真的可以兼得。"),
#         ("And these metrics deserve a word.",
#          "这些指标也值得说一说。"),
#         ("FVD measures raw generation quality.",
#          "FVD 衡量的是原始的生成质量。"),
#         ("The LET scores are longitudinal-error-tolerant 3D vehicle detection; F1 judges lane lines.",
#          "LET 分数对应纵向误差容忍的三维车辆检测；F1 则评判车道线。"),
#         ("So the frames aren't just pretty — downstream perception models can genuinely read them.",
#          "所以这些画面不只是好看——下游的感知模型真的能读懂它们。"),
#         ("The little table at the bottom is the real insight.",
#          "底部那张小表，才是真正的洞见。"),
#         ("A progressive long-context teacher, tested on clips up to twenty seconds, slashes error versus a short-context one.",
#          "一个渐进式的长上下文教师，在长达二十秒的片段上测试，相比短上下文者大幅削减了误差。"),
#         ("The lesson: to keep a long dream from drifting, how far your teacher can see is decisive.",
#          "教训是：要让一场长梦不漂移，教师能看多远，起着决定性作用。"),
#     ]),

#     (11, "重建伪影修正", [
#         ("The next few pages are my favorite — what can this world model actually do?",
#          "接下来几页是我最喜欢的——这个世界模型究竟能做什么？"),
#         ("First, reconstruction artifact correction.",
#          "第一，重建伪影修正。"),
#         ("The top row is input; the bottom is output.",
#          "上面一行是输入，下面一行是输出。"),
#         ("See the warping, blur, and ghosting up top?",
#          "看到上面的扭曲、模糊和重影了吗？"),
#         ("In the output, it's all cleaned up.",
#          "在输出里，这些全被清理干净了。"),
#         ("The trick is the pipeline below.",
#          "诀窍就在下方的流水线。"),
#         ("Start from real, multi-view video and build a 3DGS — a Gaussian-splatting reconstruction.",
#          "从真实的多视角视频出发，构建一个 3DGS——高斯泼溅重建。"),
#         ("Render it from new viewpoints, deliberately producing degraded images full of artifacts.",
#          "从新视角渲染它，故意产生满是伪影的退化图像。"),
#         ("Pair each degraded image with its clean original, and train Cosmos on those pairs.",
#          "把每张退化图像与它干净的原图配对，用这些数据对训练 Cosmos。"),
#         ("The model learns one thing: map dirty frames back to clean, realistic ones.",
#          "模型学会的只有一件事：把脏帧映射回干净、逼真的画面。"),
#         ("And this hints at a deeper logic — generation can patch the holes reconstruction leaves behind.",
#          "这暗示了一个更深的逻辑——生成可以填补重建留下的空洞。"),
#         ("Two roads that usually compete, here shake hands.",
#          "两条通常相互竞争的路，在这里握手言和。"),
#     ]),

#     (12, "可控场景编辑", [
#         ("Second capability: controllable scenario editing.",
#          "第二项能力：可控的场景编辑。"),
#         ("Same road, same trajectory — but we can rewrite the world at will.",
#          "同样的道路，同样的轨迹——但我们可以随心所欲地改写这个世界。"),
#         ("Row one is the original scene.",
#          "第一行是原始场景。"),
#         ("Row two drops in a pedestrian crossing the street.",
#          "第二行加入了一个正在过马路的行人。"),
#         ("Row three buries the whole block in snow.",
#          "第三行把整个街区埋进了大雪。"),
#         ("Row four switches to night and scatters a line of traffic cones.",
#          "第四行切换到夜晚，并撒上一排交通锥。"),
#         ("For autonomous driving, this is huge.",
#          "对自动驾驶来说，这意义重大。"),
#         ("Rare, dangerous, long-tail events — snowstorms, a child darting out — barely show up in real data.",
#          "罕见、危险的长尾事件——暴风雪、突然窜出的孩子——在真实数据里几乎见不到。"),
#         ("Here, we manufacture them cheaply, at scale, to stress-test how a policy reacts.",
#          "而在这里，我们能低成本、大规模地制造它们，来压力测试策略的反应。"),
#     ]),

#     (13, "分布外物体建模", [
#         ("If a pedestrian or snow felt routine, this page shows off.",
#          "如果说行人或大雪还算寻常，这一页就要秀一秀真本事了。"),
#         ("Out-of-distribution object modeling.",
#          "分布外物体建模。"),
#         ("Up top, a triceratops strolls right down the middle of the road.",
#          "上方，一只三角龙正大摇大摆地走在马路中央。"),
#         ("Below, a giraffe takes its place.",
#          "下方，则换成了一只长颈鹿。"),
#         ("These things are simply not in any driving dataset.",
#          "这些东西，任何驾驶数据集里都根本没有。"),
#         ("Yet paste one into the first frame, and the model makes it walk plausibly across dozens of frames, blending into the scene — shadows, occlusion, motion and all.",
#          "可一旦把它贴进首帧，模型就能让它在数十帧里逼真地行走，融入场景——阴影、遮挡、运动，一应俱全。"),
#         ("Behind this is the world knowledge Cosmos absorbed from massive internet video.",
#          "这背后，是 Cosmos 从海量互联网视频中汲取的世界知识。"),
#         ("And this is the deepest edge of generation over reconstruction: it doesn't just replay what it saw.",
#          "这正是生成相对重建最深层的优势：它不只是回放看过的东西。"),
#         ("It understands what the world should look like — so it can create what it never saw.",
#          "它理解世界应有的样子——因此能创造出自己从未见过的东西。"),
#     ]),

#     (14, "闭环对比NuRec", [
#         ("Showmanship aside, simulation must answer one serious question: if you evaluate a policy inside your generated world, can you trust the verdict?",
#          "炫技归炫技，仿真必须回答一个严肃的问题：如果你在生成的世界里评估一个策略，那结论可信吗？"),
#         ("This page is the answer.",
#          "这一页就是答案。"),
#         ("Orange is NuRec, the established reconstruction-based simulator; green is OmniDreams.",
#          "橙色是 NuRec，那个成熟的、基于重建的仿真器；绿色是 OmniDreams。"),
#         ("Each group is a different policy; the y-axis is incident rate — collisions and off-road events.",
#          "每一组是一个不同的策略；纵轴是事故率——碰撞与驶离道路。"),
#         ("And the key result is simple: the orange and green bars are almost the same height.",
#          "关键结果很简单：橙色和绿色的柱子几乎一样高。"),
#         ("Whatever policy, whatever incident type, OmniDreams lines up tightly with mature NuRec.",
#          "无论哪种策略、哪类事故，OmniDreams 都与成熟的 NuRec 紧紧贴合。"),
#         ("That validates the headline: it can reliably replace reconstruction-based simulation for policy evaluation.",
#          "这验证了那句标题：它能在策略评估中可靠地替代基于重建的仿真。"),
#         ("Not a pretty toy — a trustworthy measuring stick.",
#          "它不是一个好看的玩具——而是一把值得信赖的标尺。"),
#     ]),

#     (15, "FVD偏离曲线", [
#         ("If the verdicts match, why bother switching to generative at all?",
#          "如果结论都一致，那又何必费劲改用生成式呢？"),
#         ("This page is OmniDreams' true trump card.",
#          "这一页，才是 OmniDreams 真正的王牌。"),
#         ("The x-axis is subtle but crucial: how far the simulated trajectory has drifted from the recorded path.",
#          "横轴微妙却关键：仿真轨迹偏离记录路径有多远。"),
#         ("In a closed loop, the moment a policy chooses differently, the car wanders further from the captured data.",
#          "在闭环里，策略一旦做出不同选择，车辆就会越来越远离采集到的数据。"),
#         ("On the left, where deviation is small, the two look comparable.",
#          "在左侧，偏离很小时，两者看起来不相上下。"),
#         ("But as deviation grows, in the gray zone, NuRec degrades sharply — its FVD rockets to 207.",
#          "但随着偏离增大，进入灰色区域，NuRec 急剧退化——它的 FVD 飙升到 207。"),
#         ("OmniDreams barely flinches, holding near 125 — an 82-point gap.",
#          "OmniDreams 却几乎不为所动，稳稳保持在 125 左右——足足相差 82 分。"),
#         ("This exposes reconstruction's fatal flaw: it's essentially replaying the exact region it scanned.",
#          "这暴露了重建的致命缺陷：它本质上只是在回放自己扫描过的那块区域。"),
#         ("Step outside that region, and it runs out of data and falls apart.",
#          "一旦踏出那块区域，它就无数据可用，随即崩溃。"),
#         ("Generation runs on imagination — wherever you drift, it can still paint a plausible world.",
#          "生成靠的是想象——无论你漂到哪里，它都能描绘出一个合理的世界。"),
#         ("And that is the fundamental reason a world model needs to exist.",
#          "而这，正是世界模型必须存在的根本理由。"),
#     ]),

#     (16, "定性对比", [
#         ("After the cold numbers, here's the intuition you can feel.",
#          "看完冰冷的数字，来点能直观感受的。"),
#         ("Same scene, same moments — NuRec on top, OmniDreams below.",
#          "相同的场景、相同的时刻——上面是 NuRec，下面是 OmniDreams。"),
#         ("Watch the genuinely hard parts: harsh sun glare, a pedestrian mid-crossing, fine detail far away.",
#          "注意那些真正困难的地方：刺眼的阳光、正在横穿的行人、远处的精细细节。"),
#         ("On strong light and moving objects, NuRec visibly smears and leaves ghosts.",
#          "面对强光和运动物体，NuRec 明显出现拖影和重影。"),
#         ("OmniDreams stays cleaner, steadier, and far more believable.",
#          "OmniDreams 则更干净、更稳定，也更可信得多。"),
#         ("Seeing is believing — and here, the gap really does speak for itself.",
#          "眼见为实——在这里，差距确实不言自明。"),
#     ]),

#     (17, "真人闭环驾驶", [
#         ("If it's truly real-time and closed-loop, what's the ultimate proof?",
#          "如果它真的既实时又闭环，那终极证明是什么？"),
#         ("Simple — put a human in the seat and let them drive.",
#          "很简单——让一个人坐进驾驶座，亲自来开。"),
#         ("Here, a researcher holds a real steering wheel, and the screen shows a world OmniDreams generates live — at fifty kilometers an hour.",
#          "这里，一位研究员握着真实的方向盘，屏幕上是 OmniDreams 实时生成的世界——时速五十公里。"),
#         ("They steer, they hit the throttle, and the scene responds in real time — no stutter, no lag.",
#          "他转动方向、踩下油门，画面实时响应——不卡顿，不延迟。"),
#         ("Letting someone drive it like a video game, with no sense of wrongness, is everything we've discussed, the causal design, the KV-cache, the distillation — all converging into one smooth, interactive moment.",
#          "能让人像玩电子游戏一样去驾驶、且毫无违和感，正是我们讨论过的一切——因果设计、KV 缓存、蒸馏——汇聚成这一个流畅而可交互的瞬间。"),
#     ]),

#     (18, "自己上手与总结", [
#         ("Finally, because the whole project is open-sourced, I ran it myself.",
#          "最后，因为整个项目都开源了，我亲自跑了一遍。"),
#         ("This is my own output from the code: a rainy night street, with vehicle boxes and lane lines overlaid — and honestly, it holds up impressively well.",
#          "这是我用代码跑出的结果：一条雨夜的街道，叠加着车辆框和车道线——说实话，效果好得令人惊喜。"),
#         ("Let's recap the essence in one breath.",
#          "让我们一口气回顾一下精髓。"),
#         ("On the Cosmos foundation, OmniDreams uses Diffusion Forcing, Self Forcing, and DMD distillation to turn a slow, offline video model into one that's fast, stable, and interactive — all at once.",
#          "在 Cosmos 的基础上，OmniDreams 用扩散强制、自强制和 DMD 蒸馏，把一个慢速、离线的视频模型，一举变得快速、稳定、可交互。"),
#         ("It can reliably stand in for reconstruction-based simulators in policy evaluation; it crushes them when trajectories deviate far; it can edit scenes and conjure the impossible; and it can even be flipped into a driving policy — a 2-billion-parameter model beating one five times its size.",
#          "它能在策略评估中可靠地替代基于重建的仿真器；在轨迹大幅偏离时把它们远远甩开；能编辑场景、变出不可能之物；甚至还能反过来变成一个驾驶策略——一个二十亿参数的模型，击败了体量五倍于它的对手。"),
#         ("To me, this points to a genuine shift in direction.",
#          "在我看来，这预示着一次真正的方向性转变。"),
#         ("Simulation may no longer reconstruct the world that already happened — but generate the world that could happen.",
#          "仿真或许不再是重建那个已经发生的世界——而是生成那个可能发生的世界。"),
#         ("Thank you all!",
#          "谢谢大家！"),
#     ]),
# ]


# def main():
#     out_dir = "assets/media/blog/script/talk"
#     os.makedirs(out_dir, exist_ok=True)

#     for num, topic, sents in pages:
#         sentences = [
#             {"en": " ".join(en.split()), "zh": " ".join(zh.split())}
#             for en, zh in sents
#         ]
#         data = {"page": num, "topic": topic, "sentences": sentences}
#         filename = f"{num:02d}_{topic}.json"
#         path = os.path.join(out_dir, filename)
#         with open(path, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#         en_chars = sum(len(s["en"]) for s in sentences)
#         zh_chars = sum(len(s["zh"]) for s in sentences)
#         print(f"已生成: {path}  ({len(sentences)} 句 / EN {en_chars} 字符 / ZH {zh_chars} 字)")

#     print(f"\n全部完成！共生成 {len(pages)} 个 JSON 文件，位于 ./{out_dir}/ 目录下。")
#     print("提示: talk2video.py 会优先读取 *.json；如目录里还残留旧的 *.txt，可一并删除以免混淆。")


# if __name__ == "__main__":
#     main()










# ------------------------------- ------------------------------- ------------------------------- ------------------------------- ------------------------------- -------------------------------




# # -*- coding: utf-8 -*-
# """
# 运行后在当前目录生成 talk/ 文件夹，内含 15 个 .json 文件。
# 每个文件是对应 PPT 页面的「逐句中英对照」讲稿，结构为:
#     {"page": 1, "topic": "标题",
#      "duration_sec": 41,
#      "sentences": [{"en": "...", "zh": "..."}, ...]}

# 设计要点:
#   * 以「句」为对齐单位 —— 同一份句子列表同时驱动 TTS 配音与字幕，
#     因此「英文语音 / 英文字幕 / 中文字幕」三者天然一一对应。
#   * 英文逐句即 PPT 旁白(驱动配音)，中文为对应翻译(驱动字幕)。
#   * duration_sec 为每页建议停留时长(秒)，按英文语速自动估算:
#     约 2.5 词/秒 + 每句 0.6 秒停顿，单句不少于 2 秒。
# 主题: One-Step Generative Models
#   1) Mean Flows for One-step Generative Modeling          (FID 3.43, 1-NFE)
#   2) Improved Mean Flows (iMF)                            (FID 1.72, 1-NFE)
#   3) Generative Modeling via Drifting                     (FID 1.54 / 1.61)
#   4) Representation Fréchet Loss (FD-loss)                (FID 0.72, 1-NFE)
# 直接运行: python generate_talk.py
# """
# import os
# import json

# # (页码, 主题, [(英文句, 中文句), ...])
# pages = [
#     (1, "标题-One-Step Generative Models", [
#         ("Hi everyone, welcome.",
#          "大家好，欢迎。"),
#         ("Today we're diving into one of the most exciting frontiers in generative AI — one-step generative models.",
#          "今天，我们要深入生成式 AI 最激动人心的前沿之一——一步生成模型。"),
#         ("Over the past year, a remarkable line of work, much of it from Kaiming He's group, has been chasing a single, audacious goal.",
#          "过去一年里，一系列出色的工作——其中很多来自何恺明团队——都在追逐同一个大胆的目标。"),
#         ("Can we generate a high-quality image in just one forward pass — one network evaluation — instead of the hundreds that diffusion models need?",
#          "我们能否只用一次前向、一次网络推理，就生成一张高质量图像，而不是扩散模型所需的成百上千次？"),
#         ("We'll walk through four papers that, together, tell a beautiful story of how this idea evolved.",
#          "我们会串讲四篇论文，它们合在一起，讲述了这个想法演进的精彩故事。"),
#         ("MeanFlow, Improved MeanFlow, Generative Modeling via Drifting, and finally the Representation Fréchet Loss.",
#          "MeanFlow、改进版 MeanFlow、基于漂移的生成建模，以及最后的表示空间 Fréchet 损失。"),
#         ("Let's get started.",
#          "我们开始吧。"),
#     ]),

#     (2, "目录与路线图", [
#         ("Here's our roadmap for today.",
#          "这是今天的路线图。"),
#         ("We'll start with the heart of MeanFlow — the distinction between instantaneous and average velocity.",
#          "我们先从 MeanFlow 的核心讲起——瞬时速度与平均速度的区别。"),
#         ("Then the MeanFlow identity, the elegant equation that makes the whole thing trainable.",
#          "接着是 MeanFlow 恒等式，正是这个优雅的等式让整套方法变得可训练。"),
#         ("Next, the Jacobian-vector product, or JVP, which turns that identity into something a GPU can compute efficiently.",
#          "然后是雅可比-向量积，也就是 JVP，它把这个恒等式变成 GPU 能高效计算的东西。"),
#         ("From there we move to Improved MeanFlow, which quietly fixes a subtle flaw in the original objective.",
#          "由此我们转到改进版 MeanFlow，它悄悄修复了原始目标里一个微妙的缺陷。"),
#         ("And we'll finish with the boldest idea of all — Generative Modeling via Drifting — plus a bonus on turning FID itself into a loss.",
#          "最后，我们以最大胆的想法收尾——基于漂移的生成建模，再加一个彩蛋：把 FID 本身变成损失函数。"),
#         ("Think of these as four steps up a ladder, each one getting us closer to perfect one-step generation.",
#          "可以把它们看作一架梯子的四级台阶，每一级都让我们更接近完美的一步生成。"),
#     ]),

#     (3, "背景-扩散、流匹配与一致性模型", [
#         ("Before we get to the new ideas, let's set the stage.",
#          "在进入新想法之前，先把背景铺垫好。"),
#         ("Generative modeling has gone through several eras.",
#          "生成建模经历了几个时代。"),
#         ("GANs and VAEs were fast — one shot, one image — but notoriously hard to train, prone to mode collapse and limited diversity.",
#          "GAN 和 VAE 很快——一步出图——但出了名地难训练，容易模式坍塌，多样性也受限。"),
#         ("Autoregressive models predict token by token; powerful in theory, but painfully slow at high resolution.",
#          "自回归模型逐 token 预测，理论上限很高，但在高分辨率下慢得让人心疼。"),
#         ("Then came diffusion and flow matching, which define a smooth, continuous process from noise to data, governed by an ordinary differential equation.",
#          "随后是扩散与流匹配，它们用一个常微分方程，定义了从噪声到数据的平滑连续过程。"),
#         ("The core idea is elegant: picture a particle flowing through a velocity field v-t. Generation is just solving dX equals v-t of X, dt — riding that flow from noise to a real image.",
#          "核心思想很优雅：想象一个粒子在速度场 v_t 中流动。生成无非就是求解 dX = v_t(X) dt——顺着这股流，从噪声漂到真实图像。"),
#         ("These models give us stunning quality and stable training. That's why they took over the field.",
#          "这类模型带来了惊艳的质量和稳定的训练，这也是它们统治这个领域的原因。"),
#         ("But there's a catch — the bottleneck on the right: numerical integration.",
#          "但有个代价——右边的瓶颈：数值积分。"),
#         ("To follow the curved path accurately, you must take tiny steps. Like navigating a winding road, you can't just stare at the start and end — you have to keep correcting your direction.",
#          "为了精确地跟住弯曲的轨迹，步长必须很小。就像走一条蜿蜒的山路，你不能只盯着起点和终点，而要时刻修正方向。"),
#         ("And every single step is one full network evaluation. Generating one image can take hundreds of them.",
#          "而每走一步，就是一次完整的网络推理。生成一张图，可能要算上几百次。"),
#         ("So the entire quest of today's talk is this: how do we collapse those hundreds of steps into just one?",
#          "所以今天整场分享的追求就是：我们如何把这几百步，压缩成区区一步？"),
#     ]),

#     (4, "MeanFlow-平均速度场长什么样", [
#         ("Here's the central character of MeanFlow — the average velocity field, written u of z, r, t.",
#          "这位是 MeanFlow 的主角——平均速度场，记作 u(z, r, t)。"),
#         ("Let's read this figure carefully, because it captures the whole intuition.",
#          "我们仔细读一下这张图，因为它浓缩了全部的直觉。"),
#         ("On the left, the purple arrows are the instantaneous velocity v — always tangent to the curved path, telling you which way you're heading right now.",
#          "左边那些紫色箭头是瞬时速度 v——它们始终与曲线相切，告诉你此刻正朝哪个方向走。"),
#         ("But the orange arrow, u, points differently. It points straight from the start point r to the end point t.",
#          "但橙色的箭头 u 指向不同。它从起点 r 笔直指向终点 t。"),
#         ("That's the average velocity — total displacement divided by elapsed time — the direct, as-the-crow-flies direction.",
#          "这就是平均速度——总位移除以经过的时间——那条最直接的、笔直飞过去的方向。"),
#         ("And the key relation: the displacement itself is exactly (t minus r) times u.",
#          "关键关系是：位移本身恰好等于 (t − r) 乘以 u。"),
#         ("The three plots on the right show this field changes with where you're going — it's conditioned on both the start time r and the end time t.",
#          "右边三幅图说明，这个场会随你要去的地方而变化——它同时以起点时间 r 和终点时间 t 为条件。"),
#         ("Why does this matter? Because if a network knows the average velocity directly, it can jump from noise to data in a single straight shot — no integration needed.",
#          "这为什么重要？因为如果网络直接知道平均速度，它就能从噪声到数据一步直达——无需任何积分。"),
#         ("That one idea is exactly what makes one-step generation possible.",
#          "正是这一个想法，让一步生成成为可能。"),
#     ]),

#     (5, "MeanFlow-瞬时速度 vs 平均速度", [
#         ("Now let's sharpen the core tension.",
#          "现在，我们把这个核心矛盾说透。"),
#         ("In flow matching, there are two quantities we care about.",
#          "在流匹配里，我们关心两个量。"),
#         ("First, the instantaneous velocity v — the tangent direction at the current moment. Crucially, it's easy to get; it's our known ground truth.",
#          "第一个是瞬时速度 v——当前时刻的切线方向。关键是它很容易得到，是我们已知的真值。"),
#         ("Second, the average velocity u, from r to t — the straight-line speed connecting start and end. This is what MeanFlow actually wants to learn.",
#          "第二个是平均速度 u，从 r 到 t——连接起点和终点的那条直线速度。这才是 MeanFlow 真正想学的目标。"),
#         ("In the picture, red is the instantaneous velocity, the tangent; blue is the average velocity, the chord. And as the endpoint t moves, that blue line keeps changing.",
#          "图中红色是瞬时速度，是切线；蓝色是平均速度，是割线。而随着终点 t 移动，这条蓝线也会不断变化。"),
#         ("So here's the dilemma.",
#          "于是两难就来了。"),
#         ("During training, all we know is how the car drives moment to moment — that's v.",
#          "训练时，我们只知道车每一刻怎么开——那就是 v。"),
#         ("But we want our network, a DiT or a U-Net, to learn the straight flight path, u, so it can teleport in one step.",
#          "但我们想让网络，比如 DiT 或 U-Net，学会那条笔直的飞行路线 u，好让它一步瞬移到位。"),
#         ("The problem? Computing u directly means integrating v along the entire path — running the whole route every time. Far too slow.",
#          "问题在哪？直接算 u 意味着要沿整条路径对 v 积分——每次都把整条路重跑一遍，太慢了。"),
#         ("So we need a clever shortcut. And that shortcut is the MeanFlow identity.",
#          "所以我们需要一条巧妙的捷径。而这条捷径，就是 MeanFlow 恒等式。"),
#     ]),

#     (6, "MeanFlow-MeanFlow 恒等式", [
#         ("This is the cornerstone of the whole paper — the MeanFlow identity. And the beauty is, it comes entirely from the definition. No new assumptions.",
#          "这是整篇论文的基石——MeanFlow 恒等式。它的美妙之处在于，它完全源自定义本身，没有任何额外假设。"),
#         ("Start with the definition: average velocity u is the integral of v from r to t, divided by the interval (t minus r).",
#          "从定义出发：平均速度 u 等于 v 从 r 到 t 的积分，再除以时间间隔 (t − r)。"),
#         ("Step one — a small trick. Multiply both sides by (t minus r). Now the left side is the displacement, and the right side is just the raw integral of v.",
#          "第一步，一个小技巧：两边同乘 (t − r)。这样左边就是位移，右边只剩下 v 的原始积分。"),
#         ("Step two — and this is the magic — differentiate both sides with respect to the end time t.",
#          "第二步，也是最神奇的一步——对等式两边关于终点时间 t 求导。"),
#         ("On the left, the product rule gives the derivative of (t minus r) times u — that's u, plus (t minus r) times du-dt.",
#          "左边用乘法法则，对 (t − r) 乘 u 求导，得到 u 加上 (t − r) 乘 du/dt。"),
#         ("On the right, the fundamental theorem of calculus collapses the integral to a single point — it's simply v at z-t and t.",
#          "右边由微积分基本定理，积分塌缩成一个点——就是 v 在 z_t 和 t 处的取值。"),
#         ("Setting the two sides equal gives: u plus (t minus r) du-dt equals v.",
#          "令两边相等，得到：u 加上 (t − r) du/dt 等于 v。"),
#         ("Rearrange, and we arrive at the identity: u equals v, minus (t minus r) times the time derivative of u.",
#          "移项整理，就得到了恒等式：u 等于 v，减去 (t − r) 乘以 u 对时间的导数。"),
#         ("In plain words: the average velocity equals the instantaneous velocity, minus a correction term that captures how things change over time.",
#          "用大白话说：平均速度等于瞬时速度，再减去一个修正项，这个修正项刻画了随时间发生的变化。"),
#         ("This is gorgeous. We've turned an intractable integral into a clean, local, differential relationship — something a network can actually be trained on.",
#          "这太漂亮了。我们把一个无从下手的积分，变成了一个干净、局部的微分关系——一个网络真正可以拿来训练的东西。"),
#     ]),

#     (7, "MeanFlow-JVP 雅可比-向量积", [
#         ("There's still one hurdle. That time derivative, du-dt, is a total derivative — how do we compute it efficiently?",
#          "还剩一道坎。那个时间导数 du/dt 是一个全导数——我们怎么高效地算它？"),
#         ("Remember, u depends on three things: the position z, the start time r, and the end time t.",
#          "记住，u 依赖三个变量：位置 z、起点时间 r、终点时间 t。"),
#         ("So by the chain rule, du-dt expands into three terms — how u changes with each variable, times how each variable changes with time.",
#          "于是由链式法则，du/dt 展开成三项——u 对每个变量的变化，乘以每个变量随时间的变化。"),
#         ("Now plug in what we know. The position changes at the instantaneous velocity, so dz-dt is v. The start time r is fixed, so dr-dt is zero. And dt-dt is trivially one.",
#          "现在代入已知条件。位置的变化率就是瞬时速度，所以 dz/dt 是 v；起点时间 r 是固定的，所以 dr/dt 是零；而 dt/dt 自然是一。"),
#         ("Everything simplifies beautifully: du-dt equals the partial of u in z, times v, plus the partial of u in t.",
#          "一切便优美地化简了：du/dt 等于 u 对 z 的偏导乘以 v，再加上 u 对 t 的偏导。"),
#         ("And here's the punchline for anyone who's coded this up — this expression is exactly a Jacobian-vector product.",
#          "对任何动手写过代码的人来说，重点来了——这个表达式，恰好就是一个雅可比-向量积。"),
#         ("It's the Jacobian of u — its partials with respect to z, r, and t — multiplied by the tangent vector (v, 0, 1).",
#          "它就是 u 的雅可比矩阵——也就是它对 z、r、t 的偏导——乘以切向量 (v, 0, 1)。"),
#         ("Frameworks like PyTorch and JAX compute this in a single efficient pass. You just say: differentiate along the direction (v, 0, 1), and it hands you du-dt directly.",
#          "PyTorch 和 JAX 这样的框架，能用一次高效的前向把它算出来。你只要说一句：沿着 (v, 0, 1) 这个方向求导，它就直接把 du/dt 交给你。"),
#         ("No finite differences, no explicit integration. This is the engineering insight that makes MeanFlow practical.",
#          "不用有限差分，不用显式积分。正是这个工程洞见，让 MeanFlow 真正落地可用。"),
#     ]),

#     (8, "MeanFlow-训练目标与 Stop-Gradient", [
#         ("Now we can build the training objective. From the identity, we construct an ideal target for u.",
#          "现在可以构造训练目标了。基于恒等式，我们为 u 构造一个理想的回归目标。"),
#         ("The target is simply v, minus (t minus r) times that JVP we just computed — which is precisely du-dt.",
#          "这个目标就是 v，减去 (t − r) 乘以我们刚算出的那个 JVP——而它正是 du/dt。"),
#         ("The loss is then a plain regression: push the network's prediction u-theta toward this target, in squared L2.",
#          "损失于是就是一个朴素的回归：用平方 L2，把网络的预测 u_theta 推向这个目标。"),
#         ("But notice one subtle thing wrapped around the target — s-g, stop-gradient. Why is it there?",
#          "但请注意目标外面包了一层微妙的东西——sg，也就是停止梯度。它为什么在那？"),
#         ("The target itself contains the network's own derivative. If we let gradients flow through it, computing the loss gradient would mean differentiating a derivative — a second-order term, what people call double backprop.",
#          "因为目标本身就含有网络自己的导数。如果让梯度穿过它，那么求损失梯度时，就要对一个导数再求导——这是个二阶项，也就是人们说的二次反向传播。"),
#         ("That's expensive and unstable. Stop-gradient cuts that path, keeping the whole thing a clean, first-order optimization.",
#          "那既昂贵又不稳定。停止梯度切断了这条路径，让整个训练保持为干净的一阶优化。"),
#         ("And here's the reassuring part. Even though we're bootstrapping — using the network to define its own target — the paper proves that if the loss reaches zero, the network must satisfy the MeanFlow identity.",
#          "而最让人安心的一点是：尽管我们在做自举——用网络去定义它自己的目标——论文证明了，只要损失降到零，网络就必然满足 MeanFlow 恒等式。"),
#         ("And satisfying the identity means it has recovered the true average velocity. The math closes the loop.",
#          "而满足恒等式，就意味着它还原了真正的平均速度。整个数学逻辑自洽闭环。"),
#     ]),

#     (9, "MeanFlow-训练伪代码", [
#         ("Here's the entire training algorithm — and it's remarkably short.",
#          "这就是完整的训练算法——短得惊人。"),
#         ("First, sample two timesteps, t and r, and draw Gaussian noise e.",
#          "首先，采样两个时间步 t 和 r，并抽取高斯噪声 e。"),
#         ("Build the interpolation point z — a linear blend of the clean data x and the noise e. This is the standard flow-matching path.",
#          "构造插值点 z——干净数据 x 与噪声 e 的线性混合。这就是标准的流匹配路径。"),
#         ("The conditional velocity along that path is simply v equals e minus x.",
#          "沿这条路径的条件速度，就是 v 等于 e 减 x。"),
#         ("Then the one line that does the heavy lifting — a single jvp call gives you both the network's output u and its time derivative dudt, along the direction (v, 0, 1).",
#          "接着是挑大梁的那一行——一次 jvp 调用，沿 (v, 0, 1) 方向，同时给出网络输出 u 和它的时间导数 dudt。"),
#         ("Construct the target — v minus (t minus r) times dudt — and wrap it in stop-gradient.",
#          "构造目标——v 减去 (t − r) 乘 dudt——再用停止梯度包住它。"),
#         ("The error is the prediction minus that frozen target, and the loss is just a norm of the error.",
#          "误差就是预测减去这个冻结的目标，而损失只是误差的一个范数。"),
#         ("That's it. No ODE solver, no noise schedule tuning, no teacher model. A handful of lines, trained from scratch.",
#          "就这些。没有 ODE 求解器，没有噪声调度调参，没有教师模型。寥寥几行，从零训练。"),
#         ("Turning a deep theoretical identity into eight lines of code — that elegance is the hallmark of really good research.",
#          "把一个深刻的理论恒等式，化成八行代码——这种优雅，正是顶级研究的标志。"),
#     ]),

#     (10, "MeanFlow-实验与消融", [
#         ("Let's look at what actually matters, through the ablations. These are all 1-NFE results on ImageNet.",
#          "我们通过消融实验，看看到底什么才是关键。这些都是 ImageNet 上的一步生成结果。"),
#         ("Table (a) is the most telling. If you never sample r different from t — that's zero percent — you collapse back to plain flow matching, and the one-step FID is a disastrous 328.",
#          "表 (a) 最说明问题。如果你从不让 r 不等于 t——也就是 0%——就退化回了普通的流匹配，一步生成的 FID 高达灾难性的 328。"),
#         ("Just mixing in 25 percent of cases where r and t differ drops it to 61. That's the average-velocity signal kicking in.",
#          "只要混入 25% 的 r 不等于 t 的情形，FID 就降到 61。这正是平均速度信号开始起作用了。"),
#         ("Table (b) validates the theory directly. The correct JVP tangent, (v, 0, 1), gives the best result. Every wrong tangent fails badly.",
#          "表 (b) 直接验证了理论。正确的 JVP 切向量 (v, 0, 1) 给出最好的结果；任何错误的切向量都崩得很惨。"),
#         ("So this isn't a tuning trick — the precise math is exactly what makes it work.",
#          "所以这并不是调参的小把戏——是那一步精确的数学，才让它真正奏效。"),
#         ("The other tables fine-tune the details — how to embed the two timesteps, how to sample them, the loss metric, and the guidance scale.",
#          "其余几张表则在打磨细节——如何嵌入两个时间步、如何采样它们、损失度量，以及引导强度。"),
#         ("Keep in mind these numbers are from a small model for ablation. Scaled up, the same recipe reaches the headline 3.43 FID — a 50 to 70 percent leap over the previous best one-step models.",
#          "记住，这些数字来自用于消融的小模型。一旦放大，同样的配方就能达到标志性的 3.43 FID——比此前最好的一步模型提升了 50% 到 70%。"),
#     ]),

#     (11, "MeanFlow-一步生成可视化", [
#         ("And here's the payoff — actual images.",
#          "而这就是回报——真实的生成图像。"),
#         ("Every one of these was generated in a single forward pass. One step. No iteration.",
#          "这里每一张，都是一次前向生成的。一步。没有任何迭代。"),
#         ("Parrots, chameleons, dogs, mushrooms, volcanoes, pizza — sharp, diverse, photorealistic.",
#          "鹦鹉、变色龙、狗、蘑菇、火山、披萨——清晰、多样、逼真。"),
#         ("This is MeanFlow-XL/2, hitting 3.43 FID on ImageNet 256 by 256.",
#          "这是 MeanFlow-XL/2，在 ImageNet 256×256 上达到 3.43 FID。"),
#         ("Just two years ago, quality like this in one step seemed almost impossible without a multi-step teacher to distill from.",
#          "就在两年前，不靠一个多步教师来蒸馏，想在一步里做到这种质量，几乎是不可想象的。"),
#         ("MeanFlow did it from scratch, with nothing but a clean mathematical identity. That's the power of getting the foundations right.",
#          "而 MeanFlow 从零做到了，凭借的只是一个干净的数学恒等式。这就是把根基做对的力量。"),
#     ]),

#     (12, "Improved MeanFlow-更干净的目标", [
#         ("Now to the sequel — Improved MeanFlow. The team went back and asked: what's still not quite right about the original?",
#          "接下来是续集——改进版 MeanFlow。团队回头追问：原始版本还有什么没做对的地方？"),
#         ("Both versions learn the same thing — the average velocity u. The difference is how they train it.",
#          "两个版本学的是同一样东西——平均速度 u。区别在于怎么去训练它。"),
#         ("Here's the subtle flaw they spotted. In the original, the regression target contains the network itself, and worse, it secretly depends on the conditional velocity, epsilon minus x.",
#          "他们发现的微妙缺陷是这样：原始版本的回归目标里含有网络自身，更糟的是，它还偷偷依赖于条件速度 ε 减 x。"),
#         ("Think about what that means — the function's input isn't just the noisy sample z. There's a hidden second input sneaking in, making it a non-standard, unstable regression.",
#          "想想这意味着什么——函数的输入不只是带噪样本 z，还偷偷溜进了第二个隐藏输入，这就让它变成了一个非标准、不稳定的回归。"),
#         ("Improved MeanFlow rewrites the whole thing as a clean v-loss — a standard regression onto the instantaneous velocity, where the only input is the legitimate one, z, giving a single-valued prediction.",
#          "改进版把整件事重写成一个干净的 v-loss——对瞬时速度做标准回归，唯一的输入就是合法的 z，给出单值的预测。"),
#         ("It also swaps the JVP tangent from the pair-specific conditional velocity to the network's own predicted marginal velocity — subtle, but it removes that hidden dependency.",
#          "它还把 JVP 的切向量，从依赖样本对的条件速度，换成网络自己预测的边际速度——很微妙，但正好除掉了那个隐藏依赖。"),
#         ("Then they rethought guidance. The original fixed the CFG scale during training. iMF makes the guidance scale — and even the interval — explicit conditioning variables, tunable at test time.",
#          "然后他们重新思考了引导。原始版本在训练时固定了 CFG 强度；iMF 把引导强度——甚至引导区间——都变成显式的条件变量，可在测试时自由调节。"),
#         ("And instead of squeezing all conditions through adaLN, they feed them as multiple tokens, in-context — which actually shrinks the model and improves quality.",
#          "而且，他们不再把所有条件都挤进 adaLN，而是把它们作为多个 token，以 in-context 的方式喂入——这反而缩小了模型、提升了质量。"),
#         ("The result? From scratch, no distillation, one step: 1.72 FID — a 50 percent improvement over the original. A small conceptual fix, a big payoff.",
#          "结果呢？从零训练、无需蒸馏、一步生成：1.72 FID——比原始版本提升了 50%。一个小小的概念修正，换来巨大的回报。"),
#     ]),

#     (13, "Drifting-把迭代搬到训练期", [
#         ("Now for the most radical idea of the four — Generative Modeling via Drifting.",
#          "现在轮到四篇中最激进的想法——基于漂移的生成建模。"),
#         ("All the previous methods still live in the world of flows and ODEs. Drifting throws that out entirely.",
#          "前面所有方法都还活在流与 ODE 的世界里。而漂移把它整个抛弃了。"),
#         ("Here's the conceptual leap. Every generative model does a pushforward — you push noise epsilon through a network f to get a generated distribution q. We want q to match the data distribution p.",
#          "概念上的飞跃在这里。每个生成模型都在做一次前推——把噪声 ε 推过网络 f，得到生成分布 q。我们希望 q 去匹配数据分布 p。"),
#         ("Diffusion does this iteratively at inference time, over many steps. Drifting asks: what if we move that iteration into training time instead?",
#          "扩散是在推理期、用很多步迭代地做这件事。漂移则反问：如果我们把这个迭代搬到训练期，会怎样？"),
#         ("The insight is that training is already iterative. Every SGD update nudges the samples a little — so let those updates be the steps that march the generated distribution toward the data.",
#          "洞见在于，训练本身就是迭代的。每次 SGD 更新都把样本轻轻推一下——那就让这些更新，成为推动生成分布走向数据的步伐。"),
#         ("Each sample drifts — the next position equals the current one, plus a drifting field V.",
#          "每个样本都在漂移——下一个位置等于当前位置，加上一个漂移场 V。"),
#         ("And now the elegant part — Proposition 3.1. The field is designed to be anti-symmetric: swapping the roles of p and q flips its sign.",
#          "优雅之处在于命题 3.1。这个场被设计成反对称的：交换 p 和 q 的角色，它就变号。"),
#         ("That single property gives a free guarantee. If the generated distribution ever equals the data distribution, the field must equal its own negative — which means it's exactly zero. Equilibrium. The samples stop moving.",
#          "仅凭这一条性质，就白送了一个保证。一旦生成分布等于数据分布，这个场就必须等于它自身的相反数——那就只能是零。平衡到达，样本停止移动。"),
#         ("The loss makes this concrete — the network's output should match a frozen target: the current sample plus its drift. Stop-gradient holds the target fixed, so we just keep nudging samples in the field's direction, until the field vanishes.",
#          "损失把这一切落到实处——网络输出要去匹配一个冻结的目标：当前样本加上它的漂移。停止梯度把目标固定住，于是我们只需不断沿着场的方向轻推样本，直到场归零。"),
#         ("No noise schedule, no ODE solver, no teacher. Just drift toward equilibrium.",
#          "没有噪声调度，没有 ODE 求解器，没有教师。只是朝着平衡漂移而去。"),
#     ]),

#     (14, "Drifting-吸引与排斥的漂移场", [
#         ("So what is this drifting field, concretely? It's beautifully physical — think attraction and repulsion.",
#          "那么这个漂移场具体是什么？它有种优美的物理感——想想吸引与排斥。"),
#         ("V-plus is the attraction. For a generated sample x, you look at the real data points around it — the positives — and get pulled toward them, weighted by how close they are.",
#          "V⁺ 是吸引。对一个生成样本 x，你看它周围的真实数据点——也就是正样本——被它们拉过去，权重取决于有多近。"),
#         ("V-minus is the repulsion. You look at other generated samples — the negatives — and get pushed away from them.",
#          "V⁻ 是排斥。你看其他生成样本——也就是负样本——被它们推开。"),
#         ("The full field is attraction minus repulsion. And combining the two naturally produces an anti-symmetric form — exactly the property we needed for equilibrium.",
#          "完整的场就是吸引减去排斥。而把两者合并起来，自然就得到一个反对称的形式——正是我们达成平衡所需要的那条性质。"),
#         ("The weighting uses a simple kernel — closer points matter more, controlled by a temperature tau.",
#          "权重用的是一个简单的核——越近的点越重要，由一个温度 τ 来控制。"),
#         ("If this feels familiar, it should — it's deeply related to contrastive learning. Data points are positives that attract; your own generations are negatives that repel.",
#          "如果你觉得似曾相识，那是对的——它与对比学习深度相关。数据点是吸引你的正样本；你自己的生成则是排斥你的负样本。"),
#         ("And that gives a wonderful side benefit — it's naturally robust to mode collapse. If your generator forgets a mode, real data there keeps pulling samples back. GANs struggle with exactly this.",
#          "这还带来一个绝妙的副产品——它天然抗模式坍塌。如果生成器漏掉了某个模式，那个区域的真实数据会不断把样本拉回来。而这恰恰是 GAN 的老大难。"),
#         ("One crucial detail, bottom-left — this all happens in a feature space, through an encoder phi, not raw pixels. In a semantic space, the direction from a generated cat to a real cat is actually meaningful.",
#          "左下角有个关键细节——这一切都发生在特征空间里，经过一个编码器 φ，而不是原始像素。在语义空间中，从一只生成的猫指向一只真实的猫，这个方向才真正有意义。"),
#         ("Put it together and you get state of the art — 1.54 FID in latent space, 1.61 in pixel space. One step, no teacher, no adversary.",
#          "把这些拼在一起，就得到了最优结果——隐空间 1.54 FID，像素空间 1.61。一步生成，没有教师，没有对抗。"),
#     ]),

#     (15, "FD-Loss-把评估指标变成损失", [
#         ("Let's end with a delightfully clever idea — turning the scoreboard into the game itself.",
#          "我们以一个妙到极致的想法收尾——把记分牌本身，变成比赛。"),
#         ("For almost a decade, FID — the Fréchet Distance in Inception space — has been the metric everyone optimizes for, indirectly. The whole field has been doing gradient descent on this one number, by hand.",
#          "近十年来，FID——也就是 Inception 空间里的 Fréchet 距离——一直是所有人间接优化的指标。整个领域，都在对这一个数字手动做梯度下降。"),
#         ("So the obvious question — why not just train on it directly? Every term in FID is differentiable.",
#          "于是有个显而易见的问题——为什么不干脆直接拿它来训练？FID 里的每一项都是可微的。"),
#         ("The reason no one did — FID needs a huge population, say 50,000 samples, to estimate the distribution's mean and covariance. Backpropagating through all of them, every step, is hopeless.",
#          "没人这么做的原因是——FID 需要一个庞大的总体，比如 5 万个样本，才能估出分布的均值和协方差。每一步都对它们全部反向传播，根本不现实。"),
#         ("The fix is wonderfully simple — decouple the two numbers. Use a large population, 50k, to estimate the statistics, accumulated cheaply through a queue or an EMA. But only backpropagate through one small batch, about a thousand samples.",
#          "解法妙在简单——把这两个数解耦。用一个大总体，5 万，来估计统计量，通过队列或 EMA 廉价地累积。但只对一个小批次、大约一千个样本做反向传播。"),
#         ("Look at the algorithm — generate a batch, extract features, update the running mean and second moment with EMA, compute the Fréchet Distance against the real statistics, and step. Large population, cheap gradient.",
#          "看这个算法——生成一批样本，提取特征，用 EMA 更新滑动均值和二阶矩，与真实统计量算出 Fréchet 距离，然后更新一步。总体很大，梯度却很便宜。"),
#         ("The chef cooks a few dishes at a time, but the critic tastes the whole menu before giving feedback.",
#          "厨师一次只做几道菜，但评论家要尝遍整桌菜，才给出反馈。"),
#         ("The results are striking. In Inception space, a one-step generator hits 0.72 FID. And the same loss repurposes a multi-step model into a one-step one — no distillation, no adversarial training, no per-sample targets.",
#          "结果令人震撼。在 Inception 空间里，一步生成器达到 0.72 FID。而同一个损失，还能把一个多步模型改造成一步模型——无需蒸馏、无需对抗训练、无需逐样本目标。"),
#         ("It even exposes a deeper truth — FID can misrank quality. Better representations sometimes give better images despite a worse Inception score, which is why they propose a multi-representation metric.",
#          "它甚至揭示了一个更深的真相——FID 会把质量排错序。更好的表示空间有时能给出更好的图像，哪怕 Inception 分数更差，这正是他们提出多表示指标的原因。"),
#         ("And that's the arc of our whole story — from rethinking velocity, to fixing the objective, to abandoning ODEs, to training on the metric itself. Four bold steps, each bringing genuine one-step generation closer to reality. Thank you.",
#          "这就是我们整个故事的弧线——从重新思考速度，到修正目标，到抛弃 ODE，再到直接对指标本身训练。四个大胆的步伐，每一步都让真正的一步生成，更接近现实。谢谢大家。"),
#     ]),
# ]


# def estimate_duration(sentences):
#     """按英文语速估算每页停留时长(秒): 约 2.5 词/秒 + 每句 0.6s 停顿，单句≥2s。"""
#     total = 0.0
#     for s in sentences:
#         words = len(s["en"].split())
#         total += max(2.0, words / 2.5 + 0.6)
#     return int(round(total))


# def main():
#     out_dir = "assets/media/blog/script/talk/"
#     os.makedirs(out_dir, exist_ok=True)

#     grand_total = 0
#     for num, topic, sents in pages:
#         sentences = [
#             {"en": " ".join(en.split()), "zh": " ".join(zh.split())}
#             for en, zh in sents
#         ]
#         duration = estimate_duration(sentences)
#         grand_total += duration
#         data = {
#             "page": num,
#             "topic": topic,
#             "duration_sec": duration,
#             "sentences": sentences,
#         }
#         filename = f"{num:02d}_{topic}.json"
#         path = os.path.join(out_dir, filename)
#         with open(path, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#         en_chars = sum(len(s["en"]) for s in sentences)
#         zh_chars = sum(len(s["zh"]) for s in sentences)
#         print(f"已生成: {path}  ({len(sentences)} 句 / 建议 {duration}s / EN {en_chars} 字符 / ZH {zh_chars} 字)")

#     mins, secs = divmod(grand_total, 60)
#     print(f"\n全部完成！共生成 {len(pages)} 个 JSON 文件，位于 ./{out_dir}/ 目录下。")
#     print(f"预计总时长约 {grand_total}s（约 {mins} 分 {secs} 秒）。")
#     print("提示: talk2video.py 会优先读取 *.json；如目录里还残留旧的 *.txt，可一并删除以免混淆。")


# if __name__ == "__main__":
#     main()


# ------------------------------- ------------------------------- ------------------------------- ------------------------------- ------------------------------- -------------------------------


# # -*- coding: utf-8 -*-
# """
# 生成自动驾驶全栈系统分享视频的中英双语逐句讲稿。

# 运行后在当前目录生成 talk/ 文件夹，内含 20 个 .json 文件。
# 每个文件是对应 PPT 页面的「逐句中英对照」讲稿，结构为:
#     {"page": 1, "topic": "标题",
#      "sentences": [{"en": "...", "zh": "..."}, ...]}

# 设计要点:
#   * 以「句」为对齐单位 —— 同一份句子列表同时驱动 TTS 配音与字幕，
#     因此「英文语音 / 英文字幕 / 中文字幕」三者天然一一对应。
#   * 讲稿与每页图示的模块、配色、数据流严格呼应(图文一致),
#     在解释本质原理的同时引入最新进展与底层逻辑思考。
# 直接运行: python generate_talk.py
# """
# import os
# import json

# # (页码, 主题, [(英文句, 中文句), ...])
# pages = [
#     (1, "标题-全栈自动驾驶系统架构", [
#         ("Hello everyone, and welcome.",
#          "大家好，欢迎观看。"),
#         ("In this talk, I'll walk you through a complete, full-stack autonomous driving system architecture — from the raw sensor photons all the way to the steering wheel.",
#          "在这次分享中，我将带大家走完一套完整的全栈自动驾驶系统架构——从最原始的传感器光子，一直到方向盘的转动。"),
#         ("This isn't a pile of isolated algorithms; it's a single, coherent machine that has to perceive, understand, predict, decide, and act — all within tens of milliseconds, and all without ever failing dangerously.",
#          "这并不是一堆孤立算法的拼凑，而是一台统一、连贯的机器，它必须在几十毫秒内完成感知、理解、预测、决策与执行，并且永远不能发生危险的失效。"),
#         ("My goal is that, by the end, you won't just know what each module does — you'll understand why the whole system is built this way.",
#          "我的目标是，看完之后，你不仅知道每个模块在做什么，更能理解整个系统为何如此设计。"),
#         ("Let's begin.",
#          "让我们开始吧。"),
#     ]),

#     (2, "目录-六大章节", [
#         ("Here's the roadmap for our journey, in six chapters.",
#          "这是我们旅程的路线图，共分为六章。"),
#         ("We start with the overall architecture and middleware — the skeleton and the nervous system of the whole vehicle.",
#          "我们从总体架构与中间件开始——它们是整车的骨架与神经系统。"),
#         ("Then multimodal sensor perception: how the car turns cameras and LiDAR into a 3D understanding of the world.",
#          "接着是多模态传感器感知：车辆如何把相机与激光雷达，转化为对世界的三维理解。"),
#         ("Third, scene understanding and static elements — lanes, road edges, and traffic rules woven into a map.",
#          "第三，场景理解与静态要素——把车道、路沿与交通规则，编织成一张地图。"),
#         ("Fourth, dynamic target modeling and high-precision positioning — knowing where everything is, and where we are, down to the centimeter.",
#          "第四，动态目标建模与高精定位——厘米级地知道万物在哪、我们在哪。"),
#         ("Fifth, the brain of driving: behavior prediction, decision making, and motion planning.",
#          "第五，驾驶的大脑：行为预测、决策与运动规划。"),
#         ("And finally, control execution, parking, and the data closed loop that lets the whole system keep improving.",
#          "最后是控制执行、泊车，以及让整个系统持续进化的数据闭环。"),
#         ("Notice the logic: this sequence mirrors the exact flow of information through a driving brain — sense, model, predict, plan, act, and learn.",
#          "请注意这个逻辑：这一顺序，恰好复刻了信息在一个驾驶大脑中流动的全过程——感知、建模、预测、规划、执行、再学习。"),
#     ]),

#     (3, "总体架构-双脑域控", [
#         ("Let's start with the single most important design decision in the entire system: the dual-brain domain controller.",
#          "我们先从整个系统中最重要的一个设计决策讲起：双脑域控制器。"),
#         ("On the left sits the APU — the intelligent driving domain, a high-performance AI SoC. On the right, the RPU — the safety and execution domain, certified to ASIL-D and running in lockstep.",
#          "左边是 APU——智能驾驶域，一颗高性能 AI 芯片；右边是 RPU——安全与执行域，达到 ASIL-D 认证，并以锁步方式运行。"),
#         ("Why split the brain in two? Here's the deep reason.",
#          "为什么要把大脑一分为二？这背后有一个深刻的原因。"),
#         ("Modern AI is powerful but statistical — it cannot be formally proven correct, and it can fail in surprising ways on rare inputs.",
#          "现代 AI 强大，但本质是统计性的——它无法被形式化地证明正确，面对罕见输入时还可能以意想不到的方式失效。"),
#         ("Yet braking and steering must never fail. So we physically isolate the un-provable intelligence from the provably-safe execution.",
#          "可刹车与转向绝不能失效。于是我们把“无法被证明的智能”与“可被证明安全的执行”，在物理上隔离开。"),
#         ("Follow the colors: blue is perception, green is planning, orange is safety and control, and gray is middleware and hardware.",
#          "跟着颜色看：蓝色是感知，绿色是规划，橙色是安全与控制，灰色是中间件与硬件。"),
#         ("The APU runs the full pipeline — sensing, fusion, environment model, localization, prediction, planning — then sends a safety control request across to the RPU.",
#          "APU 跑完整条流水线——感知、融合、环境模型、定位、预测、规划——再向 RPU 发出一个“安全控制请求”。"),
#         ("The RPU does the final handshake, actuator management, and post-processing, while feeding vehicle state back.",
#          "RPU 完成最后的握手、执行器管理与后处理，同时把车辆状态回传。"),
#         ("This is what engineers call a fail-operational design: even if the AI brain goes dark, the safety brain still brings the car to a controlled stop.",
#          "这就是工程师所说的“失效可运行”设计：即便 AI 大脑彻底宕机，安全大脑依然能把车辆安全地控制停下。"),
#     ]),

#     (4, "传感器输入层", [
#         ("Now, what does this car actually see? Let's look at the sensor layout.",
#          "那么，这台车究竟“看”到了什么？我们来看传感器的布局。"),
#         ("Around the vehicle are eleven cameras with deliberately different fields of view: a narrow thirty-degree front long-range camera to see far, a sixty-degree main camera, a one-hundred-twenty-degree wide camera, plus wing and rear cameras, and four nearly one-hundred-ninety-degree fisheyes for parking.",
#          "车身周围有十一颗相机，它们的视场角是刻意设计成不同的：一颗窄至三十度的前向长距相机用于看远，一颗六十度主相机，一颗一百二十度广角相机，外加侧翼与后向相机，以及四颗近一百九十度的鱼眼相机用于泊车。"),
#         ("Wrapping it all, a LiDAR provides a full three-hundred-sixty-degree point cloud.",
#          "在最外圈，一颗激光雷达提供完整的三百六十度点云。"),
#         ("Why so many different lenses? Because far-away objects need narrow, high-resolution vision, while close cut-ins need wide coverage — no single camera can do both.",
#          "为什么要用这么多不同的镜头？因为远处目标需要窄而高分辨率的视野，而近处的加塞则需要广阔的覆盖——没有任何一颗相机能同时做到。"),
#         ("But here's the clever engineering on the right: every physical camera is wrapped in a virtual camera abstraction that normalizes resolution, field of view, and frame rate.",
#          "但真正巧妙的工程在右侧：每一颗物理相机，都被一层“虚拟相机”抽象所封装，它把分辨率、视场角与帧率统一归一化。"),
#         ("Then comes time synchronization and calibration — solving for the intrinsics, the extrinsics, and the time offset between sensors.",
#          "之后是时间同步与标定——求解相机内参、外参，以及传感器之间的时间偏移。"),
#         ("The payoff is decoupling: the perception model no longer cares which exact camera shipped on which car. Swap the hardware, and the model still just works.",
#          "其回报是解耦：感知模型不再关心具体哪台车装了哪颗相机。更换硬件，模型依然照常工作。"),
#         ("That is how you scale one single algorithm across an entire, ever-changing vehicle fleet.",
#          "这正是把同一套算法，规模化部署到不断变化的整个车队的关键。"),
#     ]),

#     (5, "视觉BEV感知", [
#         ("With clean, synchronized images in hand, the first big perception trick is the Bird's-Eye-View transform.",
#          "有了干净、同步的图像后，感知的第一个重磅技巧，是鸟瞰视角（BEV）变换。"),
#         ("On the left, six surround-view images each pass through a CNN or Vision-Transformer backbone to extract multi-scale features.",
#          "左侧，六路环视图像各自通过一个 CNN 或视觉 Transformer 主干网络，提取多尺度特征。"),
#         ("Now the core idea: we lay down a grid of learnable BEV queries — one per cell of a top-down map — and let them ask the image features, through spatial cross-attention, 'what is at my location?'",
#          "接下来是核心思想：我们铺设一张由可学习的 BEV 查询组成的栅格——俯视地图的每个格子对应一个查询——再让它们通过空间交叉注意力去“询问”图像特征：“我这个位置上有什么？”"),
#         ("Here the BEV queries are the Q, and the multi-view image features are the keys and values.",
#          "这里，BEV 查询就是 Q，多视角图像特征则是键 K 和值 V。"),
#         ("A temporal self-attention then links the current frame to past frames, which is exactly what lets the network infer velocity and reason through brief occlusions.",
#          "随后的时间自注意力，把当前帧与历史帧关联起来——这正是网络得以推断速度、并在短暂遮挡中持续推理的关键。"),
#         ("This is the BEVFormer family of architectures, and it reshaped the whole industry.",
#          "这就是 BEVFormer 这一系列架构，它重塑了整个行业。"),
#         ("From the unified BEV space, three heads branch out: a static head for lanes, road edges, and the drivable path; a dynamic head for 3D boxes and velocities; and an occupancy head for dense semantic occupancy.",
#          "从统一的 BEV 空间，分出三个任务头：静态头预测车道、路沿与可行驶路径；动态头预测三维框与速度；占用头则预测稠密的语义占用。"),
#         ("The essence is profound: we've turned a confusing pile of perspective images into a single, metric, God's-eye map — the natural coordinate system in which all downstream planning actually happens.",
#          "其本质极为深刻：我们把一堆令人困惑的透视图像，转化成了一张统一、带尺度的“上帝视角”地图——而这，正是下游所有规划真正赖以工作的天然坐标系。"),
#     ]),

#     (6, "在线矢量化建图", [
#         ("Next, how does the car build a map of the road itself — in real time, without a pre-built HD map?",
#          "接下来，车辆如何为道路本身建图——而且是实时的，不依赖预先制作的高精地图？"),
#         ("We feed the BEV feature pyramid into a map decoder driven by hierarchical queries: instance queries, one per map element like a lane, and point queries, several points that trace out each element's shape.",
#          "我们把 BEV 特征金字塔送入一个由分层查询驱动的地图解码器：实例查询，每个对应一个地图元素，比如一条车道；点查询，则用若干个点勾勒出每个元素的形状。"),
#         ("Through stacked cross-attention, self-attention, and feed-forward layers, these queries directly output vectorized polylines — not pixels, but clean geometric curves.",
#          "经过堆叠的交叉注意力、自注意力与前馈层，这些查询直接输出矢量化的折线——不是像素，而是干净的几何曲线。"),
#         ("This is the MapTR and StreamMapNet line of work: end-to-end online vectorized mapping.",
#          "这正是 MapTR、StreamMapNet 这一脉络的工作：端到端的在线矢量化建图。"),
#         ("But raw geometry isn't enough — you need topology: which lane leads into which, where lanes merge and split.",
#          "但仅有几何还不够——你需要拓扑：哪条车道接入哪条，车道在何处合流与分叉。"),
#         ("So a lightweight SD-map prior is injected, and a topology reasoning module enforces consistency, refines geometry, and assigns lane types and directions.",
#          "于是，一个轻量的 SD 地图先验被注入进来，再由拓扑推理模块强制一致性、细化几何，并赋予车道的类型与方向。"),
#         ("A temporal tracker stabilizes lane identities and shapes across frames, so the map doesn't flicker.",
#          "一个时序跟踪器，在帧与帧之间稳定车道的身份与形状，让地图不会闪烁。"),
#         ("The deep shift here: the industry is moving away from expensive, hard-to-maintain offline HD maps toward 'maplessness' — letting the car draw its own fresh map every moment it drives.",
#          "这里深层的转变是：行业正在告别昂贵、难以维护的离线高精地图，走向“无图化”——让车辆在行驶的每一刻，都现场绘制属于自己的、最新鲜的地图。"),
#     ]),

#     (7, "占用网络", [
#         ("Now a question that keeps every perception engineer up at night: what about objects you've never seen before — a fallen ladder, an overturned truck, debris with no category?",
#          "现在来看一个让每个感知工程师夜不能寐的问题：那些你从未见过的物体怎么办——掉落的梯子、侧翻的卡车、没有类别的散落物？"),
#         ("Bounding boxes fail here, because a box assumes you already know what the object is.",
#          "包围框在这里会失效，因为画框的前提，是你已经知道那是什么物体。"),
#         ("The answer is the occupancy network. We lift multi-view features into 3D with voxel queries, run them through a 3D voxel encoder, and predict, for every little cube of space, whether it's occupied, what it is, and how it's moving.",
#          "答案是占用网络。我们用体素查询把多视角特征提升到三维，经过一个三维体素编码器，再为空间中的每一个小立方体预测：它是否被占据、它是什么、以及它如何运动。"),
#         ("Look at the comparison at the bottom: bounding-box detection misses irregular objects, while dense occupancy captures any shape.",
#          "看底部的对比：包围框检测会漏掉不规则物体，而稠密占用则能捕捉任意形状。"),
#         ("And the arrows — occupancy flow — give each voxel its own motion vector.",
#          "再看那些箭头——占用流——它为每个体素都赋予一个运动矢量。"),
#         ("The essence: instead of asking 'what objects are there,' the occupancy network asks the safer, more fundamental question — 'which space is free, and which is solid?'",
#          "其本质在于：占用网络不再问“那里有哪些物体”，而是问一个更安全、更本质的问题——“哪里是空的，哪里是实的？”"),
#         ("This is the open-set safety net of modern perception, and increasingly it is the shared 3D representation that end-to-end models are built on top of.",
#          "这正是现代感知的“开集安全网”，并且越来越成为端到端模型赖以构建的、共享的三维表示。"),
#     ]),

#     (8, "单目与激光雷达3D检测", [
#         ("Let's zoom into two complementary detection paths that feed the fusion stage.",
#          "我们放大看两条互补的检测路线，它们共同喂给融合环节。"),
#         ("On top, the camera path: a single image goes through 2D detection plus a depth and geometry prior, then regresses full 3D boxes — position, size, and yaw — finally projecting them back onto the image.",
#          "上方是相机路线：单张图像经过二维检测，再叠加深度与几何先验，回归出包含位置、尺寸与朝向角的完整三维框，最后投影回图像上。"),
#         ("Below, the LiDAR path: the point cloud is voxelized into pillars — the famous PointPillars trick — passed through a sparse 3D CNN backbone, and a detection head outputs class, box, and direction.",
#          "下方是激光雷达路线：点云被体素化为“柱状”——著名的 PointPillars 技巧——再经过稀疏三维 CNN 主干，由检测头输出类别、框与朝向。"),
#         ("Why keep both? Because they fail in opposite ways.",
#          "为什么两条都要保留？因为它们的失效方式恰好相反。"),
#         ("The camera is rich in semantics and global context but only guesses at depth; LiDAR gives accurate, metric geometry but is sparse and color-blind.",
#          "相机语义丰富、全局上下文充足，却只能“猜测”深度；激光雷达提供精确、带尺度的几何，却稀疏且“色盲”。"),
#         ("Camera knows what it is; LiDAR knows exactly where it is.",
#          "相机知道“那是什么”；激光雷达知道“它精确在哪”。"),
#         ("Converging them gives you the best of both — and crucially, physical redundancy, so no single sensor failure can ever blind the car.",
#          "把它们汇聚起来，就能取两者之长——更关键的是带来物理冗余，使得任何单一传感器的失效，都无法让车辆“失明”。"),
#     ]),

#     (9, "交通灯与标志识别", [
#         ("Traffic lights look easy, but they hide one of the trickiest problems in all of driving.",
#          "红绿灯看似简单，却隐藏着驾驶中最棘手的问题之一。"),
#         ("Stage one is physical detection: a traffic-light detector first finds the light boxes, then a second-stage classifier reads each bulb's color and arrow shape — red, yellow, green, straight, turn.",
#          "第一阶段是物理检测：交通灯检测器先找出“灯框”，再由第二阶段分类器读取每个灯泡的颜色与箭头形状——红、黄、绿，直行、转弯。"),
#         ("But detecting the lights is the easy half. The hard question is: which of those lights actually governs MY lane?",
#          "但检测到灯，只是简单的一半。真正难的问题是：这些灯里，究竟哪一盏在管“我这条车道”？"),
#         ("That's stage two, logical association. Using a prior HD-map binding of traffic-lights to lanes, the system reasons out a logical signal for each ego-lane — go, stop, or turn.",
#          "这就是第二阶段——逻辑关联。借助一份“交通灯—车道”的高精地图先验绑定，系统为每条自车车道推理出一个逻辑信号——通行、停止，或转弯。"),
#         ("Traffic signs like 'no turn on red' are folded in as additional rule modifiers.",
#          "像“红灯禁止右转”这样的交通标志，则作为额外的规则修正项被纳入其中。"),
#         ("The output on the right is a clean, per-lane command bound directly to the map.",
#          "右侧的输出，是一条干净的、与地图绑定的、逐车道的指令。"),
#         ("The essence here: perception alone is never enough — you must fuse what you see with what you know, the map, to turn raw detections into actionable meaning.",
#          "这里的本质是：仅有感知永远不够——你必须把“看到的”与“已知的”（地图）融合起来，才能把原始检测，转化为可执行的语义。"),
#     ]),

#     (10, "多目标跟踪融合", [
#         ("Detection gives you objects in a single frame. But driving needs continuity — stable identities over time.",
#          "检测给你的是单帧里的物体。但驾驶需要的是连续性——随时间稳定的身份。"),
#         ("Here four input streams converge: vision 3D, LiDAR 3D, radar, and occupancy.",
#          "这里有四路输入流汇聚：视觉三维、激光雷达三维、毫米波雷达，以及占用。"),
#         ("The fusion pipeline runs in order: time synchronization, then data association — matching detections to existing tracks with the Hungarian algorithm and probabilistic gating — then state estimation with a Kalman or interacting-multiple-model filter, then track lifecycle management deciding when to birth, confirm, or delete a track, and finally a transform into the global frame.",
#          "融合流水线按序执行：先时间同步；再数据关联——用匈牙利算法与概率门控，把检测匹配到已有航迹；接着用卡尔曼或交互多模型滤波器做状态估计；然后由航迹生命周期管理决定何时“新生、确认、删除”一条航迹；最后变换到全局坐标系。"),
#         ("Notice the side module: a radar cross-check that re-scores detections and pins down the CIPV — the closest-in-path vehicle.",
#          "注意那个旁路模块：毫米波雷达交叉校验，它对检测重新打分，并锁定 CIPV——本车路径上最近的那辆车。"),
#         ("The CIPV is special: it is the single most safety-critical target, the car you are directly following.",
#          "CIPV 很特殊：它是单个最关键的安全目标——也就是你正紧跟其后的那辆车。"),
#         ("The output is a fused track list, each object carrying a persistent ID and a velocity, painted into a coherent top-down scene.",
#          "输出是一份融合航迹列表，每个目标都带着一个持久的 ID 和速度，被绘制进一个连贯的俯视场景中。"),
#         ("The deep point: planning cannot react to flickering, frame-by-frame blobs — it needs objects with memory, identity, and predictable motion. Tracking is what turns perception into something you can actually plan against.",
#          "深层要点在于：规划无法对逐帧闪烁的“光斑”做出反应——它需要的是有记忆、有身份、运动可预测的物体。跟踪，正是把感知转化为“可供规划之物”的那一步。"),
#     ]),

#     (11, "场景理解-活地图", [
#         ("Now we assemble everything into one unified picture — aptly called the Living Map.",
#          "现在，我们把一切组装成一幅统一的图景——它有个很贴切的名字，叫“活地图”。"),
#         ("Five sources flow in on the left: lane generation, road geometry and edges, topology self-consistency, traffic-light and sign fusion, and the dynamic scene with traffic-flow speed.",
#          "左侧有五路信息汇入：车道生成、道路几何与路沿、拓扑自洽、交通灯与标志融合，以及带交通流速度的动态场景。"),
#         ("These are fused — topo-lane with an SD pro-map — through localization, lane association, and lightweight lane attributes, then aligned against the global navigation SD-map.",
#          "它们被融合在一起——拓扑车道与 SD 增强地图——经由定位、车道关联与轻量化车道属性，再与全局导航 SD 地图对齐。"),
#         ("The result on the right is a single representation that layers together topology, semantics, traffic states, and dynamics — all color-coded into lane, road, topology, traffic-control, scene, and navigation layers.",
#          "右侧的结果，是一个统一表示，它把拓扑、语义、交通状态与动态分层叠合——并以颜色编码为车道层、道路层、拓扑层、交通控制层、场景层与导航层。"),
#         ("Why call it 'living'? Because it is refreshed continuously, every cycle, fusing the freshest perception with prior map knowledge.",
#          "为什么叫“活”？因为它在每一个周期都被持续刷新，把最新鲜的感知与先验地图知识融合在一起。"),
#         ("The essence: planning should never talk to a dozen raw modules directly. It talks to one clean, machine-readable world model — and the quality of this representation sets the ceiling for everything downstream.",
#          "其本质在于：规划绝不应该直接对接十几个原始模块。它只面对一个干净的、机器可读的世界模型——而这个表示的质量，决定了下游一切的上限。"),
#     ]),

#     (12, "高精定位", [
#         ("To use a map, you have to know exactly where you are on it — and that is harder than it sounds.",
#          "要用地图，你就必须精确地知道自己在地图的哪个位置——而这远比听上去要难。"),
#         ("On the left, the information sources: GNSS with RTK corrections, a corrected IMU, wheel-speed sensors, LiDAR and vision map matching, and the HD/SD map itself.",
#          "左侧是信息来源：带 RTK 修正的 GNSS、经过校正的 IMU、轮速传感器、激光雷达与视觉地图匹配，以及高精/标精地图本身。"),
#         ("They all feed a tightly-coupled filter — an extended Kalman filter or a factor graph — that estimates a rich state: position, velocity, attitude, plus the gyroscope and accelerometer biases and a scale factor.",
#          "它们共同喂入一个紧耦合滤波器——扩展卡尔曼滤波，或因子图——估计出一个丰富的状态量：位置、速度、姿态，外加陀螺仪与加速度计的零偏，以及一个尺度因子。"),
#         ("The output splits into global localization in map coordinates, and local odometry in the vehicle frame.",
#          "输出分为两路：地图坐标系下的全局定位，与车体坐标系下的局部里程计。"),
#         ("Why fuse so many sources? Because each one fails alone: GNSS dies in tunnels and urban canyons, the IMU drifts within seconds, wheels slip, and map matching needs visible features.",
#          "为什么要融合这么多来源？因为单独使用时，每一个都会失效：GNSS 在隧道与城市峡谷中失灵，IMU 在数秒内漂移，轮速会打滑，地图匹配则需要可见的特征。"),
#         ("Look at the bottom: before fusion, a huge uncertainty ellipse; after fusion, it collapses into a tight, confident estimate.",
#          "看底部：融合前，是一个巨大的不确定性椭圆；融合后，它收缩成一个紧致、可信的估计。"),
#         ("The word 'tightly-coupled' is the key insight — instead of fusing each sensor's final answer, you fuse their raw measurements, so the strengths of one fill the blind spots of another.",
#          "“紧耦合”这个词，是关键洞见——你融合的不是每个传感器的“最终答案”，而是它们的“原始观测”，于是一个的长处，恰好填补另一个的盲区。"),
#     ]),

#     (13, "行为预测", [
#         ("We know where everyone is. Now comes the hardest cognitive leap: predicting what they'll do next.",
#          "我们已经知道每个人在哪。现在是最难的认知飞跃：预测他们下一步要做什么。"),
#         ("The input is the tracked agents plus map context, expressed as a lane graph.",
#          "输入是被跟踪的交通参与者，外加以“车道图”形式表达的地图上下文。"),
#         ("Inside the motion-prediction module runs a sequential reasoning loop: schedule the prediction, analyze scenarios, analyze priorities, assign relative intentions with respect to the autonomous vehicle, assign a risk status, and finally generate multi-modal predictions.",
#          "运动预测模块内部，运行着一个序贯推理循环：调度预测、分析场景、分析优先级、相对于自车赋予意图、评定风险状态，最后生成多模态预测。"),
#         ("The encoder is built on agent-map-agent attention — every agent attends both to the map and to every other agent.",
#          "编码器构建在“智能体—地图—智能体”注意力之上——每个智能体既关注地图，也关注其他每一个智能体。"),
#         ("Look at the output on the right: from one target agent, three futures branch out with probabilities of zero-point-six, zero-point-three, and zero-point-one, summing to one.",
#          "看右侧输出：从同一个目标智能体，分出三种未来，概率分别为零点六、零点三、零点一，加起来等于一。"),
#         ("This multi-modality is not a flaw — it is the truth. A car at an intersection genuinely might go straight or turn, and a good predictor must hold all possibilities at once.",
#          "这种多模态并不是缺陷——它就是真相。一辆停在路口的车，确实可能直行，也可能转弯，一个好的预测器，必须同时“持有”所有可能。"),
#         ("And notice the loop also reasons about the AV's own intentions — because prediction is interactive: other drivers react to what we do.",
#          "还要注意，这个循环也会推理自车自身的意图——因为预测是交互的：其他司机会对我们的行为做出反应。"),
#         ("This game-theoretic, staged reasoning is exactly where large-model thinking is now entering the prediction stack.",
#          "这种博弈式的、分阶段的推理，正是当下大模型思维进入预测栈的切入点。"),
#     ]),

#     (14, "决策与规划", [
#         ("With predictions in hand, we plan. And planning here is split into two beautifully clean layers.",
#          "有了预测，我们就开始规划。这里的规划，被拆分成两个极为干净的层次。"),
#         ("The top layer is behavior decision, a finite-state machine cycling between lane keep, lane change, overtake, yield, and adaptive cruise — with a drive-priority arbitration deciding which behavior wins.",
#          "顶层是行为决策，一个有限状态机，在车道保持、变道、超车、让行与自适应巡航之间切换——再由“驾驶优先级仲裁”决定哪种行为胜出。"),
#         ("The bottom layer is the planner loop: search multi-lane paths, filter candidates, build a path boundary with constraints, do a spatio-temporal joint search and optimization, select a trajectory, and finally optimize speed.",
#          "底层是规划器循环：搜索多车道路径、筛选候选、构建带约束的路径边界、做时空联合搜索与优化、选出一条轨迹，最后优化速度。"),
#         ("This is the classic Apollo EM-Planner philosophy: decompose an impossibly hard joint problem into path — where to go — and speed — when to be there — over a spatio-temporal graph.",
#          "这正是经典的 Apollo EM-Planner 思想：把一个难到不可解的联合问题，在时空图上分解为路径（去哪里）与速度（何时到达）。"),
#         ("Look at the bottom-right S-T view: the chosen green trajectory threads precisely between obstacle one and obstacle two in distance-time space — that's how the planner decides whether to overtake before, or yield behind.",
#          "看右下角的 S-T 图：被选中的绿色轨迹，在“距离—时间”空间里精准地从障碍物一与障碍物二之间穿过——这正是规划器决定“抢在前面超车”还是“跟在后面让行”的方式。"),
#         ("And notice modules 7a and 7b: an AI planner proposing multiple trajectories, and a rule-based fallback planner for safety.",
#          "再注意 7a 与 7b 模块：一个 AI 规划器提出多条轨迹，一个基于规则的兜底规划器负责安全。"),
#         ("That pairing — a learned planner for performance, a classical planner as a guaranteed safety net — is the dominant industrial pattern right now, and it is the bridge toward the end-to-end future.",
#          "这种搭配——用学习型规划器追求性能，用经典规划器作为有保障的安全网——是当下业界的主流范式，也是通往端到端未来的桥梁。"),
#     ]),

#     (15, "控制与RPU执行", [
#         ("Planning produces a desired trajectory. Control is what makes the physical car actually follow it.",
#          "规划产出的是一条期望轨迹。而控制，才是让物理车辆真正去跟随它的那一环。"),
#         ("The planned trajectory — reference position, heading, speed, and curvature — splits into two controllers.",
#          "规划轨迹——包含参考位置、航向、速度与曲率——被分为两个控制器。"),
#         ("Lateral control handles steering, tracking heading and curvature with pure-pursuit, LQR, or MPC; longitudinal control handles throttle and brake, tracking speed with PID or MPC.",
#          "横向控制管转向，用纯追踪、LQR 或 MPC 跟踪航向与曲率；纵向控制管油门与刹车，用 PID 或 MPC 跟踪速度。"),
#         ("They merge into a single control request — steering angle, acceleration, and brake torque.",
#          "它们汇成一条统一的控制请求——转向角、加速度、刹车扭矩。"),
#         ("Now watch the red dashed line: this request crosses from the APU into the RPU, the safety domain, where the Actuation Manager — Actman — does final arbitration before commanding the steering, drivetrain, and brakes.",
#          "现在看那条红色虚线：这条请求跨过边界，从 APU 进入 RPU 安全域，由执行管理器——Actman——在指令下达给转向、动力总成与刹车之前，做最后的仲裁。"),
#         ("The small diagram explains the core control objective: minimize the cross-track error, the perpendicular distance between the actual path and the reference path.",
#          "右下角的小图，解释了控制的核心目标：最小化横向跟踪误差，也就是实际路径与参考路径之间的垂直距离。"),
#         ("The essence: the compute brain proposes, but the safety brain disposes — every actuator command passes through a certified gate, so intelligence never directly, unilaterally moves the wheels.",
#          "其本质是：计算大脑负责“提议”，安全大脑负责“裁决”——每一条执行器指令，都要穿过一道经过认证的关卡，于是智能永远无法直接、单方面地驱动车轮。"),
#     ]),

#     (16, "泊车-HPA-AVP", [
#         ("Parking might look like a minor feature, but it is actually a whole separate driving stack — because everything about it is different.",
#          "泊车看起来只是个小功能，但它其实是一整套独立的驾驶栈——因为它的方方面面都不一样。"),
#         ("Stage one, near-field perception, runs on fisheye BEV: estimating free space, detecting parking slots, ranging with ultrasonic sensors, and tracking nearby dynamic objects.",
#          "第一阶段，近场感知，运行在鱼眼 BEV 上：估计可行驶的自由空间、检测车位、用超声波传感器测距、并跟踪附近的动态物体。"),
#         ("Stage two, parking decision and planning, has its own state machine — automated parking, remote parking, proximity collision warning, and emergency braking — fusing slots with confidence scores, planning the maneuver, and controlling at low speed.",
#          "第二阶段，泊车决策与规划，有它自己的状态机——自动泊车、遥控泊车、近距碰撞预警、紧急制动——融合带置信度的车位、规划泊车动作、并做低速运控。"),
#         ("Stage three is memory and valet parking: on-board mapping builds a local map, global re-localization finds your pose in it, a map server aggregates and enhances maps, and an end-to-end module plans and controls the full route.",
#          "第三阶段是记忆泊车与代客泊车：车端建图构建局部地图，全局重定位在其中找回位姿，地图服务器聚合并增强地图，再由一个端到端模块，规划并控制完整的路线。"),
#         ("Green slots are free, red are occupied, and the dashed line is the ego path threading in.",
#          "绿色是空车位，红色是已占用，虚线则是自车驶入的路径。"),
#         ("Why a dedicated stack? Because at parking speeds the sensors are fisheye and ultrasonic, the precision demands are centimeter-level, and the geometry — tight slots, sharp angles — is utterly unlike highway driving. Different problem, different solution.",
#          "为什么要专门一套栈？因为在泊车速度下，传感器是鱼眼与超声波，精度要求是厘米级，而几何环境——狭窄车位、刁钻角度——与高速行驶截然不同。不同的问题，需要不同的解法。"),
#     ]),

#     (17, "中间件与通信", [
#         ("Everything we've discussed has to communicate — and that is the job of the middleware, the system's nervous system.",
#          "我们讨论的一切，都必须相互通信——这正是中间件的职责，它是整个系统的神经系统。"),
#         ("At the top, layer three, the application services — perception, fusion, planning, and map — do not call each other directly.",
#          "顶部，第三层，应用服务——感知、融合、规划与地图——彼此之间并不直接调用。"),
#         ("Instead they all publish and subscribe over a DDS / SOA backbone in layer two, a service-oriented bus.",
#          "取而代之，它们都在第二层的 DDS / SOA 主干上发布与订阅——这是一条面向服务的总线。"),
#         ("Below that, layer one-point-five gateways route signals: a CAN gateway, a SOME/IP gateway for HMI and navigation, and a sensor pre-processing gateway.",
#          "再往下，第一点五层的网关负责信号路由：一个 CAN 网关，一个用于人机交互与导航的 SOME/IP 网关，以及一个传感器预处理网关。"),
#         ("The two domains each get their own middleware — Adaptive AUTOSAR on the APU, and a real-time-focused stack on the RPU — handling service, execution, communication, persistency, plus safety, QoS, and health management.",
#          "两个域各有自己的中间件——APU 上是 Adaptive AUTOSAR，RPU 上是面向实时的栈——分别处理服务、执行、通信、持久化，以及安全、服务质量与健康管理。"),
#         ("At the bottom, layer zero, the execution platform: a multi-core SoC with A-cores and R-cores, hardware time synchronization, security isolation, and resource management.",
#          "在最底层，第零层，是执行平台：一颗带 A 核与 R 核的多核 SoC、硬件级时间同步、安全隔离与资源管理。"),
#         ("The deep idea: service-oriented architecture decouples modules so completely that any service can be developed, tested, updated, or even moved to a different chip — without breaking the others. This is what makes a software-defined vehicle actually possible.",
#          "深层思想是：面向服务的架构，把模块解耦得如此彻底，以至于任何一个服务都可以被独立开发、测试、更新，甚至迁移到另一颗芯片上，而不破坏其他模块。这，正是“软件定义汽车”得以成真的根本。"),
#     ]),

#     (18, "数据闭环", [
#         ("Here's the secret that separates leaders from followers: it's not the model, it's the data engine.",
#          "这里有一个区分领先者与追随者的秘密：决胜的不是模型，而是数据引擎。"),
#         ("Follow the flywheel. On the car, shadow mode runs silently — a trigger detects corner cases, or disagreements between the deployed and the candidate model.",
#          "跟着这个飞轮看。在车端，影子模式静默运行——一个触发器，专门检测长尾的边缘场景，或量产模型与候选模型之间的“分歧”。"),
#         ("When triggered, the vehicle records the clip, compresses, encrypts, and anonymizes it, then uploads over 5G.",
#          "一旦触发，车辆就记录下这个片段，压缩、加密、脱敏，再通过 5G 上传。"),
#         ("In the cloud, foundation models auto-label the data, long-tail mining sorts it into a scenario bank, models are trained and tested in simulation, validated, and finally pushed back to the car via OTA.",
#          "在云端，基础模型对数据自动标注，长尾挖掘把它归入“场景库”，模型在仿真中被训练与测试、通过验证，最后经 OTA 回灌到车端。"),
#         ("And then the loop closes — the improved model drives, finds new corner cases, and the wheel spins again.",
#          "然后闭环就此合拢——升级后的模型上路行驶，发现新的边缘场景，飞轮再次转动。"),
#         ("The genius of shadow mode is efficiency: you don't upload everything — that's impossible at fleet scale. You only upload the moments where the model is uncertain or wrong, mining the long tail with surgical precision.",
#          "影子模式的精妙之处，在于“效率”：你不会上传所有数据——在车队规模下那根本不可能。你只上传模型“不确定”或“出错”的那些瞬间，以外科手术般的精度去挖掘长尾。"),
#         ("This is the Tesla-style data flywheel — and it is why autonomous driving is, at its core, a data problem disguised as an algorithm problem.",
#          "这就是特斯拉式的数据飞轮——也正因如此，自动驾驶在本质上，是一个伪装成算法问题的“数据问题”。"),
#     ]),

#     (19, "趋势一-模块化到端到端", [
#         ("So we've walked the entire classical stack. Now let's ask the big question — where is all of this heading?",
#          "至此，我们已经走完了整条经典栈。现在，让我们追问那个大问题——这一切，正走向何方？"),
#         ("Diagram (a) is the modular pipeline of today: perception, fusion, environment model, prediction, planning, control — each a separate box, joined by hand-crafted interfaces.",
#          "图（a）是今天的模块化流水线：感知、融合、环境模型、预测、规划、控制——每个都是独立的方块，由手工设计的接口连接。"),
#         ("Those red crosses mark the pain points. As a recent survey puts it, these hand-crafted interfaces and rule-based components tend to break down in complex, long-tailed scenarios, and the cascaded design propagates perception errors downstream, degrading planning and control.",
#          "那些红色的叉，标记的正是痛点。正如近期一篇综述所指出的：这些手工接口与基于规则的组件，在复杂的长尾场景中往往会失效，而级联式的设计，会把感知误差向下游传播，劣化规划与控制。"),
#         ("Diagram (b) is the emerging answer — End-to-End 2.0: a unified perception-plus-prediction module producing BEV and occupancy tokens, feeding a joint differentiable planner, then control — with shared features and gradients flowing end-to-end.",
#          "图（b）是正在浮现的答案——端到端 2.0：一个统一的“感知＋预测”模块，产出 BEV 与占用 token，喂给一个联合可微的规划器，再到控制——特征共享，梯度端到端地流动。"),
#         ("Watch what's disappearing: hand-tuned fusion, rule interfaces, separate trackers — they're all being absorbed into the network.",
#          "看看什么正在消失：手工调校的融合、规则接口、独立的跟踪器——它们都正被吸收进网络之中。"),
#         ("The deep reason this works: when gradients flow all the way from the final driving outcome back to the raw features, every module learns to produce exactly what the next one needs — not what a human engineer guessed it should produce.",
#          "它之所以奏效，深层原因在于：当梯度从最终的驾驶结果，一路回传到最原始的特征时，每个模块都学会去产出“下一个模块真正需要的东西”，而不是“人类工程师猜测它应该产出的东西”。"),
#         ("The timeline says it all: 2020 was modular, 2026 is the transition, and the future is unified. This isn't just a refactor — it's a change in the fundamental unit of optimization.",
#          "时间线说明了一切：2020 是模块化，2026 是过渡期，而未来是统一的。这不只是一次重构——而是“优化的基本单元”本身的改变。"),
#     ]),

#     (20, "趋势二-VLA与世界模型", [
#         ("And beyond end-to-end lies the real frontier — the move from modules to foundation models. Three paradigms are emerging.",
#          "而在端到端之外，是真正的前沿——从模块走向基础模型。三种范式正在涌现。"),
#         ("First, one-stage end-to-end: raw sensor tokens go straight into a single unified driving model that outputs a planned trajectory — perception, prediction, and planning fully fused into one network.",
#          "第一，一段式端到端：原始传感器 token 直接进入一个统一的驾驶模型，输出规划轨迹——感知、预测、规划，被彻底融合进同一个网络。"),
#         ("Second, Vision-Language-Action models. Multi-view vision plus a natural-language instruction — 'turn left at the next intersection and yield to pedestrians' — flow into a large VLM backbone that reasons with chain-of-thought, then emits action tokens.",
#          "第二，视觉—语言—动作（VLA）模型。多视角视觉，加上一句自然语言指令——“在下个路口左转并礼让行人”——一起流入一个大型 VLM 主干，它以思维链进行推理，再输出动作 token。"),
#         ("A recent survey organizes VLA into two paradigms: End-to-End VLA, which fuses perception, reasoning, and planning in one model; and Dual-System VLA, which separates slow deliberation by the VLM from fast, safety-critical execution by a planner — the snail and the rocket you see here.",
#          "一篇近期综述，把 VLA 归纳为两大范式：端到端 VLA，在单一模型内融合感知、推理与规划；以及双系统 VLA，把 VLM 的“慢思考”，与规划器的“快速、安全攸关的执行”分离开——也就是你在这里看到的“蜗牛”与“火箭”。"),
#         ("The value of VLA is that it breaks the boundaries between perception, prediction, and planning, generating decisions directly from multimodal inputs of vision and language — making the policy interpretable and grounded in real-world knowledge.",
#          "VLA 的价值，在于它打破了感知、预测与规划之间的边界，直接从视觉与语言这两种多模态输入生成决策，让策略变得可解释，并扎根于真实的世界知识。"),
#         ("Third, the world model: a latent model that imagines how the future will unfold, rolls out candidate trajectories in this dreamed simulation, and selects the best — learning physics and putting simulation directly in the loop.",
#          "第三，世界模型：一个潜在模型，它想象未来将如何展开，在这个“梦境般”的仿真中推演候选轨迹，再选出最优——它学习物理规律，并把仿真直接置于闭环之中。"),
#         ("World models let an end-to-end policy interact with a learned simulator, understanding real physics more deeply and breaking past the limits of pure imitation learning.",
#          "世界模型，让端到端策略得以与一个“学出来的仿真器”交互，更深刻地理解真实物理，并突破纯模仿学习的局限。"),
#         ("But notice the bottom row — what survives as the safety net: the RPU safety domain, the fallback planner, redundant control. No matter how smart the foundation model becomes, the certified safety brain stays.",
#          "但请注意最底下那一行——什么作为安全网而存续：RPU 安全域、兜底规划器、冗余控制。无论基础模型变得多么聪明，那个经过认证的安全大脑，始终在场。"),
#         ("Intelligence may be absorbed into one giant model, but safety remains physically separate. That is the enduring lesson of this entire architecture. Thank you.",
#          "智能或许会被吸收进一个庞大的模型，但安全，永远在物理上保持独立。这，正是整套架构留给我们的、最恒久的一课。谢谢大家。"),
#     ]),
# ]


# def main():
#     out_dir = "assets/media/blog/script/talk"
#     os.makedirs(out_dir, exist_ok=True)

#     for num, topic, sents in pages:
#         sentences = [
#             {"en": " ".join(en.split()), "zh": " ".join(zh.split())}
#             for en, zh in sents
#         ]
#         data = {"page": num, "topic": topic, "sentences": sentences}
#         filename = f"{num:02d}_{topic}.json"
#         path = os.path.join(out_dir, filename)
#         with open(path, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#         en_chars = sum(len(s["en"]) for s in sentences)
#         zh_chars = sum(len(s["zh"]) for s in sentences)
#         print(f"已生成: {path}  ({len(sentences)} 句 / EN {en_chars} 字符 / ZH {zh_chars} 字)")

#     print(f"\n全部完成！共生成 {len(pages)} 个 JSON 文件，位于 ./{out_dir}/ 目录下。")
#     print("提示: talk2video.py 会优先读取 *.json；如目录里还残留旧的 *.txt，可一并删除以免混淆。")


# if __name__ == "__main__":
#     main()




# ------------------------------- ------------------------------- ------------------------------- ------------------------------- ------------------------------- -------------------------------



# # -*- coding: utf-8 -*-
# """
# 运行后在当前目录生成 talk/ 文件夹，内含 20 个 .json 文件。
# 每个文件是对应 PPT 页面的「逐句中英对照」讲稿，结构为:
#     {"page": 1, "topic": "标题",
#      "sentences": [{"en": "...", "zh": "..."}, ...]}

# 设计要点:
#   * 以「句」为对齐单位 —— 同一份句子列表同时驱动 TTS 配音与字幕，
#     因此「英文语音 / 英文字幕 / 中文字幕」三者天然一一对应。
#   * 内容基于三篇核心综述:
#       1) Aligning Cyber Space with Physical World: A Comprehensive Survey on Embodied AI
#       2) World Model for Robot Learning: A Comprehensive Survey
#       3) Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses
#   * 讲解以「大道至简」为目标: 学术严谨, 但通俗易懂, 直击底层原理与逻辑。
# 直接运行: python generate_talk.py
# """
# import os
# import json

# # (页码, 主题, [(英文句, 中文句), ...])
# pages = [
#     (1, "标题", [
#         ("Hi everyone, welcome.",
#          "大家好，欢迎。"),
#         ("Today I want to walk you through the full stack of Embodied AI — how we get intelligence to step off the screen and into the physical world.",
#          "今天，我想带大家走一遍具身智能的完整技术栈——看看我们如何让智能走出屏幕，进入真实的物理世界。"),
#         ("I'm Jiang Chaokang, and this talk is built on three landmark surveys published between 2024 and 2026.",
#          "我是蒋超康，这次分享建立在 2024 到 2026 年间的三篇里程碑式综述之上。"),
#         ("We'll go in order: from the body of an embodied agent, to its brain, and finally to its conscience.",
#          "我们会按顺序展开：从一个具身智能体的“身体”，讲到它的“大脑”，最后到它的“良知”。"),
#         ("Let's dive in.",
#          "让我们开始吧。"),
#     ]),

#     (2, "目录", [
#         ("The whole talk has three parts, and they follow one simple logic.",
#          "整场分享分为三部分，它们遵循一条简单的逻辑主线。"),
#         ("Part one is a comprehensive survey of embodied AI — this is the full stack: the body and the senses.",
#          "第一部分，是具身智能的全面综述——这就是完整的技术栈：身体与感官。"),
#         ("Part two is the world model for robot learning — this is the predictive brain, the part that can imagine the future.",
#          "第二部分，是面向机器人学习的世界模型——这是会预测、能想象未来的“大脑”。"),
#         ("Part three is safety — the shadow that grows with every new capability.",
#          "第三部分，是安全——它是随每一项新能力一同生长的“影子”。"),
#         ("So the storyline is simple: build the body, give it a brain that thinks ahead, then make sure it never hurts anyone.",
#          "所以故事线很简单：先造出身体，再赋予它一个会预判的大脑，最后确保它绝不会伤害任何人。"),
#     ]),

#     (3, "具身智能体的整体框架", [
#         ("Let's start with the big picture: what is an embodied agent, really?",
#          "我们先看全局：一个具身智能体，究竟是什么？"),
#         ("The core idea is a closed loop between cyber space and the physical world.",
#          "它的核心思想，是在赛博空间与物理世界之间，形成一个闭环。"),
#         ("On the left is the virtual environment — cyber space — where robots and scenes can be trained cheaply and safely, then transferred to reality through sim-to-real.",
#          "左边，是虚拟环境，也就是赛博空间——机器人和场景可以在这里低成本、安全地训练，再通过 sim-to-real 迁移到现实。"),
#         ("In the center sits the brain: an embodied world model.",
#          "正中央，是大脑：一个具身世界模型。"),
#         ("And look at its structure — perception feeds memory and a world model; an actor proposes actions; a critic scores them with cost and intrinsic cost.",
#          "看它的结构——感知喂给记忆和世界模型；行动器提出动作；评论家再用“代价”和“内在代价”给动作打分。"),
#         ("This is essentially LeCun's blueprint — the world model predicts what will happen, so the agent imagines the consequences before it ever moves.",
#          "这本质上就是 LeCun 的蓝图——世界模型预测会发生什么，于是智能体在真正行动之前，先在脑中想象后果。"),
#         ("On the right, this brain is aligned to human values, causal understanding, and physical laws — and that is what makes manipulation reliable and safe.",
#          "右边，这个大脑还要对齐人类价值、因果理解和物理规律——这正是让操作变得可靠、安全的前提。"),
#         ("Now look at the table at the bottom, because it captures the essential difference.",
#          "再看底部那张表格，因为它点明了最本质的区别。"),
#         ("Disembodied AI, like ChatGPT, lives in cyber space; its cognition is disentangled from any physical body.",
#          "离身的 AI，比如 ChatGPT，活在赛博空间，它的认知与任何物理身体是分离的。"),
#         ("Embodied AI, like RT-1 and RT-2, fuses cognition directly into a physical entity.",
#          "而具身 AI，比如 RT-1、RT-2，把认知直接融进了物理实体。"),
#         ("And here's the deep point: intelligence is not just in the head — it emerges from the loop of brain, body, and environment.",
#          "这里有一个深层洞见：智能不只在脑子里——它诞生于大脑、身体与环境的循环之中。"),
#     ]),

#     (4, "具身智能的发展全景", [
#         ("If I had to compress this entire field into one sentence, it's right there at the top: embodied AI is about aligning cyber space with the physical world.",
#          "如果让我把整个领域压缩成一句话，它就写在最上面：具身智能，就是让赛博空间与物理世界对齐。"),
#         ("Under that goal sit five pillars.",
#          "在这个目标之下，立着五根支柱。"),
#         ("From the left: embodied robots are the body; simulators are the training ground; embodied perception is the senses; embodied interaction is acting on objects and people; and the embodied agent is the foundation-model brain.",
#          "从左到右：具身机器人是身体；仿真器是训练场；具身感知是感官；具身交互是对物体和人的行动；具身智能体则是基础模型构成的大脑。"),
#         ("Notice that all five arrows funnel down into one bottleneck: sim-to-real adaptation.",
#          "注意，这五个箭头最终都汇聚到同一个瓶颈：sim-to-real，也就是仿真到现实的迁移。"),
#         ("That's no accident — because we train mostly in simulation, but we have to deploy in the messy real world.",
#          "这绝非偶然——因为我们主要在仿真里训练，却必须部署到杂乱的真实世界。"),
#         ("Underneath lies the technical foundation: the world model, data collection and training, and embodied control.",
#          "再往下，是技术底座：世界模型、数据采集与训练、以及具身控制。"),
#         ("And the applications fan out across robotics, autonomous driving, healthcare, domestic help, industry, and search-and-rescue.",
#          "而应用，则铺展到机器人、自动驾驶、医疗、家政、工业自动化和搜救等领域。"),
#         ("The engineering lesson here: no single module wins; embodied AI is a systems problem, where the real difficulty is the integration.",
#          "这里的工程启示是：没有任何单一模块能独赢；具身智能是一个系统问题，真正难的是把它们整合起来。"),
#     ]),

#     (5, "各类具身机器人", [
#         ("Let's talk about the body, because in embodied AI, the body literally shapes the mind.",
#          "我们先聊身体，因为在具身智能里，身体会实实在在地塑造心智。"),
#         ("Here are six families of robots.",
#          "这里有六大类机器人。"),
#         ("The top row shows a fixed-base arm like the Franka Panda, a wheeled robot like Jackal, and a tracked robot like the iRobot PackBot.",
#          "上排，是像 Franka Panda 这样的固定底座机械臂、像 Jackal 这样的轮式机器人、以及像 iRobot PackBot 这样的履带机器人。"),
#         ("The middle row shows a quadruped like Boston Dynamics' Spot and a humanoid like Tesla's Optimus.",
#          "中排，是像波士顿动力 Spot 这样的四足机器人，和像特斯拉 Optimus 这样的人形机器人。"),
#         ("And at the bottom are biomimetic robots that copy fish, insects, and other animals.",
#          "最下面，是模仿鱼、昆虫等动物的仿生机器人。"),
#         ("Each form is a trade-off — dexterity versus mobility, stability versus terrain coverage.",
#          "每一种形态都是一种取舍——灵巧性与移动性的权衡，稳定性与地形适应力的权衡。"),
#         ("So why is everyone obsessed with humanoids right now?",
#          "那么，为什么现在所有人都痴迷于人形机器人？"),
#         ("Because our entire world — tools, doorknobs, stairs — is built for the human body, so a human-shaped robot can reuse human tools and even learn from human videos.",
#          "因为我们的整个世界——工具、门把手、楼梯——都是为人体设计的，所以人形机器人能复用人类的工具，甚至能从人类的视频里学习。"),
#         ("The takeaway: there is no universal best body — you choose the embodiment to match the task and the environment.",
#          "结论是：不存在通用的最优身体——你要根据任务和环境，去选择合适的形态。"),
#     ]),

#     (6, "通用仿真器示例", [
#         ("If robots are the body, simulators are where they go to school.",
#          "如果说机器人是身体，那仿真器就是它们上学的地方。"),
#         ("Why simulate at all? Because real-world data is slow, expensive, and sometimes dangerous, while simulation gives you infinite, safe, parallel, perfectly-labeled experience.",
#          "为什么要仿真？因为真实数据采集得慢、成本高、有时还很危险；而仿真能提供无限量的、安全的、可并行的、标注完美的经验。"),
#         ("These platforms split into two families.",
#          "这些平台分为两大家族。"),
#         ("The first is physics and robotics engines — Isaac Sim, Gazebo, PyBullet, MuJoCo — which care about accurate dynamics and contact.",
#          "第一类是物理与机器人引擎——Isaac Sim、Gazebo、PyBullet、MuJoCo——它们关心的是精确的动力学和接触。"),
#         ("The second is photorealistic scene simulators — AI2-THOR, Habitat, iGibson, Matterport3D — which care about how the world looks, for perception and navigation.",
#          "第二类是照片级真实感的场景仿真器——AI2-THOR、Habitat、iGibson、Matterport3D——它们关心的是世界“看起来”如何，服务于感知与导航。"),
#         ("And there's an unavoidable tension: physical accuracy, visual realism, and speed — you usually can't max out all three at once.",
#          "这里有一个绕不开的矛盾：物理精度、视觉真实感、运行速度——你通常没法把三者同时拉满。"),
#         ("Here's a thought worth sitting with: a simulator is really just a world model that humans hand-crafted.",
#          "有一个值得细品的观点：仿真器，其实就是一个由人类手工打造的世界模型。"),
#         ("And that is exactly why the next part of this talk matters — modern neural world models try to learn that simulator automatically, straight from data.",
#          "而这恰恰是下一部分的意义所在——现代的神经世界模型，试图从数据中自动地“学”出这个仿真器。"),
#     ]),

#     (7, "主动视觉感知", [
#         ("Now the senses — and the key idea here is the shift from passive to active perception.",
#          "现在讲感官——这里的核心思想，是从“被动感知”到“主动感知”的转变。"),
#         ("In the orange box on the left, passive perception takes a fixed image and does the classic work: 3D scene understanding, visual SLAM, and semantics.",
#          "左边那个橙色框里，是被动感知：拿到一张固定的图像，做经典的工作——三维场景理解、视觉 SLAM、语义分析。"),
#         ("But on the right, active perception adds a loop: observe, decide where to look, then move to look — and each move reduces uncertainty about the world.",
#          "但右边的主动感知，多了一个回路：观察、决定看哪里、然后移动去看——而每一次移动，都在降低对世界的不确定性。"),
#         ("The example on the right makes this concrete: grounding the phrase 'the sofa chair near a couch' inside a 3D scene.",
#          "右侧的例子让这一点很具体：在三维场景中，把“长沙发旁边的那把沙发椅”这句话，定位到具体的物体上。"),
#         ("A two-stage method first detects, then matches — and you can see it makes wrong predictions, marked in red.",
#          "两阶段方法先检测、再匹配——你能看到它做出了错误预测，标成了红色。"),
#         ("A one-stage method grounds directly and gets it right, marked in green.",
#          "而一阶段方法直接定位，得到了正确结果，标成了绿色。"),
#         ("Here's the deep insight: perception is not a passive readout — choosing the best next viewpoint is itself an action.",
#          "这里的深层洞见是：感知，从来不是被动的读数——“下一眼该看哪里”，本身就是一个动作。"),
#         ("And that is the unique superpower of embodiment — when you're unsure, you can simply move to see better.",
#          "而这，正是“具身”独有的超能力——当你不确定时，你可以直接动起来，去看得更清楚。"),
#     ]),

#     (8, "视觉语言导航与具身抓取", [
#         ("Let's look at two flagship embodied tasks: navigation and grasping.",
#          "我们来看两个旗舰级的具身任务：导航和抓取。"),
#         ("On the top is Vision-Language Navigation, where an agent, an oracle, and the environment form a loop of observation and action.",
#          "上方是视觉语言导航——智能体、指令者（Oracle）和环境，构成一个“观察—行动”的回路。"),
#         ("It comes in three flavors of rising difficulty: step-by-step turn-here-turn-there instructions; then described-goal navigation, where you must find the target yourself; and finally navigation with interaction — go to the kitchen, take an apple, wash it, put it on the table.",
#          "它有三种难度递增的形式：一步步“在这里转、在那里拐”的逐步指令；然后是“描述目标”式导航，你得自己找到目标；最后是“带交互的导航”——去厨房，拿一个苹果，洗一洗，再放到桌上。"),
#         ("At the bottom is language-guided grasping.",
#          "下方，是语言引导的抓取。"),
#         ("And watch how the language gets harder: from naming an object directly, to spatial reasoning like 'the keyboard to the right of the brown kleenex box,' to logical reasoning like 'I'm thirsty, give me something to drink.'",
#          "看这里的语言是如何变难的：从直接说出物体名字，到“棕色纸巾盒右边的键盘”这样的空间推理，再到“我渴了，给我点喝的”这样的逻辑推理。"),
#         ("The bar chart on the right shows publications exploding year after year — this field is on fire.",
#          "右边的柱状图显示，相关论文逐年爆发式增长——这个方向正炙手可热。"),
#         ("The deep point: language is the universal interface, but the real challenge is grounding — turning fuzzy words into precise geometry and a concrete grasp pose.",
#          "深层要点是：语言是通用的接口，但真正的难点在“接地”——把模糊的词语，转化成精确的几何位置和一个具体的抓取姿态。"),
#     ]),

#     (9, "触觉传感器", [
#         ("Vision gets all the attention, but real manipulation needs touch.",
#          "视觉总是抢尽风头，但真正的操作离不开触觉。"),
#         ("Why? Because in contact-rich tasks, the very thing you care about — the contact point — is usually hidden from the camera by the hand itself.",
#          "为什么？因为在富接触的任务里，你最关心的东西——接触点本身——往往被手自己挡住，相机根本看不到。"),
#         ("Tactile sensors split into two families, shown here.",
#          "触觉传感器分为两大家族，如图所示。"),
#         ("Non-vision sensors, like BioTac, directly measure pressure, vibration, and temperature.",
#          "非视觉类，比如 BioTac，直接测量压力、振动和温度。"),
#         ("Vision-based sensors, like GelSight, are wonderfully clever — they put a camera behind a soft gel and literally watch how the gel deforms when it touches something.",
#          "视觉类，比如 GelSight，设计得非常巧妙——它在一层柔软的凝胶后面放一个相机，去“看”凝胶接触物体时是如何形变的。"),
#         ("That trick turns a hard touch-sensing problem into an image problem, so you can reuse the entire computer-vision toolbox.",
#          "这个技巧，把一个棘手的触觉感知问题，变成了一个图像问题，于是你能复用整套计算机视觉的工具箱。"),
#         ("And the applications follow: estimating force and slip, guiding manipulation, and recognizing materials and textures.",
#          "应用也随之而来：估计力和滑动、引导操作、以及识别材质与纹理。"),
#         ("The essence: dexterous manipulation is fundamentally about contact, and touch closes the last-millimeter gap that vision simply cannot see.",
#          "本质是：灵巧操作的根本在于接触，而触觉，正好补上了视觉看不见的“最后一毫米”。"),
#     ]),

#     (10, "探索场景：具身问答", [
#         ("Here's a task that ties everything together: Embodied Question Answering.",
#          "这里有一个把一切串起来的任务：具身问答。"),
#         ("The twist is that the agent can't answer from a single snapshot — it has to actively explore to find the evidence.",
#          "它的精妙之处在于，智能体无法靠单张快照回答——它必须主动探索，去找到线索。"),
#         ("You can see it turning right, moving forward, wandering the house, building up understanding before it answers.",
#          "你能看到它向右转、向前走、在屋子里游走，一点点建立起理解，然后才作答。"),
#         ("And the question types on the right probe very different abilities.",
#          "而右边的问题类型，考察的是截然不同的能力。"),
#         ("Knowledge-based asks for commonsense — 'is there something to lower the temperature?' — and the answer is the air conditioner.",
#          "“基于知识”的问题考常识——“有没有能降温的东西？”——答案是空调。"),
#         ("Episodic memory asks 'where is the clock?' — so it must recall what it saw earlier.",
#          "“情景记忆”问“时钟在哪里？”——所以它必须回忆起之前看到的画面。"),
#         ("Others test multiple objectives, multi-agent answering, interaction — like opening the fridge to check — and object states, like whether the TV is on.",
#          "其它的还考多目标、多智能体协同作答、交互——比如打开冰箱去查看——以及物体状态，比如电视是不是开着的。"),
#         ("The deep point: this is the closest thing we have to a physical Turing test — it forces perception, memory, reasoning, and action to all work together.",
#          "深层要点是：这是我们最接近“物理图灵测试”的任务——它逼着感知、记忆、推理、行动这整个回路协同工作。"),
#     ]),

#     (11, "具身智能体的架构", [
#         ("So how do we actually wire up the brain? The modern recipe is a hierarchy.",
#          "那我们到底如何搭建这个大脑？现代的范式，是一个分层结构。"),
#         ("Top-left, in panel (a): a human says 'take an apple to my room,' and the agent splits this into task planning, then action planning.",
#          "左上角的 (a)：人说“把一个苹果拿到我房间”，智能体把它拆成两步——先做任务规划，再做动作规划。"),
#         ("Top-right, panel (b), answers a subtle question — how do you feed vision into a language model?",
#          "右上角的 (b)，回答了一个微妙的问题——你如何把视觉喂给一个语言模型？"),
#         ("There are four ways, from symbolic to neural: an object list, an image caption, a scene graph, or raw visual tokens.",
#          "有四种方式，从符号到神经：物体列表、图像描述、场景图、或者原始的视觉 token。"),
#         ("Panel (c) is high-level task planning: an LLM or VLM breaks the goal into steps — go to the kitchen, find the apple, pick it up.",
#          "(c) 是高层任务规划：一个 LLM 或 VLM 把目标拆解成步骤——去厨房、找到苹果、拿起苹果。"),
#         ("And crucially, it can replan when reality surprises it — if the apple is in the fridge, it adds the step 'open the fridge.'",
#          "而最关键的是，当现实出乎意料时，它能够重新规划——如果苹果在冰箱里，它就会补上一步“打开冰箱”。"),
#         ("Panel (d) is low-level action planning: each sub-task becomes concrete grounding, navigation, or grasping, often through a VLA model that outputs a target and a location.",
#          "(d) 是低层动作规划：每个子任务，被落地成具体的定位、导航或抓取，通常由一个 VLA 模型输出“目标”和“位置”。"),
#         ("The deep idea here is the System-2 versus System-1 split: slow deliberate reasoning by the LLM on top, fast reactive control by the VLA below — and that's the dominant paradigm today.",
#          "这里的深层思想，是“系统二 / 系统一”的分工：上层由 LLM 做缓慢的深思熟虑，下层由 VLA 做快速的反应式控制——这正是当下的主流范式。"),
#     ]),

#     (12, "数据采集与仿真到现实", [
#         ("Every powerful model is hungry for data, and embodied AI is bottlenecked by it.",
#          "每一个强大的模型都对数据极度饥渴，而具身智能恰恰被数据卡住了脖子。"),
#         ("The data comes from two worlds, shown across the top.",
#          "数据来自两个世界，展示在最上方。"),
#         ("Real-world data — robot teleoperation and human demonstration videos — is high quality but slow and expensive to collect.",
#          "真实世界数据——机器人遥操作和人类示范视频——质量高，但采集起来又慢又贵。"),
#         ("Simulated data — expert demonstrations and auto-labeled scenes — is cheap and endlessly scalable.",
#          "仿真数据——专家示范和自动标注的场景——便宜，而且可以无限扩展。"),
#         ("And it's deeply multimodal: video, text, RGB-D, tactile, point cloud, even voice.",
#          "而且它是深度多模态的：视频、文本、RGB-D、触觉、点云，甚至语音。"),
#         ("But the moment you train in sim and deploy in real, you hit the reality gap — and the bottom row shows five ways to cross it.",
#          "但只要你在仿真里训练、到现实中部署，就会撞上“现实鸿沟”——底部这一行，展示了跨越它的五种方法。"),
#         ("Real2Sim2Real reconstructs the real scene inside the simulator; TRANSIC adds human-in-the-loop corrections; domain randomization scrambles the simulation so the real world looks like just one more variation.",
#          "Real2Sim2Real，把真实场景在仿真器里重建出来；TRANSIC，引入“人在回路”的纠正；域随机化，则把仿真搅得五花八门，让真实世界看起来只是其中一种变化而已。"),
#         ("System identification goes the other way — it calibrates the simulator's physics to match reality; and Lang4Sim2Real uses language as the domain-invariant anchor.",
#          "系统辨识则反其道而行——它去标定仿真的物理参数，让它匹配现实；而 Lang4Sim2Real，用语言作为跨域不变的锚点。"),
#         ("The essence is two opposing philosophies: either make the simulation match reality, or make your policy so robust it doesn't care which world it's in.",
#          "本质是两种对立的哲学：要么让仿真去贴近现实，要么把你的策略训练得足够鲁棒，鲁棒到它根本不在乎自己身处哪个世界。"),
#     ]),

#     (13, "多种运动模式的具身控制", [
#         ("Once you have a brain and a plan, the body still has to actually move — that's control.",
#          "当你有了大脑和计划，身体还得真正动起来——这就是控制。"),
#         ("There are three columns here, organized by capability.",
#          "这里有三列，按能力划分。"),
#         ("On the left, bipedal and quadruped control: picking up objects, climbing, crossing obstacles, running, walking, roaming.",
#          "左边，是双足和四足控制：拾取物体、攀爬、跨越障碍、奔跑、行走、漫游。"),
#         ("In the middle, humanoid control — climbing, writing, high-fiving, even leaping — a blend of fine manipulation and whole-body athleticism.",
#          "中间，是人形控制——攀爬、书写、击掌，甚至跳跃——这是精细操作与全身运动能力的结合。"),
#         ("On the right, multi-robot control: collaborating, finding and planning paths together.",
#          "右边，是多机器人控制：协同合作、共同寻找并规划路径。"),
#         ("And control is genuinely hard — it's high-dimensional, contact-rich, and it has to stay stable in real time.",
#          "控制是真的难——它维度高、富含接触，而且必须实时保持稳定。"),
#         ("The modern answer is reinforcement learning in simulation, then sim-to-real, with learned controllers steadily replacing hand-tuned ones.",
#          "现代的答案，是在仿真中做强化学习，再做 sim-to-real，并让学习出来的控制器，一步步取代手工调参的控制器。"),
#         ("The essence: control is where intelligence finally meets physics — because the most brilliant plan in the world is worthless if the robot falls over.",
#          "本质是：控制，是智能最终与物理相遇的地方——因为再天才的计划，只要机器人一摔倒，就一文不值。"),
#     ]),

#     (14, "面向机器人学习的世界模型", [
#         ("Now we move into part two — and here's the brain's secret weapon: the world model.",
#          "现在我们进入第二部分——这里是大脑的秘密武器：世界模型。"),
#         ("So what is a world model? It's a predictive model of how the environment evolves under your actions — in plain terms, the robot's imagination.",
#          "那么，什么是世界模型？它是一个预测模型，预测环境在你的动作下将如何演变——说白了，就是机器人的想象力。"),
#         ("This slide lays out three ways to use it, one per row.",
#          "这一页列出了它的三种用法，每行一种。"),
#         ("In section three, the world model is folded into the policy itself — through inverse dynamics, shared backbones, mixture-of-experts, unified VLA, or latent designs.",
#          "在第三节，世界模型被折叠进策略本身——通过逆动力学、共享骨干、专家混合、统一 VLA、或潜空间设计。"),
#         ("In section four, the world model becomes a simulator — a learned environment for reinforcement learning and for evaluation.",
#          "在第四节，世界模型变成一个仿真器——一个用于强化学习和评估的、学习得到的环境。"),
#         ("And in section five, it becomes a video generator — imagining future frames, made controllable, structure-aware, and eventually foundation-scale.",
#          "在第五节，它又变成一个视频生成器——想象未来的画面，并让它可控、能感知结构，最终走向基础模型的规模。"),
#         ("Here's the motivation, and it's important: purely reactive policies hit a ceiling on long-horizon tasks.",
#          "这里的动机很重要：纯反应式的策略，在长程任务上会撞到天花板。"),
#         ("A world model breaks that ceiling by giving the agent foresight — the ability to think before it acts.",
#          "而世界模型，通过赋予智能体“预见力”——也就是“先思考、再行动”的能力——打破了这层天花板。"),
#     ]),

#     (15, "机器人策略学习的世界模型时间线", [
#         ("This slide is basically a family tree of the field, and it's evolving fast.",
#          "这一页，基本就是这个领域的“家族谱”，而且它演化得飞快。"),
#         ("The top branch is the world model for policy.",
#          "上面这条分支，是“面向策略的世界模型”。"),
#         ("It starts back in 2023 with works like UniPi and GR-1, tightens through DreamVLA, UniVLA, and WorldVLA, and by 2026 explodes into CosmosPolicy, GigaWorld, JEPA-VLA, and many more.",
#          "它从 2023 年的 UniPi、GR-1 起步，经由 DreamVLA、UniVLA、WorldVLA 不断收紧，到 2026 年，更是爆发出 CosmosPolicy、GigaWorld、JEPA-VLA 等一大批工作。"),
#         ("The clear trend is from decoupled — predict first, then act — toward fully integrated, where prediction and action happen together.",
#          "清晰的趋势是：从“解耦”——先预测、再行动——走向“完全融合”，让预测和行动同时发生。"),
#         ("The bottom branch is the world model as simulator, moving from just validating and ranking candidate actions, to serving as a real RL environment, to actually co-evolving with the policy.",
#          "下面这条分支，是“作为仿真器的世界模型”：从仅仅验证、排序候选动作，到充当真正的强化学习环境，再到与策略真正地“共同进化”。"),
#         ("The color-coded legend on the right is the taxonomy itself — IDM-style, unified VLA, single-backbone, mixture-of-transformers, latent modeling, validation, and RL.",
#          "右边那个按颜色编码的图例，本身就是一套分类法——IDM 式、统一 VLA、单骨干、Transformer 混合、潜空间建模、验证、以及强化学习。"),
#         ("The deep takeaway: world modeling is no longer a bolt-on predictor — it's being absorbed straight into the core of the policy.",
#          "深层结论是：世界模型，不再是一个外挂的预测器——它正被直接吸收进策略的核心。"),
#     ]),

#     (16, "世界模型的架构范式", [
#         ("Let's zoom into the architectures — exactly how do you couple prediction with action?",
#          "我们放大来看架构——预测和行动，到底是怎么耦合的？"),
#         ("The top row shows three styles of rising integration.",
#          "上面一行，展示了三种融合程度递增的风格。"),
#         ("In (a), the IDM-style: a video model predicts future frames, and an inverse dynamics model reads off the action — intuitive, but prediction errors pile up over time.",
#          "(a) 是 IDM 式：视频模型预测未来的帧，再由逆动力学模型“读出”动作——直观，但预测误差会随时间不断累积。"),
#         ("In (b), the single-backbone style: one shared network models video and action jointly, in a common latent space.",
#          "(b) 是单骨干式：一个共享网络，在同一个潜空间里，联合建模视频和动作。"),
#         ("In (c), the mixture-of-transformers style: separate video and action experts, but they talk to each other through joint attention — specialized, yet tightly coupled.",
#          "(c) 是 Transformer 混合式：视频专家和动作专家各自独立，但通过“联合注意力”彼此对话——既专精，又紧密耦合。"),
#         ("The bottom row shows two routes built on multimodal LLMs.",
#          "下面一行，展示了两条构建在多模态大模型之上的路线。"),
#         ("On the left, a unified vision-language-action model outputs reasoning, a visual prediction, and an action, all from one backbone.",
#          "左边，统一的视觉-语言-动作模型，用一个骨干同时输出推理、视觉预测和动作。"),
#         ("On the right, latent world modeling predicts in a compact latent space — JEPA-style — skipping pixels entirely, then mapping straight to action, which is far more efficient.",
#          "右边，潜空间世界建模，在一个紧凑的潜空间里做预测——JEPA 风格——完全跳过像素，再直接映射到动作，效率高得多。"),
#         ("The deep design axis is simply how tightly you fuse prediction and action — tighter transfers more world knowledge but is harder to train, and honestly, the field hasn't converged yet, which is exactly what makes it exciting.",
#          "深层的设计轴线，其实就是：你把预测和动作融合得多紧——越紧，迁移的世界知识越多，但也越难训练；说实话，这个领域还没收敛，而这恰恰是它最激动人心的地方。"),
#     ]),

#     (17, "世界模型的两种用途", [
#         ("Here are the two ways a world model actually serves a policy.",
#          "这里是世界模型服务于策略的两种方式。"),
#         ("On the left, the world model for reinforcement learning: it becomes the environment itself.",
#          "左边，是用于强化学习的世界模型：它本身变成了环境。"),
#         ("The policy rolls out actions inside imagination, a reward model scores the imagined outcomes, and the policy updates — all without ever touching the real robot.",
#          "策略在“想象”中推演动作，一个奖励模型给想象出的结果打分，然后策略更新——整个过程，完全不碰真实机器人。"),
#         ("On the right, the world model for validation: at decision time, the agent imagines the result of several candidate actions, scores them — 0.6, 0.8, 0.3 — and picks the best.",
#          "右边，是用于验证的世界模型：在决策时刻，智能体想象出几个候选动作的结果，给它们打分——0.6、0.8、0.3——然后挑出最好的那个。"),
#         ("If that sounds familiar, it should — it's essentially learned Model Predictive Control.",
#          "如果你觉得这很眼熟，那就对了——它本质上就是“学出来的模型预测控制”，也就是 MPC。"),
#         ("At the bottom is the unified view of robotic video world models — one core engine, conditioned on action, observation, language, and structure, and supervised by imagination itself.",
#          "底部，是机器人视频世界模型的统一视角——一个核心引擎，以动作、观察、语言和结构为条件，并由“想象”本身来监督。"),
#         ("The essence: it's the same predictive engine running in two modes — offline to train the policy, and online to choose the action — and both turn imagination into better decisions.",
#          "本质是：同一个预测引擎，运行在两种模式下——离线训练策略，在线挑选动作——而两者，都是把“想象”转化为更好的决策。"),
#     ]),

#     (18, "具身智能安全：能力与风险二象性", [
#         ("Now part three — the shadow side — and it opens with one profound idea: capability-risk duality.",
#          "现在进入第三部分——影子的一面——它以一个深刻的思想开场：能力与风险的二象性。"),
#         ("On the left, in blue, capabilities grow outward — from perception, to cognition, to planning, to action, all the way out to a full agentic system.",
#          "左边，蓝色的部分，是能力的向外生长——从感知，到认知，到规划，到行动，一直延伸到完整的智能体系统。"),
#         ("On the right, in red, is the mirror image — every new capability opens a new attack surface: perceptual, cognitive, decisional, behavioral, and agentic attacks.",
#          "右边，红色的部分，是它的镜像——每一项新能力，都打开了一个新的攻击面：感知攻击、认知攻击、决策攻击、行为攻击、智能体攻击。"),
#         ("And here's the uncomfortable truth: the very things that make an embodied agent powerful are the same things that make it dangerous.",
#          "这里有一个令人不安的真相：让一个具身智能体变强大的那些东西，恰恰也是让它变危险的东西。"),
#         ("A more capable robot is, by definition, a larger attack surface.",
#          "一个能力更强的机器人，按定义，就是一个更大的攻击面。"),
#         ("And unlike a chatbot, when an embodied agent is compromised, the damage is physical — it can hit a person, crash a car, or break things.",
#          "而且，与聊天机器人不同，当一个具身智能体被攻破时，损害是物理性的——它可能打到人、撞毁车，或者损坏东西。"),
#         ("The deep lesson: safety cannot be bolted on at the end — it has to scale together with capability; as we push the blue outward, we have to push the red back just as hard.",
#          "深层教训是：安全不能等到最后再外挂上去——它必须与能力同步扩展；我们把蓝色向外推多远，就得把红色往回压多狠。"),
#     ]),

#     (19, "具身智能安全：攻击面", [
#         ("This slide maps concrete attacks across the four capability layers, arranged around the agentic system in the center.",
#          "这一页，把四个能力层上的具体攻击都标了出来，围绕着中心的“智能体系统”排布。"),
#         ("Top-left is the perception attack — adversarial attacks, with seventy-six reviewed papers, plus backdoor and sensor attacks — leading to misread road signs and security failures.",
#          "左上角，是感知攻击——对抗攻击，光被综述的论文就有 76 篇，再加上后门攻击和传感器攻击——会导致误读路标、安防系统失效。"),
#         ("Top-right is the cognition attack — jailbreaks and emerging risks that hit scene understanding and spatial reasoning, causing wrong navigation and poor environment assessment.",
#          "右上角，是认知攻击——越狱和新兴风险，攻击的是场景理解和空间推理，造成错误的导航决策和糟糕的环境评估。"),
#         ("Bottom-right is the planning attack — adversarial, jailbreak, and backdoor attacks on task and trajectory planning — leading to collisions and bypassed safety mechanisms.",
#          "右下角，是规划攻击——针对任务规划和轨迹规划的对抗、越狱、后门攻击——会导致碰撞、以及安全机制被绕过。"),
#         ("Bottom-left is the action-and-interaction attack — corrupting control and human-robot interaction, causing physical harm and broken trust.",
#          "左下角，是行动与交互攻击——破坏控制和人机交互，造成物理伤害和信任崩塌。"),
#         ("Now notice something: adversarial attacks on perception dominate the count, at seventy-six — the eyes are simply the easiest part to fool.",
#          "注意一个细节：针对感知的对抗攻击，数量最多，高达 76 篇——眼睛，就是最容易被骗的那一部分。"),
#         ("And the deepest point is propagation: fool the perception at the inner layer, and the error cascades outward, breaking the entire stack downstream.",
#          "而最深层的要点，是“传播”：你在内层骗过了感知，错误就会层层向外级联，把下游的整个技术栈全部冲垮。"),
#     ]),

#     (20, "具身智能安全：攻防全景与总结", [
#         ("Finally, this Sankey diagram captures the whole safety landscape in a single flow.",
#          "最后，这张桑基图，用一条条流，把整个安全版图浓缩在了一起。"),
#         ("On the far left are the five layers — perception, cognition, planning, action, and agentic; they split in the middle into attack versus defense; and on the right they fan out into concrete techniques, from adversarial and sensor attacks to robust training, robust inference, and anti-spoofing.",
#          "最左边，是五个层级——感知、认知、规划、行动、智能体；它们在中间分成“攻击”与“防御”两支；再到右边，扇形铺开成具体的技术——从对抗、传感器攻击，到鲁棒训练、鲁棒推理和反欺骗。"),
#         ("And the width of each stream is the number of papers, so you can literally see where the community's effort flows — heavily toward perception.",
#          "而每条流的宽度，就是论文的数量，所以你能一眼看出，社区的精力都流向了哪里——重重地压在了感知上。"),
#         ("The reassuring message is that for every attack, a defense is emerging, and the mature pattern is defense-in-depth — layered, redundant safeguards running from the sensor all the way to the actuator.",
#          "令人安心的信息是：每一种攻击，都有相应的防御正在涌现；而成熟的范式是“纵深防御”——从传感器一路到执行器，层层设防、冗余兜底。"),
#         ("So let me close by tying the three parts together.",
#          "那么，请允许我把三部分收束起来作结。"),
#         ("Part one built the body and the senses; part two gave it a predictive, world-model brain; part three armored it with safety.",
#          "第一部分，造出了身体和感官；第二部分，赋予了它一个会预测的、世界模型构成的大脑；第三部分，为它披上了安全的铠甲。"),
#         ("That is the full stack of embodied AI — the bridge from cyber space into the physical world.",
#          "这，就是具身智能的完整技术栈——一座从赛博空间通往物理世界的桥。"),
#         ("And the future belongs to systems that are all three at once: capable, foresighted, and safe.",
#          "而未来，属于那些同时做到这三点的系统：有能力、能预见、且安全。"),
#         ("Thank you.",
#          "谢谢大家。"),
#     ]),
# ]


# def main():
#     out_dir = "/workspace/jca3code/jiangchaokang/assets/media/blog/script/talk"
#     os.makedirs(out_dir, exist_ok=True)

#     for num, topic, sents in pages:
#         sentences = [
#             {"en": " ".join(en.split()), "zh": " ".join(zh.split())}
#             for en, zh in sents
#         ]
#         data = {"page": num, "topic": topic, "sentences": sentences}
#         filename = f"{num:02d}_{topic}.json"
#         path = os.path.join(out_dir, filename)
#         with open(path, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#         en_chars = sum(len(s["en"]) for s in sentences)
#         zh_chars = sum(len(s["zh"]) for s in sentences)
#         print(f"已生成: {path}  ({len(sentences)} 句 / EN {en_chars} 字符 / ZH {zh_chars} 字)")

#     print(f"\n全部完成！共生成 {len(pages)} 个 JSON 文件，位于 ./{out_dir}/ 目录下。")
#     print("提示: talk2video.py 会优先读取 *.json；如目录里还残留旧的 *.txt，可一并删除以免混淆。")


# if __name__ == "__main__":
#     main()


# ------------------------------- ------------------------------- ------------------------------- ------------------------------- ------------------------------- -------------------------------


# -*- coding: utf-8 -*-
"""
运行后在指定目录生成 talk/ 文件夹，内含 11 个 .json 文件。
每个文件是对应 PPT 页面的「逐句中英对照」讲稿，结构为:
    {"page": 1, "topic": "标题",
     "sentences": [{"en": "...", "zh": "..."}, ...]}

设计要点:
  * 以「句」为对齐单位 —— 同一份句子列表同时驱动 TTS 配音与字幕，
    因此「英文语音 / 英文字幕 / 中文字幕」三者天然一一对应。
  * 讲稿对应论文: GE-Sim 2.0: A Roadmap Towards Comprehensive Closed-loop
    Video World Simulators for Robotic Manipulation (arXiv:2605.27491, AgiBot)。
  * 口语化、通俗易懂，但坚持讲清底层原理与系统逻辑。
直接运行: python generate_talk.py
"""
import os
import json

# (页码, 主题, [(英文句, 中文句), ...])
pages = [
    (1, "标题", [
        ("Hi everyone, welcome.",
         "大家好，欢迎观看。"),
        ("Today I'll walk you through a paper I really like — GE-Sim 2.0, from the AgiBot Genie team.",
         "今天我带大家读一篇我很喜欢的论文——来自智元 Genie 团队的 GE-Sim 2.0。"),
        ("Its full title is: a roadmap towards comprehensive closed-loop video world simulators for robotic manipulation.",
         "它的全名是：迈向面向机器人操作的、全面闭环的视频世界模拟器的路线图。"),
        ("That's a mouthful, but the key word is simple — closed-loop.",
         "标题有点长，但关键词很简单——闭环。"),
        ("The big idea is to turn a video generation model into a real environment that a robot policy can train and be tested inside.",
         "核心想法，是把一个视频生成模型，变成机器人策略真正能在里面训练、被测试的环境。"),
        ("Let's see how they pull it off.",
         "我们来看看，他们是怎么做到的。"),
    ]),

    (2, "GE-Sim 2.0 总览", [
        ("This one diagram is basically the whole paper, so let's read it slowly.",
         "这一张图基本就是整篇论文，我们慢慢读。"),
        ("On the top-left are the inputs.",
         "左上角是输入。"),
        ("The visual input is multi-view history frames — a left view, a head view, and a right view — passed through a sampler into a long-horizon context.",
         "视觉输入是多视角历史帧——左视角、头部视角、右视角——经过采样器，变成长时程的上下文记忆。"),
        ("The action input is a robot trajectory, which gets calibrated and projected into a condition the model can read.",
         "动作输入是一段机器人轨迹，它会被标定、投影，变成模型能读懂的条件。"),
        ("These two streams feed the core in the middle — GE-Sim 2.0, an action-conditioned world simulator.",
         "这两路信息送进中间的核心——GE-Sim 2.0，一个动作条件化的世界模拟器。"),
        ("Given the action, it rolls out what the robot will see next, in all three views at once.",
         "给定动作，它就推演出机器人接下来会看到什么，而且三个视角同时生成。"),
        ("Now here's what makes version 2.0 special — the two modules at the bottom.",
         "而真正让 2.0 与众不同的，是下面这两个模块。"),
        ("On the bottom-left, a proprioceptive state expert reads the robot's joint angles and gripper states straight out of the video latent.",
         "左下角，一个本体状态专家，直接从视频隐空间里读出机器人的关节角和夹爪状态。"),
        ("On the bottom-right, a VLM-based world judge watches the generated video and scores whether the task is being done — that's an automatic reward.",
         "右下角，一个基于视觉语言模型的世界裁判，看着生成的视频，判断任务有没有完成——这就是一个自动奖励。"),
        ("So the simulator no longer just shows pixels; it also reports state and reward — exactly what a policy needs to close the loop.",
         "所以这个模拟器不再只是给你画面；它还给出状态和奖励——这正是策略闭环所需要的一切。"),
    ]),

    (3, "视觉专家与本体状态专家", [
        ("Let's zoom into the engine room — how vision and state are actually produced.",
         "我们放大看看引擎内部——视觉和状态到底是怎么生成的。"),
        ("On the far left, two things go in: the corresponding video frames, and the action conditions.",
         "最左边，有两样东西进入：对应的视频帧，和动作条件。"),
        ("Those little clock-like circles are the action conditions — in a moment we'll see they're the end-effector trajectory drawn into the image.",
         "那些像时钟一样的小圆圈，就是动作条件——待会儿会看到，它们其实是把末端执行器轨迹画进了图像里。"),
        ("Both pass through a VAE into a compact latent space, then into a stack of Video DiT blocks — the diffusion transformer that does the heavy lifting.",
         "两者都经过 VAE 进入紧凑的隐空间，再送入一叠 Video DiT 模块——也就是承担主要计算的扩散 Transformer。"),
        ("The bottom path decodes those latents back into pixels — the visual state, the future video.",
         "下面这条路径，把这些隐变量解码回像素——这就是视觉状态，也就是未来的视频。"),
        ("Now the clever part is the tall block in the middle: the Scalar Mix Layer.",
         "巧妙的地方，在中间这个竖条：标量混合层。"),
        ("It blends features from different DiT layers, because different depths capture different things — some carry geometry, some carry motion.",
         "它把不同 DiT 层的特征融合起来，因为不同深度捕捉的东西不一样——有的偏几何，有的偏运动。"),
        ("That mixed feature feeds the State DiT blocks on the right, which decode the robot's proprioceptive state.",
         "融合后的特征送进右边的 State DiT 模块，解码出机器人的本体状态。"),
        ("Notice its inputs on top: history state, future action, and a noised state — so the state head is itself a small conditional diffusion model.",
         "注意它顶部的输入：历史状态、未来动作，还有一个加噪状态——所以这个状态头本身就是一个小型的条件扩散模型。"),
        ("And the output, on the far right, is exactly what a controller speaks: joint angles and gripper, for both arms, across time.",
         "而最右边的输出，正是机器人控制器所讲的语言：双臂的关节角和夹爪，随时间一帧帧展开。"),
        ("The deep point: the state isn't predicted separately — it's read out of the same latent that draws the video, so picture and pose always agree.",
         "深层的点在于：状态不是另外单独预测的——它是从画视频的同一份隐变量里读出来的，所以画面和姿态永远一致。"),
    ]),

    (4, "世界裁判", [
        ("A simulator that only renders is half a simulator — you also need to know if the task succeeded.",
         "只会画面的模拟器，只是半个模拟器——你还得知道任务到底成没成。"),
        ("That's the job of the World Judge, at the top of this slide.",
         "这就是这页顶部「世界裁判」的工作。"),
        ("It takes the video frames through a vision encoder, and the instruction — here, 'fold the towel' — through a text encoder.",
         "它把视频帧送进视觉编码器，把指令——这里是「叠毛巾」——送进文本编码器。"),
        ("Then it labels every frame along the timeline: orange means the task is ongoing, green means success.",
         "然后它沿时间轴给每一帧打标签：橙色表示任务进行中，绿色表示成功。"),
        ("So a free-form video becomes a clean, machine-verifiable signal — no human needs to sit and watch it.",
         "于是一段自由的视频，就变成了干净的、机器可验证的信号——不需要人坐着盯。"),
        ("The bottom-left lists the six test tasks, from pouring water to cleaning mirror stains.",
         "左下角列出了六个测试任务，从倒水到擦镜面污渍。"),
        ("The middle bar chart is the headline result — agreement error, where lower is better.",
         "中间的柱状图是核心结果——一致性误差，越低越好。"),
        ("Their judge with state scores 0.058, versus 0.125 without state, versus 0.283 for Ctrl-World — they win by a wide margin.",
         "他们带状态的裁判误差是 0.058，不带状态是 0.125，Ctrl-World 是 0.283——他们大幅领先。"),
        ("The right scatter plot puts simulated success rate against real success rate; the closer to the diagonal, the more trustworthy the simulator.",
         "右边的散点图，把模拟成功率和真实成功率放在一起；越靠近对角线，模拟器就越可信。"),
        ("Their fitted line is the steepest and closest to ideal, meaning: if it works in the sim, it tends to work for real.",
         "他们拟合的直线最陡、也最接近理想——意思是：在模拟里成功，现实里大概率也成功。"),
        ("The takeaway: a small, task-aware specialist beats prompting a giant general VLM like Qwen to act as the reward.",
         "结论是：一个小而专、懂任务的裁判，胜过去硬提示一个像 Qwen 那样的通用大模型来当奖励。"),
    ]),

    (5, "GE-Sim 2.0 定位", [
        ("Let's step back and say, in plain words, what GE-Sim 2.0 actually is.",
         "我们退一步，用大白话说说 GE-Sim 2.0 到底是什么。"),
        ("It's an embodied world simulator for robotic manipulation, built on top of GE-Sim 1.0.",
         "它是一个面向机器人操作的具身世界模拟器，建立在 GE-Sim 1.0 之上。"),
        ("Version 1.0 could already generate action-conditioned video — that's the picture part.",
         "1.0 版本已经能做动作条件化的视频生成——这是「画面」那一块。"),
        ("Version 2.0 adds the three things that picture alone was missing.",
         "2.0 版本补上了「只有画面」所缺的三样东西。"),
        ("State estimation, so the policy gets proprioception, not just pixels.",
         "状态估计，让策略拿到本体感知，而不只是像素。"),
        ("Automatic task evaluation, so success becomes a number instead of a human opinion.",
         "自动任务评估，让「成功」变成一个数字，而不是靠人主观判断。"),
        ("And efficient rollout, so you can run this at scale instead of one slow episode at a time.",
         "还有高效推演，让你能大规模地跑，而不是一次只能慢慢跑一条。"),
        ("Put together, it moves from a video toy to a real platform for closed-loop policy learning.",
         "三者合起来，它就从一个视频玩具，升级成了真正能做闭环策略学习的平台。"),
        ("That's the one-sentence thesis: stop just watching the world, and start training inside it.",
         "这就是一句话的主旨：别只是旁观世界，开始在世界里训练。"),
    ]),

    (6, "控制信号注入机制", [
        ("Here's the question that quietly decides everything: how do you tell the model what action to take?",
         "有一个悄悄决定一切的问题：你到底怎么告诉模型，要执行什么动作？"),
        ("Different robots have different arms, joints, and action spaces — a raw number vector simply won't transfer.",
         "不同机器人有不同的手臂、关节、动作空间——一串原始数字向量根本没法通用。"),
        ("Their answer is the signature trick on this slide: pixel-aligned action conditions.",
         "他们的答案，就是这页的招牌技巧：像素对齐的动作条件。"),
        ("Instead of feeding joint numbers, they use forward kinematics to draw the end-effector's future path right into the camera image.",
         "他们不喂关节数字，而是用正向运动学，把末端执行器未来的轨迹，直接画进相机图像里。"),
        ("You can see it at the top of each clip — those colored trails and axis markers are the planned motion.",
         "你能在每段视频上方看到——那些彩色轨迹和坐标轴标记，就是规划好的运动。"),
        ("The color even encodes the gripper: dark means closed, light means open, with left and right arms in different color families.",
         "颜色还编码了夹爪：深色表示闭合，浅色表示张开，左右臂用不同的色系。"),
        ("Because this lives in image space, it's the same representation for any robot — that's the unified control space.",
         "因为它活在图像空间里，所以对任何机器人都是同一种表示——这就是统一的控制空间。"),
        ("The bottom row shows the generated vision state — the arm faithfully following that drawn trajectory.",
         "下面一行是生成的视觉状态——手臂忠实地跟着那条画出来的轨迹运动。"),
        ("The elegance here runs deep: by rendering control as pixels, action and observation finally speak the same language.",
         "这里的优雅很深刻：把控制渲染成像素，动作和观测终于讲上了同一种语言。"),
    ]),

    (7, "高一致性多视角生成", [
        ("Real robots don't see from one camera — they have a head view, plus a wrist camera on each hand.",
         "真实机器人不是只用一个相机——它头上有一个视角，每只手腕上还各有一个相机。"),
        ("So a good simulator has to generate all of them, and keep them consistent with each other.",
         "所以好的模拟器必须把它们都生成出来，而且要彼此一致。"),
        ("Watch the towel in this example: at first it's hidden in the blind spot of the left view.",
         "看这个例子里的毛巾：一开始，它藏在左视角的盲区里。"),
        ("As the left arm moves, the towel comes into frame — and it matches exactly what the head view already showed.",
         "当左臂移动，毛巾进入画面——而且和头部视角早已显示的内容完全吻合。"),
        ("Even the reflection in the mirror is rendered convincingly.",
         "甚至连镜子里的倒影，都生成得令人信服。"),
        ("That's only possible if the model holds one coherent 3D scene in its head, not three independent videos.",
         "这只有在模型脑子里维持着一个统一、连贯的三维场景时才可能做到，而不是三段各自为政的视频。"),
        ("And it matters in practice: a wrist-camera policy and a head-camera policy must be tested on the same world, or the evaluation is a lie.",
         "这在实践中很关键：手腕相机的策略和头部相机的策略，必须在同一个世界里被测试，否则评估就是假的。"),
        ("Consistency across views is what lets the simulation stand in, trustworthily, for reality.",
         "跨视角的一致性，正是让这套模拟，足以可信地替代现实的原因。"),
    ]),

    (8, "分钟级稳定视频生成", [
        ("Most video models look great for a few seconds, then drift into mush.",
         "大多数视频模型，前几秒看着很棒，然后就糊成一团、开始漂移。"),
        ("But real manipulation tasks — pouring, folding, tidying a table — take a long time.",
         "可真实的操作任务——倒水、叠衣服、收拾桌子——都需要很长时间。"),
        ("This slide shows minute-level generation that stays stable and coherent the whole way through.",
         "这页展示的是分钟级的生成，全程都保持稳定和连贯。"),
        ("The trick is a chunk-wise autoregressive design plus a sparse memory.",
         "诀窍在于分块的自回归设计，再加上一套稀疏记忆。"),
        ("The model generates a short chunk, then conditions on a sparse summary of the past to generate the next one.",
         "模型先生成一小段，然后基于对过去的稀疏总结，再生成下一段。"),
        ("Sparse memory is the key phrase: it keeps the important history without dragging the whole long sequence through every step.",
         "稀疏记忆是关键词：它保留重要的历史，又不必让整条长序列在每一步都被拖着走。"),
        ("That keeps the compute tractable while the temporal context stays long.",
         "这样既把计算成本控制住，又让时间上下文保持得足够长。"),
        ("Without this, you simply can't simulate a long-horizon policy end to end — and long-horizon is where real tasks live.",
         "没有这个，你根本没法从头到尾模拟一个长时程策略——而真实任务，恰恰都在长时程里。"),
    ]),

    (9, "视觉与本体联合预测", [
        ("This slide makes the state expert concrete.",
         "这页把状态专家讲得很具体。"),
        ("The simulator generates the future video, and at the same time the state expert decodes proprioception from those very same latents.",
         "模拟器生成未来的视频，与此同时，状态专家从同一份隐变量里解码出本体感知。"),
        ("Look at the radar chart in the upper-left corner.",
         "看左上角那个雷达图。"),
        ("The yellow line is the action condition — what the robot was commanded to do.",
         "黄线是动作条件——也就是给机器人下达的指令。"),
        ("The blue line is the state the model generated — what it thinks actually happened.",
         "蓝线是模型生成的状态——它认为实际发生了什么。"),
        ("J stands for joint, G stands for gripper, and the two lines sit almost on top of each other.",
         "J 代表关节，G 代表夹爪，两条线几乎完全重合。"),
        ("That tight overlap means the simulated robot really did move the way it was told to.",
         "这种紧密重合，意味着模拟里的机器人，确实是按指令在动。"),
        ("Why do we care? Because most policies don't act on pixels alone — they need to know where their own joints are.",
         "为什么在乎这个？因为大多数策略不是只看像素行动的——它们需要知道自己的关节在哪儿。"),
        ("By handing back both the picture and the proprioceptive state, the simulator gives the policy everything it needs to predict its next move.",
         "通过同时交还画面和本体状态，模拟器就给了策略，预测下一步动作所需要的一切。"),
        ("Visual plus proprioceptive — that's what turns a video model into a usable robot environment.",
         "视觉加本体感知——这正是把一个视频模型，变成一个可用机器人环境的关键。"),
    ]),

    (10, "世界模拟器中的评估", [
        ("Now we put every piece together into the closed loop, and this diagram shows the full cycle.",
         "现在我们把每一块拼成闭环，这张图展示了完整的循环。"),
        ("Start on the left: the policy model outputs an action chunk.",
         "从左边开始：策略模型输出一段动作块。"),
        ("That action goes into GE-Sim 2.0 in the center, which simulates what happens next.",
         "动作进入中间的 GE-Sim 2.0，由它来模拟接下来会发生什么。"),
        ("It returns two things: the proprioceptive state — the joint radar in the middle — and the vision state, the generated camera views.",
         "它返回两样东西：本体状态——中间那个关节雷达图——还有视觉状态，也就是生成的相机画面。"),
        ("Both flow back to the policy so it can decide its next action — that's the loop closing.",
         "这两样都流回策略，让它决定下一步动作——闭环就这样合上了。"),
        ("Meanwhile, the vision state also goes to the reward model on the right.",
         "与此同时，视觉状态还会送到右边的奖励模型。"),
        ("Given the instruction — here, 'place the Sprite into the red plastic basket' — it outputs a reward probability over time.",
         "给定指令——这里是「把雪碧放进红色塑料筐」——它就输出一条随时间变化的奖励概率。"),
        ("That curve in the top-right is the success probability climbing as the task gets done.",
         "右上角那条曲线，就是任务逐步完成时，成功概率不断爬升。"),
        ("So in one diagram: the policy acts, the world responds, the judge scores — entirely without a real robot.",
         "所以一张图说清了：策略行动、世界回应、裁判打分——全程不需要一台真实机器人。"),
        ("This is the dream — evaluate a policy thousands of times, safely and cheaply, before it ever touches hardware.",
         "这就是我们梦寐以求的——在策略碰到真实硬件之前，安全地、廉价地，把它评估成千上万次。"),
    ]),

    (11, "世界模拟器中的闭环学习", [
        ("The last slide zooms all the way out to the endgame: a learning flywheel.",
         "最后一页，把视角彻底拉远，看终极目标：一个学习的飞轮。"),
        ("Step one, on the left: record the real-world environment, just once.",
         "第一步，在左边：录制真实世界环境，只需要录一次。"),
        ("Step two, on top: spin that environment up inside a distributed world simulator, and let policies learn closed-loop, in parallel, at scale.",
         "第二步，在上方：把这个环境在分布式世界模拟器里复现，让策略在里面闭环学习、并行、规模化。"),
        ("Step three, on the right: take the improved policy and execute it in the physical world.",
         "第三步，在右边：把改进后的策略，拿到物理世界里执行。"),
        ("Then the new real data flows back to the start, and the wheel turns again.",
         "然后新的真实数据又流回起点，飞轮再转一圈。"),
        ("Remember the reward model? It quietly filters the good rollouts and feeds them back as training data.",
         "还记得那个奖励模型吗？它在背后默默筛选出好的推演，作为训练数据喂回去。"),
        ("In the paper, that filtered behavior cloning gives a fifteen-point jump in real-robot success.",
         "在论文里，这种经过筛选的行为克隆，让真实机器人的成功率，足足跳升了 15 个百分点。"),
        ("And because diffusion was distilled to a few steps, a 25-frame rollout takes just over two seconds on one GPU — fast enough to make this flywheel actually spin.",
         "而正因为扩散被蒸馏到了几步，一段 25 帧的推演，在单张 GPU 上只要两秒多——快到足以让这个飞轮真正转起来。"),
        ("That's the whole vision: the world model becomes the place where robots learn, are judged, and get better — before they ever risk the real world.",
         "这就是全部的愿景：世界模型，成为机器人学习、被评判、变得更强的地方——而这一切，都发生在它们冒险进入真实世界之前。"),
        ("From a view-only video tool to a closed-loop engine for embodied intelligence — that's the leap GE-Sim 2.0 represents. Thanks for watching.",
         "从一个只能看的视频工具，到一台驱动具身智能的闭环引擎——这就是 GE-Sim 2.0 所代表的跨越。感谢观看。"),
    ]),
]


def main():
    out_dir = "/workspace/jca3code/jiangchaokang/assets/media/blog/script/talk"
    os.makedirs(out_dir, exist_ok=True)

    for num, topic, sents in pages:
        sentences = [
            {"en": " ".join(en.split()), "zh": " ".join(zh.split())}
            for en, zh in sents
        ]
        data = {"page": num, "topic": topic, "sentences": sentences}
        filename = f"{num:02d}_{topic}.json"
        path = os.path.join(out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        en_chars = sum(len(s["en"]) for s in sentences)
        zh_chars = sum(len(s["zh"]) for s in sentences)
        print(f"已生成: {path}  ({len(sentences)} 句 / EN {en_chars} 字符 / ZH {zh_chars} 字)")

    print(f"\n全部完成！共生成 {len(pages)} 个 JSON 文件，位于 {out_dir}/ 目录下。")
    print("提示: talk2video.py 会优先读取 *.json；如目录里还残留旧的 *.txt，可一并删除以免混淆。")


if __name__ == "__main__":
    main()