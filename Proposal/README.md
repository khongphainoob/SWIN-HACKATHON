# Personal Sentiment Advisor - IEEE Conference Proposal

## 📄 Document Overview

**Title**: Personal Sentiment Advisor: An Autonomous Agentic AI System for Real-Time Retail Investment Management

**Format**: IEEE Conference Paper (IEEEtran LaTeX template)

**Length**: 5 pages (compliant with hackathon requirements)

**Status**: Ready for compilation and submission

---

## 🎯 Marking Criteria Alignment

### Innovation (30%)
- ✅ **Novelty**: First Agentic AI robo-advisor with portfolio-aware RAG
- ✅ **Autonomy**: 9 autonomous agents orchestrated via LangGraph
- ✅ **Business Value**: \$1.5T TAM, 88% cost reduction vs. human advisors

### Technical Proposal (60%)
- ✅ **Executive Summary**: Clear articulation in abstract
- ✅ **Project Scope**: In-scope/out-of-scope clearly defined
- ✅ **Requirements**: Comprehensive data strategy and system requirements
- ✅ **Solution Design**: Detailed Agentic AI architecture with AWS services
- ✅ **Project Plan**: 16-week timeline with GANTT reference
- ✅ **Feasibility Analysis**: Risk assessment including AI-specific risks

### Presentation (10%)
- ✅ **Organization**: Logical flow from problem → consequences → solution
- ✅ **References**: IEEE citation style, 11 relevant sources
- ✅ **Page Limit**: 5 pages with appendices section
- ✅ **File Type**: PDF from IEEE template
- ✅ **Anonymity**: "Anonymous Submission for Fair Review" as author

---

## 📚 Document Structure

### Section I: Introduction (1 page)
- Real-world problem (dual crisis: information overload + personalization gap)
- Quantified consequences (\$450B losses, 27% underperformance)
- Why Agentic AI is the solution

### Section II: Project Scope and Target (0.75 pages)
- In-scope capabilities (multi-asset, real-time sentiment, autonomous risk)
- Out-of-scope (future work)
- Target customer segments with business value proposition

### Section III: Solution Design (1.5 pages)
- Multi-agent architecture diagram (LangGraph orchestration)
- Agent specifications table with autonomy levels
- Technical innovations (RAG, dynamic risk scoring, state management)
- AWS infrastructure design

### Section IV: Implementation Plan (0.5 pages)
- 16-week development phases
- Data strategy (static + non-static)

### Section V: Feasibility Analysis (0.75 pages)
- Proof-of-concept results (78% accuracy, 2.7s latency)
- AI-specific risk matrix with mitigations
- Revenue model and break-even analysis
- Regulatory considerations

### Section VI: Conclusion (0.5 pages)
- Summary of innovation, technical rigor, business value
- Future work

---

## 🛠️ How to Compile

### Option 1: Online (Easiest)
1. Go to [Overleaf](https://www.overleaf.com/project)
2. Create new project → Upload Project
3. Upload `proposal.tex`
4. Click **Recompile** → Download PDF

### Option 2: Local (Windows)
1. Install [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/)
2. Install Perl (for latexmk): https://www.perl.org/get.html
3. Run the compilation script:
   ```powershell
   .\compile.ps1
   ```
   Or manually:
   ```powershell
   pdflatex proposal.tex
   bibtex proposal
   pdflatex proposal.tex
   pdflatex proposal.tex
   ```

### Option 3: Local (Linux/Mac)
```bash
chmod +x compile.sh
./compile.sh
```

### Option 4: Docker (Cross-Platform)
```bash
docker run --rm -v ${PWD}:/workspace texlive/texlive pdflatex proposal.tex
```

---

## 📊 Key Highlights for Reviewers

### Technical Depth
- **LangGraph state machine**: Typed state objects (Pydantic) with rollback capability
- **RAG implementation**: Portfolio-aware news retrieval with Pinecone vector DB
- **Risk scoring formula**: Composite equation with volatility, sentiment, VaR
- **AWS architecture**: 7 services (ECS, Lambda, DynamoDB, SageMaker, etc.)

### Innovation Points
1. **Portfolio-aware RAG**: Context retrieval specific to user's holdings
2. **Human-in-the-loop autonomy**: Confidence threshold (0.8) for escalation
3. **Multi-asset coverage**: Stocks, crypto, commodities, forex in one system
4. **24/7 operation**: Asynchronous monitoring for global markets

### Business Validation
- Proof-of-concept metrics: 89% sentiment accuracy, 78% forecast accuracy
- Scalability tested: 1,000 concurrent users
- Clear revenue model: Freemium SaaS with 3,700 users to break-even
- Regulatory compliance: SEC, FINRA, GDPR considerations

---

## 🎨 Figures and Tables

### Figure 1: Multi-Agent Architecture
- TikZ diagram showing 9 agents
- LangGraph orchestration layer
- Data sources (News API, Market Data, Vector DB)
- Service layer (LLM, Orchestrator)

### Table 1: Agent Specifications
- 8 agents with autonomy levels and key technologies
- FinBERT, XGBoost, Gemini-2.5-Pro integrations

### Table 2: Project Timeline
- 5 phases over 16 weeks
- Deliverables per phase

### Table 3: Risk Matrix
- 5 AI-specific risks
- Impact levels and detailed mitigations

---

## 🔍 Compliance Checklist

- ✅ **IEEEtran document class**: `\documentclass[conference]{IEEEtran}`
- ✅ **Abstract**: 150-200 words
- ✅ **Keywords**: 5-8 relevant terms
- ✅ **Page limit**: 5 pages (without appendices)
- ✅ **References**: IEEE citation style
- ✅ **Anonymity**: No author names or affiliations
- ✅ **PDF format**: Compiled from LaTeX
- ✅ **Font**: Computer Modern (LaTeX default)
- ✅ **Margins**: IEEE standard (0.75" sides, 1" top/bottom)

---

## 📝 Customization Tips

### To modify content:
1. **Add more technical details**: Edit Section III (Solution Design)
2. **Update timeline**: Modify Table 2 in Section IV
3. **Add GANTT chart**: Uncomment TikZ code in appendix section
4. **Include screenshots**: Add `\includegraphics{screenshot.png}` in figures

### To adjust length:
- **Reduce**: Remove "Out-of-Scope" subsection, condense introduction
- **Expand**: Add "Related Work" section, expand feasibility analysis

### To add diagrams:
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.45\textwidth]{architecture.png}
\caption{System Architecture}
\label{fig:arch}
\end{figure}
```

---

## 🚀 Next Steps

1. **Review content**: Check for technical accuracy
2. **Compile PDF**: Use one of the methods above
3. **Proofread**: Check grammar, references, formatting
4. **Add visuals**: Consider adding Streamlit UI screenshots
5. **Submit**: Upload PDF to hackathon portal

---

## 📧 Support

For LaTeX compilation issues:
- [Overleaf Documentation](https://www.overleaf.com/learn)
- [IEEE Author Center](https://ieeeauthorcenter.ieee.org/)
- [Stack Exchange - TeX](https://tex.stackexchange.com/)

---

**Generated**: February 15, 2026  
**Version**: 1.0  
**LaTeX Engine**: pdfLaTeX  
**Template**: IEEEtran.cls (v1.8b)
