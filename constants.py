"""
Web part
"""
ACCESS_DENIED_STR: str = "Access Denied"
ACCESS_QUERYSTRING_PARAM = "access_token"
CORS_ALL_WILDCARD: str = "*"
CORS_ALLOWED_HTTP_METHODS: str = "GET, POST, PUT, OPTIONS"
CORS_ALLOWED_HTTP_HEADERS: str = (
    "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"
)
JSON_CONTENT_TYPE: str = "application/json"

"""
Parser HC part
"""
DOT: str = "."
RIGHT_QUOTE_MARKER: str = "»"
SPACE: str = " "
COMMA: str = ","
VACANCY_URL_STARTS: str = "https://career.habr.com/vacancies/"
FULLTIME_MARKER: str = "Полный рабочий день."
REMOTE_MARKER: str = "Можно удалённо."
SKILLS_MARKER: str = "Требуемые навыки:"
WANTS_PREFIX: str = "Требуется «"
HAS_TOWN_SALARY_MARKER: str = "» ("

SALARY_START_MARKER: str = "от "
SALARY_END_MARKER: str = " до "
SALARY_IN_TEXT_MARKER: str = ". От"

CURRENCY_RUB_MARKER: str = "₽"
CURRENCY_EURO_MARKER: str = "€"
CURRENCY_DOLLAR_MARKER: str = "$"

CURRENCY_MARKER_LIST: list[str] = [
    CURRENCY_RUB_MARKER,
    CURRENCY_EURO_MARKER,
    CURRENCY_DOLLAR_MARKER,
]
CURRENCY_NAMES_LIST: list[str] = [
    "RUR",
    "EURO",
    "USD",
]
SENIOR_LEVEL: str = "Senior"
SENIOR_SHORT_LEVEL: str = "Sr"
SENIOR_RUS: str = "Ведущий"
SENIOR_OR_MIDDLE: str = "Middle/Senior"
SENIOR_OR_MIDDLE_PLUS: str = "Middle+/Senior"

MIDDLE_PLUS: str = "Middle+"
MIDDLE_LEVEL: str = "Middle"

JUINOR_LEVEL: str = "Junior"
JUINOR_RUS_LEVEL: str = "Младший"
LEAD_LEVEL: str = "Lead"

DEVELOPER_LEVELS: list[str] = [
    SENIOR_LEVEL,
    SENIOR_SHORT_LEVEL,
    SENIOR_OR_MIDDLE,
    MIDDLE_PLUS,
    MIDDLE_LEVEL,
    JUINOR_LEVEL,
    LEAD_LEVEL,
]

HABR_CAREER = "HC"
EXISTS_HC_VACANCIES_IDS_KEY = "exists_vacancies_hc_ids"
