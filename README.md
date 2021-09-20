# BERTify

This is an easy-to-use python module that helps you to extract the **BERT embeddings** for a large text dataset efficiently. It is intended to be used for Bengali and English texts.


## Quick Installation
```bash
$ pip install git+https://github.com/khalidsaifullaah/BERTify
```

## Requirements
- numpy
- torch
- tqdm
- transformers

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

## Tips

- Try passing all your text data through the `.embedding()` function at once by turning it into a list of texts.
- For faster inference, make sure you're using your colab/kaggle GPU while making the `.embedding()` call
- Try increasing the `batch_size` to make it even faster, by default we're using `64` (to be on the safe side) which doesn't throw any `CUDA out of memory` but I believe we can go even further. Thanks to [Alex](https://afmck.in/), from his empirical findings, it seems like it can be pushed until `96`. So, before making the `.embedding()` call, you can do `bertify.batch_zie=96` to set a larger `batch_zie`

## Definitions
---------------
### **`class BERTify(lang: str = "en", last_four_layers_embedding: bool = False)`**
---------------
A module for extracting embedding from BERT model for Bengali or English text datasets.
    For `'en'` -> English data, it uses [`bert-base-uncased`](https://huggingface.co/bert-base-uncased) model embeddings, 
    for `'bn'` -> Bengali data, it uses [`sahajBERT`](https://huggingface.co/neuropark/sahajBERT) model embeddings.
    
> Parameters:

> **_`lang (str, optional)`_**: language of your data. Currently supports only `'en'` and `'bn'`. Defaults to `'en'`.
**_`last_four_layers_embedding (bool, optional)`_**: [`BERT`](https://arxiv.org/abs/1810.04805) paper discusses they've reached the best results 
by concatenating the output of the last four layers, so if this argument is set to `True`, 
your embedding vector would be (for `bert-base` model for example) `4*768=3072` dimensional, otherwise it'd be `768` dimensional. Defaults to `False`.

---------------
### **`def BERTify.embedding(texts: List[str])`**
---------------
The embedding function, that takes a list of texts, feed them through the model and returns a list of embeddings.
> Parameters:

> **_`texts (List[int])`_**: A list of texts, that you want to extract embedding for (e.g. `["This movie was a total waste of time.", "Whoa! Loved this movie, totally loved all the characters"]`)

> Returns:

> **_`np.ndarray`_**: A numpy matrix of shape `num_of_texts x embedding_dimension`


## License

[MIT License](https://github.com/khalidsaifullaah/BERTify/blob/main/LICENSE).
