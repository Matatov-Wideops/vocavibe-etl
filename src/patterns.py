import re
from enum import Enum
from src.database import Language, AllRecordType, Timing, OnMed, FeelOnOff

# from database import Database

from enum import Enum
import re

# Assuming these are defined elsewhere
# from your_module import Language, AllRecordType, Timing, OnMed, FeelOnOff

# Generate the regex patterns outside the class
languages_regex = "|".join(map(re.escape, Language.values()))
exercises_regex = "|".join(map(re.escape, AllRecordType.values()))
timing_regex = "|".join(map(re.escape, Timing.values()))
onmed_regex = "|".join(map(re.escape, OnMed.values()))
onoff_regex = "|".join(map(re.escape, FeelOnOff.values()))

class Patterns(str, Enum):

    # _ignore_ = ['_date', '_time', '_datetime', '_username', '_language', '_exercise', '_timing', '_onmed', '_onoff']

    _date = r"\d{4}-\d{2}-\d{2}"
    _time = r"\d{2}:\d{2}:\d{2}"
    _datetime = rf"{_date}_{_time}"
    _username = r"^((?:s_|hc_)?[^_]+)"
    _language = rf"_({languages_regex})"
    _exercise = rf"_({exercises_regex})"
    _timing = rf"_({timing_regex})"
    _onmed = rf"_({onmed_regex})"
    _onoff = rf"_({onoff_regex})"

    # Final patterns (enum members)
    REGISTRATION0 = rf"^user\.csv$"
    REGISTRATION = rf"^user_register_{_date}_{_time}\.csv$"
    UPDATE = rf"^user_{_date}_{_time}\.csv$"
    RECORDING = rf"{_username}{_language}_{_date}_{_time}{_timing}{_exercise}{_onmed}{_onoff}$"
    RECORDING1 = rf"{_username}{_language}_{_date}_{_time}{_timing}{_exercise}_(on|off)$"
    MEDICATIONS = rf"{_username}{_language}_{_date}_{_time}_medications\.csv$"
    UPDRS = rf"{_username}{_language}{_timing}_{_date}_{_time}_updrs\.csv$"
    UPDRS3 = rf"{_username}{_language}{_timing}_{_date}_{_time}_updrs3\.csv$"
    UPDRS124 = rf"{_username}{_language}{_timing}_{_date}_{_time}_updrs124\.csv$"
    MOCA = rf"{_username}{_language}{_timing}_{_date}_{_time}_moca\.csv$"
    PDQ8 = rf"{_username}{_language}{_timing}_{_date}_{_time}_pdq8\.csv$"
    FOG = rf"{_username}{_language}{_timing}_{_date}_{_time}_fog_off\.csv$"
    SDQ = rf"{_username}{_language}{_timing}_{_date}_{_time}_sdq_off\.csv$"
    WOQ = rf"{_username}{_language}{_timing}_{_date}_{_time}_woq_off\.csv$"
    APKINSOPN = rf"^feedback\.csv$"


    @classmethod
    def values(cls):
        return [
            cls.REGISTRATION,
            cls.REGISTRATION0,
            cls.UPDATE,
            cls.RECORDING,
            cls.RECORDING1,
            cls.MEDICATIONS,
            cls.UPDRS,
            cls.UPDRS3,
            cls.UPDRS124,
            cls.MOCA,
            cls.PDQ8,
            cls.FOG,
            cls.SDQ,
            cls.WOQ,
            cls.APKINSOPN
        ]




def get_pattern(key):
    patterns = {
        'date': Patterns._date,
        'time': Patterns._time,
        'datetime': Patterns._datetime,
        'username': Patterns._username,
        'language': Patterns._language,
        'exercise': Patterns._exercise,
        'timing': Patterns._timing,
        'onmed': Patterns._onmed,
        'onoff': Patterns._onoff,
    }
    return patterns.get(key, [])



def extract_from_filename(filename, key):
    pattern = get_pattern(key)
    remove_underscore_keys = ['language', 'exercise', 'timing', 'onmed', 'onoff']
    match = re.search(pattern, filename)
    if match:
        return match.group(1) if key in remove_underscore_keys else match.group()
    return None


    