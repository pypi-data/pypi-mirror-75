from copy import deepcopy
from typing import Optional, Any, List, cast

import pandas as pd

from cryptocompsdk.response import ResponseException, ResponseAPIBase
from cryptocompsdk.general.parse import from_int, from_none, from_union, from_float, from_str, to_float, from_bool, \
    from_dict, to_class, is_type, from_int_or_str, from_na, from_str_number, from_list, from_stringified_bool, \
    from_plain_dict


class SourceInfo:
    name: Optional[str]
    lang: Optional[str]
    img: Optional[str]

    def __init__(self, name: Optional[str], lang: Optional[str], img: Optional[str]) -> None:
        self.name = name
        self.lang = lang
        self.img = img

    @staticmethod
    def from_dict(obj: Any) -> 'SourceInfo':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        lang = from_union([from_str, from_none], obj.get("lang"))
        img = from_union([from_str, from_none], obj.get("img"))
        return SourceInfo(name, lang, img)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["lang"] = from_union([from_str, from_none], self.lang)
        result["img"] = from_union([from_str, from_none], self.img)
        return result


class NewsRecord:
    id: Optional[int]
    guid: Optional[str]
    published_on: Optional[int]
    imageurl: Optional[str]
    title: Optional[str]
    url: Optional[str]
    source: Optional[str]
    body: Optional[str]
    tags: Optional[str]
    categories: Optional[str]
    upvotes: Optional[int]
    downvotes: Optional[int]
    lang: Optional[str]
    source_info: Optional[SourceInfo]

    def __init__(self, id: Optional[int], guid: Optional[str], published_on: Optional[int], imageurl: Optional[str], title: Optional[str], url: Optional[str], source: Optional[str], body: Optional[str], tags: Optional[str], categories: Optional[str], upvotes: Optional[int], downvotes: Optional[int], lang: Optional[str], source_info: Optional[SourceInfo]) -> None:
        self.id = id
        self.guid = guid
        self.published_on = published_on
        self.imageurl = imageurl
        self.title = title
        self.url = url
        self.source = source
        self.body = body
        self.tags = tags
        self.categories = categories
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.lang = lang
        self.source_info = source_info

    @staticmethod
    def from_dict(obj: Any) -> 'NewsRecord':
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        guid = from_union([from_str, from_none], obj.get("guid"))
        published_on = from_union([from_int, from_none], obj.get("published_on"))
        imageurl = from_union([from_str, from_none], obj.get("imageurl"))
        title = from_union([from_str, from_none], obj.get("title"))
        url = from_union([from_str, from_none], obj.get("url"))
        source = from_union([from_str, from_none], obj.get("source"))
        body = from_union([from_str, from_none], obj.get("body"))
        tags = from_union([from_str, from_none], obj.get("tags"))
        categories = from_union([from_str, from_none], obj.get("categories"))
        upvotes = from_union([from_none, lambda x: int(from_str(x))], obj.get("upvotes"))
        downvotes = from_union([from_none, lambda x: int(from_str(x))], obj.get("downvotes"))
        lang = from_union([from_str, from_none], obj.get("lang"))
        source_info = from_union([SourceInfo.from_dict, from_none], obj.get("source_info"))
        return NewsRecord(id, guid, published_on, imageurl, title, url, source, body, tags, categories, upvotes, downvotes, lang, source_info)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.id)
        result["guid"] = from_union([from_str, from_none], self.guid)
        result["published_on"] = from_union([from_int, from_none], self.published_on)
        result["imageurl"] = from_union([from_str, from_none], self.imageurl)
        result["title"] = from_union([from_str, from_none], self.title)
        result["url"] = from_union([from_str, from_none], self.url)
        result["source"] = from_union([from_str, from_none], self.source)
        result["body"] = from_union([from_str, from_none], self.body)
        result["tags"] = from_union([from_str, from_none], self.tags)
        result["categories"] = from_union([from_str, from_none], self.categories)
        result["upvotes"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.upvotes)
        result["downvotes"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.downvotes)
        result["lang"] = from_union([from_str, from_none], self.lang)
        result["source_info"] = from_union([lambda x: to_class(SourceInfo, x), from_none], self.source_info)
        return result

    @property
    def is_empty(self) -> bool:
        is_empty_cols = [
            'id',
            'guid',
            'published_on',
            'imageurl',
            'title',
            'url',
            'source',
            'body',
            'tags',
            'categories',
            'upvotes',
            'downvotes',
            'lang',
            'source_info',
        ]

        for col in is_empty_cols:
            if getattr(self, col) != 0:
                return False
        return True


