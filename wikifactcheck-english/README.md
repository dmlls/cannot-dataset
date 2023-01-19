Data from the paper [**"Automated Fact-Checking of Claims from
Wikipedia"**](http://www.lrec-conf.org/proceedings/lrec2020/pdf/2020.lrec-1.849.pdf).

**Source**: https://github.com/wikifactcheck-english/wikifactcheck-english

<br>

### Cleaning process

1. Remove entries without the field `"refuted"`.
2. Entries in which the `"claim"` and `"refuted"` fields have a Jaccard index
   below `0.55`.
3. Entries in which the `"claim"` and `"refuted"` fields differ in length by 4
   or more words.
4. Remove entries in which the field `"claim"` contains named entities that
   don't appear in the field `"refuted"` or vice versa.

<br>

### Running the data processing script

The processed data is already provided under `processed/`. To redo the
processing, simply run:

```Python
python process_wikifactcheck_english_data.py original/wikifactcheck-english_full0.jsonl
```
