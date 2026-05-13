# Mutual Fund FAQ Assistant: Facts-Only Q&A System

## Project Overview

This project aims to develop a comprehensive FAQ assistant specifically designed for mutual fund schemes, with Groww serving as the reference product context. The system will provide objective, verifiable responses to mutual fund queries by exclusively retrieving information from official public sources including AMC (Asset Management Company) websites, AMFI, and SEBI.

The assistant operates under strict compliance guidelines, avoiding any form of investment advice, opinions, or recommendations. Each response is required to include a single, clear source citation while maintaining high standards of clarity, accuracy, and regulatory compliance.

## Core Objectives

Design and implement a lightweight Retrieval-Augmented Generation (RAG)-based assistant that:

- **Answers factual queries** about mutual fund schemes with precision
- **Utilizes a curated corpus** of official documents and sources
- **Delivers concise, source-backed responses** with verifiable information

## Target Audience

- **Retail investors** comparing different mutual fund schemes
- **Customer support teams** handling repetitive mutual fund inquiries
- **Content teams** requiring quick access to verified mutual fund information

## Project Scope

### 1. Data Corpus Development

- **Select one Asset Management Company (AMC)** for initial implementation
- **Choose 3-5 diverse mutual fund schemes** across categories (large-cap, flexi-cap, ELSS, etc.)
- **Gather 15-25 official public URLs** including:
  - Scheme factsheets and performance data
  - Key Information Memorandum (KIM)
  - Scheme Information Document (SID)
  - AMC FAQ and help documentation
  - AMFI/SEBI regulatory guidance
  - Statement and tax document download procedures

### 2. Assistant Functionality Requirements

The system must respond to factual queries including:

- **Financial metrics**: Expense ratios, exit loads, minimum SIP amounts
- **Regulatory information**: ELSS lock-in periods, riskometer classifications
- **Benchmark data**: Index information and performance benchmarks
- **Procedural guidance**: Statement downloads and capital gains reports

**Response Standards:**
- Maximum 3 sentences per response
- Exactly one citation link per answer
- Footer: "Last updated from sources: <date>"

### 3. Query Handling Protocol

The assistant must refuse non-factual or advisory queries such as:
- "Should I invest in this fund?"
- "Which fund performs better?"

**Refusal Response Guidelines:**
- Maintain polite and professional tone
- Clearly state the facts-only limitation
- Provide relevant educational resources (AMFI/SEBI links)

### 4. User Interface Design

Implement a minimal, intuitive interface featuring:
- Welcome message with system capabilities
- Three example questions for user guidance
- Prominent disclaimer: "Facts-only. No investment advice."

## System Constraints

### Data Source Requirements
- **Exclusively use official sources**: AMC, AMFI, SEBI websites
- **Prohibited sources**: Third-party blogs, aggregator platforms, unofficial content

### Privacy and Security Standards
- **Never collect, store, or process**:
  - PAN or Aadhaar numbers
  - Account numbers or financial identifiers
  - OTPs or authentication codes
  - Email addresses or phone numbers

### Content Restrictions
- **No investment advice** or personalized recommendations
- **No performance comparisons** or return calculations
- **Performance queries**: Direct users to official factsheets only

### Transparency Requirements
- **Short, factual, verifiable responses**
- **Source citations and update dates** for every answer
- **Clear disclaimers** about system limitations

## Deliverables

### 1. Comprehensive Documentation
- **README file** with:
  - Detailed setup and installation instructions
  - Selected AMC and mutual fund schemes
  - System architecture overview (RAG implementation)
  - Known limitations and future enhancements

### 2. Compliance Materials
- **Standard disclaimer**: "Facts-only. No investment advice."
- **Source attribution templates** for consistent citation formatting

## Success Metrics

- **Accuracy**: Precise retrieval of factual mutual fund information
- **Compliance**: Strict adherence to facts-only response guidelines
- **Transparency**: Consistent inclusion of valid source citations
- **Safety**: Proper refusal of advisory and speculative queries
- **Usability**: Clean, minimal, and user-friendly interface experience

## Conclusion

This project delivers a trustworthy, transparent, and regulatory-compliant mutual fund FAQ assistant that prioritizes accuracy over computational intelligence. The system ensures users receive only verified, source-backed financial information without any advisory bias or speculative content, maintaining the highest standards of financial information integrity.
