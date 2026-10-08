import json
import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials


load_dotenv()


def get_required_env(name):
    value = os.getenv(name)

    if not value:
        raise ValueError(f"{name} is not set in .env")

    return value


GOOGLE_CREDENTIALS_FILE = get_required_env("GOOGLE_CREDENTIALS_FILE")
GOOGLE_SHEET_ID = get_required_env("GOOGLE_SHEET_ID")
WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME", "Amazon Products")


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


def get_google_sheet():
    credentials = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE,
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

    try:
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=WORKSHEET_NAME,
            rows=1000,
            cols=10
        )

        setup_headers(worksheet)

    return worksheet


def setup_headers(worksheet):
    headers = [
        "title",
        "price",
        "rating",
        "review_count",
        "asin",
        "overview_specs",
        "about",
        "detailed_info",
        "images",
        "link",
    ]

    worksheet.update(
        range_name="A1:J1",
        values=[headers]
    )


def save_product(worksheet, product):
    asin = product.get("asin")

    if not asin:
        raise ValueError("Product does not have an ASIN")

    row = [
        product.get("title"),
        product.get("price"),
        product.get("rating"),
        product.get("review_count"),
        asin,

        json.dumps(
            product.get("overview_specs", {}),
            ensure_ascii=False
        ),

        json.dumps(
            product.get("about", []),
            ensure_ascii=False
        ),

        json.dumps(
            product.get("detailed_info", {}),
            ensure_ascii=False
        ),

        json.dumps(
            product.get("images", []),
            ensure_ascii=False
        ),

        product.get("link"),
    ]

    asin_column = worksheet.col_values(5)

    asin_column = [
        value.strip()
        for value in asin_column
    ]

    if str(asin).strip() in asin_column:
        row_number = asin_column.index(str(asin).strip()) + 1

        worksheet.update(
            range_name=f"A{row_number}:J{row_number}",
            values=[row]
        )

    else:
        worksheet.append_row(
            row,
            value_input_option="USER_ENTERED"
        )