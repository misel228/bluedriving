#!/usr/bin/python
#  Copyright (C) 2009  Veronica Valeros, Juan Manuel Abrigo, Sebastian Garcia
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# Author:
# Veronica Valeros  vero.valeros@gmail.com
#
# Changelog
#
# TODO
#
# KNOWN BUGS
#
# Description
# manageDB is a python tool to manage bluedriving database
#

# standar imports
import sys
import re
import getopt
import copy
import os
import time
import sqlite3


# Global variables
vernum = '0.1'
debug = False


def version():
    """
    This function prints information about this utility
    """

    print
    print "   "+ sys.argv[0] + " Version "+ vernum +" @COPYLEFT                    "
    print "   Authors: verovaleros, eldraco, nanojaus                               "
    print "   manageDB is a python tool to manage bluedriving database.            "
    print

def usage():
    """
    This function prints the posible options of this program.
    """
    print
    print "   "+ sys.argv[0] + " Version "+ vernum +" @COPYLEFT                    "
    print "   Authors: verovaleros, eldraco, nanojaus                               "
    print "   manageDB is a python tool to manage bluedriving database.            "
    print
    print "\n   Usage: %s <options>" % sys.argv[0]
    print "   Options:"
    print "  \t-h, --help                           Show this help message and exit."
    print "  \t-D, --debug                          Debug mode ON. Prints debug information on the screen."
    print "  \t-d, --database-name                  Name of the database to store the data."
    print "  \t-l, --limit                          Limits the number of results when querying the database"
    print "  \t--get-devices                        List all the MAC addresses of the devices stored in the DB"
    print "  \t--get-devices-with-names             List all the MAC addresses and the names of the devices stored in the DB"
    print "  \t--device-exists <mac>                Check if a MAC address is present on the database"
    print "  \t--remove-device <mac>                Remove a device using a MAC address"
    print "  \t--grep-names <string>                Look names matching the given string"
    print "  \t--rank-devices                       Shows a top 10 of the most seen devices on the database"
    print "  \t-m, --merge-with <db>                Merge the database (-d) with this database.Ex. bluedriving.py -d blu.db -m netbook.db"


def db_create(database_name):
    """
    This function creates a connection to the database and return the connection
    """
    global debug
    global verbose

    connection = ""

    try:
        # We check if the database exists
        if not os.path.exists(database_name):
            if debug:
                print 'Creating database'
            # Creating database
            connection = sqlite3.connect(database_name)
            # Creating tables
            connection.execute("CREATE TABLE Devices(Id INTEGER PRIMARY KEY AUTOINCREMENT, Mac TEXT , Info TEXT, UNIQUE(Mac))")
            connection.execute("CREATE TABLE Locations(Id INTEGER PRIMARY KEY AUTOINCREMENT, MacId INTEGER, GPS TEXT, FirstSeen TEXT, LastSeen TEXT, Address TEXT, Name TEXT, UNIQUE(MacId,GPS))")
            connection.execute("CREATE TABLE Notes(Id INTEGER, Note TEXT)")
            connection.execute("CREATE TABLE Alarms(Id INTEGER, Alarm TEXT)")
            connection.commit()
            connection.close()
            if debug:
                print 'Database created'
            return True
        else:
            if debug:
                print 'Database already exist. Choose a different name.'
            return False
    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_connect(database_name) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)


def db_connect(database_name):
    """
    This function creates a connection to the database and return the connection
    """
    global debug
    global verbose

    connection = ""

    try:
        if not os.path.exists(database_name):
            return False
        connection = sqlite3.connect(database_name)
        if debug:
            print 'Database connection retrieved'
        return connection

    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_connect(database_name) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)

def db_count_devices(connection):
    """
    """
    global debug
    global verbose

    try:
        result = connection.execute("SELECT count(*) FROM Devices")
        if result:
            result = result.fetchall()
            return result[0][0]

    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_list_devices(connection) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)

