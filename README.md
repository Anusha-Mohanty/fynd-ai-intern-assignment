# Fynd AI Intern – Take Home Assignment
**Candidate:** Anusha Mohanty

---

## Task 1: Prompt Engineering & Evaluation

**Goal:**  
Evaluate how different prompting strategies affect star-rating prediction accuracy, JSON validity, and consistency.

**Approaches Implemented:**
1. Baseline prompt
2. Schema-constrained prompt
3. Decision-guided prompt

Each prompt is clearly shown and evaluated on sampled Yelp reviews.

**Notebook:**  
`task1/Yelp_Prompt_Evaluation.ipynb`

---

## Task 2: AI-Powered Restaurant Review System

A web-based review system with:
- User dashboard to submit reviews
- Admin dashboard to monitor feedback
- AI-generated user responses
- AI summaries and recommended actions

**Tech Stack:**  
Streamlit + Groq LLM + JSON storage

### Live Deployment
- **User Dashboard:**  
  https://huggingface.co/spaces/AnushaMohanty12/ai-restaurant-feedback

- **Admin Dashboard:**  
  https://huggingface.co/spaces/AnushaMohanty12/ai-restaurant-feedback  
  *(Admin view accessible via dashboard selector)*

> API keys are securely managed using Hugging Face Secrets.

---

## Notes
- Both dashboards share a single data source.
- The app is fully deployed and publicly accessible.
