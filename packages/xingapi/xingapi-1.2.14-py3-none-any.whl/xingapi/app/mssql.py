import pyodbc

class MSSQL:
    def __init__(self, con_str='', **kwargs):
        self.con_str = con_str
        self.kwargs = kwargs

    def __call__(self, con_str='', **kwargs):
        self.con_str += con_str
        self.kwargs.update(kwargs)
        return self

    def create_database(self, name, file_dir='D:\MSSQL', drop_if_exist=False):
        with pyodbc.connect(self.con_str, **self.kwargs) as con:
            c = con.cursor()
            if drop_if_exist:
                c.execute(f"""IF DB_ID (N'{name}') IS NOT NULL DROP DATABASE {name}""")
            c.execute(f"""CREATE DATABASE [{name}] 
                ON PRIMARY 
                ( NAME = N'{name}', FILENAME = N'{file_dir}\Data\{name}.mdf' ) 
                LOG ON 
                ( NAME = N'{name}_log', FILENAME = N'{file_dir}\Log\{name}_log.ldf' ) 
                """)
            c.execute(f"""ALTER DATABASE [{name}] ADD FILEGROUP [Optimized_FG] CONTAINS MEMORY_OPTIMIZED_DATA""")
            c.execute(f"""ALTER DATABASE [{name}] ADD FILE ( NAME = N'{name}_optimized_data', FILENAME = N'{file_dir}\Data\{name}_optimized_data.ndf') TO FILEGROUP [Optimized_FG] """)
            c.execute(f"""ALTER DATABASE [{name}] SET MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT = ON """)

    def create_table(self, name, struct):
        with pyodbc.connect(self.con_str, **self.kwargs) as con:
            c = con.cursor()
            c.execute(f"""IF OBJECT_ID('dbo.{name}', 'U') IS NULL 
            CREATE TABLE {name} ({struct}) 
            WITH(MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_AND_DATA, 
            SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.{name}_history))
            """)

if __name__ == "__main__":
    mssql = MSSQL('Trusted_Connection=yes;', driver='{ODBC Driver 17 for SQL Server}', server='localhost', autocommit=True)
    mssql.create_database(name='TestTemporal6', drop_if_exist=False)
    mssql(database='TestTemporal6').create_table(
        name='test', 
        struct="""
        CustomerId INT IDENTITY(1,1)  
        ,FirstName VARCHAR(30) NOT NULL 
        ,LastName VARCHAR(30) NOT NULL 
        ,Amount_purchased DECIMAL NOT NULL 
        ,StartDate datetime2 generated always as row START NOT NULL 
        ,EndDate datetime2 generated always as row END NOT NULL 
        ,PERIOD FOR SYSTEM_TIME (StartDate, EndDate), 
        CONSTRAINT [PK_CustomerID1] PRIMARY KEY NONCLUSTERED HASH (CustomerId) WITH (BUCKET_COUNT = 131072)""")