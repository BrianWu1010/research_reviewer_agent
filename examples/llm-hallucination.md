# What techniques reduce hallucination in large language models?

## Answer

The papers describe several families of techniques for reducing hallucination: retrieval grounding, decoding-time interventions, prompting and self-verification, and training-time alignment with factuality-oriented signals. Some also combine these, for example retrieval-based rewards or detection-triggered retuning. Evidence is strongest where quantitative gains over named baselines are reported, such as DPO-based factuality tuning [7], binary retrieval-augmented reward [10], and DoLa [8]. Several other papers report gains only qualitatively, and the families are rarely compared head to head.

## Key findings

**Retrieval grounding and its refinements**
- Self-RAG trains a model to retrieve on demand and critique its own outputs with reflection tokens. It reports gains in factuality and citation accuracy over ChatGPT and retrieval-augmented Llama2-chat, and it avoids the unhelpful generations that indiscriminate retrieval can cause [1].
- Retrieval can itself introduce hallucination. Multi-source retrieval can worsen it through sparse data and source conflicts, which MultiRAG addresses with graph-based aggregation and confidence filtering [15]. VOTE-RAG targets "hallucination on hallucination" with voting over retrieval and response generation, and reports results comparable to or better than more complex RAG frameworks [14].
- AutoRAG-LoRA combines retrieval, hallucination detection, and LoRA adapter retuning. It reports reduced factual drift but gives no quantitative evidence [13].

**Decoding-time methods**
- Contrastive decoding is the most represented family. DoLa contrasts later and earlier layers, needs no retrieval or fine-tuning, and improves LLaMA models on TruthfulQA by 12–17% absolute points [8]. LOL extends this idea with multi-layer fusion and a truthfulness-refocusing module, but it outperforms baselines only "in most cases" [6].
- Other methods contrast against an induced-hallucination model. HICD disperses attention in selected heads to induce hallucinations [4]. DHI trains an "Evil LLM" for more diverse hallucinations and adds an adaptive rationality constraint [5]. Both claim gains over other contrastive approaches [4, 5]. DHI's setup implies extra training and inference overhead, though this is not quantified [5].
- Token-Guard performs token-level self-checking with pruning and regeneration, without retrieval or fine-tuning. It reports substantial reductions but gives no quantitative detail [16].

**Prompting and self-verification**
- Chain-of-Verification drafts an answer, plans verification questions, answers them independently, and revises. It reduces hallucination across list-based, closed-book QA, and longform tasks, though the size of the effect is not given [9].
- A comparative study finds that chain-of-thought alone does not fully solve hallucination. It examines CoT+RAG, self-consistency, and self-verification, but its abstract does not say which works best [11].
- Self-evaluation is plausible in principle. Models can judge their own answers (P(True)) and predict whether they know an answer (P(IK)), although this work is groundwork for honesty rather than a tested mitigation [2]. P(IK) calibration is poor on new tasks [2].

**Training-time alignment and fine-tuning**
- General human-feedback alignment improves truthfulness modestly, though the improvement is not quantified and InstructGPT still makes simple mistakes [3]. FLAME argues that conventional alignment often increases false facts. SFT on unfamiliar knowledge and RL rewards that favor long, detailed answers both encourage hallucination, so it proposes factuality-aware SFT and DPO [20].
- Factuality-targeted preference optimization is well supported. DPO on automatically generated factuality rankings, built with retrieval or a retrieval-free confidence approach, beats RLHF and factuality-targeted decoding. It cuts factual error rates by 58% for biographies and 40% for medical QA relative to Llama-2-chat at 7B [7].
- The training signal can come from the model itself. Self-alignment with self-evaluation and SK-Tuning, followed by DPO, improves factuality on TruthfulQA and BioGEN without human factuality labels [18]. PKUE uses preference optimization on self-generated answers to precise questions, and reports gains that extend to general tasks and another language [19].
- Binary retrieval-augmented reward in online RL cuts hallucination by 39.3% in open-ended generation, outperforms supervised training and continuous-reward RL, and preserves instruction-following, math, and code performance. Continuous rewards caused quality regressions [10].
- Calibrated abstention is an additional route. Binary RAR yields "I don't know" answers that lower incorrect answers on PopQA and GPQA [10]. VeriFY teaches self-verification and abstention, reducing hallucination by 9.7–53.3% at a small recall cost of 0.4–5.7% [12].

**Surveys and framing**
- One paper organizes mitigation into retrieval augmentation, hallucination-aware fine-tuning, logit calibration, and fact-verification modules, alongside detection by uncertainty, calibration, and attention checks. It also separates intrinsic from extrinsic hallucination. It is theoretical and survey-level and reports no empirical comparison [17].

## Open questions and gaps

- **Cross-family comparison is thin.** Only the DPO factuality paper directly compares against RLHF and decoding baselines [7]. DHI's evaluation is limited to contrastive-decoding baselines [5]. Whether retrieval, decoding, prompting, or training is best remains unresolved, and the survey does not establish relative effectiveness [17].
- **Many results are unquantified.** Several abstracts give no datasets, baselines, or effect sizes [9, 11, 13, 15, 16]. The comparative study does not name its best technique [11].
- **Capability trade-offs are inconsistently handled.** Continuous-reward RL regressed in quality [10]. VeriFY loses some recall [12]. Existing abstention methods are described as overly conservative [12], while other papers claim to preserve general ability [10, 19, 20].
- **Self-evaluation is limited by what the model knows.** Self-alignment depends solely on internal knowledge [18], and P(IK) calibration is poor on new tasks [2]. How far self-verification can go without external grounding is unclear.
- **Cost and overhead are rarely measured.** The contrastive methods that need extra models [5] and Token-Guard's iterative regeneration [16] have unquantified inference costs.
- **Scope of evidence.** Retrieval methods address context-dependent errors but not parametric-knowledge errors, as MultiRAG's limitation shows [15]. Evaluations are often limited to particular model families, such as Llama [18] or Qwen3 [10], so generalization is uncertain.