def db_get_mac_from_id(connection, MacId):
    """
    """
    global debug
    global verbose

    try:
        result = connection.execute("SELECT Mac FROM Devices WHERE Id = "+str(MacId)+";")
        if result:
            result = result.fetchall()
            return result[0][0]

    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_list_devices(connection) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)

def db_get_id_from_mac(connection, Mac):
    """
    """
    global debug
    global verbose

    try:
        result = connection.execute("SELECT Id FROM Devices WHERE Mac = \""+str(Mac)+"\";")
        if result:
            result = result.fetchall()
            return result[0][0]

    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_list_devices(connection) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)

def db_merge(db_merged_connection,db_to_merge_connection):
    """
    This function creates a connection to the database and return the connection
    """
    global debug
    global verbose

    count_dev = 0
    count_loc = 0
    count_ala = 0
    count_not = 0

    try:
        # Adding data from devices database
        result = db_to_merge_connection.execute("SELECT Id, Mac,Info FROM Devices")
        devices = result.fetchall()
        for (MacId,Mac,Info) in devices:
            #result = db_merged_connection.execute("INSERT OR IGNORE INTO Devices (Mac,Info) VALUES(\"11:11:11:11:11:11\",\"[]\");")
            try:
                result= db_merged_connection.execute("INSERT OR IGNORE INTO Devices (Mac,Info) VALUES(\""+str(Mac)+"\",\""+str(Info[0])+"\");")
            except:
                print 'Exception mergin this device: {}, {}'.format(Mac,Info[0])

            db_merged_connection.commit()

            #Adding data from locations table
            result = db_to_merge_connection.execute("SELECT MacId,GPS,FirstSeen,LastSeen,Address,Name FROM Locations WHERE MacId="+str(MacId)+";")
            locationinfo = result.fetchall()
            for (MacIdLoc,GPS,FSeen,LSeen,Address,Name) in locationinfo:
                    if debug:
                        print '{} {} {} {} {} {}'.format(MacIdLoc,GPS,FSeen,LSeen,Address,Name)
                    newMacId = db_get_id_from_mac(db_merged_connection,Mac)
                    result = db_merged_connection.execute("INSERT OR IGNORE INTO Locations (MacId, GPS, FirstSeen, LastSeen, Address, Name) VALUES("+str(newMacId)+",\""+str(GPS)+"\",\""+str(FSeen)+"\",\""+str(LSeen)+"\",\""+str(Address)+"\","+Name+");")

        db_merged_connection.commit()
        db_to_merge_connection.close()

    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_merge(database_name) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)

def db_list_devices(connection, limit):
    """
    This function creates a connection to the database and return the connection
    """
    global debug
    global verbose

    devices=""

    try:
        try:
            result = connection.execute("SELECT Mac FROM Devices LIMIT "+str(limit))
            devices = result.fetchall()
            return devices
        except:
            return False
    
    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_list_devices(connection) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)


def db_list_devices_and_names(connection, limit):
    """
    This function creates a connection to the database and return the connection
    """
    global debug
    global verbose

    devices=""
    deviceswname=[]

    try:
        try:
            result = connection.execute("SELECT Id,Mac FROM Devices LIMIT "+str(limit))
            devices = result.fetchall()
            for dev in devices:
                name=""
                result = connection.execute("SELECT Name FROM Locations WHERE MacId=\""+str(dev[0])+"\" LIMIT 1") 
                name = result.fetchall()
                deviceswname.append([dev[1],name[0][0]])
                if debug:
                    print "{} - {} - {}".format(dev[0],dev[1],name[0][0])
            if debug:
                print deviceswname
            return deviceswname
        except:
            print "Exception in db_list_devices_and_names"
            return False
    
    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_list_devices(connection) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)

