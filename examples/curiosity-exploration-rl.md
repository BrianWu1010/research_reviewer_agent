# How does curiosity improve exploration in reinforcement learning?

## Answer

Curiosity improves exploration by giving the agent an intrinsic reward for experiences it cannot yet predict or has not yet seen. This reward substitutes for or supplements sparse extrinsic reward [1, 4, 9]. Prediction-error curiosity works well in many benchmarks [1, 2], but it is vulnerable to unpredictable noise. Much of the later work therefore refines what counts as "interesting," for example by separating learnable from unlearnable surprise, using episodic novelty, or using model disagreement [3, 5, 6, 8, 10].

## Key findings

**Core mechanism: prediction error or surprise as intrinsic reward.**
- Rewarding a forward model's prediction error, computed in a learned feature space, lets agents reach goals with far fewer interactions under sparse reward. It also drives efficient exploration with no extrinsic reward [1].
- Rewarding experiences a learned transition model predicts poorly (surprisal, k-step learning progress) enabled success on sparse-reward continuous control and Atari RAM tasks. There, ε-greedy and Gaussian noise made no progress [4].
- A large-scale study found that purely curiosity-driven agents do surprisingly well across 54 environments. The curiosity objective was often aligned with hand-designed game rewards, and random features sufficed in many benchmarks [2].
- Experience gathered through curiosity also transfers: it sped up exploration of new levels of the same game [1]. Learned features generalized better than random ones [2].

**Episodic novelty and directed exploration.**
- Episodic Curiosity rewards observations that are many environment steps from anything in episodic memory. It outperformed ICM on ViZDoom and DMLab navigation [3].
- Never Give Up uses k-nearest-neighbour episodic novelty over embeddings trained with inverse dynamics, which biases novelty toward controllable aspects of the environment. It also uses one network to represent many exploration/exploitation trade-offs. It doubled the base agent's performance on hard-exploration Atari games and was the first to obtain non-zero reward in Pitfall! without demonstrations [9].

**Main failure mode: stochastic or unpredictable observations.**
- Prediction-based rewards are limited in stochastic setups [2]. Agents can be drawn to hardly predictable outcomes, the "couch-potato" problem [3]. Prediction-error curiosity is also hindered by curiosity traps [6].
- Proposed remedies differ in approach:
  - Reachability against episodic memory [3].
  - Ensemble disagreement, which is designed to avoid getting stuck in stochastic dynamics [10].
  - A free-energy-based hidden-state curiosity (KL between predictive prior and posterior), which stayed resilient to noise in maze tasks [6].
  - Rewarding the novelty of the surprise via a surprise memory, which boosted performance in sparse-reward settings including Noisy-TV and Atari [8].
  - Subtracting a learned noise-floor baseline so that reward falls to zero on stochastic transitions and remains high on learnable ones [5].
  - Calibrating curiosity with peer context in multi-agent settings while filtering noisy surprise [7].
- Paper [5] also argues that earlier prediction-error formulations are special cases of its framework, each with a particular approximation of the error baseline.

**Combination with other signals and broader framing.**
- In maze navigation, entropy and curiosity both improved exploration, and the effect was strongest when they were combined [6].
- Surveys frame intrinsic motivation, including surprise and novelty, as a response to hard exploration and sparse rewards. They suggest it may also support hierarchies of transferable skills [11, 12].

## Open questions and gaps

- **Comparability of the noise-robust methods.** The papers each address noise in different ways and on different benchmarks, so the evidence does not show which approach is best [3, 5, 6, 8, 10]. Several results are reported only in abstracts without quantitative detail [6, 7, 10].
- **Limited evaluation scope.** Curiosity-Critic was tested only on a stochastic grid world and reports world-model accuracy rather than task reward [5]. The maze study is likewise simulation-only [6].
- **Feature space.** Random features sufficed in many benchmarks but generalized worse than learned features [2]. How to choose features for the harder settings is not resolved by these notes.
- **Skills and abstraction.** The claim that curiosity supports skill hierarchies and action abstraction comes from surveys and is not backed by empirical detail in these notes [11, 12].
- **Multi-agent calibration.** The benefit of peer-context calibration is asserted in the abstract and not analyzed in detail [7].

## Reviewer assessment

