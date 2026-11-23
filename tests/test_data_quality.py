
import pandas as pd


def test_no_duplicate_records():
    """Check that duplicate records are detected."""

    df = pd.DataFrame({
        "customer_id": ["C001", "C002", "C003"]
    })

    assert df["customer_id"].is_unique


def test_missing_values_detection():
    """Check that missing values are detected."""

    df = pd.DataFrame({
        "customer_id": ["C001", None, "C003"]
    })

    assert df["customer_id"].isnull().sum() == 1


def test_valid_review_scores():
    """Check that review scores are within 1 to 5."""

    df = pd.DataFrame({
        "review_score": [1, 2, 3, 4, 5]
    })

    assert df["review_score"].between(1, 5).all()


def test_no_negative_prices():
    """Check that product prices are non-negative."""

    df = pd.DataFrame({
        "price": [100.0, 250.0, 500.0]
    })

    assert (df["price"] >= 0).all()


def test_valid_payment_values():
    """Check that payment values are non-negative."""

    df = pd.DataFrame({
        "payment_value": [100.0, 250.0, 500.0]
    })

    assert (df["payment_value"] >= 0).all()





import pandas as pd
import pytest

from ingestion.clean_customers import clean_customers


def sample_customers():
    """Create sample customer data for testing."""

    return pd.DataFrame({
        "customer_id": ["C001", "C002", "C003"],
        "customer_unique_id": ["U001", "U002", "U003"],
        "customer_zip_code_prefix": ["12345", "54321", "67890"],
        "customer_city": ["city_a", "city_b", "city_c"],
        "customer_state": ["sp", "rj", "mg"]
    })


def test_customer_text_cleaning():
    df = sample_customers()

    df.loc[0, "customer_city"] = "  sao paulo  "
    df.loc[0, "customer_state"] = " sp "

    result = clean_customers(df)

    assert result.loc[0, "customer_city"] == "sao paulo"
    assert result.loc[0, "customer_state"] == "SP"


def test_customer_ids_are_unique():
    df = sample_customers()

    df.loc[1, "customer_id"] = "C001"

    with pytest.raises(ValueError, match="Duplicate customer IDs"):
        clean_customers(df)


def test_missing_customer_id_is_rejected():
    df = sample_customers()

    df.loc[0, "customer_id"] = None

    with pytest.raises(ValueError, match="customer_id contains missing"):
        clean_customers(df)


def test_invalid_zip_code_is_rejected():
    df = sample_customers()

    df.loc[0, "customer_zip_code_prefix"] = "12AB5"

    with pytest.raises(ValueError, match="Invalid customer ZIP"):
        clean_customers(df)


def test_inconsistent_customer_location_is_flagged():
    df = pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "customer_unique_id": ["U001", "U001"],
        "customer_zip_code_prefix": ["12345", "54321"],
        "customer_city": ["city_a", "city_b"],
        "customer_state": ["sp", "sp"]
    })

    result = clean_customers(df)

    assert result["inconsistent_location_flag"].all()


def test_customer_rows_are_preserved():
    df = sample_customers()

    result = clean_customers(df)

    assert len(result) == len(df)



from ingestion.clean_products import clean_products


def sample_products():
    return pd.DataFrame({
        "product_id": ["P001", "P002", "P003"],
        "product_category_name": [
            "electronics",
            None,
            "furniture"
        ],
        "product_weight_g": [500, None, 1200]
    })


def test_missing_product_category_replaced():
    df = sample_products()

    result = clean_products(df)

    assert result.loc[1, "product_category_name"] == "unknown"


def test_product_categories_have_no_missing_values():
    df = sample_products()

    result = clean_products(df)

    assert result["product_category_name"].notna().all()


def test_other_missing_values_are_preserved():
    df = sample_products()

    result = clean_products(df)

    assert pd.isna(result.loc[1, "product_weight_g"])


def test_product_rows_are_preserved():
    df = sample_products()

    result = clean_products(df)

    assert len(result) == len(df)


def test_original_dataframe_is_not_modified():
    df = sample_products()
    original_df = df.copy(deep=True)

    clean_products(df)

    pd.testing.assert_frame_equal(df, original_df)


from ingestion.clean_orders import clean_orders


def sample_orders():
    return pd.DataFrame({
        "order_id": ["O001", "O002", "O003"],
        "order_status": ["delivered", "delivered", "shipped"],
        "order_purchase_timestamp": [
            "2018-01-01 10:00:00",
            "2018-01-02 11:00:00",
            "2018-01-03 12:00:00"
        ],
        "order_approved_at": [
            "2018-01-01 10:30:00",
            None,
            "2018-01-03 12:30:00"
        ],
        "order_delivered_carrier_date": [
            "2018-01-02 10:00:00",
            None,
            None
        ],
        "order_delivered_customer_date": [
            "2018-01-05 10:00:00",
            None,
            None
        ],
        "order_estimated_delivery_date": [
            "2018-01-06 10:00:00",
            "2018-01-07 10:00:00",
            "2018-01-08 10:00:00"
        ]
    })


