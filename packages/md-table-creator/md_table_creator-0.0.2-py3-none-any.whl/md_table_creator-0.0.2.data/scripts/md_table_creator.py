"""
MySql create table syntax documentation was heavily referenced to create the regex strings
https://dev.mysql.com/doc/refman/5.7/en/create-table.html
"""
import re
from typing import List, Tuple


def create_md_tables(sql_create_tables: str) -> str:
    if sql_create_tables == "":
        raise ValueError("Empty input")
    sql_create_tables_arr = list(filter(None, sql_create_tables.split(";")))
    md_tables = [create_md_table(t) for t in sql_create_tables_arr]
    return "\n\n".join(md_tables)


def create_md_table(sql_create_table: str) -> str:
    """Converts sql create table syntax into md table."""
    # replace whitespace with spaces
    sql_create_table = " ".join(sql_create_table.split())
    table_name = extract_table_name(sql_create_table)
    columns, attributes = extract_columns(sql_create_table)
    columns_str = "\n".join(f"|{name}|{type}||" for (name, type) in columns)
    attribute_str = "Attributes:\n" + "\n".join(attributes) + "\n" if attributes else ""

    md_table = (
        f"**{table_name}**"
        "\n"
        f"{attribute_str}"
        "|Column | Type | Comments|\n"
        "|-|-|-|\n"
        f"{columns_str}"
    )
    return md_table


def extract_table_name(sql_create_table: str) -> str:
    """Uses regex to extract the table name from the sql syntax.

    CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name (
    """
    if raw_table := re.search(
        r"create (?:temporary )?table (?:if not exists)?(.*?)\(",
        sql_create_table,
        re.IGNORECASE,
    ):
        if group := raw_table.group(1):
            return group.strip()
    raise ValueError(
        "Could not parse table name from SQL create table syntax. Make sure it's valid SQL syntax"
    )


def extract_columns(sql_create_table: str) -> Tuple[List[Tuple[str, str]], List[str]]:
    if all_columns_re := re.search(r"\((.*)\)", sql_create_table):
        all_columns = split_columns(all_columns_re.group(1))
        extracted_values = []
        attributes = []
        for column in all_columns:
            column = column.strip()
            name = column.split(" ")[0]
            if re.search(
                r"index|key|fulltext|spatial|constraint|primary|unique|foreign|check",
                name,
                re.IGNORECASE,
            ):
                attributes.append(column)
                continue
            type = " ".join(column.split(" ")[1:])
            extracted_values.append((name, type))
        return extracted_values, attributes

    raise ValueError(
        "Could not parse columns from SQL create table syntax. Make sure it's valid SQL syntax"
    )


def split_columns(all_columns_str):
    """Splits commas that are outside of parenthesis"""
    paren_count = 0
    columns = []
    previous_index = 0
    for index, c in enumerate(all_columns_str):
        if c == "(":
            paren_count += 1
        elif c == ")":
            paren_count -= 1
        elif c == "," and paren_count == 0:
            columns.append(all_columns_str[previous_index:index])
            # The + 1 is to skip the comma
            previous_index = index + 1
    columns.append(all_columns_str[previous_index:])
    return columns


def main():
    sql_string = ""
    first = input(
        "Paste your Create SQL string here (Press enter 4 times to submit)..."
    )
    if not first:
        return
    sql_string = first
    enter_count = 0
    while True:
        input_string = input()
        enter_count = enter_count + 1 if not input_string else 0
        # 3 lines with only newline characters created after 4 enters
        # The first newline is part of the end of the sql statement
        if enter_count == 3:
            print("Submitted! Here are your md tables:\n")
            break
        sql_string += input_string
    print(create_md_tables(sql_string))


if __name__ == "__main__":
    main()
