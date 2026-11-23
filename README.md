# WAEC English Mastery (Streamlit)

An examination-practice prototype using structured WAEC English question datasets.

## Technology stack
- Python
- Streamlit
- Pandas
- OpenAI SDK
- gTTS

## Verified implementation
- Provides a styled examination interface
- stores year-specific CSV question files
- includes OpenAI and text-to-speech integrations in code.

## Getting started

```bash
git clone https://github.com/ebukaxyrus/waecdemoapp.git
cd waecdemoapp
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run check3.py
```

Review the source for required API credentials, data files, local environment settings, and device permissions before running. Never commit real API keys or passwords.

## Important limitations

Verify that deployed AI/audio features work with configured credentials and that examination question content is legally publishable.

## Project structure

- `check3.py`: primary application entry point.
- `requirements.txt`: Python package requirements.
- `waec_english_*_complete.csv`: year-specific question data files.

## Suggested next improvements

- [ ] Test installation from scratch and pin versions.
- [ ] Include real screenshots, verified live URL and a demo walkthrough.
- [ ] Add automated tests and document tested configuration.
- [ ] Verify source/data rights and operational security.

## Maintainer

**Dimakunne Chukwuebuka Francis**  
[GitHub](https://github.com/ebukaxyrus) · [Portfolio](https://xyrusportfolio.netlify.app/) · [XY AI Solution](https://xyaisolution.online/)

*Documentation is grounded in source review; the application was not independently deployed or benchmarked for this update.*
