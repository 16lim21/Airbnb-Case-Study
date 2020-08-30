This was done as part of a case study project for LionBase. 

### The prompt
Using historical NYC data from AirBnB, identify a problem or opportunity and discuss how you would address it. The main goal is to deliver analytical insights backed by real data and models. You can choose how much data to use, what kind of data to use, and whether or not you want to bring in outside data. Clearly state and justify any assumptions you make. When thinking about a problem or opportunity, think about how it could add actual business value. http://insideairbnb.com/get-the-data.html - Please use the New York City data

### The project
As part of the case study, I created a program that allowed you to search for the top keywords that appeared in different neighborhoods withing NYC as well as allowing you to search for the neighborhoods that did or did not have a keyword associated with it in the reviews. I used python's natural language toolkit to filter only adjective keywords. 

### To run the program
Note: If the folder already contains the files fullData.json and topData.json (which it should), just run the airbnb.py file. You can answer “yes” when asked if the neighborhood files were processed. 

If json files are not there, download the data from the link below then unzip the data. 
https://drive.google.com/file/d/1Xx0e6OjOHL4vunPEzRXExrPIdrAS0qt-/view?usp=sharing

Unzip the Data.zip file to create the data folder with the CSVs.
Open the Jupyter notebook and run all cells to create the database file. 
Then run the airbnb.py file to run the search in terminal or any other IDE. Answer no when asked if the neighborhood files were processed. The main method should ask a series of questions involving the search process. 

The Jupyter notebook was used to create the database file from the data and to test out sql implementations in python.
