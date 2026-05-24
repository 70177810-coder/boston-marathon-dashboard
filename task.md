# Task: Improve Boston Marathon Dashboard

## Issues to Fix
1. **countplot error** — `sns.countplot` with `hue` parameter can fail with newer seaborn when Decade_Label has limited data
2. **Error handling** — filters can produce empty subsets causing chart crashes
3. **Smoothness** — add CSS animations (fade-in, slide-up for sections, hover effects)
4. **General robustness** — handle edge cases in all chart functions

## Plan
1. Update `charts.py` — add try/except to all chart functions, fix countplot
2. Update `app.py` — add CSS animations (keyframes, fade-in, staggered delays), wrap chart calls in error handling
3. Push to GitHub → auto-deploy on Render

## Status
- [ ] Fix charts.py
- [ ] Add animations to app.py  
- [ ] Push to GitHub
