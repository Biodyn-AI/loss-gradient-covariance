# Online validation of the expanded paper bibliography

Checked on **17 November 2026**. The revised paper has **50 distinct references**, all cited in context. Every work was individually opened online and checked against a publisher, proceedings, author-hosted paper, or publisher-deposited record. The check covered the title, authors, year and publication status, and the claim for which the paper cites it. Preprint and published versions of one work count as one reference.

This is a source and citation audit, not independent verification of every proof in the cited literature. Access limitations are stated below. In particular, the Pemantle entry was checked through publisher-deposited metadata and its abstract, rather than a successfully retrieved full paper. The accepted status of Su et al. is reported by the authors’ arXiv record. No external human review is implied.

The machine-readable companion is `research/papers/q2_coupling_phases_20261117/reference_validation.json`. Citation line numbers refer to the revised `main.tex`.

## Individual checks

### 1. Adaptive Subgradient Methods for Online Learning and Stochastic Optimization

**Authors:** John Duchi; Elad Hazan; Yoram Singer.
**Publication:** Journal of Machine Learning Research 12(61):2121-2159, 2011.
**Validated source:** [Adaptive Subgradient Methods for Online Learning and Stochastic Optimization](https://jmlr.org/papers/v12/duchi11a.html).

**Opened records:** [record 1](https://jmlr.org/papers/v12/duchi11a.html).

**Citation supports:** Adaptive geometry based on past gradients predates Adam; AdaGrad provides a foundational example with online-learning guarantees. These regret results do not imply the fixed-memory, constant-step stationary claims proved here.
**Evidence checked:** The publisher page supplies all authors and the complete journal citation. Its abstract develops adaptive subgradient methods whose geometry changes with previously observed gradients and gives regret guarantees relative to hindsight choices of proximal geometry.
**Evidence location:** JMLR publisher page, bibliographic header and abstract; lines 30-36.
**Manuscript citation lines:** 113.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 2. ADADELTA: An Adaptive Learning Rate Method

**Authors:** Matthew D. Zeiler.
**Publication:** arXiv preprint arXiv:1212.5701, 2012.
**Validated source:** [ADADELTA: An Adaptive Learning Rate Method](https://arxiv.org/abs/1212.5701).

**Opened records:** [record 1](https://arxiv.org/abs/1212.5701).

**Citation supports:** Coordinate-specific learning-rate adaptation using gradient history has established algorithmic precedents besides AdaGrad and Adam. The paper is background, not evidence for noise-curvature coupling or a modern LLM advantage.
**Evidence checked:** The primary submission page names Zeiler as the sole author and dates the preprint to December 2012. Its abstract presents coordinate-specific step adaptation using first-order information with modest additional computational cost.
**Evidence location:** arXiv title, author, submission date and abstract; lines 8-18.
**Manuscript citation lines:** 114.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** The opened primary page does not identify a conference or journal; retain the preprint designation.

### 3. Adam: A Method for Stochastic Optimization

**Authors:** Diederik P. Kingma; Jimmy Ba.
**Publication:** 3rd International Conference on Learning Representations (ICLR 2015), 2015.
**Validated source:** [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980).

**Opened records:** [record 1](https://arxiv.org/abs/1412.6980).

**Citation supports:** Adam uses running estimates of gradient moments to determine its update. Cite for the algorithm definition and history, not as a valid blanket convergence guarantee: subsequent work identified a problem in the original convergence argument.
**Evidence checked:** The author-deposited primary page identifies the authors, title and ICLR 2015 publication. It introduces an optimizer using adaptive first- and second-moment estimates. The initial arXiv submission is from December 2014; the conference year is 2015.
**Evidence location:** arXiv abstract and publication comment; page lines 8-19.
**Manuscript citation lines:** 115.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** The primary arXiv author field uses Jimmy Ba. Use 2015 for the ICLR paper, not the 2014 preprint date.

### 4. Decoupled Weight Decay Regularization

**Authors:** Ilya Loshchilov; Frank Hutter.
**Publication:** International Conference on Learning Representations (ICLR 2019), 2019.
**Validated source:** [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101).

**Opened records:** [record 1](https://arxiv.org/abs/1711.05101).

**Citation supports:** Decoupled weight decay and adding an L2 penalty to the gradient generally produce different adaptive-optimizer updates. This supports the manuscript's explicit AdamW decay convention.
**Evidence checked:** The primary abstract distinguishes weight decay from an L2 penalty for adaptive algorithms and proposes applying weight decay separately from the loss-gradient update. Its publication comment explicitly identifies ICLR 2019; the first preprint is from November 2017.
**Evidence location:** arXiv abstract, authors and publication comment; lines 8-20.
**Manuscript citation lines:** 116.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** The OpenReview forum was attempted but returned a browser-verification page. Validation uses the successfully opened author-deposited arXiv source, which explicitly states ICLR 2019.

### 5. Dissecting Adam: The Sign, Magnitude and Variance of Stochastic Gradients

**Authors:** Lukas Balles; Philipp Hennig.
**Publication:** Proceedings of the 35th International Conference on Machine Learning, PMLR 80:404-413, 2018.
**Validated source:** [Dissecting Adam: The Sign, Magnitude and Variance of Stochastic Gradients](https://proceedings.mlr.press/v80/balles18a.html).

**Opened records:** [record 1](https://proceedings.mlr.press/v80/balles18a.html).

**Citation supports:** Adam's normalization already has established sign-and-variance interpretations. The present paper should distinguish its fixed-marginal curvature-noise coupling classification from claiming that normalized or sign-like updates are a new observation.
**Evidence checked:** The official proceedings page identifies the complete citation. The authors decompose Adam into a sign-based direction and a step magnitude adapted to relative gradient variability, then examine these ingredients separately.
**Evidence location:** PMLR official page, title/authors/venue, abstract and BibTeX; lines 8-23.
**Manuscript citation lines:** 118.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 6. signSGD: Compressed Optimisation for Non-Convex Problems

**Authors:** Jeremy Bernstein; Yu-Xiang Wang; Kamyar Azizzadenesheli; Animashree Anandkumar.
**Publication:** Proceedings of the 35th International Conference on Machine Learning, PMLR 80:560-569, 2018.
**Validated source:** [signSGD: Compressed Optimisation for Non-Convex Problems](https://proceedings.mlr.press/v80/bernstein18a.html).

**Opened records:** [record 1](https://proceedings.mlr.press/v80/bernstein18a.html).

**Citation supports:** Sign-based update geometry and its relationship to noise and curvature already have a substantial theoretical literature. This supplies background for normalized-update mechanisms, not a prior proof of the present fixed-marginal stationary phase separation.
**Evidence checked:** The official PMLR page lists the full citation and studies sign-compressed stochastic gradients. Its abstract identifies relative l1/l2 properties of gradient, curvature and noise as relevant to comparisons with SGD, and reports a momentum variant resembling Adam empirically on ImageNet.
**Evidence location:** Official PMLR title/authors/venue, abstract and BibTeX; lines 8-26.
**Manuscript citation lines:** 119.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** Use the official PMLR full name Animashree Anandkumar; the deposited PDF byline shortens this to Anima Anandkumar.

### 7. Adaptive Methods for Nonconvex Optimization

**Authors:** Manzil Zaheer; Sashank J. Reddi; Devendra Sachan; Satyen Kale; Sanjiv Kumar.
**Publication:** Advances in Neural Information Processing Systems 31 (NeurIPS 2018), 2018.
**Validated source:** [Adaptive Methods for Nonconvex Optimization](https://proceedings.neurips.cc/paper/2018/hash/90365351ccc7437a1309dc64e4db32a3-Abstract.html).

**Opened records:** [record 1](https://proceedings.neurips.cc/paper/2018/hash/90365351ccc7437a1309dc64e4db32a3-Abstract.html).

**Citation supports:** There is established nonconvex convergence analysis whose guarantees depend on noise magnitude and minibatch size. Such results address convergence conditions and noise floors, rather than identifying sharp differences between couplings with identical complete marginals.
**Evidence checked:** The official proceedings page analyzes adaptive optimizers in nonconvex stochastic problems, including how increasing minibatch sizes affects approach to stationarity. It also introduces Yogi to regulate the effective stepsize.
**Evidence location:** Official NeurIPS title/authors/venue and abstract; lines 0-10. The primary paper PDF spells Reddi's middle initial J.
**Manuscript citation lines:** 122.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 8. On the Convergence of A Class of Adam-Type Algorithms for Non-Convex Optimization

**Authors:** Xiangyi Chen; Sijia Liu; Ruoyu Sun; Mingyi Hong.
**Publication:** International Conference on Learning Representations (ICLR 2019), 2019.
**Validated source:** [On the Convergence of A Class of Adam-Type Algorithms for Non-Convex Optimization](https://arxiv.org/pdf/1808.02941).

**Opened records:** [record 1](https://arxiv.org/pdf/1808.02941).

**Citation supports:** Adam-type convergence has sufficient-condition analyses covering several update rules. Do not state that these guarantees cover every fixed-beta, constant-learning-rate Adam process or imply convergence to its objective minimizer under the present assumptions.
**Evidence checked:** The primary PDF header states ICLR 2019 and lists all four authors. The abstract supplies sufficient conditions for a class of adaptive momentum algorithms to attain nonconvex stationarity bounds, and gives examples showing failures when those conditions are violated.
**Evidence location:** Primary paper PDF, first page header and abstract; lines 0-25. arXiv first submission is August 2018.
**Manuscript citation lines:** 122.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** The direct OpenReview PDF URL returned a verification page; the successfully opened author-deposited PDF itself confirms the conference venue.

### 9. A Sufficient Condition for Convergences of Adam and RMSProp

**Authors:** Fangyu Zou; Li Shen; Zequn Jie; Weizhong Zhang; Wei Liu.
**Publication:** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2019), pages 11127-11135, 2019.
**Validated source:** [A Sufficient Condition for Convergences of Adam and RMSProp](https://arxiv.org/abs/1811.09358).

**Opened records:** [record 1](https://arxiv.org/abs/1811.09358).

**Citation supports:** The behavior of the second-moment memory and learning-rate schedule is central to established convergence conditions. These conditions are not a claim of minimizer consistency for arbitrary fixed beta and fixed learning rate.
**Evidence checked:** The primary arXiv page provides all authors and explicitly confirms CVPR 2019 acceptance. The abstract derives a condition involving the base stepsize and historical squared-gradient weights sufficient for convergence of generic Adam/RMSProp in nonconvex stochastic optimization.
**Evidence location:** arXiv author/title/abstract/acceptance comment; lines 8-20. Official CVF indexed primary citation supplies pages 11127-11135.
**Manuscript citation lines:** 123.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** The CVF publisher page was located and its citation inspected in search, but direct opening returned 403. The successfully opened primary arXiv page independently confirms the title, authors, claim and conference; it is the validation URL.

### 10. A Simple Convergence Proof of Adam and Adagrad

**Authors:** Alexandre Défossez; Léon Bottou; Francis Bach; Nicolas Usunier.
**Publication:** Transactions on Machine Learning Research (October 2022), 2022.
**Validated source:** [A Simple Convergence Proof of Adam and Adagrad](https://arxiv.org/pdf/2003.02395).

**Opened records:** [record 1](https://arxiv.org/pdf/2003.02395).

**Citation supports:** Rigorous convergence guarantees for Adam require a specified parameter regime and assumptions. They should be distinguished from a fixed-memory, constant-step invariant-law limit and from a claim that every small-step invariant law concentrates at the population minimum.
**Evidence checked:** The final author-deposited PDF explicitly carries the TMLR October 2022 publication header. It proves nonconvex stationarity bounds for Adam and Adagrad with bounded stochastic gradients and appropriately chosen optimization parameters, with explicit dependence on momentum.
**Evidence location:** Primary PDF first-page header, authors and abstract; lines 0-28; setup discussion on second page, lines 51-70.
**Manuscript citation lines:** 125.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** Accented primary author names are Alexandre Défossez and Léon Bottou. Initial preprint 2020; journal publication 2022. Direct OpenReview PDF access was challenged; the opened arXiv PDF is the published-format version.

### 11. Adam Can Converge Without Any Modification On Update Rules

**Authors:** Yushun Zhang; Congliang Chen; Naichen Shi; Ruoyu Sun; Zhi-Quan Luo.
**Publication:** Advances in Neural Information Processing Systems 35 (NeurIPS 2022), 2022.
**Validated source:** [Adam Can Converge Without Any Modification On Update Rules](https://papers.neurips.cc/paper_files/paper/2022/hash/b6260ae5566442da053e5ab5d691067a-Abstract-Conference.html).

**Opened records:** [record 1](https://papers.neurips.cc/paper_files/paper/2022/hash/b6260ae5566442da053e5ab5d691067a-Abstract-Conference.html).

**Citation supports:** Problem-dependent hyperparameters and memory values already yield established convergence/divergence regime distinctions for vanilla Adam. The novelty claim here must concern changing the noise-curvature coupling with fixed marginals and fixed optimizer parameters, rather than the mere existence of different dynamical phases.
**Evidence checked:** The official page proves convergence to a critical-point neighborhood for sufficiently large beta2 and beta1 below its square root, with stronger conclusions under an additional growth condition. It also describes divergence regions for small beta2. Hyperparameters depend on the fixed problem.
**Evidence location:** Official NeurIPS metadata and abstract; lines 0-13.
**Manuscript citation lines:** 125.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 12. AdaBelief Optimizer: Adapting Stepsizes by the Belief in Observed Gradients

**Authors:** Juntang Zhuang; Tommy Tang; Yifan Ding; Sekhar C. Tatikonda; Nicha Dvornek; Xenophon Papademetris; James S. Duncan.
**Publication:** Advances in Neural Information Processing Systems 33 (NeurIPS 2020), 2020.
**Validated source:** [AdaBelief Optimizer: Adapting Stepsizes by the Belief in Observed Gradients](https://proceedings.neurips.cc/paper/2020/hash/d9d4f495e875a2e075a1a4a6e1b9770f-Abstract.html).

**Opened records:** [record 1](https://proceedings.neurips.cc/paper/2020/hash/d9d4f495e875a2e075a1a4a6e1b9770f-Abstract.html).

**Citation supports:** The choice of statistic in an adaptive denominator is an established algorithmic design question. The paper's mathematical results concern the stated AdamW recursion and do not automatically transfer to alternatives such as AdaBelief.
**Evidence checked:** The official proceedings identifies NeurIPS 2020 and all authors. The primary abstract motivates an adaptive stepsize using disagreement between the observed gradient and a prediction supplied by its exponential moving average, rather than only the uncentered gradient-square statistic.
**Evidence location:** Official NeurIPS title/authors/venue and abstract, lines 0-12; primary arXiv abstract, lines 16-24.
**Manuscript citation lines:** 129.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** The official page includes Sekhar C Tatikonda; the primary arXiv page supplies James S. Duncan and spells Dvornek consistently. Do not reproduce the apparent Dvornik OCR error from the indexed PDF.

### 13. Convergence rates for the Adam optimizer

**Authors:** Steffen Dereich; Arnulf Jentzen.
**Publication:** arXiv preprint, 2024.
**Validated source:** [Convergence rates for the Adam optimizer](https://arxiv.org/abs/2407.21078).

**Opened records:** [record 1](https://arxiv.org/abs/2407.21078), [record 2](https://arxiv.org/html/2407.21078v1).

**Citation supports:** The averaged Adam update depends on the complete sampling law and can differ from the population gradient; the history-space framework is prior work.
**Evidence checked:** Definition 2.4 averages the native quotient over a whole frozen innovation history. The paper develops its sequence space, observable regularity and perturbation analysis. This supports attributing the full-law field and history framework to prior work, without attributing the present matched-coupling theorem to it.
**Evidence location:** Full text Definition 2.4, equation (9); Sections 3–4 and 8.
**Manuscript citation lines:** 134.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 14. Central limit theorem for the averaged Adam optimizer

**Authors:** Steffen Dereich; Arnulf Jentzen.
**Publication:** arXiv preprint, 2026.
**Validated source:** [Central limit theorem for the averaged Adam optimizer](https://arxiv.org/abs/2606.21433).

**Opened records:** [record 1](https://arxiv.org/abs/2606.21433), [record 2](https://arxiv.org/html/2606.21433v1).

**Citation supports:** Gaussian limit theorems for averaged Adam use a field derivative, a corrected noise covariance and a stable attractor.
**Evidence checked:** The main theorem assumes a linearization with strictly negative spectral real parts and gives an averaged-iterate CLT conditional on convergence to that zero. Its covariance uses a martingale correction. This validates the stable-attractor comparison and distinguishes it from constant-step invariant-risk separation.
**Evidence location:** Definition 2.5; Theorem 2.6(b), equations (14)–(20).
**Manuscript citation lines:** 136, 161.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 15. Adam symmetry theorem: characterization of the convergence of the stochastic Adam optimizer

**Authors:** Steffen Dereich; Thang Do; Arnulf Jentzen; Philippe von Wurstemberger.
**Publication:** arXiv preprint, 2025. Revised 2026.
**Validated source:** [Adam symmetry theorem: characterization of the convergence of the stochastic Adam optimizer](https://arxiv.org/abs/2511.06675).

**Opened records:** [record 1](https://arxiv.org/abs/2511.06675), [record 2](https://arxiv.org/html/2511.06675v2).

**Citation supports:** The specifically cited symmetry theorem treats fixed isotropic sample curvature and separates symmetric from asymmetric data.
**Evidence checked:** Theorem 4.12 uses squared Euclidean distance losses and iid two-point data, hence deterministic Hessian proportional to the identity. Under its decreasing-step assumptions it equates symmetry with convergence/error properties. This supports the manuscript's theorem-specific contrast; broader results elsewhere in the paper should not be dismissed as isotropic.
**Evidence location:** Theorem 4.12, full-text lines 1812–1831.
**Manuscript citation lines:** 138, 154.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 16. On the Convergence of Adam and Beyond

**Authors:** Sashank J. Reddi; Satyen Kale; Sanjiv Kumar.
**Publication:** International Conference on Learning Representations (ICLR), 2018.
**Validated source:** [On the Convergence of Adam and Beyond](https://arxiv.org/abs/1904.09237).

**Opened records:** [record 1](https://arxiv.org/abs/1904.09237), [record 2](https://arxiv.org/html/1904.09237v1).

**Citation supports:** Adam failure on stochastic convex problems is established prior work.
**Evidence checked:** Theorem 3 supplies a stochastic convex counterexample under fixed admissible momentum parameters. This directly supports the manuscript's acknowledgment that convex stochastic nonconvergence is classical. The conference year 2018 and later arXiv identifier are consistent, not a bibliographic mismatch.
**Evidence location:** Theorem 3 and Appendix C.
**Manuscript citation lines:** 139.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** ["OpenReview forum was also attempted but returned a browser challenge; the official author-uploaded arXiv paper was accessible."]

### 17. A Stability Analysis of AdamW: Unstable Equilibria and Non-Convergence

**Authors:** Baiyu Su; Lizhang Chen; Qiang Liu.
**Publication:** NeurIPS 2026 (accepted, as stated on the authors' arXiv record), 2026.
**Validated source:** [A Stability Analysis of AdamW: Unstable Equilibria and Non-Convergence](https://arxiv.org/abs/2611.11526).

**Opened records:** [record 1](https://arxiv.org/abs/2611.11526), [record 2](https://arxiv.org/html/2611.11526v1).

**Citation supports:** Deterministic AdamW already has unstable equilibria and exact discrete-step stability conditions; fixed memory alone does not distinguish the present work.
**Evidence checked:** Proposition 4.3 characterizes stability of deterministic ODE equilibria. Appendix A.6 separately analyzes the autonomous exact-gradient discrete update and finite-step Schur/Jury conditions. The manuscript correctly acknowledges both rather than describing this source as only a continuous-time result.
**Evidence location:** Proposition 4.3; Appendix A.6, particularly Proposition A.15 and its Jury conditions.
**Manuscript citation lines:** 140, 157.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** ["Conference acceptance is verified from the primary author-uploaded arXiv record; a separate NeurIPS proceedings entry was not located. Cite as accepted if distinguishing acceptance from proceedings publication."]

### 18. Gradient Descent on Neural Networks Typically Occurs at the Edge of Stability

**Authors:** Jeremy M. Cohen; Simran Kaur; Yuanzhi Li; J. Zico Kolter; Ameet Talwalkar.
**Publication:** International Conference on Learning Representations, 2021.
**Validated source:** [Gradient Descent on Neural Networks Typically Occurs at the Edge of Stability](https://arxiv.org/abs/2103.00065).

**Opened records:** [record 1](https://arxiv.org/abs/2103.00065).

**Citation supports:** Large-step neural edge-of-stability behavior is established and differs from a fixed-law small-step stationary error floor.
**Evidence checked:** Reports full-batch neural gradient descent near a learning-rate-dependent Hessian stability threshold, with nonmonotone short-time loss.
**Evidence location:** arXiv author list, ICLR2021 comment and abstract
**Manuscript citation lines:** 142.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 19. Adaptive Gradient Methods at the Edge of Stability

**Authors:** Jeremy M. Cohen; Behrooz Ghorbani; Shankar Krishnan; Naman Agarwal; Sourabh Medapati; Michal Badura; Daniel Suo; David Cardoze; Zachary Nado; George E. Dahl; Justin Gilmer.
**Publication:** arXiv preprint, 2022. Revised 2024.
**Validated source:** [Adaptive Gradient Methods at the Edge of Stability](https://arxiv.org/abs/2207.14484).

**Opened records:** [record 1](https://arxiv.org/abs/2207.14484).

**Citation supports:** Adaptive edge-of-stability behavior is known; the current theorem concerns another limit. No NeurIPS2022 main-conference venue is inferred.
**Evidence checked:** Investigates full- and large-batch adaptive methods near a stability threshold of the preconditioned Hessian. The revised arXiv author list includes eleven authors.
**Evidence location:** arXiv v2 author list, submission/revision history and abstract
**Manuscript citation lines:** 142.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 20. Adam at the Edge of Stability: Adaptive Feedback, Provable Oscillation, and Gradient Reversal

**Authors:** Yiman Fong; Heng Yang.
**Publication:** arXiv preprint, 2026. Revised 2026.
**Validated source:** [Adam at the Edge of Stability: Adaptive Feedback, Provable Oscillation, and Gradient Reversal](https://arxiv.org/abs/2608.20638).

**Opened records:** [record 1](https://arxiv.org/abs/2608.20638), [record 2](https://arxiv.org/html/2608.20638v2).

**Citation supports:** Large-learning-rate edge-of-stability and gradient reversal are existing phenomena distinct from the present small-step stationary effect.
**Evidence checked:** The analysis studies adaptive feedback near an active stability boundary. Lemma 4.1 gives reversal under a supercritical active-curvature condition in a rank-one setting. This supports the acknowledged large-step phenomenon; it does not establish the manuscript's fixed-noise-coupling stationary-order theorem.
**Evidence location:** Sections 3–4; Lemma 4.1.
**Manuscript citation lines:** 143.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 21. Same Loss, Same Noise, Opposite Schedules: Noise Structure and Optimizer Normalization Jointly Determine Whether Learning-Rate Cooldown Helps

**Authors:** Subham Singh; Ashutosh Mishra; Subha Raut.
**Publication:** arXiv preprint, 2026.
**Validated source:** [Same Loss, Same Noise, Opposite Schedules: Noise Structure and Optimizer Normalization Jointly Determine Whether Learning-Rate Cooldown Helps](https://arxiv.org/abs/2607.12360).

**Opened records:** [record 1](https://arxiv.org/abs/2607.12360), [record 2](https://arxiv.org/html/2607.12360v1).

**Citation supports:** Normalization-dependent error floors versus SGD under multiplicative noise precede the present result.
**Evidence checked:** Proposition 1 derives multiplicative-noise SGD contraction, while Proposition 2 and its appendix establish signSGD granularity and a stationary squared-step floor. Periodicity limits single-iterate interpretations. The manuscript's broad attribution is supported; these are sign/normalized methods, not the same fixed-positive-offset AdamW coupling experiment.
**Evidence location:** Propositions 1–2; Technical Appendix A.
**Manuscript citation lines:** 149.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 22. A Stochastic Approximation Method

**Authors:** Herbert Robbins; Sutton Monro.
**Publication:** The Annals of Mathematical Statistics 22(3):400–407, 1951.
**Validated source:** [A Stochastic Approximation Method](https://doi.org/10.1214/aoms/1177729586).

**Opened records:** [record 1](https://www.columbia.edu/~ww2040/8100F16/RM51.pdf).

**Citation supports:** Noisy root finding and stochastic approximation long predate modern adaptive optimizers.
**Evidence checked:** The original paper formulates sequential root finding from noisy observations and proves convergence in probability for its decreasing-step recursion under stated monotonicity and boundedness assumptions.
**Evidence location:** Published cover metadata; §1 Summary (p.400); §3 Convergence theorems (pp.401–405).
**Manuscript citation lines:** 167.
**Scope:** Historical foundation, not a theorem about fixed-memory AdamW invariant laws.

**Additional validation detail:** Euclid landing page returned an iframe; the original published PDF and its journal cover were successfully opened.

### 23. Stochastic Approximation and Recursive Algorithms and Applications

**Authors:** Harold J. Kushner; G. George Yin.
**Publication:** Springer, Stochastic Modelling and Applied Probability 35, second edition, 2003.
**Validated source:** [Stochastic Approximation and Recursive Algorithms and Applications](https://link.springer.com/book/10.1007/b97441).

**Opened records:** [record 1](https://link.springer.com/book/10.1007/b97441).

**Citation supports:** ODE, weak-convergence and averaging methods belong to the established stochastic-approximation toolkit.
**Evidence checked:** The book develops qualitative and asymptotic analysis of recursive stochastic algorithms, with separate chapters on correlated noise, weak convergence and iterate averaging.
**Evidence location:** Author list; About this book; contents: correlated-noise convergence, weak-convergence methods, rates, averaging; bibliographic information.
**Manuscript citation lines:** 169.
**Scope:** A general methodological reference; applicability of individual results to the present native-history chain is not assumed without proof.

### 24. Dynamics of stochastic approximation algorithms

**Authors:** Michel Benaïm.
**Publication:** Séminaire de Probabilités XXXIII, Springer, pp.1–68, 1999.
**Validated source:** [Dynamics of stochastic approximation algorithms](https://numdam.org/item/SPS_1999__33__1_0/).

**Opened records:** [record 1](https://numdam.org/item/SPS_1999__33__1_0/), [record 2](https://www.numdam.org/item/SPS_1999__33__1_0.pdf).

**Citation supports:** ODE descriptions and probabilistic avoidance of unstable limiting sets are established theory.
**Evidence checked:** The notes develop the dynamical-systems approach through asymptotic pseudotrajectories, describe possible limit sets, and discuss nonconvergence to repelling sets. The introduction explicitly focuses mainly on decreasing steps.
**Evidence location:** Original paper §1, pp.3–5; §4; §9, Nonconvergence to unstable points, periodic orbits and normally hyperbolic sets.
**Manuscript citation lines:** 169.
**Scope:** Decreasing-step path nonconvergence is distinct from a positive risk floor for every small-fixed-step invariant selection.

### 25. The O.D.E. Method for Convergence of Stochastic Approximation and Reinforcement Learning

**Authors:** V. S. Borkar; S. P. Meyn.
**Publication:** SIAM Journal on Control and Optimization 38(2):447–469, 2000.
**Validated source:** [The O.D.E. Method for Convergence of Stochastic Approximation and Reinforcement Learning](https://epubs.siam.org/doi/abs/10.1137/S0363012997331639).

**Opened records:** [record 1](https://epubs.siam.org/doi/abs/10.1137/S0363012997331639), [record 2](https://faculty.eng.ufl.edu/meyn/wp-content/uploads/sites/671/archive/spm_files/Papers_pdf/ode.pdf).

**Citation supports:** Averaged-ODE stability arguments, including small bounded-step results, are established stochastic-approximation theory.
**Evidence checked:** The paper derives stability from an associated ODE and treats both decreasing steps and bounded small steps. Under additional assumptions it gives bounded-step concentration and ergodicity statements.
**Evidence location:** Full paper §2.1, Theorems2.1–2.4; journal issue metadata.
**Manuscript citation lines:** 169.
**Scope:** Do not claim classical ODE theory only treats decreasing steps, and do not claim the present invariant-law proof follows merely from a local Jacobian sign.

**Additional validation detail:** All authors are included; initials are retained as printed on the journal article.

### 26. Nonconvergence to Unstable Points in Urn Models and Stochastic Approximations

**Authors:** Robin Pemantle.
**Publication:** The Annals of Probability 18(2):698–712, 1990.
**Validated source:** [Nonconvergence to Unstable Points in Urn Models and Stochastic Approximations](https://doi.org/10.1214/aop/1176990853).

**Opened records:** [record 1](https://api.crossref.org/works/10.1214/aop/1176990853).

**Citation supports:** Avoidance of noisy unstable equilibria is classical and must not be claimed as a new general principle.
**Evidence checked:** For steps of order one over time, sufficiently multidirectional noise prevents convergence to unstable equilibria of the associated smooth deterministic flow.
**Evidence location:** Crossref fields title, author, container-title, volume, issue, page, published, abstract; HTTP200. Also cross-checked against Benaïm1999 §9.
**Manuscript citation lines:** 170.
**Scope:** Validation here covers the publisher-deposited abstract and metadata, not a fresh verification of the full original proof; the result concerns decreasing steps.

**Additional validation detail:** Euclid returned an empty iframe; the author page and Berkeley full-paper endpoint returned403. No failed fetch is represented as a full-paper read.

### 27. Asymptotic Behavior of a Markovian Stochastic Algorithm with Constant Step

**Authors:** Jean-Claude Fort; Gilles Pagès.
**Publication:** SIAM Journal on Control and Optimization, 1999.
**Validated source:** [Asymptotic Behavior of a Markovian Stochastic Algorithm with Constant Step](https://epubs.siam.org/doi/abs/10.1137/S0363012997328610).

**Opened records:** [record 1](https://epubs.siam.org/doi/abs/10.1137/S0363012997328610).

**Citation supports:** Classical constant-step stationary-distribution arguments exclude repulsive limiting sets under suitable assumptions.
**Evidence checked:** The abstract describes tight invariant families, ODE-invariant small-step limits and exclusion of repulsive thin sets; additional pseudogradient assumptions exclude saddle/spurious equilibria. This supports historical method attribution only, not a direct import of its theorem to the native AdamW recursion.
**Evidence location:** Publisher abstract.
**Manuscript citation lines:** 173.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** ["Initial DOI open failed, but the official SIAM abstract/information URL opened successfully. The displayed 2006 online-hosting date is distinct from the 1999 journal issue year."]

### 28. Bridging the gap between constant step size stochastic gradient descent and Markov chains

**Authors:** Aymeric Dieuleveut; Alain Durmus; Francis Bach.
**Publication:** The Annals of Statistics, 2020.
**Validated source:** [Bridging the gap between constant step size stochastic gradient descent and Markov chains](https://arxiv.org/abs/1707.06386).

**Opened records:** [record 1](https://arxiv.org/abs/1707.06386), [record 2](https://www.cmap.polytechnique.fr/~aymeric.dieuleveut/papers/Dieuleveut-Durmus-Bach.pdf), [record 3](https://researchportal.ip-paris.fr/en/publications/bridging-the-gap-between-constant-step-size-stochastic-gradient-d/).

**Citation supports:** Constant-step SGD, invariant distributions and Markov-chain/moment-expansion tools are established prior work.
**Evidence checked:** The source develops constant-step SGD through Markov chains and expansions of moments, including noise, step and initialization effects. It supports the classical stationary-analysis context, without supplying a native fixed-memory AdamW phase theorem.
**Evidence location:** Author-hosted full paper abstract and official institutional publication abstract.
**Manuscript citation lines:** 173.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** ["Publisher DOI endpoint redirected to a bot challenge and the official complete-issue PDF returned 502. The primary author-hosted full paper and official author-institution record were accessible."]

### 29. Stationary Behavior of Constant Stepsize SGD Type Algorithms: An Asymptotic Characterization

**Authors:** Zaiwei Chen; Shancong Mou; Siva Theja Maguluri.
**Publication:** Proceedings of the ACM on Measurement and Analysis of Computing Systems 6(1):1–24, 2022.
**Validated source:** [Stationary Behavior of Constant Stepsize SGD Type Algorithms: An Asymptotic Characterization](https://doi.org/10.1145/3508039).

**Opened records:** [record 1](https://arxiv.org/abs/2111.06328), [record 2](https://api.crossref.org/works/10.1145/3508039).

**Citation supports:** Small-step Gaussian limits of stationary stochastic-approximation laws are an established direct predecessor of the regular stationary transfer.
**Evidence checked:** The paper characterizes small-step limits of scaled stationary laws for strongly convex SGD, stable linear approximation and contractive nonlinear approximation. Under appropriate uniqueness conditions, Gaussian limits satisfy matrix Lyapunov equations.
**Evidence location:** arXiv abstract; Crossref fields title, author, container-title, volume, issue, page, published; HTTP200.
**Manuscript citation lines:** 173.
**Scope:** The native AdamW history, complete matching and all-invariant-selection repelling floor are additional arguments here, not consequences asserted from this citation.

**Additional validation detail:** ACM article endpoints returned403. The publisher-registered Crossref record was successfully read; the author arXiv abstract independently supplies the square-root-step scaling lost in plain-text publisher metadata.

### 30. Fluctuation-dissipation relations for stochastic gradient descent

**Authors:** Sho Yaida.
**Publication:** International Conference on Learning Representations (ICLR 2019), 2019.
**Validated source:** [Fluctuation-dissipation relations for stochastic gradient descent](https://arxiv.org/abs/1810.00004).

**Opened records:** [record 1](https://arxiv.org/abs/1810.00004).

**Citation supports:** Stationary expectation balances and fluctuation–dissipation identities provide classical motivation for testing stationary optimization laws.
**Evidence checked:** The paper derives exact relations among stationary SGD observables and hyperparameters and uses them to study landscape properties and learning schedules.
**Evidence location:** Author list, abstract and Comments: final version accepted at ICLR2019.
**Manuscript citation lines:** 174.
**Scope:** Its exact identities presuppose stationarity; they do not establish equilibration, uniqueness or the present conditional-noise risk floor.

**Additional validation detail:** Direct OpenReview PDF returned a browser challenge; the opened author record confirms the accepted conference version.

### 31. Central limit theorems for stochastic approximation with controlled Markov chain dynamics

**Authors:** Gersende Fort.
**Publication:** ESAIM: Probability and Statistics 19:60–80, 2015.
**Validated source:** [Central limit theorems for stochastic approximation with controlled Markov chain dynamics](https://www.numdam.org/item/PS_2015__19__60_0/).

**Opened records:** [record 1](https://www.numdam.org/item/PS_2015__19__60_0/), [record 2](https://www.numdam.org/item/PS_2015__19__60_0.pdf).

**Citation supports:** Poisson-equation martingale correction for dependent stochastic-approximation noise is a standard technique.
**Evidence checked:** The paper proves central limit results for stochastic approximation driven by controlled Markov chains and for averaged sequences. Its Poisson equation separates conditional mean-zero noise from a history-dependent remainder.
**Evidence location:** Full paper §2.1, p.63, Poisson-equation solution and martingale/remainder decomposition; abstract and bibliographic record.
**Manuscript citation lines:** 177.
**Scope:** Its CLT assumptions are not silently transferred to our infinite-history shift; the paper proves the required observable forgetting and chronology directly.

### 32. Acceleration of Stochastic Approximation by Averaging

**Authors:** B. T. Polyak; A. B. Juditsky.
**Publication:** SIAM Journal on Control and Optimization 30(4):838–855, 1992.
**Validated source:** [Acceleration of Stochastic Approximation by Averaging](https://epubs.siam.org/doi/abs/10.1137/0330046).

**Opened records:** [record 1](https://epubs.siam.org/doi/abs/10.1137/0330046).

**Citation supports:** Trajectory averaging and its precision improvements are classical stochastic-approximation results.
**Evidence checked:** The paper studies averaging stochastic-approximation trajectories, proving almost-sure convergence in a range of optimization and identification settings and optimal convergence rates under its assumptions.
**Evidence location:** Title/authors, Abstract, Information & Authors.
**Manuscript citation lines:** 179.
**Scope:** Our paper does not establish a whole-chain averaging CLT or identify this classical averaging result as new.

**Additional validation detail:** All authors are included; initials are retained exactly as displayed by the publisher.

### 33. On Linear Stochastic Approximation: Fine-grained Polyak-Ruppert and Non-Asymptotic Concentration

**Authors:** Wenlong Mou; Chris Junchi Li; Martin J. Wainwright; Peter L. Bartlett; Michael I. Jordan.
**Publication:** Proceedings of the 33rd Conference on Learning Theory, PMLR 125:2947–2997, 2020.
**Validated source:** [On Linear Stochastic Approximation: Fine-grained Polyak-Ruppert and Non-Asymptotic Concentration](https://proceedings.mlr.press/v125/mou20a.html).

**Opened records:** [record 1](https://proceedings.mlr.press/v125/mou20a.html).

**Citation supports:** Averaged linear iterates have refined finite-step covariance and concentration theory, distinct from the present unaveraged stationary comparison.
**Evidence checked:** The paper proves a fixed-step CLT for averaged stable linear stochastic approximation, identifies a step-dependent correction to classical averaging covariance, and gives matching concentration results under noise-tail assumptions.
**Evidence location:** Complete authors, bibliographic citation and abstract.
**Manuscript citation lines:** 179.
**Scope:** Theorem regimes concern averaged linear stochastic approximation; no such averaging CLT is established for the full native AdamW chain here.

### 34. Stochastic Modified Equations and Adaptive Stochastic Gradient Algorithms

**Authors:** Qianxiao Li; Cheng Tai; Weinan E.
**Publication:** Proceedings of the 34th International Conference on Machine Learning, PMLR 70:2101–2110, 2017.
**Validated source:** [Stochastic Modified Equations and Adaptive Stochastic Gradient Algorithms](https://proceedings.mlr.press/v70/li17f.html).

**Opened records:** [record 1](https://proceedings.mlr.press/v70/li17f.html), [record 2](https://proceedings.mlr.press/v70/li17f/li17f.pdf).

**Citation supports:** Continuous-time weak approximations are a standard way to study stochastic-gradient dynamics.
**Evidence checked:** The method approximates stochastic-gradient algorithms weakly by continuous-time stochastic differential equations and uses that description for adaptive parameter policies. The approximation theorem specifies a finite time horizon.
**Evidence location:** Abstract and citation metadata; full paper §2, informal Theorem1, p.2.
**Manuscript citation lines:** 186.
**Scope:** Finite-horizon weak approximation alone does not justify exchanging long-time and small-step limits.

### 35. On the SDEs and Scaling Rules for Adaptive Gradient Algorithms

**Authors:** Sadhika Malladi; Kaifeng Lyu; Abhishek Panigrahi; Sanjeev Arora.
**Publication:** Advances in Neural Information Processing Systems 35, 2022.
**Validated source:** [On the SDEs and Scaling Rules for Adaptive Gradient Algorithms](https://proceedings.neurips.cc/paper_files/paper/2022/hash/32ac710102f0620d0f28d5d05a44fe08-Abstract.html).

**Opened records:** [record 1](https://proceedings.neurips.cc/paper_files/paper/2022/hash/32ac710102f0620d0f28d5d05a44fe08-Abstract.html).

**Citation supports:** Adaptive-optimizer diffusion models depend on their scaling assumptions; the fixed-memory stationary limit in this paper is different.
**Evidence checked:** Derives diffusion approximations and batch-size scaling rules for RMSprop and Adam. The limiting construction fixes memory-to-squared-step ratios and scales noise, rather than keeping the memory and noise law fixed.
**Evidence location:** Official proceedings abstract; paper Definitions4.1,4.4, Theorems4.2,4.5, Remark4.3
**Manuscript citation lines:** 187.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 36. Adaptive Methods through the Lens of SDEs: Theoretical Insights on the Role of Noise

**Authors:** Enea Monzio Compagnoni; Tianlin Liu; Rustem Islamov; Frank Norbert Proske; Antonio Orvieto; Aurelien Lucchi.
**Publication:** International Conference on Learning Representations, 2025.
**Validated source:** [Adaptive Methods through the Lens of SDEs: Theoretical Insights on the Role of Noise](https://arxiv.org/abs/2411.15958).

**Opened records:** [record 1](https://arxiv.org/abs/2411.15958).

**Citation supports:** Noise, curvature and adaptive normalization already interact in diffusion models; this paper retains fixed memory and actual stationary histories.
**Evidence checked:** Develops noise-sensitive SDEs for normalized and adaptive methods, including AdamW. The stated AdamW approximation uses memory coefficients tending to one as the step decreases.
**Evidence location:** arXiv metadata and acceptance comment; full text Section3.2, Theorem3.12 and AppendixC.47,C.53
**Manuscript citation lines:** 187.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 37. Stochastic Gradient Descent as Approximate Bayesian Inference

**Authors:** Stephan Mandt; Matthew D. Hoffman; David M. Blei.
**Publication:** Journal of Machine Learning Research 18(134):1–35, 2017.
**Validated source:** [Stochastic Gradient Descent as Approximate Bayesian Inference](https://jmlr.org/papers/v18/17-214.html).

**Opened records:** [record 1](https://jmlr.org/papers/v18/17-214.html), [record 2](https://jmlr.org/papers/volume18/17-214/17-214.pdf).

**Citation supports:** Stationary covariance and OU-based descriptions of constant-step SGD are established precedents.
**Evidence checked:** The paper studies constant-rate SGD through approximate stationary distributions and an OU description, using explicit local assumptions to relate optimization parameters to approximate Bayesian sampling.
**Evidence location:** Journal metadata and abstract; full paper §3, pp.6–7, four assumptions and Ornstein–Uhlenbeck approximation.
**Manuscript citation lines:** 201.
**Scope:** The local diffusion assumptions and approximate Bayesian interpretation are not exact statements for every native AdamW invariant law.

### 38. A Bayesian Perspective on Generalization and Stochastic Gradient Descent

**Authors:** Samuel L. Smith; Quoc V. Le.
**Publication:** International Conference on Learning Representations (ICLR 2018), 2018.
**Validated source:** [A Bayesian Perspective on Generalization and Stochastic Gradient Descent](https://arxiv.org/abs/1710.06451).

**Opened records:** [record 1](https://arxiv.org/abs/1710.06451).

**Citation supports:** Noise scale and learning-rate/batch-size tradeoffs are established learning-dynamics questions.
**Evidence checked:** The paper interprets SGD using a diffusion description and relates noise scale to learning rate, training-set size and batch size, with empirical tests of batch-size behavior.
**Evidence location:** Author list, abstract and Comments: published as a conference paper at ICLR2018.
**Manuscript citation lines:** 201.
**Scope:** A modeling and empirical noise-scale reference, not proof that covariance alone determines native fixed-memory adaptive dynamics.

**Additional validation detail:** OpenReview forum/PDF endpoints returned a browser challenge; the author arXiv record explicitly confirms the conference and year.

### 39. Stochastic gradient descent performs variational inference, converges to limit cycles for deep networks

**Authors:** Pratik Chaudhari; Stefano Soatto.
**Publication:** International Conference on Learning Representations (ICLR 2018), 2018.
**Validated source:** [Stochastic gradient descent performs variational inference, converges to limit cycles for deep networks](https://arxiv.org/abs/1710.11029).

**Opened records:** [record 1](https://arxiv.org/abs/1710.11029), [record 2](https://openreview.net/references/pdf?id=H1-b1fs6m).

**Citation supports:** Non-isotropic noise can produce dynamics beyond isotropic equilibrium pictures; this general principle precedes the present matched-law construction.
**Evidence checked:** Within its continuous-time formulation and assumptions, non-isotropic gradient noise changes the effective potential and can introduce persistent probability currents or cycling behavior.
**Evidence location:** Official full-paper first-page publication header; §2 continuous-time SGD; §3 potential and assumptions.
**Manuscript citation lines:** 202.
**Scope:** Do not present its diffusion-based cycling claims as an exact discrete-time AdamW theorem; its explicit steady-state and current assumptions matter.

**Additional validation detail:** Venue verified from the opened official PDF header: ICLR2018, not CVPR.

### 40. On the interplay between noise and curvature and its effect on optimization and generalization

**Authors:** Valentin Thomas; Fabian Pedregosa; Bart van Merriënboer; Pierre-Antoine Manzagol; Yoshua Bengio; Nicolas Le Roux.
**Publication:** Proceedings of the Twenty Third International Conference on Artificial Intelligence and Statistics (AISTATS), PMLR, 2020.
**Validated source:** [On the interplay between noise and curvature and its effect on optimization and generalization](https://proceedings.mlr.press/v108/thomas20a.html).

**Opened records:** [record 1](https://proceedings.mlr.press/v108/thomas20a.html).

**Citation supports:** Curvature/noise interactions governing optimization speed and fluctuations are established topics.
**Evidence checked:** The abstract studies the interaction of gradient variance and curvature in optimization speed and generalization, and distinguishes Hessian, Fisher and gradient covariance. This directly supports the broad contextual attribution; no matched-copula theorem is attributed to it.
**Evidence location:** Official abstract.
**Manuscript citation lines:** 204.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 41. Noise and Fluctuation of Finite Learning Rate Stochastic Gradient Descent

**Authors:** Kangqiao Liu; Liu Ziyin; Masahito Ueda.
**Publication:** Proceedings of the 38th International Conference on Machine Learning (ICML), PMLR, 2021.
**Validated source:** [Noise and Fluctuation of Finite Learning Rate Stochastic Gradient Descent](https://proceedings.mlr.press/v139/liu21ad.html).

**Opened records:** [record 1](https://proceedings.mlr.press/v139/liu21ad.html), [record 2](https://proceedings.mlr.press/v139/liu21ad/liu21ad.pdf).

**Citation supports:** An earlier stationary-covariance analysis of Adam replaces its random denominator by a population normalizer.
**Evidence checked:** The source explicitly approximates Adam using a population second-moment preconditioner and solves stationary covariance without momentum under its prescribed noise model. This supports the manuscript's careful distinction from the native realized EMA quotient.
**Evidence location:** Published PDF page 9 (zero-index 8), discussion preceding Theorem 10 and Theorem 10.
**Manuscript citation lines:** 206.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 42. Adam Reduces a Unique Form of Sharpness: Theoretical Insights Near the Minimizer Manifold

**Authors:** Xinghan Li; Haodong Wen; Kaifeng Lyu.
**Publication:** Thirty-Ninth Conference on Neural Information Processing Systems (NeurIPS 2025), 2025.
**Validated source:** [Adam Reduces a Unique Form of Sharpness: Theoretical Insights Near the Minimizer Manifold](https://arxiv.org/abs/2511.02773).

**Opened records:** [record 1](https://arxiv.org/abs/2511.02773), [record 2](https://arxiv.org/html/2511.02773v1).

**Citation supports:** Other work studies adaptive implicit bias near a minimizer manifold under a different second-moment-memory scaling.
**Evidence checked:** The framework studies slow motion near a minimizer manifold and explicitly couples second-moment memory to the square of the learning rate. This supports the stated difference from the manuscript's fixed-memory stationary limit.
**Evidence location:** Section 4, Theorem 4.2; Appendix Theorems B.1–B.2.
**Manuscript citation lines:** 208.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 43. Towards Quantifying the Preconditioning Effect of Adam

**Authors:** Rudrajit Das; Naman Agarwal; Sujay Sanghavi; Inderjit S. Dhillon.
**Publication:** arXiv preprint, 2024.
**Validated source:** [Towards Quantifying the Preconditioning Effect of Adam](https://arxiv.org/abs/2402.07114).

**Opened records:** [record 1](https://arxiv.org/abs/2402.07114).

**Citation supports:** The benefits and limitations of Adam as a preconditioner, including non-diagonal Hessian difficulties, are prior topics.
**Evidence checked:** The abstract analyzes quadratic preconditioning, gives diagonal/diagonally-dominant bounds and reports adverse behavior for sufficiently non-diagonal Hessians. This supports the manuscript's limited preconditioning attribution, not a novel-claim assertion about noncommutation alone.
**Evidence location:** Official author-uploaded abstract.
**Manuscript citation lines:** 209.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 44. On the Implicit Bias of Adam

**Authors:** Matias D. Cattaneo; Jason Matthew Klusowski; Boris Shigida.
**Publication:** Proceedings of the 41st International Conference on Machine Learning (ICML), PMLR, 2024.
**Validated source:** [On the Implicit Bias of Adam](https://proceedings.mlr.press/v235/cattaneo24a.html).

**Opened records:** [record 1](https://proceedings.mlr.press/v235/cattaneo24a.html).

**Citation supports:** Backward-error analysis identifies regularization effects introduced by adaptive methods' discrete updates.
**Evidence checked:** The abstract relates backward-error ODEs to implicit regularization in RMSProp and Adam, with behavior depending on hyperparameters and training stage. This supports the manuscript's discrete-update implicit-bias attribution; the current text does not miscite it as a noncommuting-Hessian theorem.
**Evidence location:** Official abstract.
**Manuscript citation lines:** 210.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 45. A Tail-Index Analysis of Stochastic Gradient Noise in Deep Neural Networks

**Authors:** Umut Simsekli; Levent Sagun; Mert Gurbuzbalaban.
**Publication:** Proceedings of the 36th International Conference on Machine Learning, 2019.
**Validated source:** [A Tail-Index Analysis of Stochastic Gradient Noise in Deep Neural Networks](https://proceedings.mlr.press/v97/simsekli19a.html).

**Opened records:** [record 1](https://proceedings.mlr.press/v97/simsekli19a.html).

**Citation supports:** Covariance and Gaussian noise are not the only descriptions studied for learning dynamics; the current example uses bounded noise.
**Evidence checked:** Questions a Gaussian-noise approximation and investigates heavy tails in measured neural-network gradient noise.
**Evidence location:** Official PMLR metadata, BibTeX and abstract
**Manuscript citation lines:** 215.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 46. Why are Adaptive Methods Good for Attention Models?

**Authors:** Jingzhao Zhang; Sai Praneeth Karimireddy; Andreas Veit; Seungyeon Kim; Sashank Reddi; Sanjiv Kumar; Suvrit Sra.
**Publication:** Advances in Neural Information Processing Systems 33, 2020.
**Validated source:** [Why are Adaptive Methods Good for Attention Models?](https://proceedings.neurips.cc/paper/2020/hash/b05b57f6add810d3b7490866d74c0053-Abstract.html).

**Opened records:** [record 1](https://proceedings.neurips.cc/paper/2020/hash/b05b57f6add810d3b7490866d74c0053-Abstract.html).

**Citation supports:** Noise-tail explanations for adaptive optimization precede this work; our bounded-noise construction isolates a different dependence.
**Evidence checked:** Presents heavy-tailed gradient noise as one explanation for optimizer differences in attention models and studies coordinate clipping.
**Evidence location:** Official proceedings author list and abstract
**Manuscript citation lines:** 216.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 47. Why Transformers Need Adam: A Hessian Perspective

**Authors:** Yushun Zhang; Congliang Chen; Tian Ding; Ziniu Li; Ruoyu Sun; Zhi-Quan Luo.
**Publication:** Advances in Neural Information Processing Systems 37, 2024.
**Validated source:** [Why Transformers Need Adam: A Hessian Perspective](https://papers.nips.cc/paper_files/paper/2024/hash/ee0e45ff4de76cbfdf07015a7839f339-Abstract-Conference.html).

**Opened records:** [record 1](https://papers.nips.cc/paper_files/paper/2024/hash/ee0e45ff4de76cbfdf07015a7839f339-Abstract-Conference.html).

**Citation supports:** Curvature variation across parameter blocks is a proposed explanation for adaptive optimization in transformers; the present matching fixes the whole Hessian law.
**Evidence checked:** Studies differences in Hessian spectra across parameter blocks and their relationship to the Adam-versus-SGD gap on transformers and quadratic examples.
**Evidence location:** Official proceedings author list and abstract; paper introduction
**Manuscript citation lines:** 217.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

### 48. Noise Is Not the Main Factor Behind the Gap Between SGD and Adam on Transformers, but Sign Descent Might Be

**Authors:** Frederik Kunstner; Jacques Chen; Jonathan Wilder Lavington; Mark Schmidt.
**Publication:** International Conference on Learning Representations (ICLR 2023), 2023.
**Validated source:** [Noise Is Not the Main Factor Behind the Gap Between SGD and Adam on Transformers, but Sign Descent Might Be](https://arxiv.org/pdf/2304.13960).

**Opened records:** [record 1](https://arxiv.org/pdf/2304.13960).

**Citation supports:** The present existence theorem about curvature-noise coupling cannot establish that stochastic noise is the dominant source of Adam's empirical transformer advantage; documented full-batch gaps require additional mechanisms. This is an empirical scope limit, not a contradiction of the coupling theorem.
**Evidence checked:** The primary PDF confirms ICLR 2023. Its abstract reports batch-size-controlled experiments including full-batch training: the Adam-SGD gap persists after noise removal, and large-batch Adam resembles momentum sign descent. The arXiv author page expands J. Wilder Lavington to Jonathan Wilder Lavington.
**Evidence location:** Primary PDF first-page publication header and abstract, lines 0-23; primary arXiv author and abstract fields, lines 9-18.
**Manuscript citation lines:** 219.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** Do not abbreviate the title as Noise, Not Geometry: that is not the title of this work.

### 49. The Marginal Value of Adaptive Gradient Methods in Machine Learning

**Authors:** Ashia C. Wilson; Rebecca Roelofs; Mitchell Stern; Nati Srebro; Benjamin Recht.
**Publication:** Advances in Neural Information Processing Systems 30 (NIPS 2017), 2017.
**Validated source:** [The Marginal Value of Adaptive Gradient Methods in Machine Learning](https://proceedings.neurips.cc/paper/2017/hash/81b3833e2504647f9d794f7d7b9bf341-Abstract.html).

**Opened records:** [record 1](https://proceedings.neurips.cc/paper/2017/hash/81b3833e2504647f9d794f7d7b9bf341-Abstract.html).

**Citation supports:** Optimization behavior and test generalization can differ across adaptive and non-adaptive methods. A stationary quadratic-risk advantage or separation here does not by itself establish better language modeling or generalization.
**Evidence checked:** The official proceedings page identifies the authors and venue. It gives classification examples where adaptive methods select solutions with worse test error than SGD, and reports empirical generalization comparisons on neural-network tasks.
**Evidence location:** Official NeurIPS proceedings title/authors/venue and abstract; lines 0-10.
**Manuscript citation lines:** 220.
**Scope:** Supports the stated context; validation does not independently verify every proof in the cited work.

**Additional validation detail:** Use the current official proceedings author name Nati Srebro; the older deposited PDF uses Nathan Srebro.

### 50. Inequalities for E k(X, Y) when the marginals are fixed

**Authors:** Stamatis Cambanis; Gordon Simons; William Stout.
**Publication:** Zeitschrift für Wahrscheinlichkeitstheorie und Verwandte Gebiete 36:285–294, 1976.
**Validated source:** [Inequalities for E k(X, Y) when the marginals are fixed](https://link.springer.com/article/10.1007/BF00532695).

**Opened records:** [record 1](https://link.springer.com/article/10.1007/BF00532695).

**Citation supports:** Attained expectation extrema under fixed marginals are a direct classical mathematical ancestor of the scalar rearrangement step.
**Evidence checked:** For a class of quasi-monotone functions with fixed input distributions, the expectation is ordered by the joint distribution and attained minimum and maximum couplings are characterized.
**Evidence location:** Title, complete author list, publication/volume/pages, Abstract and Cite this article.
**Manuscript citation lines:** 227, 399.
**Scope:** The contribution here is the optimizer-specific decreasing response kernel and resulting risk interval, not the general rearrangement principle.

## Replaced indirect source

The earlier citation to Fan, Sherman and Shum (2013) was itself validated, including its rearrangement lemma. The revised bibliography replaces it with the direct mathematical source by Cambanis, Simons and Stout (1976), which was also opened and checked online. The retired entry is recorded separately in the JSON and is not counted among the 50 references.

## Editorial checks

- Exactly 50 bibliography keys, 50 unique titles and 50 cited works.
- No missing citation keys, uncited bibliography entries or duplicate preprint/publication counts.
- Original abstract, displayed mathematics, formal statement bodies, proof sources and scientific figure assets are preserved.
- Publication years are distinguished from preprint dates; no unconfirmed venue has been invented.