def test_order_timestamps_are_datetime():
    result = clean_orders(sample_orders())

    assert pd.api.types.is_datetime64_any_dtype(
        result["order_purchase_timestamp"]
    )


def test_delivered_order_missing_delivery_date_is_flagged():
    result = clean_orders(sample_orders())

    assert result.loc[1, "delivered_missing_delivery_date"] == True


def test_delivered_order_with_delivery_date_is_not_flagged():
    result = clean_orders(sample_orders())

    assert result.loc[0, "delivered_missing_delivery_date"] == False


def test_non_delivered_order_is_not_flagged():
    result = clean_orders(sample_orders())

    assert result.loc[2, "delivered_missing_delivery_date"] == False


def test_missing_timestamps_are_preserved():
    result = clean_orders(sample_orders())

    assert pd.isna(result.loc[1, "order_approved_at"])
    assert pd.isna(result.loc[1, "order_delivered_customer_date"])


def test_order_rows_are_preserved():
    df = sample_orders()

    result = clean_orders(df)

    assert len(result) == len(df)


def test_invalid_timestamp_is_rejected():
    df = sample_orders()
    df.loc[0, "order_purchase_timestamp"] = "invalid-date"

    with pytest.raises(ValueError):
        clean_orders(df)



from ingestion.clean_order_items import clean_order_items


def sample_order_items():
    return pd.DataFrame({
        "order_id": ["O001", "O001", "O002"],
        "order_item_id": [1, 2, 1],
        "product_id": ["P001", "P002", "P003"],
        "shipping_limit_date": [
            "2018-01-05 10:00:00",
            "2018-01-06 11:00:00",
            "2018-01-07 12:00:00"
        ],
        "price": [100.0, 200.0, 150.0],
        "freight_value": [10.0, 20.0, 15.0]
    })


def test_shipping_date_converted_to_datetime():
    result = clean_order_items(sample_order_items())

    assert pd.api.types.is_datetime64_any_dtype(
        result["shipping_limit_date"]
    )


def test_duplicate_order_items_are_rejected():
    df = sample_order_items()
    df.loc[1, "order_item_id"] = 1

    with pytest.raises(ValueError, match="Duplicate order-item"):
        clean_order_items(df)


def test_negative_prices_are_rejected():
    df = sample_order_items()
    df.loc[0, "price"] = -100

    with pytest.raises(ValueError, match="Negative product prices"):
        clean_order_items(df)


def test_negative_freight_values_are_rejected():
    df = sample_order_items()
    df.loc[0, "freight_value"] = -10

    with pytest.raises(ValueError, match="Negative freight"):
        clean_order_items(df)


def test_zero_price_and_freight_are_allowed():
    df = sample_order_items()
    df.loc[0, ["price", "freight_value"]] = [0, 0]

    result = clean_order_items(df)

    assert result.loc[0, "price"] == 0
    assert result.loc[0, "freight_value"] == 0


def test_order_item_rows_are_preserved():
    df = sample_order_items()

    result = clean_order_items(df)

    assert len(result) == len(df)


def test_original_order_items_dataframe_is_not_modified():
    df = sample_order_items()
    original_df = df.copy(deep=True)

    clean_order_items(df)

    pd.testing.assert_frame_equal(df, original_df)



from ingestion.clean_payments import clean_payments


def sample_payments():
    return pd.DataFrame({
        "order_id": ["O001", "O001", "O002"],
        "payment_sequential": [1, 2, 1],
        "payment_type": ["credit_card", "voucher", "boleto"],
        "payment_installments": [2, 0, 1],
        "payment_value": [100.0, 50.0, 200.0]
    })


def test_payment_data_types_are_converted():
    df = sample_payments()

    df["payment_sequential"] = df["payment_sequential"].astype(str)
    df["payment_installments"] = df["payment_installments"].astype(str)
    df["payment_value"] = df["payment_value"].astype(str)

    result = clean_payments(df)

    assert result["payment_sequential"].dtype == "int64"
    assert result["payment_installments"].dtype == "int64"
    assert pd.api.types.is_numeric_dtype(result["payment_value"])


def test_zero_installments_are_flagged():
    result = clean_payments(sample_payments())

    assert result.loc[1, "zero_installments_flag"] == True
    assert result.loc[0, "zero_installments_flag"] == False


def test_duplicate_payment_combinations_are_rejected():
    df = sample_payments()
    df.loc[1, "payment_sequential"] = 1

    with pytest.raises(ValueError, match="Duplicate payment combinations"):
        clean_payments(df)


