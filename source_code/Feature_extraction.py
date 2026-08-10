import re
import tldextract

class FeatureExtractor:
    def __init__(self):
        self.email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

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

        return features

#testing
if __name__ == "__main__":
    extractor = FeatureExtractor()
    test_mail = "admin@secure-update-apple.com"
    print("Email Features:", extractor.extract_features(test_mail))
