from typing import Optional


def prepare_imdb_model_data(res: dict[str, str], mapping={"title": "title", "description": "description",
                                                          "rate": "rating", "imdb_id": "imdb_id",
                                                          "main_poster": "poster_url"}) -> Optional[dict[str, str]]:
    """
    [Summery]
    prepare essential data to save on db
    :param res:
    :param mapping:
    :return:
    """
    return {_key: res[_value] for _key, _value in mapping.items()}
