# Python corelib
import configparser, os, pandas as pd
from typing import Sequence, Callable, Any, AnyStr
from enum import Enum
from .logger import Logger

# 3rd party lib
from pymysqlpool.pool import Pool

class MySQL:
    def __init__(self, conf_tag='mysqldb', conf_file='config.ini'):
        super().__init__()
        parser = configparser.ConfigParser()

        if os.path.isfile(conf_file):
            parser.read(conf_file)
        else:
            raise FileNotFoundError()

        config = parser[conf_tag]

        username = config['username']
        password = config['password']
        host = config['host']
        port = int(config['port'])
        schema = config['schema']

        try:
            min_size = int(config['minConnection'])
            max_size = int(config['maxConnection'])
        except:
            min_size = 0
            max_size = 10

        self._pool = Pool(user=username, password=password, host=host, port=port,
                          db=schema, min_size=min_size, max_size=max_size)
        
        self._logger = Logger()

    def execute(self, query: AnyStr, param: Sequence[Any] = (),
               func: Callable = lambda row: row) -> int:
        count: int = 0

        try:
            conn = self._pool.get_conn()
            with conn.cursor() as cursor:
                count = cursor.execute(query, param)
                conn.commit()
                rows = cursor.fetchall()
                for row in rows:
                    func(row)
        except Exception as e:
            self._logger.error(e)
        finally:
            if conn: self._pool.release(conn)

        return count
    
    def execute_df(self, query: AnyStr, param: Sequence[Any] = ()) -> pd.DataFrame:
        df:pd.DataFrame = None

        try:
            conn = self._pool.get_conn()
            with conn.cursor() as cursor:
                cursor.execute(query, param)
                conn.commit()
                rows = cursor.fetchall()
                df = pd.DataFrame(rows)
        except Exception as e:
            self._logger.error(e)
        finally:
            if conn: self._pool.release(conn)

        return df

    def execute_batch(self, query: AnyStr, 
                params: Sequence[Sequence[Any]] = (),
                func: Callable = lambda row: row) -> int:
        count:int = 0
       
        try:
            conn = self._pool.get_conn()

            with conn.cursor() as cursor:
                for param in params:
                    reg: int = cursor.execute(query, param)
                    count = count + reg
                conn.commit()
                rows = cursor.fetchall()
                for row in rows:
                    func(row)
        except Exception as e:
            self._logger.error(e)
        finally:
            if conn: self._pool.release(conn)

        return count
