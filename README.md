# 🔎 ResearchRadar

> An AI-powered research assistant that uses live web and Google Scholar search data to discover, analyze, and organize research papers, key findings, recent developments, and research gaps.

---

## 💡 Overview

ResearchRadar helps students and researchers quickly explore a research topic without manually going through dozens of search results.

The application retrieves real research papers from Google Scholar using SerpApi and uses AI to analyze the retrieved information.

It provides:

- 📚 Relevant research papers
- 🧠 Research overview and key findings
- 🔍 Major research themes
- 💡 Potential research gaps
- ❓ Possible research questions
- 📈 Publication-year trends
- 📅 Publication-year filtering
- 🔃 Sorting by citations and publication year
- 🔗 Direct links to research papers

---

## 🎯 Problem

Finding and understanding relevant research literature can be time-consuming.

Students often have to:

1. Search multiple sources
2. Open many papers
3. Identify recurring themes
4. Understand the current research landscape
5. Find possible research gaps
6. Decide what they could investigate further

ResearchRadar brings these steps together into a single research discovery workflow.

---

## 🚀 Features

### 🔎 Live Research Search

Search for any research topic and retrieve relevant papers from Google Scholar using SerpApi.

### 🧠 AI Research Insights

ResearchRadar analyzes the retrieved search-result information and provides:

- Research Overview
- Key Findings
- Major Research Themes
- Research Gaps
- Possible Research Questions

### 📚 Research Paper Explorer

Each retrieved paper displays:

- Title
- Publication information
- Publication year
- Citation count
- Description
- Link to the paper

### 📅 Year Filtering

Filter retrieved papers by publication year.

### 🔃 Paper Sorting

Sort papers by:

- Relevance
- Most cited
- Newest
- Oldest

### 📈 Publication Trend

Visualize the publication-year distribution of the papers retrieved for the current search.

---

## 🏗️ Architecture

```text
User
  │
  ▼
Streamlit Interface
  │
  ▼
Research Topic
  │
  ▼
SerpApi
  │
  ▼
Google Scholar
  │
  ▼
Research Papers
  │
  ▼
OpenAI
  │
  ▼
AI Research Analysis
  │
  ├── Research Overview
  ├── Key Findings
  ├── Major Themes
  ├── Research Gaps
  └── Research Questions