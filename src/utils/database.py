# Built-in imports
import os
import json
import uuid
from datetime import datetime
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Sequence

# Third-party imports
from psycopg2.extras import Json


# Local imports
from base.config import logger

__postgres_connection = None
__postgres_cursor = None
__redis_connection = None


"""
POSTGRESS
"""


def _set_client_postgres(postgres_connection, postgres_cursor):
    global __postgres_connection, __postgres_cursor
    __postgres_connection = postgres_connection
    __postgres_cursor = postgres_cursor


def __query_to_postgres(query: str, values=None) -> None:
    logger.trace(f"Query: {query}")
    logger.trace(f"Query values: {values}")

    if values is None:
        __postgres_cursor.execute(query)
    else:
        __postgres_cursor.execute(query, values)

    return __postgres_cursor


def __build_where_clause(
    condition: Dict[str, Any], use_or: bool
) -> tuple[str, List[Any]]:

    # Build WHERE clause based on the condition dictionary
    connector = " OR " if use_or else " AND "
    clauses: List[str] = []
    values: List[Any] = []

    for col, val in condition.items():
        if isinstance(val, list):
            placeholders = ", ".join(["%s"] * len(val))
            clauses.append(f"{col} IN ({placeholders})")
            values.extend([Json(v) if isinstance(v, (dict, list)) else v for v in val])
        else:
            clauses.append(f"{col} = %s")
            values.append(Json(val) if isinstance(val, (dict, list)) else val)

    where_clause = connector.join(clauses)
    return where_clause, values


def _check_postgres_connection() -> bool:
    try:
        __query_to_postgres("SELECT 1")
        logger.success("PostgreSQL connection is successful.")
        return True
    except Exception as e:
        logger.error(f"PostgreSQL connection error: {e}")
        return False


def _is_table_exist(table_name: str) -> bool:
    query = f"""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = '{table_name}'
        );
    """
    __postgres_cursor = __query_to_postgres(query)
    is_exist = bool(__postgres_cursor.fetchone()[0])

    logger.trace(f"Table {table_name} exists: {is_exist}")
    return is_exist


def _get_table_columns(table_name: str) -> list:
    query = f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;  
    """
    __postgres_cursor = __query_to_postgres(query)
    results = __postgres_cursor.fetchall()
    logger.trace(f"Query results: {results}")

    return [row[0] for row in results]


def _get_table_data(
    table_name: str,
    condition: dict = None,
    use_or: bool = False,
    order_by: str = None,
    order: str = "ASC",
) -> list:
    if condition:
        where_clause, values = __build_where_clause(condition, use_or)
        query = f"SELECT * FROM {table_name} WHERE {where_clause}"
    else:
        query = f"SELECT * FROM {table_name}"
        values = None

    # Add ORDER BY clause if requested
    if order_by:
        # Only allow ASC or DESC
        order = order.upper()
        if order not in ("ASC", "DESC"):
            order = "ASC"
        query += f" ORDER BY {order_by} {order}"

    query += ";"
    __postgres_cursor = __query_to_postgres(query, values)
    results = __postgres_cursor.fetchall()
    logger.trace(f"Query results: {results}")

    columns = _get_table_columns(table_name)
    data = [
        {
            key: (value.isoformat() if isinstance(value, datetime) else value)
            for key, value in zip(columns, row)
        }
        for row in results
    ]
    return data


def _insert(table_name: str, data: dict) -> None:
    # Extract columns and placeholders
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))

    values = []
    for raw_val in data.values():
        # 1. If it’s already a Python list, treat it as a TEXT[] parameter
        if isinstance(raw_val, list):
            values.append(raw_val)

        # 2. If it’s a dict, assume you want a JSON/JSONB column
        elif isinstance(raw_val, dict):
            values.append(Json(raw_val))

        # 3. If it’s a string, check if it’s valid JSON
        elif isinstance(raw_val, str):
            try:
                parsed = json.loads(raw_val)
                # 3a. If parsed → list, send as array
                if isinstance(parsed, list):
                    values.append(parsed)
                # 3b. If parsed → dict, send as JSON
                elif isinstance(parsed, dict):
                    values.append(Json(parsed))
                # 3c. Otherwise, leave it as a normal string
                else:
                    values.append(raw_val)
            except (ValueError, TypeError):
                # Not JSON at all, so just pass the original string
                values.append(raw_val)

        # 4. Anything else (int, float, etc.) gets passed through
        else:
            values.append(raw_val)

    # Build and execute the INSERT
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    __postgres_cursor = __query_to_postgres(query, values)
    __postgres_connection.commit()

    logger.success(f"Data inserted into {table_name} successfully.")


def _update(table_name: str, data: dict, condition: dict, use_or: bool = False) -> None:
    # Extract columns and values for SET clause
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    set_values = [
        Json(value) if isinstance(value, dict) else value for value in data.values()
    ]

    where_clause, where_values = __build_where_clause(condition, use_or)
    # Combine values for parameterized query
    values = set_values + where_values

    # Construct parameterized query
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

    __postgres_cursor = __query_to_postgres(query, values)
    __postgres_connection.commit()

    logger.success(f"Data updated in {table_name} successfully.")


def _is_data_exist(table_name: str, condition: dict, use_or: bool = False) -> bool:
    # Choose connector based on use_or flag
    where_clause, values = __build_where_clause(condition, use_or)
    # Build query with WHERE clause
    query = f"""
        SELECT EXISTS (
            SELECT 1
            FROM {table_name}
            WHERE {where_clause}
        );
    """
    # Execute query with values
    __postgres_cursor = __query_to_postgres(query, values)
    # Fetch result and convert to boolean
    is_exist = bool(__postgres_cursor.fetchone()[0])

    logger.info(f"Data exists in {table_name}: {is_exist}")
    return is_exist


"""
REDIS
"""


def _set_client_redis(redis_connection):
    global __redis_connection
    __redis_connection = redis_connection


def _check_redis_connection() -> bool:
    try:
        __redis_connection.ping()
        logger.success("Redis connection is successful.")
        return True
    except Exception as e:
        logger.error(f"Redis connection error: {e}")
        return False


def _store_simple_string(key: str, value: str) -> None:
    __redis_connection.set(key, value)
    logger.success(f"Stored simple string under key '{key}' successfully.")


def _retrieve_simple_string(key: str):
    data = __redis_connection.get(key)
    if data is None:
        logger.warning(f"No data found for key '{key}'.")
        return None
    return __redis_connection


def _store_hashmap(
    key: str, data: Dict[str, Any], expire_seconds: Optional[int] = None
) -> None:
    __redis_connection.hset(key, mapping=data)
    if expire_seconds:
        __redis_connection.expire(key, expire_seconds)


def _retrieve_hashmap(key: str) -> Dict[str, Any]:
    data = __redis_connection.hgetall(key)
    if data == {}:
        logger.warning(f"No data found for key '{key}'.")
        return None
    # Convert bytes to str for all values
    return data