def test_negative_payment_values_are_rejected():
    df = sample_payments()
    df.loc[0, "payment_value"] = -100

    with pytest.raises(ValueError, match="Negative payment values"):
        clean_payments(df)


def test_missing_order_ids_are_rejected():
    df = sample_payments()
    df.loc[0, "order_id"] = None

    with pytest.raises(ValueError, match="Missing order IDs"):
        clean_payments(df)


def test_missing_payment_values_are_rejected():
    df = sample_payments()
    df.loc[0, "payment_value"] = None

    with pytest.raises(ValueError, match="Missing payment values"):
        clean_payments(df)


def test_zero_payment_values_are_allowed():
    df = sample_payments()
    df.loc[0, "payment_value"] = 0

    result = clean_payments(df)

    assert result.loc[0, "payment_value"] == 0


def test_zero_installments_with_zero_payment_are_flagged():
    df = sample_payments()
    df.loc[1, "payment_value"] = 0

    result = clean_payments(df)

    assert result.loc[1, "zero_installments_flag"] == True


def test_payment_rows_are_preserved():
    df = sample_payments()

    result = clean_payments(df)

    assert len(result) == len(df)


def test_original_payment_dataframe_is_not_modified():
    df = sample_payments()
    original_df = df.copy(deep=True)

    clean_payments(df)

    pd.testing.assert_frame_equal(df, original_df)



from ingestion.clean_reviews import clean_reviews


def sample_reviews():
    return pd.DataFrame({
        "review_id": ["R001", "R002", "R003"],
        "order_id": ["O001", "O002", "O003"],
        "review_score": [5, 3, 1],
        "review_comment_title": ["Good", None, "Bad"],
        "review_comment_message": ["Excellent", None, "Poor"],
        "review_creation_date": [
            "2018-01-01 10:00:00",
            "2018-01-02 11:00:00",
            "2018-01-03 12:00:00"
        ],
        "review_answer_timestamp": [
            "2018-01-02 10:00:00",
            "2018-01-03 11:00:00",
            "2018-01-04 12:00:00"
        ]
    })


def test_review_score_is_integer():
    df = sample_reviews()
    df["review_score"] = df["review_score"].astype(str)

    result = clean_reviews(df)

    assert result["review_score"].dtype == "int64"


def test_review_scores_must_be_between_one_and_five():
    df = sample_reviews()
    df.loc[0, "review_score"] = 6

    with pytest.raises(ValueError, match="Review scores"):
        clean_reviews(df)


def test_review_timestamps_are_datetime():
    result = clean_reviews(sample_reviews())

    assert pd.api.types.is_datetime64_any_dtype(
        result["review_creation_date"]
    )
    assert pd.api.types.is_datetime64_any_dtype(
        result["review_answer_timestamp"]
    )


def test_duplicate_review_ids_are_flagged():
    df = sample_reviews()
    df.loc[1, "review_id"] = "R001"

    result = clean_reviews(df)

    assert result.loc[0, "duplicate_review_id_flag"]
    assert result.loc[1, "duplicate_review_id_flag"]
    assert not result.loc[2, "duplicate_review_id_flag"]


def test_duplicate_review_records_are_preserved():
    df = sample_reviews()
    df.loc[1, "review_id"] = "R001"

    result = clean_reviews(df)

    assert len(result) == len(df)


def test_missing_review_comments_are_preserved():
    df = sample_reviews()

    result = clean_reviews(df)

    assert pd.isna(result.loc[1, "review_comment_title"])
    assert pd.isna(result.loc[1, "review_comment_message"])


def test_missing_review_ids_are_rejected():
    df = sample_reviews()
    df.loc[0, "review_id"] = None

    with pytest.raises(ValueError, match="Missing review IDs"):
        clean_reviews(df)


def test_missing_order_ids_are_rejected():
    df = sample_reviews()
    df.loc[0, "order_id"] = None

    with pytest.raises(ValueError, match="Missing order IDs"):
        clean_reviews(df)


def test_missing_review_timestamps_are_rejected():
    df = sample_reviews()
    df.loc[0, "review_creation_date"] = None

    with pytest.raises(ValueError, match="Missing review creation dates"):
        clean_reviews(df)


def test_original_reviews_dataframe_is_not_modified():
    df = sample_reviews()
    original_df = df.copy(deep=True)

    clean_reviews(df)

    pd.testing.assert_frame_equal(df, original_df)



from ingestion.clean_sellers import clean_sellers


def sample_sellers():
    return pd.DataFrame({
        "seller_id": ["S001", "S002", "S003"],
        "seller_zip_code_prefix": ["13000", "20000", "30000"],
        "seller_city": [" sao paulo ", "rio de janeiro ", " curitiba"],
        "seller_state": ["sp", "rj", "pr"]
    })


