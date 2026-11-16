connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=127.0.0.1;"
    "DATABASE=your_database;"
    "UID=your_user;"
    "PWD=your_password;"
    "TrustServerCertificate=yes;"  # Forces the handshake to pass
    "Connection Timeout=30;"       # Prevents early dropping
)