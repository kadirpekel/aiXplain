from enum import Enum
from aixplain.client import enums

Function = enums.populate_function_enum()
License = enums.populate_license_enum()
Language = enums.populate_language_enum()


class DataSplit(Enum):
    TRAIN = "train"
    VALIDATION = "validation"
    TEST = "test"


class DataSubtype(Enum):
    AGE = "age"
    GENDER = "gender"
    INTERVAL = "interval"
    OTHER = "other"
    RACE = "race"
    SPLIT = "split"
    TOPIC = "topic"


class DataType(Enum):
    AUDIO = "audio"
    FLOAT = "float"
    IMAGE = "image"
    INTEGER = "integer"
    LABEL = "label"
    TENSOR = "tensor"
    TEXT = "text"
    VIDEO = "video"


class ErrorHandler(Enum):
    SKIP = "skip"
    FAIL = "fail"


class FileType(Enum):
    CSV = ".csv"
    JSON = ".json"
    TXT = ".txt"
    XML = ".xml"
    FLAC = ".flac"
    MP3 = ".mp3"
    WAV = ".wav"
    JPEG = ".jpeg"
    PNG = ".png"
    JPG = ".jpg"
    GIF = ".gif"
    WEBP = ".webp"
    AVI = ".avi"
    MP4 = ".mp4"
    MOV = ".mov"
    MPEG4 = ".mpeg4"


class OnboardStatus(Enum):
    ONBOARDING = "onboarding"
    ONBOARDED = "onboarded"
    FAILED = "failed"
    DELETED = "deleted"


class Privacy (Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"
    RESTRICTED = "Restricted"


class StorageType(Enum):
    TEXT = "text"
    URL = "url"
    FILE = "file"
