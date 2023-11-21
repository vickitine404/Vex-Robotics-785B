import sqlite3
# import sqlite3 for all of our database handling

import os
# import os for all the path stuff to find the .db file

from datetime import date
# the .db has the current season's year in it, so it pulls the current year from the local system to make sure its pulling from the up-to-date database
# this means that I dont have to do two tables in one .db file, hehe

def getTeamData(team_number, comp_code="", match_number=""):

    cwd = os.getcwd()
    # Get the current working directory, so it can find the database to open
    try:
        conn = sqlite3.connect(os.path.join(cwd,'DB','scoutingData{0}.db'.format(date.today().year)))
        # make the connection to the database
        # os.path.join is for path creation across multiple platforms, I think Windows uses / but Linux uses \, saves us the headache

        c = conn.cursor()
        # all the actual command stuff
        
            
        sqlCommand = "SELECT * FROM teams WHERE team_number={0}".format(str(team_number))
        # So the way I form the query is I add on to a base string of just the team number

        results = []
        # sets up the empty list for us to dump the results into
        
        comp_code = comp_code.replace(" ", "").lower()
        # formatting the competition code so we can remove any blank characters and put it all into lower case
        if(comp_code!=""):
            # if the competition code isnt a blank string (both the default for the argument but also if you leave it blank on the site, double protection)
            # I do the formatting first, so if the code is a space like " " it will get turned into an empty string, stops errors

            sqlCommand+=" AND comp_code='{0}'".format(comp_code)
            # tack on a little bit of SQL onto the query, pretty jank but it hasn't failed me yet

        match_number = match_number.replace(" ", "").lower()
        # same thing as the comp code, format first
        if(match_number != ""):
            # if the match number isn't a blank string,

            sqlCommand+=" AND match_number='{0}'".format(match_number)
            # tack on the SQL code to check for match numbers
            
        for row in c.execute(sqlCommand):
            # when we execute the command, for every result (or "table row") we get back,

            results.append(row)
            # add it into the list of results

        # print the SQL query as a sanity check, it helps make sure its working on the server (and you can see when people are actually submitting data
        print(sqlCommand)

        # save and close the .db, makes sure our data is safe
        conn.commit()
        conn.close()

        if(results==[]):
            # if we didn't get any results, we must not have scouted them
            return("NOT IN TABLE")
        else:
            # if we got results, put this at the beginning of the list to give us some nice row headers in the HTML file
            # of course this will change year to year unless I come up with a better system, which I probably should
            results.insert(0,("Team Number","Match Number","Taxi","High Hub Scored (Auton)","Low Hub Scored (Auton)","Total Balls Fired (Auton)","High Hub Scored (Driver)","Low Hub Scored (Driver)","Total Balls Fired (Driver)","Strat","Catastrophes","Additional Notes"))

            # return the results to the main page
            return(results)
    except:
        pass
    # if if reaches this far, something bad happened cause it really should never get here but just in case:
    return("NOT IN TABLE")


def addData(collectedData):
    
    cwd = os.getcwd()
    # Get the current working directory, so it can find the database to open
    try:
        conn = sqlite3.connect(os.path.join(cwd,'DB','scoutingData{0}.db'.format(date.today().year)))
        # make the connection to the database
        # os.path.join is for path creation across multiple platforms, I think Windows uses / but Linux uses \, saves us the headache

        c = conn.cursor()
        # all the actual command stuff

        c.execute("INSERT INTO teams VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",collectedData)
        # add all the data in the database, just take it right from the list it was submitted as

        print(collectedData)
        # print out the collected data, another nice thing to see in the terminal

        # save and close the .db
        conn.commit()
        conn.close()
    except:
        pass
                           
def createNewTable():

    ###### THIS WAS CREATED AS A DEBUG FUNCTION ######
    # it was made so you could create a table in the blank .db file, this never gets called by the program, I called it from the terminal whenever I needed to use it 
    
    cwd = os.getcwd()
    # get cwd, find the db

    conn = sqlite3.connect(os.path.join(cwd,'DB','scoutingData{0}.db'.format(date.today().year)))
    # get this year's db

    c = conn.cursor()
    # used for command stuff

    # sanity order of how everything should be read/submitted

    ###### cross reference with your submission form!!!!!!! ######
    """
    Team number
    Comp code
    Match number
    Taxi?
    High Auton Scored
    Low Auton Scored
    Total Auton fired
    High Driver Scored
    Low Driver Scored    Total Driver fired
    Strat
    Hub
    Rungs Hung
    Fired Against Hub?
    Fired in tarmac
    Fired outside tarmac
    Didn't fire
    Catastrophes?
    Additional notes
    """
    
    c.execute("""CREATE TABLE teams (team_number int, comp_code text, match_number text, taxi text, high_balls_scored_auton int, low_balls_scored_auton int,
              total_balls_fired_auton int, high_balls_scored_driver int, low_balls_scored_driver int, total_balls_fired_driver int, strat text,
              hub text, rungs_hung text, fired_against_hub text, fired_in_tarmac text, fired_outside text, didnt_fire text, catastrophes text, additional text)""")

    # create the table
    # this is the longest SQL query I've ever written
    # I hate that it had to be this way, but I don't think I can do it any other way
    # I'll try some stuff but no promises

    # save and close .db
    conn.commit()
    conn.close()
