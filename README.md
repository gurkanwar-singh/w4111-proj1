# w4111-proj1
Databases project 1

account: acc2193
URL:

Database Search
This is the basic database search tool that allows the user to search for players by name, maximum and minimum overall rating, and position. It also allows the user to select how the players are ordered by a specific attribute, an additional feature not mentioned before in part 1.
 
Sortbot
This tool allows users to view the best players based on a set of desired attributes. The user inputs three attributes, and the sortbot displays the players who are rated highest in the combined total of those specific attributes. 

Chemistry Tool
The chemistry tool we implemented is slightly different from the tool we described in part 1. We proposed to implement a tool that creates a team of 11 players given a smaller subset of players in order to maximize their team chemistry. However, this tool did not work well as it simply chose players from the same team as the user given players and there were many ties while determining which players to select. Instead, we implemented a tool that returned a score for the chemistry of a team given 10 user defined players in respective positions. 

Sortbot Page
This page implements the sortbot tool described above. There are three dropdown menus on this page in addition to the sortby, overall rating, and position inputs found on the database search page. The three dropdown menus allow the user to input attributes that they would like the sortbot to take into consideration when selecting players. These attributes are then passed into the database query such that the database takes the sum of the attributes for all the players and selects the name and attributes of the player who's sum is the highest. It then repeats this search creating a list of players who excel in the three attributes. This is interesting because it allows you to see how players of certain positions excel in similar attributes, and can give you an idea of how a player plays. 

Chemistry Page
This page implements the chemistry tool described above. This page has inputs for 10 field positions that the user can choose players to place into. These names are then entered into the database and their club team, national team, and position are retrieved. This required the use of nested queries in order to retrieve both club and national teams which have seperate team id's. Using these attributes, the chemistry is calculated. For example, players playing in their usual position and with players who they play with either on the same national team or club team will have a higher chemistry. This is interesting because it allows the user to see how well players from any team, around the world would play together.  
