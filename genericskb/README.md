Data from the paper [**"GenericsKB: A Knowledge Base of Generic
Statements"**](https://arxiv.org/abs/2005.00660).

**Source**:
https://allenai.org/data/genericskb

The GenericsKB is available under the Creative Commons - Attribution 4.0
International - licence. More info at the [project's
repo](https://drive.google.com/drive/folders/1vqfVXhJXJWuiiXbUa4rZjOgQoJvwZUoT).

<br>

### Cleaning process

1. Keep only the `SENTENCE` column and rename it to `premise`. Clean up:
   1. Replace "isa" with "is a".
   2. Replace "have (part)" to "have", and "has (part)" to "has".
   3. Remove instances with "has-part".
2. Keep only the `SENTENCE` column and rename it to `premise`.
3. Keep only sentences that have at most 33 words.
4. For each sentence, run the Python "[negate](https://github.com/dmlls/negate)"
   module to get its negated version. Non-supported sentences are removed.

<br>

### Running the data processing script

The processed data is already provided under `processed/`. To redo the
processing, simply run:

```Python
python process_generics_kb.py original/GenericsKB-Best.tsv
```
