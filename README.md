# BiTextion: Sociotechnical Alignment in Automated Optimization Modeling via Textual Bisection for Task Disambiguation
[![Paper](https://img.shields.io/badge/Paper-007ACC?style=for-the-badge&labelColor=007ACC)](https://github.com/batu-el/bitextion/blob/main/bitextion_paper.pdf)

## Abstract
When interacting with automated optimization modeling systems, such as [Optimus](https://arxiv.org/abs/2310.06116), the burden of clearly and precisely describing complex problems falls upon the users, which can be challenging, especially for non-experts, who are the primary user base for these systems. This observation motivates our research to develop a system that can ask clarifying questions to help non-expert users precisely describe complex optimization problems. We introduce Textual Bisection (**BiTextion**) a general framework that (i) samples candidate *detailed problem descriptions* conditioned on a *vague problem description*, and (ii) narrows down the search space by posing questions that efficiently resolve ambiguities. Our simulated user study provides experimental evidence showing that  **BiTextion**  improves the performance of Llama3.1-8b when eliciting the objective and constraints of an optimization problem. We find that **BiTextion**  can enhance the performance of smaller models but may not consistently deliver similar gains when applied to more capable larger models, underscoring the need for model-specific test-time strategies.

## BiTextion
![Alt text](assets/bitextion.png)

## Datasets
![Alt text](assets/datasets.png)

## Results
![Alt text](assets/results.png)

## Citation
```bibtex
@article{elbitextion2024,
    title={BiTextion: Sociotechnical Alignment in Automated Optimization Modeling via Textual Bisection for Task Disambiguation},
    author={El, Batu and Udell, Madeleine},
    journal={preprint},
    year={2024}
}
