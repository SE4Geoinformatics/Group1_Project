Ⅰ The project use the Bootstrap v5.0.0 plugins(https://getbootstrap.com/) to build the View of pages.


Ⅱ The project use the postgresql as the database:

1: create a database in your postgresql: iUrbanDB
2: edit the configuration file: database.ini or dbConfig.txt
3: run the database.py to create db tables into your database


Ⅲ The project structure:

|--iUrban
    |--static
    |    |--bootstrap-5.0.0-beta3-dist
    |    |--css
    |    |    |--******.css
    |    |--img
    |    |--js
    |        |--******.js
    |--templates
    |    |--base.html
    |    |--index.html
    |--app.py              // Start the application***
    |--database.ini        // Database info file      
    |--database.py         // Drop and Create DB Table
    |--dbConfig.py           // Read the DB info from databse.ini 
    |--dbConfig.txt         //the same as the database.ini
    |--readme.md    
    |--requirements.txt    // Record the virtual environment info
    
    
Ⅳ The project environment:

/***************************************************************************/   
/*A requirements.txt file must be included in the Python project to record */
/*all dependent packages and their precise version numbers for deployment  */
/*in the new environment                                                   */
/*                                                                         */
/*In the virtual environment, use the following command to generate the    */
/*dependent packages in /the current virtual environment into the file     */
/*with the version number:                                                 */
/*                    ***pip freeze >requirements.txt***                   */
/*When you need to create a complete copy of this virtual environment,     */
/*you can create a new /*virtual /*environment and run the following       */
/*commands on it:                                                          */
/*                  ***pip install -r requirements.txt***                  */
/***************************************************************************/