import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    output_df = pd.DataFrame(columns=["anon_id", "matched_name"])
    for _, anon_row in anon_df.iterrows():
        count_match = 0
        chosen_row = anon_row
        for _, aux_row in aux_df.iterrows():
            if anon_row["age"] == aux_row["age"] and anon_row["zip3"] == aux_row["zip3"] and anon_row["gender"] == aux_row["gender"]:
                chosen_row = aux_row
                count_match += 1
            if count_match > 1: break
        if count_match == 1:
            name = chosen_row["name"]
            id = anon_row["anon_id"]
            output_df.loc[len(output_df)] = [id, name]
    return output_df
    # raise NotImplementedError


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    sum = 0
    total = len(anon_df)
    for _, anon_row in anon_df.iterrows():
        for _, match_row in matches_df.iterrows():
            if match_row["anon_id"] == anon_row["anon_id"]:
                sum += 1
    fraction = sum / total
    return fraction
    # raise NotImplementedError
