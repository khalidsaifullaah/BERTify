# Author: Khalid Saifullah (https://twitter.com/k_saifullaah)

from typing import List

import numpy as np
from tqdm.auto import tqdm

from transformers import AutoModel, AutoTokenizer
from transformers import DataCollatorWithPadding

import torch
from torch.utils.data import DataLoader, Dataset


class BERTify():
    """A module for extracting embedding from BERT model for Bengali or English text datasets.
    For `'en'` -> English data, it uses `bert-base-uncased` model embeddings, 
    for `'bn'` -> Bengali data, it uses `sahajBERT` model embeddings.
    Args:
        lang (str, optional): language of your data. Must be in ['en', 'bn']. Defaults to "en".
        last_four_layers_embedding (bool, optional): BERT paper discusses they've reached the best results 
        by concatenating the output of the last four layers, so if this argument is true, 
        your embedding vector would be (for bert-base model for example) 4*768=3072, else it'd be 768 dimensional. 
        Defaults to False.
    """
    def __init__(self, lang: str = "en", last_four_layers_embedding: bool = False):


        # Set the device to GPU (cuda) if available, otherwise stick with CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.last_four_layers_embedding = last_four_layers_embedding
        self.batch_size = 64    # keep pushing this one for faster inference (for now we kept it hard coded)

        if lang.lower() == "en":
            checkpoint = "bert-base-uncased"

        elif lang.lower() == "bn":
            checkpoint = "neuropark/sahajBERT"

        else:
            raise ValueError("Unknown language. Use 'en' for English data or 'bn' for Bengali data.")
        
        self.model_name_or_path = checkpoint    # if you want to use a custom model, just pass the HF path to the model here (caution: the rest of the code is not tested for custom models)

        print("#"*10)
        print(f"Using {self.device} for computation")
        print(f"using {self.model_name_or_path} model for {lang} embedding")
        print("#"*10)

        # Download the model and tokenizer from the checkpoint
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, use_fast=True)
        self.model = AutoModel.from_pretrained(self.model_name_or_path, output_hidden_states=True).to(self.device)
        self.model.eval()


    def embedding(self, texts: List[str]) -> np.ndarray:
        """The embedding function, that takes a list of texts, feed them through the model 
            and returns a list of embeddings.
        Args:
            texts (List[str]): A list of texts, that you want to extract embedding for 
            (e.g. ["This movie was total B.S.", "I totally loved all the characters"])
        Returns:
            np.ndarray: A numpy matrix of shape `num_of_texts x embedding_dimension`
        """

        # Turning the list of texts into a Dataset, so that we can batchify using DataLoader and speedup inference
        class TextsData(Dataset):
            def __init__(self, texts, tokenizer):
                self.texts = texts
                self.tokenizer = tokenizer


            def __getitem__(self, idx):
                encodings = self.tokenizer(self.texts[idx], truncation=True)
                
                return encodings

            def __len__(self):
                return len(self.texts)

        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        texts_data = TextsData(texts, self.tokenizer)
        texts_dl = DataLoader(texts_data, batch_size=self.batch_size, collate_fn=data_collator)

        # A list for storing all the batch embeddings
        text_embeddings = []

        for batch in tqdm(texts_dl):
            # forward pass
            with torch.inference_mode():
                out = self.model(input_ids=batch['input_ids'].to(self.device))

            # we only want the hidden_states
            hidden_states = out[2]  # batch_size x sequence_length x embedding_dim
            
            if self.last_four_layers_embedding:
                # get last four layers embedding
                last_four_layers = [hidden_states[i] for i in (-1, -2, -3, -4)]

                # cast layers to a tuple and concatenate over the last dimension
                cat_hidden_states = torch.cat(tuple(last_four_layers), dim=-1)

                # take the mean of the concatenated embedding vectors over the token dimension
                text_embedding = torch.mean(cat_hidden_states, dim=1)   

            else:
                # take the embedding vector from the last layer
                text_embedding = torch.mean(hidden_states[-1], dim=1).squeeze()

            text_embeddings.append(text_embedding.to('cpu'))

            # clearing out the GPU cache
            torch.cuda.empty_cache()

        # turning the list of embeddings into a matrix by concatnating them all in vertical dimension/row axis
        text_embeddings = torch.cat(tuple(text_embeddings), 0)

        # clearing out the GPU cache
        torch.cuda.empty_cache()

        return text_embeddings.numpy()