# ✅ SUBMISSION CHECKLIST - Personal Sentiment Advisor Proposal

## 📋 Pre-Compilation Checklist

### Content Verification
- [ ] Introduction section covers problem, consequences, and Agentic AI solution
- [ ] Project scope clearly defines in-scope vs. out-of-scope
- [ ] Solution design includes multi-agent architecture diagram
- [ ] Agent specification table shows 8+ agents with autonomy levels
- [ ] AWS infrastructure lists 5+ services (ECS, Lambda, DynamoDB, etc.)
- [ ] Project timeline shows realistic 16-week plan
- [ ] Feasibility section includes PoC results (accuracy, latency, scalability)
- [ ] Risk matrix addresses 5+ AI-specific risks with mitigations
- [ ] Business model includes revenue strategy and break-even analysis
- [ ] References section has 10+ citations in IEEE format

### Technical Accuracy
- [ ] LangGraph terminology used correctly (state machine, typed state)
- [ ] RAG explanation is accurate (retrieval-augmented generation)
- [ ] FinBERT cited correctly (sentiment analysis model)
- [ ] AWS service names are correct (not "AWS EC2 Container Service" → "ECS Fargate")
- [ ] Mathematical formulas render properly (Risk composite equation)
- [ ] No placeholder text remains (e.g., "TODO", "Lorem ipsum")

### Format Compliance
- [ ] Document class is `\documentclass[conference]{IEEEtran}`
- [ ] Author shows "Anonymous Submission for Fair Review"
- [ ] Abstract is 150-200 words
- [ ] Keywords listed (5-8 terms)
- [ ] Page count is ≤5 pages (before appendices)
- [ ] All figures have captions and labels
- [ ] All tables have captions and labels
- [ ] In-text citations match bibliography entries

---

## 🛠️ Compilation Checklist

### Step 1: Compile LaTeX
- [ ] Installed LaTeX distribution (MiKTeX/TeX Live/Overleaf)
- [ ] Run `.\compile.ps1` (Windows) or `./compile.sh` (Linux/Mac)
- [ ] No compilation errors (check `proposal.log` if errors occur)
- [ ] PDF generated successfully (`proposal.pdf` exists)

### Step 2: Visual Inspection
- [ ] Open `proposal.pdf` in PDF reader
- [ ] All pages render correctly (no missing text or figures)
- [ ] Figure 1 (architecture diagram) displays properly
- [ ] All 3 tables are readable (not cut off at margins)
- [ ] Font is consistent throughout (Computer Modern)
- [ ] No strange characters or encoding issues
- [ ] Page numbers appear in footer
- [ ] References section is complete and formatted correctly

### Step 3: Content Validation
- [ ] Read abstract—does it clearly state problem, solution, and results?
- [ ] Read introduction—does it explain why Agentic AI is the solution?
- [ ] Check Section III (Solution Design)—is architecture diagram understandable?
- [ ] Check Section V (Feasibility)—are PoC results convincing?
- [ ] Read conclusion—does it summarize innovation, technical rigor, and business value?

### Step 4: Technical Validation
- [ ] All in-text citations link to bibliography (e.g., \cite{ref} → [1])
- [ ] All figures referenced in text (e.g., "Figure \ref{fig:architecture}")
- [ ] All equations render properly (no $$$ symbols visible)
- [ ] No LaTeX commands visible in PDF (e.g., `\textbf` should be bold text)
- [ ] TikZ diagram (architecture) renders without errors

---

## 🔒 Anonymity Checklist

### Metadata Scrubbing
- [ ] Author field in LaTeX shows "Anonymous Submission"
- [ ] No team member names anywhere in document
- [ ] No company/institution names (unless generic examples)
- [ ] No URLs containing personal/company identifiers
- [ ] PDF metadata cleared:
  ```powershell
  # Check PDF metadata
  exiftool proposal.pdf
  # Should show: Author = "Anonymous Submission"
  ```

### Content Anonymization
- [ ] No "we built this at XYZ company" statements
- [ ] No "our team at ABC university" references
- [ ] No identifying screenshots (e.g., username "john.doe" visible)
- [ ] Email addresses removed or anonymized (use generic@example.com)
- [ ] No acknowledgments section (premature for submission)

---

## 📊 Marking Criteria Self-Assessment

### Innovation (Target: 28-30/30)
- [ ] **Novelty (10 pts)**: Is "portfolio-aware RAG" clearly explained as unique?
- [ ] **Autonomy (10 pts)**: Do 9 agents demonstrate sufficient autonomy?
- [ ] **Business Value (10 pts)**: Is \$1.5T TAM and 88% cost reduction credible?

**Self-Grade**: ___/30

### Technical Proposal (Target: 55-60/60)
- [ ] **Executive Summary (5 pts)**: Does abstract cover all key points?
- [ ] **Project Scope (5 pts)**: Are in-scope and out-of-scope clear?
- [ ] **Requirements (10 pts)**: Is data strategy comprehensive?
- [ ] **Solution Design (20 pts)**: Does architecture diagram show Agentic AI logic?
- [ ] **Project Plan (10 pts)**: Is 16-week timeline realistic with GANTT?
- [ ] **Feasibility (10 pts)**: Are PoC results and risk mitigation convincing?

**Self-Grade**: ___/60

