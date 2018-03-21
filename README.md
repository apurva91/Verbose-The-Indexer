# Verbose-The-Indexer

Verbose is a python based application which helps you to search in txt as well as pdf files easily by using indexing and providing a good User Interface.

Setting Up

```
sudo apt-get install libgtk-3-dev
pip3 install -r requirements.txt
```

To run

```
python3 main.py
```

### Salient Features:

* Multiple Word Searching
* Stemming of Words (Eg:- Spelling -> spell; heroes -> hero). This feature helps us to ignore the form of verbs 
* Did You Mean:- If a particular word is not found then we apply did you mean to get results
* Exact Searching:- If the query is contained in quotes then the results will contain exactly those results otherwise it may be in some other order. ( Eg:- searching for good boy will show both good boy as well as boy good, but when exact search is selected “good boy” only results of good boy will be shown.
* Saving of Indexes:- Once you have indexed a file we save the indexes of it so that we don’t have to wait again for indexing it.
* GUI:- GTK+ has been used to make User Interface for this application, the key benefit of using this is it adapts to the theme you are using on your desktop
* Recent Searches:- Recent searches are stored in a file so that whenever you run you have them with you
* Searches for both PDF as well as txt files.
* On click of a particular result the file opens from that particular Page Number or Line Number of File where the occurrence is present.
* Ranking is done by TF-IDF algorithm

### Data Structures:

The data structures used in the project are Dictionary, Lists and Sets.

* Main Index Dictionary = { Word : { Book : { Page/Line : [occurrences] } } }

* Individual File Dictionary(The one that is saved) = { Word : { Page/Line : [occurrences] } }

* Answer = { Book : [Page/Line Numbers] }



### References:
* Peter Norvig's Did You Mean Implementation [Link](norvig.com/spell-correct.html)

* Quora's answer that gave us basic idea [Link](http://qr.ae/TU1TXh)

* GTK+ Documentation [Link](https://python-gtk-3-tutorial.readthedocs.io/en/latest/)

* Dataset by [Project Guntenburg](https://www.guntenburg.org), [20Newsgroup](http://qwone.com/~jason/20Newsgroups/ ) & various other sites.
