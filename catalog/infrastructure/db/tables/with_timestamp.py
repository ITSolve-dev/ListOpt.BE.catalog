from sqlalchemy import Column, DateTime, Table, func


def with_timestamp(table: Table) -> Table:
    table.append_column(
        Column(
            "created_at",
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        )
    )
    table.append_column(
        Column(
            "updated_at",
            DateTime(timezone=True),
            nullable=True,
            server_default=None,
            onupdate=func.now(),
        )
    )
    return table
