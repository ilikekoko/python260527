import re

result = re.search("[0-9]*th", "  35th")
print(result)
print(result.group())

# result = re.match("[0-9]*th", "  35th")
# print(result)
# print(result.group())

result = re.search("\d{4}", "year 3456 입니다")
print(result.group())
