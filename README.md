<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# 🚀 Edu.ai - Comprehensive Sprint Plan for AI-Powered Educational Platform

## 🎯 Project Overview

**Edu.ai** is an innovative AI-powered educational platform designed to teach programming to children aged 6-18. The platform leverages cutting-edge Azure services to deliver personalized, interactive learning experiences through AI-driven avatars and intelligent content generation.

[^1]

## 🎪 Key Technical Recommendations

### 🔍 RAG vs Fine-tuning Strategy

**Recommendation:** Use RAG (Retrieval-Augmented Generation) with Azure AI Search instead of fine-tuning[^2]

**Benefits:**

- **Cost-effective:** RAG is significantly cheaper than fine-tuning (\$1.70 per million tokens)[^3]
- **Flexible:** Real-time content updates without retraining
- **Transparent:** Clear source attribution for educational content
- **Maintainable:** Easy content base updates


## ⚙️ How to Set Up RAG on Azure

1. **Prepare Knowledge Base**
    - Aggregate your lesson material (PDFs, docs, markdown) into an Azure Blob Storage container.
    - Ensure each document has metadata (title, topic, grade-level).
2. **Azure AI Search**
    - Create an **Azure Cognitive Search** service.
    - Define an index schema matching your document fields.
    - Use the Data Source \& Indexer to crawl your Blob Storage.
3. **Azure Functions (Retrieval Layer)**
    - Write a function that:

4. Accepts user query via HTTP trigger.
5. Calls Azure Cognitive Search REST API to retrieve top K passages.
6. Returns those passages to the next step.
1. **GPT-4.1 Generation**
    - In a second Azure Function (or same, chaining calls):

2. Build a “RAG prompt” combining retrieved passages + user question.
3. Invoke the Azure OpenAI GPT-4.1 endpoint.
4. Return the generated answer along with source citations.
1. **Configuration \& Services**
    - **Azure Functions:** Serverless compute for retrieval + generation logic.
    - **Azure Cognitive Search:** Index, query, and rank document passages.
    - **Azure OpenAI Service:** Host GPT-4.1 model.
    - **Azure Static Web Apps:** Serve your frontend (HTML/CSS/JS) with built-in routing, authentication, and GitHub CI/CD.

# 🗓️ 8-Week Sprint Plan (Markdown)

| Sprint | Dates | Focus |
| :-- | :-- | :-- |
| 1 | Jul 12 – Jul 18, 2025 | Frontend \& Hosting |
| 2 | Jul 19 – Jul 25, 2025 | Backend \& Database |
| 3 | Jul 26 – Aug 1, 2025 | RAG Retrieval Layer |
| 4 | Aug 2 – Aug 8, 2025 | GPT-4.1 Integration |
| 5 | Aug 9 – Aug 15, 2025 | Avatar \& TTS |
| 6 | Aug 16 – Aug 22, 2025 | Interactive Q\&A |
| 7 | Aug 23 – Aug 29, 2025 | Tracking \& Analytics |
| 8 | Aug 30 – Sep 5, 2025 | Testing \& Production Launch |

## 🚦 Sprint 1 (Jul 12 – Jul 18): Frontend \& Hosting

1. Convert Figma prototype into responsive HTML/CSS/JS.
2. Deploy to **Azure Static Web Apps** (Standard tier).
3. Implement page routing \& basic UI tests.
4. Configure GitHub CI/CD for automatic builds.

## 🗄️ Sprint 2 (Jul 19 – Jul 25): Backend \& Database

1. Design **Cosmos DB** containers: Users, Content, Interactions.
2. Build FastAPI + Azure Functions for auth \& CRUD.
3. Secure endpoints with Azure AD B2C.
4. Document APIs via Swagger UI.

## 🔎 Sprint 3 (Jul 26 – Aug 1): RAG Retrieval Layer

1. Set up Azure Cognitive Search index on lesson docs.
2. Implement Azure Function “search” endpoint:
    - Receives query → returns top 3 passages.
3. Test search relevance \& tune index scoring.

## 🤖 Sprint 4 (Aug 2 – Aug 8): GPT-4.1 Integration

1. Create Azure Function “generate” endpoint:
    - Combines passages + question → calls GPT-4.1.
2. Handle token limits \& errors.
3. Return answer with inline citations.

## 🎭 Sprint 5 (Aug 9 – Aug 15): Avatar \& TTS

1. Integrate **Azure Speech Services** (Neural TTS).
2. Connect **Azure TTS Avatar** for lip-sync.
3. Add play/pause controls.
4. Select three avatar expressions (smile, nod, wave).

## 🙋 Sprint 6 (Aug 16 – Aug 22): Interactive Q\&A

1. Build “Raise Hand” UI \& backend queue.
2. Classify questions (short vs long) via GPT-4.1.
3. Implement fallback auto-reply on failure.
4. Log errors \& notify admin.

## 📊 Sprint 7 (Aug 23 – Aug 29): Tracking \& Analytics

1. Log user events to Cosmos DB (clicks, questions, quiz results).
2. Build dashboard (React + D3 or Power BI).
3. Monitor accuracy, session time.
4. Send weekly reports via email.

## 🔒 Sprint 8 (Aug 30 – Sep 5): Testing \& Production Launch

1. Perform security \& COPPA compliance audit.
2. Load-test Functions for 100 concurrent users.
3. Optimize API latency (< 2 s).
4. Deploy to production \& configure Azure Monitor alerts.

> **Simple Phase Explanation:**
> Each sprint delivers one core layer—UI, backend, retrieval, generation, avatar, interactivity, analytics, and launch—iteratively building a secure, budget-friendly, AI-driven learning platform.

<div style="text-align: center">⁂</div>

[^1]: Edu.ai-2.pdf

