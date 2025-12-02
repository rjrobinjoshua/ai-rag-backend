# rag-notes.md
### RAG Evaluation Notes

**Document:** FastAPI overview (~1,200 words)
**Collection:** `docs`
**Goal:** Observe differences in retrieval quality based on extreme chunk settings.

---

## 1. Configurations Tested

### **A) Tiny, fragmented**
```
chunk_size = 80
chunk_overlap = 10
top_k = 3
```
**Observations**
- Produced many very small chunks.
- Retrieval was extremely granular but often incomplete.
- Answers tended to be shallow because each chunk held only a sentence or two.

**When useful:** only for highly structured Q&A where small granularity matters.

---

### **B) Medium (balanced)**
```
chunk_size = 300
chunk_overlap = 40
top_k = 3
```
**Observations**
- Produced a moderate number of chunks.
- Retrieval brought in relevant content consistently.
- Answers were complete and context-rich without being too generic.

**Best default for real docs:** good balance of specificity and coverage.

---

### **C) Huge**
```
chunk_size = 800
chunk_overlap = 100
top_k = 2
```
**Observations**
- Produced 1–2 very large chunks.
- Retrieval always returned the same chunk.
- Answers were correct but not selective (vector search had no real effect).

**Useful only for:** very short documents.

---

## 2. Key Takeaway
For small documents (~1.2k words), retrieval differences are subtle because most chunks contain enough context to answer most questions.
However, **medium-sized chunks (300/40)** deliver the best balance and will scale well when multiple documents are ingested in Week 3.

---

## 3. Final Config Going Forward
```
chunk_size = 300
chunk_overlap = 40
top_k = 3
```

This will remain the default until Week 3’s multi-file ingestion.