**Verdict:** needs_more (6/10). The answer covers the core mechanism, the noisy-TV failure mode, remedies and open gaps, and it is mostly well grounded in the cited papers. But the foundational set is incomplete. It lacks several seminal works that a researcher would expect: count-based/pseudo-count exploration, VIME, RND, Schmidhuber's formal theory of curiosity, and the Noisy-TV analysis in the Burda et al. paper itself. The answer also never explains why curiosity helps (e.g. coverage of state space, reducing uncertainty, sparse-reward credit), beyond reporting benchmark results. Evidence from recent noise-robust methods ([5], [6], [7]) is thin, being abstract-level or on toy domains. Agent57, Go-Explore, and the classic distinction between novelty and prediction-error/learning-progress are also missing. These gaps mean the answer is a decent but not yet solid starting point.

Still missing:
- Exploration by Random Network Distillation
- Unifying Count-Based Exploration and Intrinsic Motivation (pseudo-counts)
- #Exploration: A Study of Count-Based Exploration for Deep RL
- VIME: Variational Information Maximizing Exploration
- Incentivizing Exploration in RL with Deep Predictive Models (Stadie)
- Schmidhuber formal theory of creativity, fun, and intrinsic motivation / learning progress
- Intrinsic motivation: Oudeyer and Kaplan, what is intrinsic motivation, computational approaches
- Agent57 / Go-Explore hard-exploration results
- Theoretical explanation of why curiosity aids exploration (uncertainty, information gain, state coverage)
- Noisy-TV problem and learning-progress / Bayesian surprise remedies
- Curiosity-driven exploration limitations: detachment, derailment, catastrophic forgetting in intrinsic reward

## References

