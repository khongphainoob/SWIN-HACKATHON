@echo off
echo ========================================
echo Compiling IEEE LaTeX Proposal (Simple)
echo ========================================
echo.

REM First compilation
echo [1/2] First pdflatex pass...
pdflatex -interaction=nonstopmode proposal.tex

REM Second compilation for references
echo.
echo [2/2] Second pdflatex pass...
pdflatex -interaction=nonstopmode proposal.tex

REM Check result
echo.
if exist proposal.pdf (
    echo ========================================
    echo SUCCESS! PDF generated: proposal.pdf
    echo ========================================
    FOR %%A IN (proposal.pdf) DO echo File size: %%~zA bytes
) else (
    echo ========================================
    echo ERROR: PDF not created - check proposal.log
    echo ========================================
)

echo.
echo Press any key to exit...
pause >nul
