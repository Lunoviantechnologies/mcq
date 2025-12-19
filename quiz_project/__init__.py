"""
Project package init.

PyMySQL is used to connect to MySQL (RDS) without requiring system build tools.
"""

try:
    import pymysql

    pymysql.install_as_MySQLdb()
except Exception:
    # If PyMySQL isn't installed (e.g., local SQLite only), ignore.
    pass