## Reviewer assessment

**Verdict:** needs_more (6/10). The answer is well organized, mostly grounded, and honest about unquantified results. It covers retrieval, decoding, prompting and self-verification, and alignment. But the evidence base is missing several foundational works and major facets. Most of the 20 papers are recent, low-citation method papers, while the seminal works are largely absent. These include the original RAG paper, SelfCheckGPT, TruthfulQA, Inference-Time Intervention, and the hallucination surveys. Hallucination detection and benchmarks (HaluEval, FActScore) are not covered, nor are representation editing and activation steering. Also missing are knowledge-editing and domain-specific mitigation such as medical or multimodal settings, and tool use or knowledge-graph grounding. Several claims rest on abstracts that report no effect sizes ([9], [11], [13], [15], [16]), which weakens the 'strongest evidence' ranking. The cross-family comparison is acknowledged as thin, but the search could have targeted comparative or survey evidence to fill it.

Still missing:
- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection
- TruthfulQA: Measuring How Models Mimic Human Falsehoods
- Inference-Time Intervention: Eliciting Truthful Answers from a Language Model
- A Survey on Hallucination in Large Language Models (Huang et al.)
- Survey of Hallucination in Natural Language Generation (Ji et al.)
- Self-Consistency Improves Chain of Thought Reasoning
- FActScore: fine-grained atomic evaluation of factual precision
- HaluEval / hallucination evaluation benchmarks
- Chain-of-thought prompting and ReAct tool-augmented grounding to reduce hallucination
- Self-Refine / self-correction of LLMs and its limits
- Representation editing and activation steering for truthfulness
- Knowledge graph grounding for hallucination mitigation
- Uncertainty estimation and semantic entropy for hallucination detection
- Why language models hallucinate / training-data causes and fine-tuning on new knowledge
- Multimodal (vision-language) hallucination mitigation
- Domain-specific hallucination mitigation in medical or legal LLMs

## References

