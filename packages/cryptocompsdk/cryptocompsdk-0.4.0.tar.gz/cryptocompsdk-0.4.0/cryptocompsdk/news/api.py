from typing import Optional, Sequence, Union, Dict

from cryptocompsdk.request import APIBase
from cryptocompsdk.news.parse import CouldNotGetNewsException, news_from_dict, NewsData
from cryptocompsdk.urls import NEWS_URL


class NewsAPI(APIBase):
    _exception_class = CouldNotGetNewsException

    def get(self, feeds: Optional[Sequence[str]] = None, categories: Optional[Sequence[str]] = None,
            exclude_categories: Optional[Sequence[str]] = None, lang: str = 'EN', sort_order: str = 'latest',
            end_time: Optional[int] = None, requests_limit: int = 1) -> NewsData:
        payload: Dict[str, Optional[Union[Sequence[str], str, int]]] = dict(
            feeds=feeds,
            categories=categories,
            excludeCategories=exclude_categories,
            lTs=end_time,
            lang=lang,
            sortOrder=sort_order,
        )

        if requests_limit == 1:
            return self._get(NEWS_URL, payload)

        return self._get_with_pagination(
            NEWS_URL, payload, max_api_calls=requests_limit, limit_in_payload=False, date_name='lTs'
        )

    def _class_factory(self, data: dict) -> NewsData:
        return news_from_dict(data)
