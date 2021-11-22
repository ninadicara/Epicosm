mongo --eval 'db.adminCommand("getCmdLineOpts").parsed.storage.dbPath' | tail -1 ;