1. **Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection**. Akari Asai, Zeqiu Wu, Yizhong Wang et al. (2023). [arXiv:2310.11511](http://arxiv.org/abs/2310.11511v1) (relevance 9/10)
2. **Language Models (Mostly) Know What They Know**. Saurav Kadavath, Tom Conerly, Amanda Askell et al. (2022). [arXiv:2207.05221](http://arxiv.org/abs/2207.05221v4) (relevance 6/10)
3. **Training language models to follow instructions with human feedback**. Long Ouyang, Jeff Wu, Xu Jiang et al. (2022). [arXiv:2203.02155](http://arxiv.org/abs/2203.02155v1) (relevance 6/10)
4. **HICD: Hallucination-Inducing via Attention Dispersion for Contrastive Decoding to Mitigate Hallucinations in Large Language Models**. Xinyan Jiang, Hang Ye, Yongxin Zhu et al. (2025). [arXiv:2503.12908](http://arxiv.org/abs/2503.12908v4) (relevance 10/10)
5. **DHI: Leveraging Diverse Hallucination Induction for Enhanced Contrastive Factuality Control in Large Language Models**. Jiani Guo, Xiangke Zeng, Jie Wu et al. (2026). [arXiv:2601.01156](http://arxiv.org/abs/2601.01156v1) (relevance 10/10)
6. **Lower Layers Matter: Alleviating Hallucination via Multi-Layer Fusion Contrastive Decoding with Truthfulness Refocused**. Dingwei Chen, Feiteng Fang, Shiwen Ni et al. (2024). [arXiv:2408.08769](http://arxiv.org/abs/2408.08769v2) (relevance 10/10)
7. **Fine-tuning Language Models for Factuality**. Katherine Tian, Eric Mitchell, Huaxiu Yao et al. (2023). [arXiv:2311.08401](http://arxiv.org/abs/2311.08401v1) (relevance 10/10)
8. **DoLa: Decoding by Contrasting Layers Improves Factuality in Large Language Models**. Yung-Sung Chuang, Yujia Xie, Hongyin Luo et al. (2023). [arXiv:2309.03883](http://arxiv.org/abs/2309.03883v2) (relevance 10/10)
9. **Chain-of-Verification Reduces Hallucination in Large Language Models**. Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu et al. (2023). [arXiv:2309.11495](http://arxiv.org/abs/2309.11495v2) (relevance 10/10)
10. **Train for Truth, Keep the Skills: Binary Retrieval-Augmented Reward Mitigates Hallucinations**. Tong Chen, Akari Asai, Luke Zettlemoyer et al. (2025). [arXiv:2510.17733](http://arxiv.org/abs/2510.17733v1) (relevance 10/10)
11. **Improving the Reliability of LLMs: Combining CoT, RAG, Self-Consistency, and Self-Verification**. Adarsh Kumar, Hwiyoon Kim, Jawahar Sai Nathani et al. (2025). [arXiv:2505.09031](http://arxiv.org/abs/2505.09031v1) (relevance 10/10)
12. **Do I Really Know? Learning Factual Self-Verification for Hallucination Reduction**. Enes Altinisik, Masoomali Fatehkia, Fatih Deniz et al. (2026). [arXiv:2602.02018](http://arxiv.org/abs/2602.02018v1) (relevance 10/10)
13. **AutoRAG-LoRA: Hallucination-Triggered Knowledge Retuning via Lightweight Adapters**. Kaushik Dwivedi, Padmanabh Patanjali Mishra (2025). [arXiv:2507.10586](http://arxiv.org/abs/2507.10586v1) (relevance 9/10)
14. **Mitigating Hallucination on Hallucination in RAG via Ensemble Voting**. Zequn Xie, Zhengyang Sun (2026). [arXiv:2603.27253](http://arxiv.org/abs/2603.27253v2) (relevance 9/10)
15. **MultiRAG: A Knowledge-guided Framework for Mitigating Hallucination in Multi-source Retrieval Augmented Generation**. Wenlong Wu, Haofen Wang, Bohan Li et al. (2025). [arXiv:2508.03553](http://arxiv.org/abs/2508.03553v1) (relevance 9/10)
16. **Token-Guard: Towards Token-Level Hallucination Control via Self-Checking Decoding**. Yifan Zhu, Huiqiang Rong, Haoran Luo (2026). [arXiv:2601.21969](http://arxiv.org/abs/2601.21969v2) (relevance 9/10)
17. **Theoretical Foundations and Mitigation of Hallucination in Large Language Models**. Esmail Gumaan (2025). [arXiv:2507.22915](http://arxiv.org/abs/2507.22915v1) (relevance 9/10)
18. **Self-Alignment for Factuality: Mitigating Hallucinations in LLMs via Self-Evaluation**. Xiaoying Zhang, Baolin Peng, Ye Tian et al. (2024). [arXiv:2402.09267](http://arxiv.org/abs/2402.09267v2) (relevance 9/10)
19. **Exploring the Generalizability of Factual Hallucination Mitigation via Enhancing Precise Knowledge Utilization**. Siyuan Zhang, Yichi Zhang, Yinpeng Dong et al. (2025). [arXiv:2502.19127](http://arxiv.org/abs/2502.19127v3) (relevance 9/10)
20. **FLAME: Factuality-Aware Alignment for Large Language Models**. Sheng-Chieh Lin, Luyu Gao, Barlas Oguz et al. (2024). [arXiv:2405.01525](http://arxiv.org/abs/2405.01525v1) (relevance 9/10)

## Paper notes

### [1] Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

- **Relevance:** Presents a technique for reducing hallucination and factual errors in LLMs: adaptive retrieval combined with self-reflection through reflection tokens. It addresses a limitation of standard RAG, which retrieves indiscriminately, and reports gains in factuality and citation accuracy.
- **Contribution:** Self-RAG, a framework that trains a single arbitrary LM to retrieve passages on demand, then generate and critique both the retrieved passages and its own outputs using special reflection tokens. The tokens also make the LM controllable at inference time.
- **Method:** Train an LM to emit reflection tokens that decide when to retrieve and assess the relevance of retrieved passages and the quality of its own generations. At inference, these tokens let the model tailor its behavior to task requirements. Evaluated with 7B and 13B parameter models on open-domain QA, reasoning, fact verification, and long-form generation.
- **Findings:**
  - Self-RAG (7B and 13B) significantly outperforms state-of-the-art LLMs and retrieval-augmented models on a diverse set of tasks.
  - It outperforms ChatGPT and retrieval-augmented Llama2-chat on open-domain QA, reasoning, and fact verification.
  - It shows significant gains in factuality and citation accuracy for long-form generation relative to these models.
  - Retrieving on demand, rather than a fixed number of passages regardless of need, avoids the loss of versatility and unhelpful generations that indiscriminate RAG can cause.
- **Limitations (from abstract):**
  - The abstract notes that standard RAG, which retrieves a fixed number of passages indiscriminately, can reduce LM versatility or lead to unhelpful generations. This motivates Self-RAG rather than being a limitation of it.
  - The abstract does not state limitations of Self-RAG itself.

### [2] Language Models (Mostly) Know What They Know

- **Relevance:** The paper does not directly present a hallucination-reduction method. It studies model self-evaluation and calibration, P(True) and P(IK), which could be used to detect likely incorrect claims or to identify questions a model is unlikely to answer correctly. The abstract frames this as groundwork for training more honest models, so it bears on the question as a basis for detection and honesty-oriented approaches, not as a demonstrated mitigation technique.
- **Contribution:** Shows that language models can evaluate the validity of their own answers (P(True)) and can be trained to predict whether they know the answer to a question (P(IK)). The paper also characterizes the calibration and scaling of both abilities.
- **Method:** The authors test calibration of larger models on multiple choice and true/false questions in a suitable format. For open-ended tasks, models first propose answers and then estimate P(True) that the answer is correct, optionally after considering many of their own samples. Separately, models are trained to predict P(IK), the probability of knowing the answer without reference to any proposed answer. P(IK) is evaluated for cross-task generalization and for sensitivity to relevant source materials and to hints on math word problems.
- **Findings:**
  - Larger models are well-calibrated on diverse multiple choice and true/false questions when the format is right.
  - P(True) self-evaluation shows encouraging performance, calibration, and scaling across a diverse array of tasks.
  - Self-evaluation improves when the model considers many of its own samples before judging one specific answer.
  - Models perform well at predicting P(IK) and partially generalize across tasks.
  - Predicted P(IK) rises appropriately when relevant source materials are in the context and when hints toward the solution of math word problems are given.
- **Limitations (from abstract):**
  - P(IK) calibration is poor on new tasks, even though the model partially generalizes across tasks.
  - The abstract presents the work as groundwork for training more honest models, not as a tested method for reducing hallucination.

### [3] Training language models to follow instructions with human feedback

- **Relevance:** Presents fine-tuning with human feedback (supervised fine-tuning on demonstrations followed by RLHF) as a technique that improves truthfulness in large language models. This is relevant to hallucination reduction, but the abstract frames the work as alignment with user intent. It does not mention hallucination explicitly and reports truthfulness improvements only in general terms.
- **Contribution:** InstructGPT: GPT-3 models aligned with user intent through a pipeline of human demonstrations and human preference rankings. The abstract reports improved truthfulness and reduced toxicity, and preference for a 1.3B InstructGPT model over 175B GPT-3.
- **Method:** Collect labeler-written prompts and prompts submitted through the OpenAI API. Collect labeler demonstrations of desired behavior and fine-tune GPT-3 on them with supervised learning. Then collect rankings of model outputs and further fine-tune the supervised model with reinforcement learning from human feedback (RLHF). Evaluate with human preference judgments on the prompt distribution and on public NLP datasets.
- **Findings:**
  - Human evaluators preferred outputs from the 1.3B InstructGPT model over those from the 175B GPT-3, despite the 100x parameter difference.
  - InstructGPT models show improvements in truthfulness compared with GPT-3.
  - InstructGPT models generate less toxic output.
  - Performance regressions on public NLP datasets are minimal.
  - Increasing model size alone does not make models better at following user intent; the abstract notes that large models can produce untruthful, toxic, or unhelpful outputs.
- **Limitations (from abstract):**
  - InstructGPT still makes simple mistakes.
  - The abstract does not quantify the truthfulness improvement or measure hallucination specifically.
  - Evaluation is mainly on the authors' own prompt distribution.

### [4] HICD: Hallucination-Inducing via Attention Dispersion for Contrastive Decoding to Mitigate Hallucinations in Large Language Models

- **Relevance:** Presents a decoding-time technique for reducing hallucination in LLMs: contrastive decoding against deliberately induced hallucinations created by dispersing attention in selected attention heads. It addresses both contextual faithfulness and factuality, directly answering the question about techniques that reduce hallucination.
- **Contribution:** HICD, a contrastive decoding method that induces hallucinations in a controlled way by selecting attention heads that are crucial to the model's prediction and dispersing their attention. The hallucinated outputs are contrasted with the original outputs to produce the final result. The abstract claims this yields more "contrast-effective" hallucinations than other hallucination-inducing methods.
- **Method:** Select attention heads important to the model's prediction as "inducing heads". Disperse the attention of these heads to induce hallucinated outputs. Compare the hallucinated outputs with the original outputs via contrastive decoding to obtain the final output. Evaluated on context completion, reading comprehension, question answering, and tasks requiring factual knowledge recall.
- **Findings:**
  - Significantly improves performance on tasks requiring contextual faithfulness: context completion, reading comprehension, and question answering.
  - Also improves factuality on tasks requiring accurate knowledge recall.
  - The inducing-head selection and attention dispersion produce more "contrast-effective" hallucinations, outperforming other hallucination-inducing methods for contrastive decoding.
  - Inducing hallucinations in a controlled manner is presented as a promising strategy for reducing hallucinations.

### [5] DHI: Leveraging Diverse Hallucination Induction for Enhanced Contrastive Factuality Control in Large Language Models

- **Relevance:** Presents a contrastive decoding technique for mitigating LLM hallucination. It addresses a limitation of existing Evil-LLM-based contrastive decoding (narrow diversity of induced hallucinations), so it is a concrete example of a decoding-time hallucination-reduction method.
- **Contribution:** DHI (Diverse Hallucination Induction), a training framework that lets an "Evil LLM" generate a broader range of hallucination types without pre-annotated hallucination data. The induced hallucinations are used for contrastive decoding against a positive model, with an adaptive rationality constraint at inference.
- **Method:** Trains the Evil LLM with a modified loss that down-weights the generation of specific factually correct tokens. This encourages diverse hallucinations at targeted positions while keeping overall factual content. A causal attention masking adaptation reduces the effect of this penalization on subsequent tokens. At inference, an adaptive rationality constraint limits contrastive decoding to tokens where the positive model is highly confident, avoiding penalties on correct tokens.
- **Findings:**
  - DHI achieves significant performance gains over other contrastive decoding-based approaches across multiple hallucination benchmarks.
  - Existing Evil-LLM approaches trained on specific error types tend to reproduce only those patterns, which limits their effectiveness (as stated by the authors).
- **Limitations (from abstract):**
  - Evaluation is described only as contrastive-decoding baselines on hallucination benchmarks; the abstract does not say how it compares to non-decoding approaches such as retrieval augmentation or fine-tuning.
  - Contrastive decoding requires an additional trained Evil LLM and a positive model, implying extra training and inference overhead (implied, not quantified in the abstract).

### [6] Lower Layers Matter: Alleviating Hallucination via Multi-Layer Fusion Contrastive Decoding with Truthfulness Refocused

- **Relevance:** Presents a decoding-time technique for reducing LLM hallucination: contrastive decoding that fuses information from multiple layers and adds a truthfulness-refocusing module. It is a concrete example of an inference-time, contrastive-decoding family of hallucination mitigation methods.
- **Contribution:** LOL (LOwer Layer Matters), a contrastive decoding framework that contrasts the original model with an amateur model that has induced hallucination, using multi-layer fusion across lower layers instead of only the final layer. It also adds a truthfulness refocused module that uses instruction guidance to improve truthfulness.
- **Method:** Contrastive decoding between the original LLM and a hallucination-induced amateur model. Contrastive information is fused from lower layers as well as the final layer, which addresses the coarse contrast and simple subtraction of prior methods. A truthfulness refocused module adds instruction guidance. The method is evaluated on four publicly available datasets.
- **Findings:**
  - LOL significantly mitigates hallucination on four publicly available datasets.
  - LOL outperforms existing baselines in most cases.
- **Limitations (from abstract):**
  - Prior contrastive decoding can disrupt the original LLM's output distribution because of coarse contrast and simple subtraction, which motivates this work.
  - LOL outperforms baselines only 'in most cases', so it does not win everywhere.
  - The abstract does not name the datasets, models, baselines, or metrics, and the code and data are promised only upon acceptance.

### [7] Fine-tuning Language Models for Factuality

- **Relevance:** Presents a concrete training-time technique for reducing hallucination: fine-tuning LLMs with Direct Preference Optimization on automatically generated factuality preference rankings, with no human labeling. It reports gains over RLHF and factuality-targeted decoding strategies, so it speaks directly to which techniques reduce hallucination and how they compare.
- **Contribution:** A method for fine-tuning language models to be more factual in open-ended generation without human labels. It uses automatically generated factuality preference rankings, built either with existing retrieval-based systems or with a novel retrieval-free approach, to train with DPO.
- **Method:** Factuality of open-ended text is estimated automatically in two ways: consistency with an external knowledge base (retrieval-based) or a large model's confidence scores (retrieval-free). These estimates are used to rank candidate model responses into preference pairs. Llama-2 is then fine-tuned on those pairs with Direct Preference Optimization (DPO). Evaluation is on held-out topics, and factuality is measured as the percent of generated claims that are correct.
- **Findings:**
  - Learning from automatically generated factuality preference rankings significantly improves the factuality of Llama-2 on held-out topics.
  - The approach outperforms RLHF and decoding strategies targeted at factuality.
  - At 7B scale, compared to Llama-2-chat, factual error rate falls by 58% for biography generation and by 40% for medical question answering.
  - Both the retrieval-based and the novel retrieval-free ways of generating preference rankings can be used, so training does not require human factuality labels.

### [8] DoLa: Decoding by Contrasting Layers Improves Factuality in Large Language Models

- **Relevance:** Presents a decoding-time technique for reducing hallucination in LLMs that needs neither retrieval of external knowledge nor additional fine-tuning. It is a concrete example of an inference-time, model-internal approach to improving factuality.
- **Contribution:** Decoding by Contrasting Layers (DoLa), a simple decoding strategy that reduces hallucinations in pretrained LLMs and better surfaces factual knowledge.
- **Method:** The next-token distribution is obtained by contrasting the logits from projecting later transformer layers versus earlier layers to the vocabulary space. This exploits the observation that factual knowledge in LLMs is generally localized to particular transformer layers.
- **Findings:**
  - DoLa better surfaces factual knowledge and reduces the generation of incorrect facts.
  - It consistently improves truthfulness across multiple-choice tasks and open-ended generation tasks.
  - It improves LLaMA family models on TruthfulQA by 12-17% absolute points.

### [9] Chain-of-Verification Reduces Hallucination in Large Language Models

- **Relevance:** Presents Chain-of-Verification (CoVe), a prompting-based technique in which the model deliberates on and fact-checks its own outputs to reduce hallucination. It is a direct example of a self-verification approach to the research question.
- **Contribution:** Introduces the Chain-of-Verification (CoVe) method, which lets a language model correct its own mistakes by drafting a response, planning verification questions, answering them independently, and producing a final verified response.
- **Method:** A four-step pipeline: (i) draft an initial response; (ii) plan verification questions to fact-check the draft; (iii) answer those questions independently so the answers are not biased by other responses; (iv) generate the final verified response. It is evaluated on list-based questions from Wikidata, closed-book MultiSpanQA, and longform text generation.
- **Findings:**
  - CoVe decreases hallucinations across a variety of tasks.
  - The tasks where it helps include list-based Wikidata questions, closed-book MultiSpanQA, and longform text generation.
  - Language models can deliberate on their own responses to correct mistakes.
- **Limitations (from abstract):**
  - The abstract describes hallucination as an unsolved issue, which implies CoVe does not eliminate it.
  - The abstract reports no quantitative results, so the size of the improvement is not stated.

### [10] Train for Truth, Keep the Skills: Binary Retrieval-Augmented Reward Mitigates Hallucinations

- **Relevance:** Presents a training-time technique for reducing extrinsic hallucination: online RL with a binary retrieval-augmented reward. It addresses the tradeoff between factuality and general capability that limits other mitigation methods, so it is a direct answer to the question.
- **Contribution:** A novel binary retrieval-augmented reward (RAR) for online reinforcement learning. The reward is 1 only if the whole output is factually correct and 0 otherwise. It reduces hallucination while preserving performance on other tasks, and it leads the model to abstain in a calibrated way.
- **Method:** Online RL on Qwen3 reasoning models using a binary reward that is computed with retrieval augmentation. The method is compared with supervised training and continuous-reward RL baselines. Evaluation covers open-ended generation, short-form QA (PopQA, GPQA), instruction following, math, and code.
- **Findings:**
  - Binary RAR reduces hallucination rates by 39.3% in open-ended generation, substantially outperforming supervised training and continuous-reward RL baselines.
  - In short-form QA the model learns calibrated abstention, outputting "I don't know" when its parametric knowledge is insufficient.
  - Abstention yields 44.4% fewer incorrect answers on PopQA and 21.7% fewer on GPQA.
  - Factuality gains come with no performance degradation on instruction following, math, or code.
  - Continuous-reward RL improves factuality but causes quality regressions.

### [11] Improving the Reliability of LLMs: Combining CoT, RAG, Self-Consistency, and Self-Verification

- **Relevance:** Directly addresses the research question by comparing several prompting and augmentation techniques for reducing LLM hallucination: CoT, CoT combined with RAG, self-consistency, and self-verification. It frames these as complementary approaches to improving factual accuracy.
- **Contribution:** A comparative evaluation of baseline LLMs against CoT, CoT+RAG, self-consistency, and self-verification techniques, aimed at identifying the most robust approach for minimizing hallucinations while preserving fluency and reasoning depth.
- **Method:** Investigates combining chain-of-thought prompting with retrieval-augmented generation (incorporating external knowledge sources during reasoning), plus self-consistency and self-verification strategies in which models verify or revise their own outputs. Baseline LLMs are compared against each technique.
- **Findings:**
  - Chain-of-thought prompting alone does not fully address the hallucination problem.
  - The abstract states that the results highlight the effectiveness of each method and identify the most robust approach, but it does not name that approach or give quantitative results.
- **Limitations (from abstract):**
  - The abstract gives no details on datasets, models, metrics, or quantitative results.
  - The abstract does not say which technique performed best.

### [12] Do I Really Know? Learning Factual Self-Verification for Hallucination Reduction

- **Relevance:** Presents a training-time technique (VeriFY) for reducing factual hallucination in LLMs via learned consistency-based self-verification and selective abstention. It is a concrete answer to the question, and it contrasts with external post-hoc verification and with plain uncertainty-to-abstention fine-tuning.
- **Contribution:** VeriFY, a training-time framework that teaches LLMs to reason about their own factual uncertainty through self-verification. It also introduces a stage-level loss masking approach that avoids reinforcing hallucinated content when training on augmented traces.
- **Method:** Training is augmented with structured verification traces. In each trace the model produces an initial answer, generates and answers a probing verification query, issues a consistency judgment, and then decides whether to answer or abstain. Stage-level loss masking excludes hallucinated answer stages from the training objective while keeping supervision over the verification behavior.
- **Findings:**
  - Across multiple model families and scales, VeriFY reduces factual hallucination rates by 9.7 to 53.3 percent.
  - The cost in recall is modest, a reduction of 0.4 to 5.7 percent.
  - The approach generalizes across datasets when trained on a single source dataset.
- **Limitations (from abstract):**
  - Existing abstention-based approaches are described as often overly conservative; VeriFY still trades off some recall (0.4 to 5.7 percent reduction).
  - Code, data, and checkpoints are not yet released (promised upon acceptance).

### [13] AutoRAG-LoRA: Hallucination-Triggered Knowledge Retuning via Lightweight Adapters

- **Relevance:** Presents a concrete combined technique for reducing LLM hallucination: retrieval grounding (RAG with prompt rewriting and hybrid retrieval), hallucination detection with confidence scoring, and a feedback loop that retunes lightweight LoRA adapters with KL-regularized contrastive loss. It illustrates retrieval-based, detection-triggered, and parameter-efficient fine-tuning approaches to the research question.
- **Contribution:** AutoRAG-LoRA, a modular RAG framework that reduces hallucination via LoRA adapters and KL-regularized training, with a hallucination detection module that can trigger an optional feedback correction loop.
- **Method:** Pipeline combining automated prompt rewriting, hybrid retrieval, and low-rank adapter (LoRA) tuning to ground responses in retrieved evidence. A hallucination detector (classifier-based and self-evaluation) assigns confidence scores to outputs; low-confidence outputs can trigger a feedback loop enforcing factual alignment through a contrastive KL loss and adapter fine-tuning.
- **Findings:**
  - The authors state that AutoRAG-LoRA significantly reduces factual drift.
  - The approach is stated to preserve the efficiency and modularity of the model.
- **Limitations (from abstract):**
  - The abstract gives no quantitative results, datasets, or baselines, so the size of the improvement cannot be assessed.
  - The feedback correction loop is described as optional, and the abstract does not say how much it contributes.

### [14] Mitigating Hallucination on Hallucination in RAG via Ensemble Voting

- **Relevance:** Presents a training-free technique, ensemble voting within RAG, for reducing hallucination in LLMs. It targets the specific failure mode where flawed retrieval compounds hallucination ("hallucination on hallucination"). It is therefore a concrete example of a retrieval-augmentation plus aggregation-based mitigation approach.
- **Contribution:** VOTE-RAG, a training-free, two-stage, parallelizable framework that uses voting at both retrieval and response generation to mitigate compounded hallucinations in RAG. The authors argue that simple ensemble voting is more efficient and reliable than more complex frameworks.
- **Method:** Stage 1, Retrieval Voting: multiple agents generate diverse queries in parallel, and all retrieved documents are aggregated. Stage 2, Response Voting: multiple agents independently generate answers from the aggregated documents, and the final answer is chosen by majority vote. The method is evaluated in comparative experiments on six benchmark datasets.
- **Findings:**
  - VOTE-RAG achieves performance comparable to or surpassing more complex RAG frameworks on six benchmark datasets.
  - It has a simpler architecture and is fully parallelizable.
  - It avoids the "problem drift" risk.
  - The authors conclude that simple ensemble voting is a superior and more efficient way to mitigate RAG hallucinations.

### [15] MultiRAG: A Knowledge-guided Framework for Mitigating Hallucination in Multi-source Retrieval Augmented Generation

- **Relevance:** Presents a RAG-based technique for reducing LLM hallucination in the multi-source setting. It uses knowledge-graph-based aggregation and confidence-based filtering of unreliable retrieved information, which is one concrete answer to the question.
- **Contribution:** MultiRAG, a knowledge-guided framework that mitigates hallucination in multi-source retrieval-augmented generation. It targets two problems: sparse multi-source data that hides logical relationships, and inconsistencies between sources that cause information conflicts.
- **Method:** Two modules. (1) A knowledge construction module uses multi-source line graphs to aggregate logical relationships across knowledge sources and address data sparsity. (2) A retrieval module uses multi-level confidence calculation, with graph-level and node-level assessments, to identify and remove unreliable information nodes and so reduce hallucinations caused by inter-source inconsistency. It was evaluated on four multi-domain query datasets and two multi-hop QA datasets.
- **Findings:**
  - Multi-source retrieval can paradoxically worsen hallucination, because of sparse data distribution and inter-source conflicts.
  - MultiRAG significantly improves the reliability and efficiency of knowledge retrieval in complex multi-source scenarios, per experiments on four multi-domain query datasets and two multi-hop QA datasets.
  - Graph-level and node-level confidence assessment can filter out unreliable information nodes to reduce conflict-induced hallucination.
- **Limitations (from abstract):**
  - The abstract gives no quantitative results, baselines, or metrics, so the size of the improvement cannot be judged.
  - The approach is specific to retrieval-augmented, multi-source settings and does not address hallucination from the model's parametric knowledge.

### [16] Token-Guard: Towards Token-Level Hallucination Control via Self-Checking Decoding

- **Relevance:** Presents a decoding-time technique for reducing LLM hallucination that works at the token level using self-checking. It is a lightweight alternative to RAG and RLHF, so it fills the decoding-based category in an overview of hallucination-mitigation techniques.
- **Contribution:** Token-Guard, a token-level hallucination control method based on self-checking decoding. It detects hallucinated tokens before they propagate and corrects them without retrieval or large-scale fine-tuning.
- **Method:** At each reasoning step the model performs internal verification to detect hallucinated tokens. Candidate fragments are evaluated in a latent space with explicit hallucination risk scoring. Iterative pruning and regeneration then dynamically correct detected errors.
- **Findings:**
  - Experiments on HALU datasets show Token-Guard substantially reduces hallucinations.
  - Token-Guard improves generation accuracy.
  - The authors describe it as a scalable, modular solution for reliable LLM outputs.
  - Code is publicly available.
- **Limitations (from abstract):**
  - The abstract gives no quantitative results, specific datasets, or baselines.
  - The abstract does not discuss computational overhead from iterative pruning and regeneration.

### [17] Theoretical Foundations and Mitigation of Hallucination in Large Language Models

- **Relevance:** Directly relevant to the question: the paper surveys and organizes mitigation techniques for LLM hallucination (retrieval-augmented generation, hallucination-aware fine-tuning, logit calibration, fact-verification modules). It also covers detection strategies and evaluation protocols that support applying and measuring those techniques, and it adds a theoretical framing of hallucination risk.
- **Contribution:** A theoretical and practical treatment of LLM hallucination that gives formal definitions (intrinsic vs. extrinsic hallucination, a 'hallucination risk'), learning-theoretic bounds on that risk, a survey of detection and mitigation strategies, a proposed unified detection-and-mitigation workflow, and recommended evaluation protocols.
- **Method:** Formal definitions and theoretical analysis, with risk bounds derived using PAC-Bayes and Rademacher complexity frameworks. A survey-style discussion of detection methods (token-level uncertainty estimation, confidence calibration, attention alignment checks) and mitigation methods (retrieval-augmented generation, hallucination-aware fine-tuning, logit calibration, fact-verification modules). A unified workflow is illustrated with a diagram. The abstract does not describe empirical experiments.
- **Findings:**
  - Hallucination can be separated into intrinsic hallucinations (unfaithful to the input) and extrinsic hallucinations (unfaithful to real-world facts), and a formal 'hallucination risk' can be defined for models.
  - Bounds on hallucination risk can be derived using PAC-Bayes and Rademacher complexity.
  - Mitigation approaches include retrieval-augmented generation, hallucination-aware fine-tuning, logit calibration, and fact-verification modules.
  - Detection strategies include token-level uncertainty estimation, confidence calibration, and attention alignment checks.
  - A unified workflow can integrate detection and mitigation strategies.
  - The paper recommends datasets, metrics, and experimental setups for evaluating hallucination.
- **Limitations (from abstract):**
  - The abstract does not report empirical results or quantitative comparisons of the mitigation techniques.
  - The mitigation methods are discussed at a survey level, so their relative effectiveness is not established in the abstract.

### [18] Self-Alignment for Factuality: Mitigating Hallucinations in LLMs via Self-Evaluation

- **Relevance:** Presents a concrete technique for reducing hallucination: a self-alignment pipeline in which the LLM evaluates the factuality of its own outputs and is then fine-tuned with preference optimization, avoiding human factuality annotations. It is an example of training-time, annotation-free mitigation.
- **Contribution:** Self-Alignment for Factuality: uses an LLM's own self-evaluation as the training signal to steer it toward factual outputs. It introduces Self-Eval and Self-Knowledge Tuning (SK-Tuning) to improve self-evaluation through better confidence estimation and calibration.
- **Method:** Self-Eval prompts the LLM to validate the factuality of its own generated responses using only its internal knowledge. SK-Tuning improves the model's confidence estimation and calibration to strengthen this self-evaluation. The self-annotated responses are used as preference data to fine-tune the model with Direct Preference Optimization (DPO). Evaluation is on Llama family models.
- **Findings:**
  - The self-alignment approach substantially enhances factual accuracy over Llama family models.
  - Improvements were shown across three knowledge-intensive tasks on TruthfulQA and BioGEN.
  - Factuality training signals can be obtained from the model's own self-evaluation, without high-quality human factuality annotations.
- **Limitations (from abstract):**
  - The self-evaluation relies solely on the model's internal knowledge, so it can only be as good as what the model already knows.
  - Evaluation is described only for Llama family models and on TruthfulQA and BioGEN.

### [19] Exploring the Generalizability of Factual Hallucination Mitigation via Enhancing Precise Knowledge Utilization

- **Relevance:** Presents a post-training technique for reducing factual hallucination in LLMs. It improves the model's precise use of its own knowledge through preference optimization on self-generated answers, and it targets the generalization and capability trade-off problems of existing mitigation methods.
- **Contribution:** Introduces PKUE (Precise Knowledge Utilization Enhancement), a method that fine-tunes an LLM to better leverage its knowledge, and FactualBench, a 181k-example Chinese factual QA dataset covering 21 domains for evaluation and training.
- **Method:** Fine-tunes the model through preference optimization on self-generated responses to precise, simple factual questions. FactualBench is used for evaluation and training.
- **Findings:**
  - PKUE significantly improves LLM overall performance.
  - The gains are consistent across factual tasks of various forms.
  - The gains extend to general tasks beyond factuality.
  - The gains also extend to tasks in a different language.
- **Limitations (from abstract):**
  - The abstract says existing post-training methods generalize poorly and trade off other capabilities. It does not state limitations of PKUE itself.

### [20] FLAME: Factuality-Aware Alignment for Large Language Models

- **Relevance:** Presents an alignment-stage technique for reducing hallucination: factuality-aware SFT and factuality-aware RL (via DPO). It also identifies the causes of hallucination in standard alignment, which helps explain why mitigation is needed there.
- **Contribution:** Identifies factors that cause hallucination in both SFT and RL alignment steps, and proposes factuality-aware alignment (factuality-aware SFT plus factuality-aware RL via direct preference optimization) to make LLM outputs more factual while preserving instruction-following.
- **Method:** Analysis of the SFT and RL alignment stages to find the sources of hallucination. For SFT, training on new knowledge or unfamiliar texts, such as human-labeled data that may be novel to the LLM, encourages hallucination. For RL, standard reward functions favor longer, more detailed, helpful responses, which also encourages hallucination. Based on these findings, the authors propose factuality-aware SFT and factuality-aware RL through direct preference optimization.
- **Findings:**
  - Conventional alignment fails to improve factual accuracy of LLMs and often leads to more false facts (hallucination).
  - Training on new knowledge or unfamiliar texts can encourage hallucination, which makes SFT on human-labeled data less factual.
  - Reward functions in standard RL can encourage hallucination because they prefer longer, more detailed responses.
  - Factuality-aware alignment guides LLMs to output more factual responses while maintaining instruction-following capability.

## Search log

**Round 1** (39 new candidates)
- `(ti:hallucination OR abs:hallucination OR abs:hallucinations) AND (abs:"retrieval-augmented generation" OR abs:"retrieval augmented" OR abs:grounding) AND abs:"large language models"`
- `(ti:hallucination OR abs:hallucinations) AND (abs:decoding OR abs:"contrastive decoding" OR abs:"inference-time intervention" OR abs:"activation steering") AND abs:"language models"`
- `(ti:hallucination OR abs:hallucination) AND (abs:"fine-tuning" OR abs:"preference optimization" OR abs:RLHF OR abs:"factuality tuning") AND (abs:factuality OR abs:truthfulness) AND abs:"language models"`
- `ti:"Survey of Hallucination in Natural Language Generation" OR ti:"A Survey on Hallucination in Large Language Models" OR ti:"SelfCheckGPT" OR ti:"Chain-of-Verification Reduces Hallucination in Large Language Models" OR ti:"DoLa: Decoding by Contrasting Layers Improves Factuality in Large Language Models" OR ti:"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" OR ti:"Inference-Time Intervention: Eliciting Truthful Answers from a Language Model"`

**Round 2** (39 new candidates)
- `ti:"Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" OR ti:"Language Models (Mostly) Know What They Know" OR ti:"Let's Verify Step by Step" OR ti:"Training language models to follow instructions with human feedback" OR ti:"ReAct: Synergizing Reasoning and Acting in Language Models" OR ti:"Self-Consistency Improves Chain of Thought Reasoning in Language Models" OR ti:"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" OR ti:"TruthfulQA: Measuring How Models Mimic Human Falsehoods" OR ti:"HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models"`
- `(abs:abstention OR abs:"uncertainty estimation" OR abs:calibration OR abs:"I don't know" OR abs:"selective prediction") AND (abs:hallucination OR abs:hallucinations OR abs:factuality) AND abs:"language models"`
- `(abs:"knowledge editing" OR abs:"model editing" OR ti:"editing factual knowledge") AND (abs:"factual errors" OR abs:hallucination OR abs:"outdated knowledge") AND abs:"language models"`
- `(abs:"tool-augmented" OR abs:"tool use" OR abs:"process supervision" OR abs:"self-verification" OR abs:"self-consistency") AND (abs:hallucination OR abs:hallucinations OR abs:factuality) AND abs:"large language models"`
