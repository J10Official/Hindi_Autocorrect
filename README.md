# Hindi Autocorrect

A Streamlit coursework application for Hindi spelling suggestions. It converts Devanagari input to a WX-style representation, generates edit candidates, ranks vocabulary matches by corpus frequency, and displays suggestions in Hindi.

## Run the application

From the repository root in a compatible Python environment:

```bash
python -m pip install -r requirements.txt
streamlit run hindi_autocorrect.py
```

Open the URL printed by Streamlit. Enter Hindi text in **Search Here** and select **Check**. The application reports known words, ranked suggestions, unsupported-character errors, or that no suggestion was found.

Keep `wx_output.txt` beside the application: the script reads that relative path when it starts.

## Files and data flow

| File | Purpose |
|---|---|
| [hindi_autocorrect.py](hindi_autocorrect.py) | Streamlit interface, transliteration, edit candidates, and ranking |
| [Hindi_corpus.txt](Hindi_corpus.txt) | Included source corpus |
| [strip.py](strip.py) | Cleans the source corpus into `output_corpus.txt` |
| [output_corpus.txt](output_corpus.txt) | Cleaned corpus |
| [hinditowxcorpus.py](hinditowxcorpus.py) | Converts the cleaned corpus into `wx_output.txt` |
| [wx_output.txt](wx_output.txt) | Vocabulary/frequency input used by the application |
| [requirements.txt](requirements.txt) | Original dependency list |

The prepared corpus files are included, so corpus preparation is separate from trying the application. Running `strip.py` or `hinditowxcorpus.py` regenerates their existing output files.

Suggestions depend on the vocabulary, corpus counts, and transliteration mappings implemented in this snapshot. The repository does not include a separate accuracy evaluation or a corpus provenance document.
