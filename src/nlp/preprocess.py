"""
Natural Language Processing (NLP) Preprocessing Pipeline
Toxic Comment Moderation System

Features:
- Text normalization (lowercasing, URL/HTML/emoji/special character removal)
- Comprehensive internet slang and toxic abbreviation expansion
- Tokenization, stopword filtering with negation preservation, lemmatization
- Sequence padding and Keras Tokenizer serialization
- Class imbalance weight calculation for multi-label classification
"""

import re
import os
import pickle
import numpy as np
from typing import List, Tuple, Dict, Any, Optional

# Attempt NLTK imports with robust fallback
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer, PorterStemmer
    from nltk.tokenize import word_tokenize
    
    # Ensure standard corpora are downloaded
    for resource in ["stopwords", "wordnet", "punkt", "punkt_tab"]:
        try:
            nltk.data.find(f"corpora/{resource}" if resource != "punkt" and resource != "punkt_tab" else f"tokenizers/{resource}")
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass
except ImportError:
    nltk = None

# Comprehensive Slang & Abbreviation Dictionary
SLANG_MAP: Dict[str, str] = {
    "u": "you",
    "r": "are",
    "ur": "your",
    "urs": "yours",
    "ure": "you are",
    "you're": "you are",
    "y'all": "you all",
    "im": "i am",
    "i'm": "i am",
    "dont": "do not",
    "don't": "do not",
    "wont": "will not",
    "won't": "will not",
    "cant": "cannot",
    "can't": "cannot",
    "didnt": "did not",
    "didn't": "did not",
    "doesnt": "does not",
    "doesn't": "does not",
    "isnt": "is not",
    "isn't": "is not",
    "arent": "are not",
    "aren't": "are not",
    "wtf": "what the fuck",
    "stfu": "shut the fuck up",
    "gtfo": "get the fuck out",
    "fubar": "fucked up beyond all recognition",
    "omg": "oh my god",
    "omfg": "oh my fucking god",
    "lmao": "laughing my ass off",
    "lmfao": "laughing my fucking ass off",
    "rofl": "rolling on the floor laughing",
    "idk": "i do not know",
    "idc": "i do not care",
    "imo": "in my opinion",
    "imho": "in my humble opinion",
    "fyi": "for your information",
    "tbh": "to be honest",
    "smh": "shaking my head",
    "ffs": "for fucks sake",
    "bs": "bullshit",
    "fck": "fuck",
    "fuk": "fuck",
    "f**k": "fuck",
    "f***": "fuck",
    "b**ch": "bitch",
    "b1tch": "bitch",
    "sh*t": "shit",
    "s**t": "shit",
    "a**hole": "asshole",
    "a$$hole": "asshole",
    "n00b": "noob",
    "noob": "newbie",
    "thx": "thanks",
    "pls": "please",
    "plz": "please",
    "ppl": "people",
    "wth": "what the hell",
    "killyourself": "kill yourself",
    "kys": "kill yourself",
    "pos": "piece of shit",
    "sob": "son of a bitch",
    "gtg": "got to go",
    "brb": "be right back",
    "afaik": "as far as i know",
    "bc": "because",
    "b/c": "because",
    "cuz": "because",
    "cos": "because",
    "w/": "with",
    "w/o": "without",
    "rt": "retweet",
    "dm": "direct message",
}

# Standard English stopwords while preserving critical negation semantics
DEFAULT_STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other", "some", "such", "only",
    "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just",
    "don", "should", "now"
}

# Exclude negations and emphasis from stopwords
NEGATIONS = {"not", "no", "nor", "neither", "never", "none", "cannot", "without"}
CUSTOM_STOPWORDS = DEFAULT_STOPWORDS - NEGATIONS

# Precompiled Regexes
URL_REGEX = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
HTML_REGEX = re.compile(r"<.*?>")
EMOJI_REGEX = re.compile(
    r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\uD83C-\uDBFF\uDC00-\uDFFF]",
    flags=re.UNICODE,
)
SPECIAL_CHAR_REGEX = re.compile(r"[^a-zA-Z0-9\s!\?]")
WHITESPACE_REGEX = re.compile(r"\s+")
REPEATED_CHAR_REGEX = re.compile(r"(.)\1{2,}")  # Replaces 'fuuuuck' -> 'fuuck'


