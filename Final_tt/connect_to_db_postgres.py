import xml.etree.ElementTree as ET
import psycopg2

# connecting the database on postgres
conn = psycopg2.connect(dbname='text_technology',
  user='postgres', host='',
  password='Sakshi19@')

cur = conn.cursor()

# execute a statement
print('PostgreSQL database version:')

# To execute the command,
# but doesn't return the result
cur.execute('SELECT version()')

# This will return the result
# of query on line 15
print(cur.fetchone())

# Query to create table
create_table_command = """
        CREATE TABLE tweet_emotions (
            region_anchor VARCHAR(20) NOT NULL,
            region_id VARCHAR(10) NOT NULL,
            node_id VARCHAR(10) NOT NULL,
            a_id VARCHAR(10) NOT NULL,
            a_label VARCHAR(20) NOT NULL,
            a_ref VARCHAR(10) NOT NULL,
            a_as VARCHAR(20) NOT NULL
        )
        """
       
cur.execute(create_table_command)

tree = ET.parse('tweet-emotions.xml')
root = tree.getroot()

# Attribute names
region_id = None
region_anchor = None
node_id = None
a_id = None
a_label = None
a_ref = None
a_as = None
isRegionScanned = False
isNodeScanned = False
isAnnotationScanned = False

# extracting the values of 
# respective attributes from root
for child in root:
  if child.tag == 'region':
    for key in child.attrib:
      if 'id' in key:
        region_id = str(child.attrib[key])

      if 'anchor' in key:
        region_anchor = str(child.attrib[key])

    isRegionScanned = True
  
  if child.tag == 'node':
    for key in child.attrib:

      if 'id' in key:
        node_id = str(child.attrib[key])

    isNodeScanned = True

  if child.tag == 'a':
    for key in child.attrib:
      if 'id' in key:
        a_id = str(child.attrib[key])

      if 'label' in key:
        a_label = str(child.attrib[key])

      if 'as' in key:
        a_as = str(child.attrib[key])

      if 'ref' in key:
        a_ref = str(child.attrib[key])

    isAnnotationScanned = True

# inserting values in the table
  if isAnnotationScanned is True and isNodeScanned is True and isRegionScanned is True:
    insert_command = """INSERT INTO tweet_emotions(region_id, region_anchor, node_id, a_id, a_ref, a_as, a_label)
             VALUES(%s, %s, %s, %s, %s, %s, %s);"""

# performing insertion
    cur.execute(insert_command, (region_id, region_anchor, node_id, a_id, a_ref, a_as, a_label))

    isAnnotationScanned = False
    isNodeScanned = False
    isRegionScanned = False

# For testing
cur.execute("SELECT count(*) FROM tweet_emotions;")
print(cur.fetchone())

# To write data to database
conn.commit()

# close the communication with the PostgreSQL
cur.close()