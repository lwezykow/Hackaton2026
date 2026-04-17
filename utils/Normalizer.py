import unicodedata
import re
from typing import List, Set

class Normalizer:

    titles: Set[str] = {
        "mr", "mrs", "ms", "dr", "prof", "sir",
        "jr", "sr", "sa", "sp", "z", "o", "oo"
    }

    def normalize_text(self, text: str) -> str:
        """
        1. Remove diacritics (NFKD)
        2. Convert to lowercase
        3. Remove non-alphanumeric characters (keep spaces)
        """
        if not text:
            return ""

        # Remove diacritics
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if not unicodedata.combining(c))

        # Lowercase
        text = text.lower()

        # Remove non-alphanumeric characters (except spaces)
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def tokenize_and_filter(self, text: str) -> List[str]:
        """
        2. Tokenisation: split by spaces
        3. Filtering:
        - remove titles
        - remove tokens of length <= 1
        """
        tokens = text.split()

        filtered_tokens = [
            token for token in tokens
            if token not in self.titles and len(token) > 1
        ]

        return filtered_tokens

    def get_similarity_score(
            self,
        lhs: str,
        rhs: str
    ) -> float:
        """
        Compares entered beneficiary name with official beneficiary account name.    
        """

        # --- Normalisation ---
        norm_entered = self.normalize_text(lhs)
        norm_official = self.normalize_text(rhs)

        # --- Tokenisation & Filtering ---
        tokens_entered = self.tokenize_and_filter(norm_entered)
        tokens_official = self.tokenize_and_filter(norm_official)

        if not tokens_entered or not tokens_official:
            return 0.0

        # --- Comparison: exact token matches ---
        official_token_set = set(tokens_official)

        matched_count = sum(
            1 for token in tokens_entered
            if token in official_token_set
        )

        # --- Scoring ---
        score = matched_count / max(len(tokens_entered), len(tokens_official))

        return round(score, 4)
