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