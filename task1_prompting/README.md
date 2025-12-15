# Yelp Review Rating Prediction — Prompt Engineering Analysis

## Objective
Analyze how different prompt designs affect an LLM’s ability to classify Yelp restaurant reviews into 1–5 star ratings, focusing on accuracy, JSON validity, and reliability.

## Model & Setup
- Model: LLaMA-3-8B via Groq
- Decoding: Temperature = 0 (deterministic)
- Dataset: Yelp reviews
- Evaluation scale: exploratory (10) + scaled (50)

## Prompting Approaches
1. **Baseline (Free-form)**  
   Minimal instructions, no structure.

2. **Schema-Constrained**  
   Enforces strict JSON output with predicted stars and a short explanation.

3. **Decision-Guided**  
   Decomposes sentiment analysis into steps before mapping to stars, prioritizing clarity and auditability.

## Key Results (50 samples)
| Prompt Strategy | Accuracy | JSON Validity | Reliability |
|-----------------|----------|---------------|-------------|
| Baseline | 0.00 | 0.00 | Very Low |
| Schema-Constrained | High | 1.00 | High |
| Decision-Guided | High | 1.00 | High (policy-based) |

## Observations
- Free-form prompting is unreliable and unsuitable for automation.
- Schema constraints significantly improve reliability and downstream usability.
- Decision-guided prompting converges with schema-based results on clear reviews when using a deterministic model, adding value mainly through interpretability and explicit decision logic.

## Conclusion
Prompt structure has a greater impact on system reliability than prompt wording. Schema-based prompts are best for scalable automation, while decision-guided prompts are useful when transparency and auditability matter.

