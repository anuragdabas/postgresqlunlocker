<p align="center">
  <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/45512833/239765695-f59489df-a4ab-4f2c-871d-fa3c1e54ce46.png" alt="Timescale Unblocker">
</p>


# TimeScale Unblocker
Timescale Unblocker is a simple script using which you can terminate all the active and idle process ids(pids) of *POSTGRESQL* which are unnecessarily aquiring locks and resources and due to which your
query waiting indefinately to run.

Note: Beware of terminating the queries because it will terminate the queries of other users accessing the database via different session i.e parallely