class KerasCompatibleTokenizer:
    """Standard Keras-compatible text Tokenizer with serialization support."""
    def __init__(self, num_words: int = 15000, oov_token: str = "<OOV>", lower: bool = True):
        self.num_words = num_words
        self.oov_token = oov_token
        self.lower = lower
        self.word_counts: Dict[str, int] = {}
        self.word_index: Dict[str, int] = {}
        self.index_word: Dict[int, str] = {}

    def fit_on_texts(self, texts: List[str]) -> None:
        for text in texts:
            if self.lower:
                text = text.lower()
            words = text.split()
            for w in words:
                self.word_counts[w] = self.word_counts.get(w, 0) + 1

        sorted_words = sorted(self.word_counts.items(), key=lambda kv: kv[1], reverse=True)
        idx = 1
        if self.oov_token:
            self.word_index[self.oov_token] = idx
            self.index_word[idx] = self.oov_token
            idx += 1

        for word, _ in sorted_words:
            if self.num_words and idx > self.num_words:
                break
            if word not in self.word_index:
                self.word_index[word] = idx
                self.index_word[idx] = word
                idx += 1

    def texts_to_sequences(self, texts: List[str]) -> List[List[int]]:
        oov_idx = self.word_index.get(self.oov_token, 1)
        sequences = []
        for text in texts:
            if self.lower:
                text = text.lower()
            words = text.split()
            seq = []
            for w in words:
                idx = self.word_index.get(w, oov_idx)
                if self.num_words and idx > self.num_words:
                    idx = oov_idx
                seq.append(idx)
            sequences.append(seq)
        return sequences


