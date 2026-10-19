"""Print a SQL Server plan saved by the HybridQO scripts as an indented operator tree.
Usage: python tools/show_plan.py results/enumerated_plans_DB/imdb_test/iterNone/21c/0.txt
"""
import sys
import xml.etree.ElementTree as ET

NS = "{http://schemas.microsoft.com/sqlserver/2004/07/showplan}"


def extract_xml(text):
    start = text.find("USE PLAN N'")
    if start == -1:
        return text
    start += len("USE PLAN N'")
    end = text.rfind("')")
    return text[start:end].replace("''", "'")


def table_of(relop):
    for child in relop:
        if child.tag == NS + "RelOp":
            continue
        obj = child.find(NS + "Object")
        if obj is not None:
            table = obj.get("Table", "").strip("[]")
            alias = obj.get("Alias", "").strip("[]")
            return f"{table} AS {alias}" if alias else table
    return ""


def walk(elem, depth=0):
    for child in elem:
        if child.tag == NS + "RelOp":
            op = child.get("PhysicalOp")
            rows = float(child.get("EstimateRows", 0))
            table = table_of(child)
            label = f"{op} [{table}]" if table else op
            print(f"{'   ' * depth}{label}   (est. rows: {rows:,.0f})")
            walk(child, depth + 1)
        else:
            walk(child, depth)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        root = ET.fromstring(extract_xml(f.read()))
    walk(root)
