from psycopg2.errors import OperationalError
from utilities import utils,consts
import argparse
from psycopg2.sql import Identifier


class TimeScaleUnblock:
    def __init__(self,dbname,state,loghandlers):
        self.dbname=dbname
        self.state=state
        self.client=utils.TimeScale.get_connection(self.dbname)
        self.cursor=utils.TimeScale.get_cursor(self.client)
        self.logger=utils.Logger.Logger(self.dbname,loghandlers)
        self.locksterminated=self.terminate_locks()
        self.clientclosed=utils.TimeScale.close(self.client)

        
    def get_info_about_locks(self):
        try:
            query=f"select pid,state,query from pg_stat_activity where datname={Identifier(self.dbname)}"
            if self.state.lower()=="active" or self.state.lower()=="idle":
                query+=" (state=%(state)s and pid!=pg_backend_pid());"
            else:
                query+=" and pid!=pg_backend_pid();"
            self.logger.info("Attempting to Fetch Pid's")
            self.cursor.execute(query,{'state':self.state})
            result = self.cursor.fetchall()
            self.logger.info("Successfully Fetched Pid's")
            return result
        except Exception as e:
            self.logger.error(f"Unable to Fetch Pid's due to '{e}'")

    def terminate_locks(self):
        try:
            locksinfo=self.get_info_about_locks()
            for data in locksinfo:
                self.logger.info(f"Attempting to terminate: \npid : {data[0]} \nstate : {data[1]} \nquery : {data[2]}\n\n")
                query="select pg_terminate_backend(%(pid)s)"
                self.cursor.execute(query,{"pid":data[0]})
                self.client.commit()
                status=self.cursor.fetchone()
                if status:
                    self.logger.info(f"Successfully terminated pid : {data[0]}")
                else:
                    self.logger.info(f"Pid : {data[0]} is already terminated")
            self.logger.info(f"DataBase {self.dbname} unblocked Successfully")
            return True

        except OperationalError as oe:
            self.client.rollback()
            self.logger.error(f"Unable to terminate Pid : {data[0]} because of server side error : {oe}")
            return False

        except Exception as e:
            self.logger.error(f"Unable to terminate Pid : {data[0]} because of internal breakage : {e}")
            return False


ar=argparse.ArgumentParser(consts.Logo.CMDLOGO.value+"\nList of Required Arguements",formatter_class=argparse.RawDescriptionHelpFormatter)
ar.add_argument("-d","--database",required=True,help="\nEnter the database name whom you want to unblock",type=str)
ar.add_argument("-s","--state",required=False,default="all",help="\nEnter which state you want to unblock.\npossible values: active,idle and all(default)",type=str)
ar.add_argument("-sl","--showlog",required=False,default=True,help="\nOption To show logs in the console/terminal default(True)",type=bool)
ar.add_argument("-wl","--writelog",required=False,default=False,help="\nOption To show write logs in the console/terminal default(True)",type=bool)
args=ar.parse_args()

if __name__=="__main__":
    print(consts.Logo.CMDLOGO.value)
    tunblock=TimeScaleUnblock(args.database,args.state,[args.showlog,args.writelog])
    del tunblock