# Research: AI Model Selection for Financial Analysis

**Generated**: 2025-11-15

## 1. AI Inference Service and Model

### Decision

The system will use the **Llama 3 8B model running on the Groq API** for all AI-powered analysis tasks, including expense categorization, pattern detection, and anomaly identification.

### Rationale

1.  **Performance**: The Groq API is engineered for extreme speed, reporting throughputs of over 800 tokens/second for the Llama 3 8B model. This is critical for our success criteria of processing large files quickly and maintaining low API latency.
2.  **Capability**: Llama 3 is a state-of-the-art language model with strong capabilities in text classification, summarization, and analysis, which directly map to our feature requirements. The 8B parameter model provides a powerful and efficient balance for understanding short-form financial transaction descriptions.
3.  **Cost-Effectiveness**: Using a high-speed, API-based model avoids the significant overhead of hosting and managing our own inference infrastructure. Groq's pricing model is competitive, and the speed reduces the total time-per-task, which can lower costs.
4.  **Alignment with Constitution**: This choice aligns with the project constitution's principles of "Performance as a Feature" and "Minimal and Deliberate Dependencies" by leveraging a specialized, high-performance external service instead of building and maintaining a complex internal one.

### Alternatives Considered

-   **Llama 3 70B (on Groq)**: While more powerful, the 70B model has lower throughput (around 300 tokens/second). For the specific task of analyzing transaction descriptions, the additional power is likely unnecessary and not worth the performance trade-off.
-   **Other Models (e.g., from OpenAI, Anthropic)**: Other providers offer capable models, but Groq's specialized hardware provides a unique performance advantage that is highly desirable for this project's success criteria.
-   **Self-Hosted Open Source Models**: This would give us more control but would introduce significant operational complexity and cost, violating the "Minimal Dependencies" principle for this stage of the project.
