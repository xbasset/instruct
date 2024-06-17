# Challenges

This is a list of challenges that we want to solve using prompt only


## Ideas

1. Is it possible to reach GPT-4 level of performance for narrowed tasks by the use small models? 
  - Use Case: Use them as rules engine, as we can do with GPT-4* by utilizing prompt-techniques.
    - sub-question 1: What's the good mix between prompt engineering technique and model size / model type – base, instruc, chat?
    - sub-question 2: What's the threshold of time invested in trying to reach that point before moving forward to fine-tuning?
    - sub-quesition 3: How to drive the process of answering sub-questions 1 and 2 to generate high data that will help build the high-quality data that is required to break the wall?

2. How good are LLMs to be used with pseudo code in prompt to use them as interpreters?
  - sub-question 1: are models themselves able to generate a new interpreted language that will fit to their internal structure, i.e. token-wise adapted to their own internal representation of the pseudo-code itself – should vary from one model to the other.
    - Analogy:
  
| Prompt Engineering | Coding             |
| ------------------ | ------------------ |
| prompting          | coding             |
| input              | source code        |
| LLM                | interpreter        |
| Output             | interpreted source |

   - sub-question 2: how to run prompt-interpretation as a probabilistic result in order to mitigate the incompressible X% chance of going in the wrong direction?
   - sub-question 3: how does parameters like `seed`, `temperature` enter into play for reliability of exploring the latent spaces?
   - sub-question 4: what would be the approach to optimize those parameters in the ~infinite latent space of LLMs

3. How to build LLM queries that pushes the auto-regressive algorithm in unexpected behaviors?
   - Use Case: Security, Steerability, Interpretability
   - sub-question 1: how does that unexpected behavior relate to art?

4. Which LLMs are capable of generating a compact yet readable pseudo-code syntax that is interpretable by the model itself and close to native english language to make it easy to use in queries?
   - Use Case: generate advanced prompt engineering techniques for developers, with a description compact enough to be included in the context window of each query that requires it, i.e. similar to an `import`
   - sub-question: is each model statistically generating a unique pseudo-code syntax or is there some convergence between models?
   - sub-question: is a strong model able to generate a syntax that is usable by smaller models?


## Ressources:

### Prompting

[Optimizing LLM Best practices from the OpenAI team](https://platform.openai.com/docs/guides/optimizing-llm-accuracy/understanding-the-tools)

[Prompt Engineering by Anthropic](https://docs.anthropic.com/en/docs/prompt-engineering)

[Anthropic's Meta-Prompt colab notebook](https://colab.research.google.com/drive/1SoAajN8CBYTl79VyTwxtxncfCWlHlyy9#scrollTo=4EiGHUcBr_LM)

[Hugging Face Open-source AI Cookbook](https://huggingface.co/learn/cookbook/index)
[GitHub repo](https://github.com/huggingface/cookbook)

[The Prompt Report: A Systematic Survey of Prompting Techniques](https://arxiv.org/abs/2406.06608)


[4M views Andrej Karpathy's pinned tweet](https://x.com/karpathy/status/1617979122625712128)

[Microsoft Prompt Book for Cybersecurity](https://learn.microsoft.com/en-us/copilot/security/using-promptbooks)

[LLM usage in Mathematics](https://www.scientificamerican.com/article/ai-will-become-mathematicians-co-pilot/)

[100k+ LLMs out there: the Cambrian explosion](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending)

["Be Concise" paper](https://arxiv.org/pdf/2401.05618)

[Reddit discussion on frameworks to run LLM commands locally](https://www.reddit.com/r/ollama/comments/1d80y6r/are_there_any_frameworks_or_ways_to_make_a)

[26 guiding principles designed to streamline the process of querying and prompting large language models](https://arxiv.org/pdf/2312.16171v2)
[Project page: Atlas](https://github.com/VILA-Lab/ATLAS)

[Prompt Engineering Guide](https://www.promptingguide.ai/)

[What is prompt optimization?](https://jxnl.co/writing/2024/05/22/what-is-prompt-optimization/)

### Chunking

["An emerging technique to better represent your data for RAG/LLM applications is to only chunk the data"](https://x.com/llama_index/status/1773522853939577243?s=46&t=YoCMQef82OIOPui_nLLC0A)

### Evaluation

[Some Work on LLM tasks evaluations](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch07/03_model-evaluation/llm-instruction-eval-ollama.ipynb)

### FineTuning

[Understanding Fine-Tuning](https://x.com/rasbt/status/1802327699937009807?s=46&t=YoCMQef82OIOPui_nLLC0A)

[🤗 PEFT (Parameter-Efficient Fine-Tuning)](https://huggingface.co/docs/peft/en/index)

[FineWeb Article](https://huggingface.co/spaces/HuggingFaceFW/blogpost-fineweb-v1)

[Mistral fine-tuning guide](https://github.com/mistralai/mistral-finetune)

[Unsloth fine-tuning Reddit post](https://www.reddit.com/r/LocalLLaMA/comments/1cy7tv3/mistral_v3_4bit_quantized_bnb_2x_faster_with_70)

### Architecture

[Apple Technical report on private cloud LLM inference](https://security.apple.com/blog/private-cloud-compute/)

[Apple Technical documentation on foundation models implementation](https://machinelearning.apple.com/research/introducing-apple-foundation-models)

[Quantization course](https://www.deeplearning.ai/short-courses/quantization-in-depth/)

[Thom Wolf: The Little guide to building Large Language Models in 2024](https://www.youtube.com/watch?v=2-SPH9hIKT8) [slides](https://docs.google.com/presentation/d/1IkzESdOwdmwvPxIELYJi8--K3EZ98_cL6c5ZcLKSyVg/edit#slide=id.p)

### Cool projects

[lama-fs: LlamaFS is a self-organizing file manager.](https://github.com/iyaja/llama-fs)

[Instructor: Structured LLM Outputs](https://github.com/jxnl/instructor)

[DSPy: Programming—not prompting—Foundation Models](https://github.com/stanfordnlp/dspy)

[Perplexity-Inspired LLM Answer Engine](https://github.com/developersdigest/llm-answer-engine)

[Instruct's Commercial alternative](https://docs.composableprompts.com/)

[Funny model comparison tool: "hadoken!"](https://github.com/OpenGenerativeAI/llm-colosseum)