1. **Curiosity-driven Exploration by Self-supervised Prediction**. Deepak Pathak, Pulkit Agrawal, Alexei A. Efros et al. (2017). [arXiv:1705.05363](http://arxiv.org/abs/1705.05363v1) (relevance 10/10)
2. **Large-Scale Study of Curiosity-Driven Learning**. Yuri Burda, Harri Edwards, Deepak Pathak et al. (2018). [arXiv:1808.04355](http://arxiv.org/abs/1808.04355v1) (relevance 10/10)
3. **Episodic Curiosity through Reachability**. Nikolay Savinov, Anton Raichuk, Raphaël Marinier et al. (2018). [arXiv:1810.02274](http://arxiv.org/abs/1810.02274v5) (relevance 10/10)
4. **Surprise-Based Intrinsic Motivation for Deep Reinforcement Learning**. Joshua Achiam, Shankar Sastry (2017). [arXiv:1703.01732](http://arxiv.org/abs/1703.01732v1) (relevance 9/10)
5. **Curiosity-Critic: Cumulative Prediction Error Improvement as a Tractable Intrinsic Reward for World Model Training**. Vin Bhaskara, Haicheng Wang (2026). [arXiv:2604.18701](http://arxiv.org/abs/2604.18701v3) (relevance 9/10)
6. **Intrinsic Rewards for Exploration without Harm from Observational Noise: A Simulation Study Based on the Free Energy Principle**. Theodore Jerome Tinker, Kenji Doya, Jun Tani (2024). [arXiv:2405.07473](http://arxiv.org/abs/2405.07473v1) (relevance 9/10)
7. **Wonder Wins Ways: Curiosity-Driven Exploration through Multi-Agent Contextual Calibration**. Yiyuan Pan, Zhe Liu, Hesheng Wang (2025). [arXiv:2509.20648](http://arxiv.org/abs/2509.20648v3) (relevance 9/10)
8. **Beyond Surprise: Improving Exploration Through Surprise Novelty**. Hung Le, Kien Do, Dung Nguyen et al. (2023). [arXiv:2308.04836](http://arxiv.org/abs/2308.04836v2) (relevance 9/10)
9. **Never Give Up: Learning Directed Exploration Strategies**. Adrià Puigdomènech Badia, Pablo Sprechmann, Alex Vitvitskyi et al. (2020). [arXiv:2002.06038](http://arxiv.org/abs/2002.06038v1) (relevance 9/10)
10. **Self-Supervised Exploration via Disagreement**. Deepak Pathak, Dhiraj Gandhi, Abhinav Gupta (2019). [arXiv:1906.04161](http://arxiv.org/abs/1906.04161v1) (relevance 9/10)
11. **A survey on intrinsic motivation in reinforcement learning**. Arthur Aubret, Laetitia Matignon, Salima Hassas (2019). [arXiv:1908.06976](http://arxiv.org/abs/1908.06976v2) (relevance 9/10)
12. **An information-theoretic perspective on intrinsic motivation in reinforcement learning: a survey**. Arthur Aubret, Laetitia Matignon, Salima Hassas (2022). [arXiv:2209.08890](http://arxiv.org/abs/2209.08890v1) (relevance 9/10)

## Paper notes

### [1] Curiosity-driven Exploration by Self-supervised Prediction

- **Relevance:** Directly addresses the question by defining curiosity as an intrinsic reward, namely the agent's error in predicting the consequences of its own actions. The abstract describes how this reward drives exploration when extrinsic rewards are sparse or absent. It also describes how the feature space is chosen so that the agent ignores parts of the environment it cannot affect.
- **Contribution:** An intrinsic curiosity formulation in which the reward is the prediction error of a forward model operating in a visual feature space learned by a self-supervised inverse dynamics model. The formulation scales to high-dimensional continuous state spaces such as images, avoids direct pixel prediction, and ignores environment aspects that cannot affect the agent.
- **Method:** The agent receives an intrinsic reward equal to its error in predicting the consequence of its own actions. Prediction happens in a feature space learned by a self-supervised inverse dynamics model. The approach is evaluated in VizDoom and Super Mario Bros. under three settings: sparse extrinsic reward, no extrinsic reward, and generalization to unseen scenarios such as new levels of the same game.
- **Findings:**
  - With sparse extrinsic reward, curiosity allows the agent to reach the goal with far fewer environment interactions.
  - With no extrinsic reward, curiosity pushes the agent to explore more efficiently.
  - In unseen scenarios such as new levels of the same game, knowledge gained from earlier curiosity-driven experience helps the agent explore new places much faster than starting from scratch.

### [2] Large-Scale Study of Curiosity-Driven Learning

- **Relevance:** Provides large-scale empirical evidence on how curiosity, defined as prediction error used as an intrinsic reward, drives agent behavior without extrinsic rewards. It shows when this works (alignment with game rewards, choice of feature space) and when it fails (stochastic environments), which bears directly on how curiosity improves exploration.
- **Contribution:** The first large-scale study of purely curiosity-driven learning, with no extrinsic rewards, across 54 standard benchmark environments including Atari. It also compares feature spaces for computing prediction error and demonstrates a limitation of prediction-based curiosity in stochastic setups.
- **Method:** Agents are trained using prediction error as the intrinsic reward signal, with no extrinsic reward. The study covers 54 benchmark environments, including the Atari suite. Different feature spaces for computing prediction error are compared, including random features and learned features. Generalization is tested, e.g. to novel levels in Super Mario Bros. Stochastic setups are also examined.
- **Findings:**
  - Purely curiosity-driven agents achieve surprisingly good performance across many environments without extrinsic rewards.
  - The intrinsic curiosity objective is highly aligned with the hand-designed extrinsic rewards in many game environments.
  - Random features are sufficient for computing prediction error in many popular RL game benchmarks.
  - Learned features appear to generalize better than random features, e.g. to novel game levels in Super Mario Bros.
  - Prediction-based rewards have limitations in stochastic setups.
- **Limitations (from abstract):**
  - Prediction-error-based curiosity is limited in stochastic environments.
  - Random features, though sufficient for many benchmarks, generalize less well than learned features.

### [3] Episodic Curiosity through Reachability

- **Relevance:** Shows one concrete mechanism by which curiosity aids exploration: an intrinsic novelty bonus, based on episodic memory and reachability in environment steps, densifies sparse rewards. It also addresses a known failure mode of prediction-error curiosity, the "couch-potato" problem.
- **Contribution:** A new curiosity method, Episodic Curiosity (EC), that computes a novelty bonus by comparing the current observation to observations in episodic memory. The comparison uses how many environment steps it takes to reach the current observation from those in memory. This avoids the couch-potato issue of earlier methods, where agents exploit actions with hardly predictable consequences for instant self-gratification.
- **Method:** The agent adds an intrinsic novelty bonus to the real task reward and trains with standard RL on the combined reward. The bonus is determined by comparing the current observation against an episodic memory of observations. The comparison is based on reachability, i.e. the number of environment steps needed to reach the current observation from the memory entries. The method is evaluated in visually rich 3D environments (ViZDoom, DMLab, MuJoCo) and compared with the ICM curiosity method.
- **Findings:**
  - In ViZDoom and DMLab navigational tasks, the agent outperforms the state-of-the-art curiosity method ICM.
  - In MuJoCo, an ant equipped with the curiosity module learns locomotion from first-person-view curiosity only.
  - Reachability-based comparison against episodic memory incorporates rich information about environment dynamics and overcomes the couch-potato issue of prior work.

### [4] Surprise-Based Intrinsic Motivation for Deep Reinforcement Learning

- **Relevance:** Shows one concrete way curiosity (surprise-driven intrinsic motivation) improves exploration in RL: the agent learns a transition model and is rewarded for experiences that the model predicts poorly, which helps in sparse-reward tasks where ε-greedy or Gaussian noise exploration fails to make progress.
- **Contribution:** Two scalable intrinsic reward formulations that approximate the KL-divergence between the true MDP transition probabilities and a learned model: one based on surprisal, and one based on k-step learning progress. They are used to drive exploration in deep RL.
- **Method:** Learn a model of the MDP transition probabilities concurrently with the policy. Form intrinsic rewards that approximate the KL-divergence of the true transition distribution from the learned model. The two approximations yield surprisal and k-step learning progress. Evaluate on continuous control tasks and Atari RAM games with high-dimensional states and very sparse rewards.
- **Findings:**
  - Surprise-based intrinsic rewards let agents succeed in a wide range of environments with high-dimensional state spaces and very sparse rewards.
  - The approach works on continuous control tasks and Atari RAM games.
  - It outperforms several other heuristic exploration techniques.
  - Simple heuristics such as ε-greedy and Gaussian control noise are insufficient on many tasks, where they make no learning progress.

### [5] Curiosity-Critic: Cumulative Prediction Error Improvement as a Tractable Intrinsic Reward for World Model Training

- **Relevance:** Addresses how curiosity-driven intrinsic rewards can improve exploration by directing an agent toward transitions where the world model can still learn, and away from stochastic, unlearnable ones (the noisy-TV issue). It gives a principled account of what makes curiosity effective: separating epistemic from aleatoric prediction error.
- **Contribution:** Curiosity-Critic, an intrinsic reward based on the improvement in the world model's cumulative prediction error across all visited transitions. It reduces to a tractable per-step surrogate: current prediction error minus the asymptotic error baseline for that transition. The paper also shows that earlier prediction-error curiosity formulations (Schmidhuber 1991 through learned-feature-space variants) are special cases, each corresponding to a particular approximation of this baseline.
- **Method:** A learned critic is co-trained alongside the world model to estimate online the asymptotic error baseline (irreducible noise floor) of each state transition. The intrinsic reward is the current prediction error minus this baseline. The critic only has to learn how hard a transition is to predict, so its estimate converges before the world model saturates. The method is evaluated on a stochastic grid world against prediction-error, visitation-count, and Random Network Distillation (RND) baselines.
- **Findings:**
  - The reward is higher for learnable transitions and collapses toward zero for stochastic ones, separating reducible (epistemic) from irreducible (aleatoric) prediction error online.
  - The critic's estimate of the noise floor converges well before the world model saturates, which redirects exploration toward learnable transitions.
  - Prior prediction-error curiosity formulations emerge as special cases with specific approximations of the error baseline.
  - On a stochastic grid world, Curiosity-Critic outperforms prediction-error, visitation-count, and RND methods in training speed and final world model accuracy.
- **Limitations (from abstract):**
  - Experiments described in the abstract are limited to a stochastic grid world, so generalization to more complex environments is not shown.
  - Evaluation focuses on world model training speed and accuracy; the abstract does not report downstream task reward.

### [6] Intrinsic Rewards for Exploration without Harm from Observational Noise: A Simulation Study Based on the Free Energy Principle

- **Relevance:** Shows how curiosity as an intrinsic reward improves exploration in RL. It compares two formulations, prediction error curiosity and a proposed hidden state curiosity, and tests them alone and combined with policy entropy in maze navigation. It also shows how curiosity can fail when observations contain unpredictable noise (curiosity traps), and how a free-energy-based formulation avoids this.
- **Contribution:** Proposes hidden state curiosity, grounded in the Free Energy Principle. It rewards the KL divergence between the predictive prior and posterior over latent variables. The paper shows this form is robust to curiosity traps, which hinder prediction error curiosity.
- **Method:** Simulation study in maze navigation with six agent types: a baseline with no entropy or curiosity reward, and agents rewarded for entropy and/or prediction error curiosity or hidden state curiosity. The comparison covers exploration efficiency and resilience to observational noise (curiosity traps).
- **Findings:**
  - Entropy and curiosity both lead to efficient exploration, and the effect is strongest when the two are used together.
  - Agents with hidden state curiosity stay resilient to curiosity traps (unpredictable observational noise).
  - Prediction error curiosity agents are hindered by curiosity traps.
  - The authors suggest that implementing the FEP may improve the robustness and generalization of RL models and align artificial with biological learning.
- **Limitations (from abstract):**
  - Evidence comes from simulated maze navigation tasks only.
  - The abstract gives no quantitative results, so the strength of the effects cannot be assessed from it.

### [7] Wonder Wins Ways: Curiosity-Driven Exploration through Multi-Agent Contextual Calibration

- **Relevance:** Addresses how curiosity-based intrinsic motivation can improve exploration in sparse-reward multi-agent RL. It identifies two weaknesses of standard curiosity (confusing environmental stochasticity with novelty, and treating all surprises equally) and proposes calibrating curiosity with multi-agent context to address them.
- **Contribution:** CERMIC, a framework for multi-agent curiosity-driven exploration. It filters noisy surprise signals and dynamically calibrates intrinsic curiosity using context inferred from peer behavior. It also produces intrinsic rewards that are theoretically grounded in information gain.
- **Method:** Agents in decentralized, communication-free MARL infer multi-agent context from peers' behavior novelty. They use it to calibrate a self-supervised curiosity signal and to robustly filter noisy surprise. The resulting intrinsic reward encourages state transitions with high information gain. The approach is inspired by how children calibrate exploration by observing peers. It is evaluated on VMAS, Meltingpot, and SMACv2.
- **Findings:**
  - Exploration with CERMIC significantly outperforms state-of-the-art algorithms in sparse-reward environments, according to the abstract.
  - Evaluation covers the benchmark suites VMAS, Meltingpot, and SMACv2.
  - Calibrating curiosity with inferred peer or multi-agent context, and filtering stochastic noise, is presented as improving exploration over uniform-novelty curiosity.

### [8] Beyond Surprise: Improving Exploration Through Surprise Novelty

- **Relevance:** The paper addresses how surprise-driven curiosity can improve exploration in RL. It proposes rewarding the novelty of the surprise rather than the surprise magnitude, which targets a known failure mode of curiosity: attraction to unpredictable or noisy observations. It therefore bears on how curiosity-based intrinsic rewards should be designed.
- **Contribution:** A new intrinsic reward model, the surprise memory (SM), that rewards surprise novelty instead of the surprise norm. It is meant to augment existing surprise-based intrinsic motivators.
- **Method:** A memory network stores and reconstructs surprises produced by a surprise predictor. The retrieval error of this memory is the estimate of surprise novelty and serves as the intrinsic reward. SM is combined with various surprise predictors.
- **Findings:**
  - SM combined with various surprise predictors exhibits efficient exploring behaviors.
  - SM significantly boosts final performance in sparse reward environments, including Noisy-TV, navigation and challenging Atari games.
  - SM maintains the agent's interest in exciting exploration while reducing unwanted attraction to unpredictable or noisy observations.

### [9] Never Give Up: Learning Directed Exploration Strategies

- **Relevance:** Shows how a curiosity-style intrinsic reward (episodic novelty) can drive exploration in hard-exploration RL tasks. It describes a mechanism: reward for reaching states that are novel within the current episode, using embeddings that capture controllable aspects of the environment, plus a family of policies with differing exploration/exploitation trade-offs.
- **Contribution:** Introduces the Never Give Up (NGU) agent, which learns a range of directed exploratory policies using an episodic-memory-based intrinsic reward. It combines this with a self-supervised inverse dynamics model for embeddings and a UVFA framework to learn many exploration/exploitation trade-offs in one network. It reports the first non-zero reward in Pitfall! without demonstrations or hand-crafted features.
- **Method:** An intrinsic reward is computed from k-nearest neighbors over the agent's recent experience in an episodic memory, which encourages repeatedly revisiting all states. The embeddings used for the nearest-neighbour lookup are trained with a self-supervised inverse dynamics model, which biases novelty toward what the agent can control. Universal Value Function Approximators let a single neural network represent many directed exploration policies with different exploration/exploitation weightings. The approach is designed to run with modern distributed RL agents that use many parallel actors.
- **Findings:**
  - Doubles the performance of the base agent on all hard-exploration games in the Atari-57 suite.
  - Maintains very high scores on the remaining Atari games, with a median human-normalised score of 1344.0%.
  - First algorithm to obtain non-zero reward in Pitfall! (mean score 8,400) without demonstrations or hand-crafted features.
  - Using one network for different degrees of exploration/exploitation transfers from predominantly exploratory policies to effective exploitative policies.

### [10] Self-Supervised Exploration via Disagreement

- **Relevance:** Presents a curiosity-style intrinsic motivation, disagreement among an ensemble of learned dynamics models, as an exploration signal. It addresses how curiosity can drive exploration without external reward, in stochastic environments, and with better sample efficiency than prediction-error-based approaches.
- **Contribution:** An exploration formulation inspired by active learning in which the agent is rewarded for maximizing the disagreement of an ensemble of dynamics models. The disagreement objective is also used to optimize the policy in a differentiable manner, without reinforcement learning, which gives sample-efficient exploration.
- **Method:** Train an ensemble of dynamics models and incentivize the agent to visit states where the ensemble's predictions disagree most, giving a self-supervised intrinsic signal with no external reward. The policy is then optimized differentiably through this disagreement objective instead of with standard RL. The method is evaluated on stochastic-Atari, Mujoco and Unity benchmarks and on a real robot.
- **Findings:**
  - Maximizing ensemble disagreement lets agents learn skills through self-supervised exploration without any external reward.
  - The formulation is designed to avoid getting stuck in environments with stochastic dynamics, a failure the abstract attributes to many prior formulations.
  - Optimizing the policy differentiably with the disagreement objective, without RL, gives sample-efficient exploration.
  - The authors report efficacy across stochastic-Atari, Mujoco and Unity benchmark environments.
  - On a real robot, the method learns to interact with objects completely from scratch.
- **Limitations (from abstract):**
  - The abstract reports no quantitative results or specific baseline comparisons, so the size of the gains cannot be judged from it.
  - The abstract says prior formulations are inefficient or get stuck in stochastic settings, but it does not describe this method's own limitations.

### [11] A survey on intrinsic motivation in reinforcement learning

- **Relevance:** This survey addresses the question indirectly. It frames intrinsic motivation (the family of methods that includes curiosity) as a way to tackle the difficulty of exploring the environment in deep RL. It categorizes the kinds of intrinsic motivation and discusses their advantages and limitations for exploration. The abstract does not describe specific curiosity mechanisms or give empirical evidence, so it serves as a taxonomy and overview rather than a detailed answer.
- **Contribution:** A survey of the role of intrinsic motivation in deep RL. It categorizes types of intrinsic motivation and details each category's advantages and limitations with respect to exploration and action abstraction. It also examines open research questions and proposes a developmental architecture built from an RL algorithm plus an intrinsic motivation module that compresses information.
- **Method:** Literature survey. It categorizes intrinsic motivation approaches and analyzes them from the perspective of learning how to achieve tasks. It then proposes a conceptual developmental architecture made of building blocks.
- **Findings:**
  - Intrinsic motivation is identified as a way to address the difficulty of exploring the environment in deep RL, as well as the challenge of abstracting actions.
  - Different kinds of intrinsic motivation can be categorized, each with its own advantages and limitations for these challenges.
  - The authors suggest that solving current challenges could lead to a larger developmental architecture able to tackle most tasks, built from an RL algorithm and an intrinsic motivation module that compresses information.
- **Limitations (from abstract):**
  - The abstract gives no specific curiosity mechanisms, quantitative results, or empirical comparisons.
  - The proposed developmental architecture is described as a suggestion, so it is conceptual and not validated in the abstract.

### [12] An information-theoretic perspective on intrinsic motivation in reinforcement learning: a survey

- **Relevance:** Surveys intrinsic motivation (IM), the main computational framing of curiosity in RL, and organizes it via information theory into surprise, novelty and skill learning. It bears on the question by identifying how these curiosity-like signals help exploration, especially in sparse-reward settings. The abstract gives only high-level claims, with no mechanisms or quantitative evidence.
- **Contribution:** A new information-theoretic taxonomy of intrinsic motivation methods in (deep) RL. It computationally revisits the notions of surprise, novelty and skill learning, and uses them to identify the advantages and disadvantages of methods and to outline current research outlooks.
- **Method:** Literature survey. The works are organized by a taxonomy built on information theory (surprise, novelty, skill learning).
- **Findings:**
  - Intrinsic motivation can address the difficulty of exploring the environment in sparse-reward settings.
  - Intrinsic motivation can also help with the ability to abstract actions.
  - The analysis suggests that novelty and surprise can assist the building of a hierarchy of transferable skills.
  - Such a skill hierarchy further abstracts the environment and makes the exploration process more robust.

## Search log

**Round 1** (35 new candidates)
- `(ti:curiosity OR ti:"intrinsic motivation" OR ti:"intrinsic reward") AND abs:exploration AND abs:"reinforcement learning"`
- `(abs:"prediction error" OR abs:"forward dynamics" OR abs:"random network distillation" OR abs:"inverse dynamics") AND abs:curiosity AND abs:exploration`
- `(abs:"count-based" OR abs:"pseudo-count" OR abs:novelty OR abs:"information gain") AND abs:exploration AND abs:"sparse reward" AND abs:"reinforcement learning"`
- `ti:"Curiosity-driven Exploration by Self-supervised Prediction" OR ti:"Exploration by Random Network Distillation" OR ti:"Large-Scale Study of Curiosity-Driven Learning" OR ti:"Unifying Count-Based Exploration and Intrinsic Motivation" OR ti:"VIME: Variational Information Maximizing Exploration"`

**Round 2** (28 new candidates)
- `ti:"Exploration by Random Network Distillation" OR ti:"VIME: Variational Information Maximizing Exploration" OR ti:"Self-Supervised Exploration via Disagreement" OR ti:"Exploration: A Study of Count-Based Exploration for Deep Reinforcement Learning" OR ti:"Episodic Curiosity through Reachability" OR ti:"Never Give Up: Learning Directed Exploration Strategies" OR ti:"Agent57: Outperforming the Atari Human Benchmark"`
- `ti:"Go-Explore" OR ti:"First return, then explore" OR ti:"Formal Theory of Creativity, Fun, and Intrinsic Motivation" OR ti:"Intrinsic Motivation Systems for Autonomous Mental Development" OR ti:"What is intrinsic motivation? A typology of computational approaches" OR ti:"Intrinsically motivated reinforcement learning"`
- `(ti:"intrinsically motivated" OR ti:"intrinsic motivation" OR ti:curiosity) AND (ti:survey OR ti:review OR ti:overview OR ti:taxonomy) AND abs:"reinforcement learning"`
- `(abs:"learning progress" OR abs:"Bayesian surprise" OR abs:"information gain" OR abs:"artificial curiosity" OR abs:disagreement) AND (abs:curiosity OR abs:"intrinsic motivation") AND (abs:exploration OR abs:"reinforcement learning")`

**Round 3** (25 new candidates)
- `ti:"Incentivizing Exploration In Reinforcement Learning With Deep Predictive Models" OR ti:"#Exploration: A Study of Count-Based Exploration for Deep Reinforcement Learning" OR ti:"Count-Based Exploration with Neural Density Models" OR ti:"Curiosity-driven Exploration in Deep Reinforcement Learning via Bayesian Neural Networks" OR ti:"Surprise-Based Intrinsic Motivation for Deep Reinforcement Learning"`
- `(abs:"noisy TV" OR abs:"noisy-TV" OR abs:"white noise" OR abs:"stochastic environment" OR abs:"stochasticity") AND (abs:curiosity OR abs:"intrinsic reward" OR abs:"intrinsic motivation") AND abs:exploration`
- `(abs:detachment OR abs:derailment OR abs:"catastrophic forgetting" OR abs:"vanishing intrinsic reward" OR abs:"intrinsic reward") AND (abs:"hard exploration" OR abs:"hard-exploration") AND (abs:curiosity OR abs:"intrinsic motivation" OR abs:"Go-Explore")`
- `(abs:"sample complexity" OR abs:"regret" OR abs:"theoretical analysis" OR abs:"state coverage" OR abs:"state space coverage" OR abs:"maximum entropy") AND (abs:curiosity OR abs:"intrinsic motivation" OR abs:"intrinsic reward" OR abs:"count-based exploration") AND abs:exploration AND abs:"reinforcement learning"`
