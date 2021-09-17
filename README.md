# BERTify

This is an easy-to-use python module that helps you to extract the **BERT embeddings** for a large text dataset efficiently. It is intended to be used for Bengali and English texts. (Use GPU for faster inference)

## Installation
```bash
$ pip install git+https://github.com/khalidsaifullaah/BERTify
```

## Usage

```python
from bertify import BERTify

# Example 1: Bengali Embedding Extraction
bn_bertify = BERTify(
    lang="bn",  # language of your text. Use `bn` for Bengali or `en` for English
    last_four_layers_embedding=True  # to get richer embeddings. (caveat: dimension is high)
)
# A list of texts that we want the embedding for, can be one or many. (You can turn your whole dataset into a list of texts and pass it into the method for faster embedding extraction)
texts = ["বিখ্যাত হওয়ার প্রথম পদক্ষেপ", "জীবনে সবচেয়ে মূল্যবান জিনিস হচ্ছে", "বেশিরভাগ মানুষের পছন্দের জিনিস হচ্ছে"]
bn_embeddings = bn_bertify.embedding(texts)   # returns numpy matrix 
# shape of the returned matrix in this example 3x4096 (3 -> num. of texts, 4096 -> embedding dim.)



# Example 2: English Embedding Extraction
en_bertify = BERTify(
    lang="en",
    last_four_layers_embedding=True
)
texts = ["how are you doing?", "I don't know about this.", "This is the most important thing."]
en_embeddings = en_bertify.embedding(texts) 
# shape of the returned matrix in this example 3x3072 (3 -> num. of texts, 3072 -> embedding dim.)
```
## License

Contents of this repository are restricted to non-commercial research purposes only under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). 

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>
