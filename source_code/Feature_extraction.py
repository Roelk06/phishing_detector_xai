from pydoc import text
import re
import math
import whois
import tldextract
from collections import Counter
from datetime import datetime

class FeatureExtractor:
    def __init__(self):
        self.email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

    def calculate_entropy(self, input):
        if not input:
            return 0.0

        entropy = 0
        length = len(input)
        counts = Counter(input)

        for count in counts.values():
            p = count/length
            entropy -= p * math.log2(p)

        return float(entropy)

    def calculate_domain_age(self, domain):
        try:
            domain_info = whois.whois(domain)
            creation_date = domain_info.creation_date

            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            if isinstance(creation_date, datetime):
                age = (datetime.now() - creation_date).days
                return age

        except Exception:
            return -1

        return -1

    def extract_features(self, input):
        features = {}

        is_email = 1 if self.email_pattern.match(input) else 0
        features["is_email"] = is_email

        splitting = input.split("@")[-1] if is_email else input
        extracted = tldextract.extract(splitting)

        features["input_length"] = len(input)
        features["domain_length"] = len(extracted.domain)
        features["dot_count"] = input.count(".")
        features["hyphen_count"] = input.count("-")
        features["apenstaartje_count"] = input.count("@")
        features["digit_count"] = sum(x.isdigit() for x in input)

        features["domain_entropy"] = self.calculate_entropy(extracted.domain)
        features["domain_age"] = self.calculate_domain_age(extracted.domain)

        return features

#testing
if __name__ == "__main__":
    extractor = FeatureExtractor()
    
    # Try a known, old domain
    test_legit = "admin@tilburguniversity.edu"
    print("Legit Features:")
    print(extractor.extract_features(test_legit))
    
    print("\n---")
    
    # Try a highly random, fake domain
    test_phish = "http://login-update-xjk89s2f.com/auth"
    print("Phishing Features:")
    print(extractor.extract_features(test_phish))
