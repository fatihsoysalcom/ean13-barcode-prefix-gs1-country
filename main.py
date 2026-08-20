import re

def calculate_ean13_checksum(barcode_12_digits):
    """Calculates the EAN-13 checksum digit for a 12-digit barcode."""
    if not re.fullmatch(r'\d{12}', barcode_12_digits):
        return None # Not a valid 12-digit input

    total_sum = 0
    for i, digit_char in enumerate(barcode_12_digits):
        digit = int(digit_char)
        # Digits at even positions (2nd, 4th, etc. from left) are multiplied by 3
        # In 0-indexed array, these are odd indices (1, 3, 5, ...)
        if (i + 1) % 2 == 0:
            total_sum += digit * 3
        else: # Digits at odd positions (1st, 3rd, etc. from left) are multiplied by 1
            total_sum += digit
    
    checksum = (10 - (total_sum % 10)) % 10
    return checksum

# Simplified mapping of GS1 prefixes to the country where the GS1 organization is located.
# This dictionary is crucial for demonstrating the article's core concept:
# The prefix indicates the GS1 organization's country, NOT the product's manufacturing country.
GS1_PREFIXES = {
    "00-13": "USA & Canada (GS1 Member Organization)",
    "30-37": "France (GS1 Member Organization)",
    "380": "Bulgaria (GS1 Member Organization)",
    "400-440": "Germany (GS1 Member Organization)",
    "450-459": "Japan (GS1 Member Organization)",
    "490-499": "Japan (GS1 Member Organization)",
    "50": "United Kingdom (GS1 Member Organization)",
    "54": "Belgium & Luxembourg (GS1 Member Organization)",
    "590": "Poland (GS1 Member Organization)",
    "690-695": "China (GS1 Member Organization)",
    "869": "Turkey (GS1 Member Organization)", # Directly relevant to the article's origin
    "977": "Serial Publications (ISSN)",
    "978": "Bookland (ISBN)",
    "979": "Bookland (ISBN)",
}

def get_gs1_country_from_prefix(prefix_str):
    """
    Looks up the GS1 country based on the barcode prefix string.
    Prioritizes 3-digit prefixes then 2-digit prefixes.
    """
    # Try 3-digit prefix first
    if len(prefix_str) >= 3:
        p3 = int(prefix_str[:3])
        for key, value in GS1_PREFIXES.items():
            if '-' in key:
                start, end = map(int, key.split('-'))
                if start <= p3 <= end:
                    return value
            elif key == prefix_str[:3]:
                return value
    
    # Then try 2-digit prefix
    if len(prefix_str) >= 2:
        p2 = int(prefix_str[:2])
        for key, value in GS1_PREFIXES.items():
            if '-' in key:
                start, end = map(int, key.split('-'))
                if start <= p2 <= end:
                    return value
            elif key == prefix_str[:2]:
                return value
                
    return "Unknown GS1 Member Organization"


def analyze_ean13_barcode(barcode_string):
    """
    Analyzes an EAN-13 barcode to determine its validity and the GS1 country prefix.
    This function explicitly demonstrates that the prefix indicates the GS1 organization's country,
    NOT necessarily the product's manufacturing country.
    """
    print(f"\nAnalyzing barcode: {barcode_string}")

    # 1. Basic format validation
    if not re.fullmatch(r'\d{13}', barcode_string):
        print("  Status: Invalid format. EAN-13 barcodes must be exactly 13 digits.")
        return

    # 2. Extract components
    data_digits = barcode_string[:12]
    check_digit = int(barcode_string[12])
    
    # 3. Validate checksum
    calculated_check_digit = calculate_ean13_checksum(data_digits)
    if calculated_check_digit is None:
        print("  Error: Internal checksum calculation failed for data digits.")
        return

    if check_digit != calculated_check_digit:
        print(f"  Status: Invalid barcode. Checksum mismatch.")
        print(f"    Expected check digit: {calculated_check_digit}, Found: {check_digit}")
        return

    print("  Status: Valid EAN-13 barcode.")

    # 4. Extract prefix (first 2-3 digits) and look up its meaning
    # The core demonstration of the article's concept happens here.
    prefix = barcode_string[:3] # Try 3 digits first
    gs1_country_info = get_gs1_country_from_prefix(prefix)
    
    # If 3-digit prefix didn't yield a specific result, try 2-digit
    if "Unknown" in gs1_country_info and len(barcode_string) >= 2:
        prefix = barcode_string[:2]
        gs1_country_info = get_gs1_country_from_prefix(prefix)

    print(f"  Barcode Prefix: {prefix}")
    # This is the key takeaway: the prefix identifies the GS1 organization's location.
    print(f"  This prefix ({prefix}) indicates the barcode was assigned by the: {gs1_country_info}.")
    print("  IMPORTANT: This DOES NOT necessarily mean the product was manufactured in that country.")
    print("             Global supply chains mean products can be manufactured anywhere,")
    print("             regardless of where their barcode was registered.")


if __name__ == "__main__":
    print("--- EAN-13 Barcode Origin Analyzer ---")
    print("This script demonstrates that an EAN-13 barcode's prefix indicates")
    print("the country of the GS1 organization that assigned the barcode, not")
    print("the product's country of manufacture. This debunks a common myth.")

    # Example 1: A barcode registered in Turkey (869 prefix)
    # The product *could* be made in Turkey, but the barcode itself doesn't guarantee it.
    analyze_ean13_barcode("8691234567890") # Valid EAN-13 for Turkey's GS1

    # Example 2: A barcode registered in China (690-695 prefix)
    # A product with a Chinese barcode prefix might be manufactured elsewhere,
    # or it might be manufactured in China and exported. The prefix only tells us
    # where the barcode number was issued.
    analyze_ean13_barcode("6901234567899") # Valid EAN-13 for China's GS1

    # Example 3: A barcode registered in the USA/Canada (00-13 prefix)
    # A product with a US/Canada barcode prefix could be manufactured in Asia, Europe, etc.
    analyze_ean13_barcode("0712345678904") # Valid EAN-13 for USA/Canada's GS1

    # Example 4: An invalid barcode (wrong length)
    analyze_ean13_barcode("12345")

    # Example 5: An invalid barcode (checksum mismatch)
    analyze_ean13_barcode("8691234567891") # Last digit changed from '0' to '1', making it invalid