class RateLimit:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'RateLimit':
        assert isinstance(obj, dict)
        return RateLimit()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class NewsData(ResponseAPIBase):
    type: Optional[int]
    message: Optional[str]
    promoted: Optional[List[Any]]
    data: Optional[List[NewsRecord]]
    rate_limit: Optional[RateLimit]
    has_warning: Optional[bool]

    def __init__(self, type: Optional[int], message: Optional[str], promoted: Optional[List[Any]], data: Optional[List[NewsRecord]], rate_limit: Optional[RateLimit], has_warning: Optional[bool]) -> None:
        self.type = type
        self.message = message
        self.promoted = promoted
        self.data = data
        self.rate_limit = rate_limit
        self.has_warning = has_warning

    @staticmethod
    def from_dict(obj: Any) -> 'NewsData':
        assert isinstance(obj, dict)
        type = from_union([from_int, from_none], obj.get("Type"))
        message = from_union([from_str, from_none], obj.get("Message"))
        promoted = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("Promoted"))
        data = from_union([lambda x: from_list(NewsRecord.from_dict, x), from_none], obj.get("Data"))
        rate_limit = from_union([RateLimit.from_dict, from_none], obj.get("RateLimit"))
        has_warning = from_union([from_bool, from_none], obj.get("HasWarning"))
        return NewsData(type, message, promoted, data, rate_limit, has_warning)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Type"] = from_union([from_int, from_none], self.type)
        result["Message"] = from_union([from_str, from_none], self.message)
        result["Promoted"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.promoted)
        result["Data"] = from_union([lambda x: from_list(lambda x: to_class(NewsRecord, x), x), from_none], self.data)
        result["RateLimit"] = from_union([lambda x: to_class(RateLimit, x), from_none], self.rate_limit)
        result["HasWarning"] = from_union([from_bool, from_none], self.has_warning)
        return result

    def to_df(self) -> pd.DataFrame:
        if not self.data:
            return pd.DataFrame()
        df = pd.DataFrame(self.to_dict()['Data'])
        df['published_on'] = df['published_on'].apply(pd.Timestamp.fromtimestamp)

        all_sources = []
        for record in self.data:
            si = record.source_info
            if si is not None:
                source_series = pd.Series(si.to_dict())
                all_sources.append(source_series)
        source_df = pd.concat(all_sources, axis=1).T
        df.drop('source_info', axis=1, inplace=True)
        new_cols = [col for col in source_df.columns if col not in df.columns]

        df = pd.concat([df, source_df[new_cols]], axis=1)

        return df

    @property
    def has_error(self) -> bool:
        # No response object in this API
        return self.message != 'News list successfully returned'

    # Pagination methods

    @property
    def is_empty(self) -> bool:
        if self.data is None:
            return True

        for record in self.data:
            if not record.is_empty:
                return False

        return True

    def __add__(self, other):
        out_obj = deepcopy(self)
        out_obj.data += other.data
        return out_obj

    def __radd__(self, other):
        out_obj = deepcopy(other)
        out_obj.data += self.data
        return out_obj

    @property
    def time_from(self) -> int:
        if self.data is None:
            raise ValueError('cannot determine time from as there is no data')

        times = [record.published_on for record in self.data]
        if not times:
            raise ValueError('could not calculate time from as there is no data')
        min_times = min(times)
        min_times = cast(int, min_times)  # for mypy
        return min_times

    def delete_record_matching_time(self, time: int):
        # not a problem with this API, no overlapping time
        pass

    def trim_empty_records_at_beginning(self):
        # Earliest records are at the end of data

        # Delete, starting from end, oldest record
        for i, record in reversed(list(enumerate(self.data))):
            if record.is_empty:
                del self.data[i]
            else:
                # First non-empty record from end, we have now hit the actual data section, stop deleting
                break


def news_from_dict(s: Any) -> NewsData:
    return NewsData.from_dict(s)


def news_to_dict(x: NewsData) -> Any:
    return to_class(NewsData, x)


class CouldNotGetNewsException(ResponseException):
    pass