def db_device_exists(connection, mac):
    """
    This function returns true if the given mac is stored on the database 
    """
    global debug
    global verbose

    device=""
    result=False

    try:
        try:
            result = connection.execute("SELECT Id FROM Devices WHERE Mac=\""+str(mac)+"\"") 
            if result:
                device = result.fetchall()
                if device:
                    return True
                else:
                    return False
            else:
                print "no result"
                return False
            
        except:
            print "Exception in idb_device_exists"
            return False
    
    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_device_exists(connection) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)

def db_grep_names(connection,string):
    """
    This function returns devices which names are similar to the given string
    """
    global debug
    global verbose

    try:
        try:
            result = connection.execute("SELECT DISTINCT Name FROM Locations WHERE Name LIKE \"%"+str(string)+"%\"") 
            if result:
                result = result.fetchall()
                return result
            else:  
                return False
            
        except:
            print "Exception in db_grep_names()"
            return False
    
    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_grep_names(connection,string) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)

def db_rank_devices(connection,limit):
    """
    This function returns a list of devices and the amount of times that were observed
    """
    global debug
    global verbose

    result = ""
    try:
        try:
            result = connection.execute("SELECT Name, MacId, count(MacId) as amount FROM Locations GROUP BY MacId ORDER BY amount DESC LIMIT 10") 
            result = result.fetchall()
            
            if result:
                return result
            else:
                return False
        except:
            print "Exception in db_rank_devices()"
            return False
    
    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_rank_devices(connection,limit) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)


def db_remove_device(connection, mac):
    """
    This function removes a device from the database
    """
    global debug
    global verbose

    try:
        try:
            #Here we check that the device is present on the database
            exists = db_device_exists(connection, mac)
            if exists:
                    result = connection.execute("SELECT Id FROM Devices WHERE Mac=\""+str(mac)+"\" LIMIT 1")
                    id = result.fetchall()
                    id = id[0][0]
                    try:
                            result = connection.execute("DELETE FROM Locations WHERE MacId = "+str(id))
                    except:
                            if debug:
                                print "No rows affected"
                    try:
                            result = connection.execute("DELETE FROM Alarms WHERE Id = "+str(id))
                    except:
                            if debug:
                                print "No rows affected"
                    try:
                            result = connection.execute("DELETE FROM Notes WHERE Id = "+str(id))
                    except:
                            if debug:
                                print "No rows affected"
                    try:
                            result = connection.execute("DELETE FROM Devices WHERE Id = "+str(id))
                    except:
                            if debug:
                                print "No rows affected"
                    
                    connection.commit()

                    print "Checking if the deletion was efective"
                    result = connection.execute("SELECT Mac FROM Devices WHERE Id = "+str(id))
                    result = result.fetchall()
                    if not result:
                        print "\t[-] Deletion from Devices was effectve"
                    result = connection.execute("SELECT Id FROM Locations WHERE MacId = "+str(id))
                    result = result.fetchall()
                    if not result:
                        print "\t[-] Deletion from Locations was effectve"
                    result = connection.execute("SELECT Id FROM Alarms WHERE Id = "+str(id))
                    result = result.fetchall()
                    if not result:
                        print "\t[-] Deletion from Alarms was effectve"
                    result = connection.execute("SELECT Id FROM Notes WHERE Id = "+str(id))
                    result = result.fetchall()
                    if not result:
                        print "\t[-] Deletion from Notes was effectve"
        except:
            print "Exception in db_remove_device(connection,mac)"
            return False
    
    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Exception in db_list_devices(connection) function'
        print 'Ending threads, exiting when finished'
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)