### Presentation (Target: 9-10/10)
- [ ] **Organization (3 pts)**: Logical flow from problem → solution?
- [ ] **Writing (3 pts)**: Professional, high-density, error-free?
- [ ] **References (2 pts)**: 10+ IEEE-style citations?
- [ ] **Format (2 pts)**: PDF from IEEE template, ≤5 pages?

**Self-Grade**: ___/10

**TOTAL TARGET**: 92+/100

---

## 📤 Submission Preparation

### File Naming
- [ ] Rename PDF according to submission guidelines (check hackathon portal)
- [ ] Common formats:
  - `proposal_anonymous.pdf`
  - `team_XXXX_proposal.pdf`
  - `hackathon2026_submission.pdf`

### File Verification
```powershell
# Check file size (should be <5 MB for 5 pages)
Get-Item proposal.pdf | Select-Object Name, @{N='SizeMB';E={[math]::Round($_.Length/1MB,2)}}

# Check page count (requires pdfinfo or similar)
pdfinfo proposal.pdf | Select-String "Pages"
```

- [ ] File size is reasonable (<5 MB, ideally <2 MB)
- [ ] Page count is exactly 5 pages (not 4.9, not 5.1)

### Backup Strategy
- [ ] Save PDF to cloud storage (Google Drive, Dropbox)
- [ ] Email PDF to yourself as backup
- [ ] Keep LaTeX source files for post-submission edits
- [ ] Export to Word (as fallback): `pandoc proposal.tex -o proposal.docx`

---

## 🚀 Submission Day Checklist

### 1 Hour Before Deadline
- [ ] Re-read submission instructions on hackathon portal
- [ ] Verify file format requirements (PDF, DOCX, etc.)
- [ ] Check maximum file size limit
- [ ] Test upload on slow internet connection (if applicable)

### 30 Minutes Before Deadline
- [ ] Log into submission portal
- [ ] Fill out submission form (title, abstract, team info)
- [ ] Upload PDF
- [ ] Preview uploaded file (ensure it displays correctly)
- [ ] Submit form

### After Submission
- [ ] Save confirmation email
- [ ] Screenshot submission receipt
- [ ] Note submission timestamp
- [ ] Prepare for presentation round (if applicable)

---

## 🎤 Presentation Preparation (If Required)

### Materials Needed
- [ ] Presentation slides (15-20 slides, 15-minute talk)
- [ ] Live demo environment ready (Streamlit app running)
- [ ] Backup demo video (in case WiFi fails)
- [ ] Printed handout (1-page summary) for judges
- [ ] Business cards or contact info

### Technical Setup
- [ ] Laptop fully charged + charger
- [ ] HDMI adapter (USB-C to HDMI if needed)
- [ ] Test projector connection beforehand
- [ ] WiFi credentials for venue
- [ ] Backup internet (mobile hotspot)

### Rehearsal Checklist
- [ ] Practiced presentation 3+ times
- [ ] Timed presentation (should be 13-15 minutes to allow buffer)
- [ ] Prepared answers for anticipated questions:
  - "How is this different from existing robo-advisors?"
  - "What if the LLM hallucinates?"
  - "Is this SEC regulated?"
  - "What's your go-to-market strategy?"
- [ ] Team roles assigned (who presents which section)

---

## 🐛 Common Issues & Fixes

### LaTeX Compilation Errors

**Error**: `! LaTeX Error: File 'IEEEtran.cls' not found`  
**Fix**: Install IEEEtran package:
```powershell
# MiKTeX
mpm --install=ieeetran

# TeX Live
tlmgr install ieeetran
```

**Error**: `! Package tikz Error: I do not know the key '/tikz/agent'`  
**Fix**: TikZ style undefined. Check `\usetikzlibrary{shapes.geometric, arrows}` is in preamble.

**Error**: `! Undefined control sequence. \cite{reference}`  
**Fix**: Reference not in bibliography. Add to `\begin{thebibliography}` section.

**Error**: `Overfull \hbox` warnings  
**Fix**: Acceptable if <5pt. Reword sentences to fit margins if >10pt overfull.

### PDF Issues

**Issue**: Architecture diagram doesn't render  
**Fix**: Simplify TikZ code or export diagram as PNG and use `\includegraphics`.

**Issue**: PDF is 6 pages instead of 5  
**Fix**: Reduce content:
- Remove "Out-of-Scope" subsection
- Condense introduction
- Shrink table font size to `\scriptsize`

**Issue**: References section is cut off  
**Fix**: Use `\small` font for bibliography:
```latex
\begin{thebibliography}{00}
\small
\bibitem{ref1} ...
\end{thebibliography}
```

---

## 📞 Emergency Contacts

### Technical Support
- **Overleaf Support**: https://www.overleaf.com/learn
- **IEEE Author Center**: https://ieeeauthorcenter.ieee.org/
- **LaTeX Stack Exchange**: https://tex.stackexchange.com/

### Submission Portal Support
- Check hackathon website for support email
- Typically: `support@hackathon.com` or organizer contact

### Backup Plan
If submission portal is down:
1. Email PDF to organizers with subject: "Emergency Submission - [Team Name]"
2. Include timestamp of email as proof of on-time submission
3. Follow up via submission portal when it's back online

---

## ✅ Final Sign-Off

**Completed By**: _________________  
**Date**: _________________  
**Time**: _________________  

**Submission Confirmation Number**: _________________

**Ready for Judging**: YES / NO

---

**Version**: 1.0  
**Last Updated**: February 15, 2026  
**Status**: 🚀 READY FOR SUBMISSION