def test_seller_text_is_cleaned():
    result = clean_sellers(sample_sellers())

    assert result.loc[0, "seller_city"] == "sao paulo"
    assert result.loc[1, "seller_city"] == "rio de janeiro"
    assert result.loc[0, "seller_state"] == "SP"


def test_seller_ids_must_be_unique():
    df = sample_sellers()
    df.loc[1, "seller_id"] = "S001"

    with pytest.raises(ValueError, match="Duplicate seller IDs"):
        clean_sellers(df)


def test_missing_seller_id_is_rejected():
    df = sample_sellers()
    df.loc[0, "seller_id"] = None

    with pytest.raises(ValueError, match="seller_id"):
        clean_sellers(df)


def test_missing_seller_zip_is_rejected():
    df = sample_sellers()
    df.loc[0, "seller_zip_code_prefix"] = None

    with pytest.raises(ValueError, match="seller_zip_code_prefix"):
        clean_sellers(df)


def test_invalid_seller_zip_is_rejected():
    df = sample_sellers()
    df.loc[0, "seller_zip_code_prefix"] = "13AB"

    with pytest.raises(ValueError, match="Invalid seller ZIP"):
        clean_sellers(df)


def test_seller_rows_are_preserved():
    df = sample_sellers()

    result = clean_sellers(df)

    assert len(result) == len(df)


def test_original_seller_dataframe_is_not_modified():
    df = sample_sellers()
    original_df = df.copy(deep=True)

    clean_sellers(df)

    pd.testing.assert_frame_equal(df, original_df)



from ingestion.clean_geolocation import clean_geolocation


def sample_geolocation():
    return pd.DataFrame({
        "geolocation_zip_code_prefix": [1000, 1000, 2000, 3000],
        "geolocation_lat": [-23.5, -23.6, -22.9, -19.9],
        "geolocation_lng": [-46.6, -46.7, -43.2, -43.9],
        "geolocation_city": ["city_a", "city_a", "city_b", "city_c"],
        "geolocation_state": ["SP", "SP", "RJ", "MG"]
    })


def test_exact_duplicate_geolocation_rows_are_removed():
    df = sample_geolocation()
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    result = clean_geolocation(df)

    assert len(result) == 4
    assert result.duplicated().sum() == 0


def test_different_coordinates_for_same_zip_are_preserved():
    df = sample_geolocation()

    result = clean_geolocation(df)

    same_zip = result[
        result["geolocation_zip_code_prefix"] == 1000
    ]

    assert len(same_zip) == 2
    assert same_zip["geolocation_lat"].nunique() == 2


def test_geolocation_rows_without_duplicates_are_preserved():
    df = sample_geolocation()

    result = clean_geolocation(df)

    assert len(result) == len(df)


def test_geolocation_input_dataframe_is_not_modified():
    df = sample_geolocation()
    original_df = df.copy(deep=True)

    clean_geolocation(df)

    pd.testing.assert_frame_equal(df, original_df)



from ingestion.clean_category_translation import clean_category_translation


def sample_category_translation():
    return pd.DataFrame({
        "product_category_name": [
            " beleza_saude ",
            "esporte_lazer",
            "informatica_acessorios"
        ],
        "product_category_name_english": [
            " health_beauty ",
            "sports_leisure",
            "computers_accessories"
        ]
    })


def test_category_names_are_trimmed():
    result = clean_category_translation(
        sample_category_translation()
    )

    assert result.loc[0, "product_category_name"] == "beleza_saude"
    assert result.loc[0, "product_category_name_english"] == "health_beauty"


def test_missing_portuguese_category_is_rejected():
    df = sample_category_translation()
    df.loc[0, "product_category_name"] = None

    with pytest.raises(ValueError, match="product_category_name"):
        clean_category_translation(df)


def test_missing_english_category_is_rejected():
    df = sample_category_translation()
    df.loc[0, "product_category_name_english"] = None

    with pytest.raises(ValueError, match="product_category_name_english"):
        clean_category_translation(df)


def test_duplicate_portuguese_categories_are_rejected():
    df = sample_category_translation()
    df.loc[1, "product_category_name"] = df.loc[0, "product_category_name"]

    with pytest.raises(ValueError, match="Duplicate Portuguese"):
        clean_category_translation(df)


def test_duplicate_english_categories_are_rejected():
    df = sample_category_translation()
    df.loc[1, "product_category_name_english"] = (
        df.loc[0, "product_category_name_english"]
    )

    with pytest.raises(ValueError, match="Duplicate English"):
        clean_category_translation(df)


def test_category_translation_rows_are_preserved():
    df = sample_category_translation()

    result = clean_category_translation(df)

    assert len(result) == len(df)


def test_original_category_dataframe_is_not_modified():
    df = sample_category_translation()
    original_df = df.copy(deep=True)

    clean_category_translation(df)

    pd.testing.assert_frame_equal(df, original_df)