class TextPreprocessor:
    """Reusable NLP preprocessing pipeline for toxicity classification."""

    def __init__(
        self,
        use_lemmatization: bool = True,
        use_stemming: bool = False,
        remove_stopwords: bool = True,
        max_vocab_size: int = 20000,
        max_sequence_length: int = 150,
    ):
        self.use_lemmatization = use_lemmatization
        self.use_stemming = use_stemming
        self.remove_stopwords = remove_stopwords
        self.max_vocab_size = max_vocab_size
        self.max_sequence_length = max_sequence_length

        self.lemmatizer = None
        self.stemmer = None
        self.stopwords = CUSTOM_STOPWORDS

        if nltk is not None:
            try:
                self.lemmatizer = WordNetLemmatizer()
            except Exception:
                self.lemmatizer = None
            try:
                self.stemmer = PorterStemmer()
            except Exception:
                self.stemmer = None

        self.tokenizer = None

    def normalize_slang(self, text: str) -> str:
        """Expands internet slang and abusive abbreviations into full tokens."""
        words = text.split()
        normalized = [SLANG_MAP.get(w.lower(), w) for w in words]
        return " ".join(normalized)

    def clean_text(self, text: str) -> str:
        """
        Executes complete text cleansing pipeline:
        - HTML stripping
        - URL removal
        - Lowercasing
        - Slang expansion
        - Emoji/special character removal
        - Repeated character normalization
        """
        if not isinstance(text, str):
            return ""

        # 1. Lowercase
        text = text.lower()

        # 2. Strip HTML tags
        text = HTML_REGEX.sub(" ", text)

        # 3. Strip URLs
        text = URL_REGEX.sub(" ", text)

        # 4. Remove emojis
        text = EMOJI_REGEX.sub(" ", text)

        # 5. Normalize slang / abbreviations
        text = self.normalize_slang(text)

        # 6. Reduce elongated repeated letters (e.g. 'loooool' -> 'lool', 'baaaad' -> 'baad')
        text = REPEATED_CHAR_REGEX.sub(r"\1\1", text)

        # 7. Strip special characters except alphanumeric, basic spaces, and sentiment-heavy marks
        text = SPECIAL_CHAR_REGEX.sub(" ", text)

        # 8. Collapse whitespace
        text = WHITESPACE_REGEX.sub(" ", text).strip()

        return text

    def tokenize_and_lemmatize(self, text: str) -> str:
        """
        Tokenizes cleaned text, filters non-essential stopwords,
        and applies lemmatization or stemming.
        """
        cleaned = self.clean_text(text)
        if not cleaned:
            return ""

        tokens = cleaned.split()

        processed_tokens: List[str] = []
        for token in tokens:
            # Optional stopword filter
            if self.remove_stopwords and token in self.stopwords:
                continue

            # Lemmatization / Stemming
            if self.use_lemmatization and self.lemmatizer:
                try:
                    token = self.lemmatizer.lemmatize(token)
                except Exception:
                    pass
            elif self.use_stemming and self.stemmer:
                try:
                    token = self.stemmer.stem(token)
                except Exception:
                    pass

            processed_tokens.append(token)

        return " ".join(processed_tokens)

    def preprocess_corpus(self, texts: List[str]) -> List[str]:
        """Processes a list of raw text strings into cleaned, tokenized strings."""
        return [self.tokenize_and_lemmatize(t) for t in texts]

    def fit_tokenizer(self, cleaned_texts: List[str]) -> Any:
        """Fits a Tokenizer on the cleaned corpus (Keras compatible)."""
        # Attempt Keras import if available and functioning, else self-contained tokenizer
        try:
            from tensorflow.keras.preprocessing.text import Tokenizer  # type: ignore
            tok = Tokenizer(num_words=self.max_vocab_size, oov_token="<OOV>", lower=True)
            tok.fit_on_texts(cleaned_texts)
            self.tokenizer = tok
        except Exception:
            tok = KerasCompatibleTokenizer(num_words=self.max_vocab_size, oov_token="<OOV>", lower=True)
            tok.fit_on_texts(cleaned_texts)
            self.tokenizer = tok

        return self.tokenizer

    def texts_to_padded_sequences(
        self, texts: List[str], maxlen: Optional[int] = None
    ) -> np.ndarray:
        """
        Converts texts to token index sequences and applies post-padding/truncation.
        """
        if self.tokenizer is None:
            raise ValueError("Tokenizer has not been fitted or loaded yet.")

        target_len = maxlen or self.max_sequence_length
        sequences = self.tokenizer.texts_to_sequences(texts)

        # Vectorized padding implementation
        N = len(sequences)
        padded = np.zeros((N, target_len), dtype=np.int32)
        for i, seq in enumerate(sequences):
            if not seq:
                continue
            truncated = seq[:target_len]
            padded[i, :len(truncated)] = truncated

        return padded

    def save_tokenizer(self, filepath: str) -> None:
        """Saves fitted tokenizer and preprocessor metadata to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(
                {
                    "tokenizer": self.tokenizer,
                    "max_vocab_size": self.max_vocab_size,
                    "max_sequence_length": self.max_sequence_length,
                },
                f,
            )

    @classmethod
    def load_tokenizer(cls, filepath: str) -> "TextPreprocessor":
        """Loads a preprocessor instance with its serialized tokenizer."""
        instance = cls()
        with open(filepath, "rb") as f:
            data = pickle.load(f)
            instance.tokenizer = data["tokenizer"]
            instance.max_vocab_size = data.get("max_vocab_size", 20000)
            instance.max_sequence_length = data.get("max_sequence_length", 150)
        return instance


def compute_multilabel_class_weights(y: np.ndarray) -> Dict[int, Dict[int, float]]:
    """
    Computes class weights for multi-label binary crossentropy.
    y: 2D numpy array of shape (N_samples, N_classes)
    Returns: Dict mapping each label index to {0: weight_neg, 1: weight_pos}
    """
    n_samples, n_classes = y.shape
    weights = {}
    for c in range(n_classes):
        pos_count = np.sum(y[:, c] == 1)
        neg_count = np.sum(y[:, c] == 0)
        if pos_count == 0 or neg_count == 0:
            weights[c] = {0: 1.0, 1: 1.0}
        else:
            w0 = n_samples / (2.0 * neg_count)
            w1 = n_samples / (2.0 * pos_count)
            weights[c] = {0: float(w0), 1: float(w1)}
    return weights


def compute_pos_weights(y: np.ndarray) -> np.ndarray:
    """
    Computes ratio of negative to positive samples per class for BCEWithLogits / Keras loss weighting.
    """
    n_samples, n_classes = y.shape
    pos_weights = np.zeros(n_classes, dtype=np.float32)
    for c in range(n_classes):
        pos_count = np.sum(y[:, c] == 1)
        neg_count = np.sum(y[:, c] == 0)
        pos_weights[c] = neg_count / max(pos_count, 1)
    return pos_weights
