import re
from pathlib import Path


def extract_schema_summary(schema_path: str = "src/chat/training/schema.sql") -> str:
    """
    Extracts a summary of tables, columns, and foreign keys from a PostgreSQL schema.sql file.
    Returns a string suitable for LLM system prompts.
    """
    summary = []
    with open(schema_path, "r") as f:
        sql = f.read()

    # Find all CREATE TABLE blocks
    table_blocks = re.findall(r"CREATE TABLE ([^\s\(]+)\s*\((.*?)\);", sql, re.DOTALL)

    # Parse ALTER TABLE blocks for foreign keys (block-based, robust to multi-line and DEFERRABLE)
    foreign_keys = {}
    # Split by semicolon to get each statement
    for stmt in sql.split(";"):
        stmt = stmt.strip()
        if not stmt.upper().startswith("ALTER TABLE ONLY"):
            continue
        # Try to match FK pattern in the whole block
        fk_match = re.search(
            r"ALTER TABLE ONLY\s+([^\s]+)\s+ADD CONSTRAINT [^\s]+ FOREIGN KEY\s*\(([^)]+)\)\s+REFERENCES\s+([^\s]+)\s*\(([^)]+)\)",
            stmt,
            re.IGNORECASE | re.DOTALL,
        )
        if fk_match:
            table, col, ref_table, ref_col = fk_match.groups()
            foreign_keys.setdefault(table, []).append(
                (col.strip(), ref_table.strip(), ref_col.strip())
            )

    for table_name, block in table_blocks:
        columns = []
        for line in block.splitlines():
            line = line.strip()
            if (
                not line
                or line.startswith("--")
                or line.lower().startswith("constraint")
                or line.lower().startswith("primary key")
                or line.lower().startswith("unique")
                or line.lower().startswith("foreign key")
            ):
                continue
            col = line.split()[0].replace(",", "")
            if col.isidentifier() or col.startswith('"'):
                columns.append(col)
        summary.append(f"Table: {table_name}\n  Columns: {', '.join(columns)}")
        if table_name in foreign_keys:
            fk_lines = [
                f"{col} -> {ref_table}.{ref_col}"
                for col, ref_table, ref_col in foreign_keys[table_name]
            ]
            summary.append(f"  Foreign Keys: {', '.join(fk_lines)}")
    return "\n".join(summary)


if __name__ == "__main__":
    print(extract_schema_summary())