def main():
    global debug
    global verbose

    database=""
    connection=""
    get_devices=""
    get_devices_with_names=""
    device_mac=""
    device_exists = False
    remove_device = False
    grep_names = False
    rank_devices = False
    ranking=""
    limit=999999
    quiet=False
    merge_db=False
    db_to_merge=""
    db_count=False
    create_db=False

    try:

        # By default we crawl a max of 5000 distinct URLs
        opts, args = getopt.getopt(sys.argv[1:], "hDd:l:enE:R:g:r:qm:Cc:", ["help","debug","database-name=","limit=","get-devices","get-devices-with-names","device-exists=","remove-device=","grep-names=","rank-devices=","quiet","merge-with=","count-devices","create-db="])
    except:
        usage()
        exit(-1)

    for opt, arg in opts:
        if opt in ("-h", "--help"): usage(); sys.exit()
        if opt in ("-D", "--debug"): debug = True
        if opt in ("-d", "--database"): database = arg
        if opt in ("-l", "--limit"): limit = arg
        if opt in ("-e","--get-devices"): get_devices = True
        if opt in ("-n","--get-devices-with-names"): get_devices_with_names = True
        if opt in ("-E","--device-exists"): device_mac = arg; device_exists=True
        if opt in ("-R","--remove-device"): device_mac = arg; remove_device=True
        if opt in ("-g","--grep-names"): string = arg; grep_names=True
        if opt in ("-r","--rank-devices"): limit = arg; rank_devices=True
        if opt in ("-q","--quiet-devices"): quiet=True
        if opt in ("-m","--merge-with"): db_to_merge=arg; merge_db=True
        if opt in ("-C","--count-devices"): db_count=True
        if opt in ("-c", "--create-db"): database = arg; create_db=True


    try:
        if create_db:
            result = db_create(database)
            if result:
                print '[+] Database created'
            else:
                print '[+] Database not created'
            sys.exit()

        if database:
            if not quiet:
                version()
                print "[+] Database: {}".format(database)
            connection = db_connect(database)

        if connection:
            if not quiet:
                print "[+] Connection established"

            #List devices
            if get_devices:
                devices = db_list_devices(connection, limit)
                if devices:
                    if not quiet:
                        print "[+] List of devices in the database:"
                    for key in devices:
                        print "\t{}".format(key[0])
            # List devices with name
            elif get_devices_with_names:
                deviceswnames= db_list_devices_and_names(connection,limit)
                if deviceswnames:
                    for (mac,name) in deviceswnames:
                        print "\t{} - {}".format(mac,name)
            elif device_exists:
                exists = db_device_exists(connection,device_mac)
                if exists:
                    print "\tDevice {} exists in the database".format(device_mac)
                else:
                    print "\tDevice {} is not present in the database".format(device_mac)
            elif remove_device:
                db_remove_device(connection,device_mac)
                exists = db_device_exists(connection,device_mac)
                if exists:
                    print "\tDevice {} exists in the database".format(device_mac)
                else:
                    print "\tDevice {} is not present in the database".format(device_mac)
            elif grep_names:
                similar_names = db_grep_names(connection,string)
                if similar_names:
                    for i in similar_names:
                        print "\t{}".format(i[0])
            elif rank_devices:
                ranking = db_rank_devices(connection,limit)
                if ranking:
                    for i in ranking:
                        print "\t{} - {}".format(i[2],i[0])
            elif merge_db:
                db_to_merge_connection = db_connect(db_to_merge)
                db_merge(connection,db_to_merge_connection)
            elif db_count:
                number_of_devices = db_count_devices(connection)
                print '\tNumber of devices on the database: {}'.format(number_of_devices)
            else:
                print "Nothing to do. Please select an option."

            if connection: 
                connection.close()
                if not quiet:
                    print "[+] Connection closed"

        else:
            print "A connection to the database could not be retrieved"

    except KeyboardInterrupt:
        print 'Exiting. It may take a few seconds.'
        sys.exit(1)
    except Exception as inst:
        print 'Error in main() function'
        print 'Ending threads, exiting when finished'
        threadbreak = True
        print type(inst) # the exception instance
        print inst.args # arguments stored in .args
        print inst # _str_ allows args to printed directly
        x, y = inst # _getitem_ allows args to be unpacked directly
        print 'x =', x
        print 'y =', y
        sys.exit(1)


if __name__ == '__main__':
        main()

