from ner import ner_extract

def clean(x):
    return x.strip().replace("\n", " ") if x else ""

def extract_structured(text: str):

    ner = ner_extract(text)

    data = {
        "shop_name": "",
        "owner_name": "",
        "owner_phone": "",                # will come as CARDINAL
        "owner_mail": "",
        "customer_name": "",
        "customer_phone": "",
        "customer_address": "",
        "customer_email": "",
        "customer_date_of_birth": "",
        "product_name": "",
        "product_brand": "",
        "purchase_date": "",
        "selling_date": "",
        "purchase_amount": "",
        "expenditure": "",
        "purchase_price": "",
        "selling_price": "",
        "warranty_period": "",
        "invoice_number": "",
        "offer_name": "",
        "offer_code": "",
        "discount_type": "",
        "raw_text": text
    }

    for ent in ner:
        txt = ent["text"]
        label = ent["label"]

        # Names
        if label == "PERSON":
            if not data["customer_name"]:
                data["customer_name"] = txt
            elif not data["owner_name"]:
                data["owner_name"] = txt

        # Emails
        if label == "EMAIL":
            if not data["owner_mail"]:
                data["owner_mail"] = txt
            if not data["customer_email"]:
                data["customer_email"] = txt

        # Organization → shop or brand
        if label == "ORG":
            if not data["shop_name"]:
                data["shop_name"] = txt
            elif not data["product_brand"]:
                data["product_brand"] = txt

        # Product name
        if label == "PRODUCT" and not data["product_name"]:
            data["product_name"] = txt

        # Address items
        if label in ["GPE", "LOC"]:
            if not data["customer_address"]:
                data["customer_address"] = txt

        # Dates
        if label == "DATE":
            if not data["purchase_date"]:
                data["purchase_date"] = txt
            elif not data["selling_date"]:
                data["selling_date"] = txt

            # Heuristic for DOB (still no regex)
            if "birth" in text.lower() or "dob" in text.lower():
                data["customer_date_of_birth"] = txt

        # Money
        if label == "MONEY":
            if not data["purchase_price"]:
                data["purchase_price"] = txt
            elif not data["selling_price"]:
                data["selling_price"] = txt
            elif not data["expenditure"]:
                data["expenditure"] = txt

        # Numbers (invoice/phone/code)
        if label == "CARDINAL":
            if not data["invoice_number"]:
                data["invoice_number"] = txt
            elif not data["owner_phone"]:
                data["owner_phone"] = txt
                data["customer_phone"] = txt
            elif not data["offer_code"]:
                data["offer_code"] = txt

        # Quantity → warranty (e.g. “12 months”)
        if label == "QUANTITY":
            if not data["warranty_period"]:
                data["warranty_period"] = txt
            elif not data["purchase_amount"]:
                data["purchase_amount"] = txt

    return {k: clean(v) for k, v in data.items()}
