# Verbose-The-Indexer

Verbose the new way of searching local files. We are trying to implement this using hashing. Because O(1) >= O(*)

 Special Thanks to [Project Guntenburg](https://www.guntenburg.org), [20Newsgroup](http://qwone.com/~jason/20Newsgroups/ ) & various other sites for providing the dataset.
 
Efficiency in storing
 
 - Try1 : 22.5 MB of files indexed to ~54 MB saved data (using filename in each index)
 
 - Try 2 = 22.5 MB of files indexed to ~6.4 MB saved data (using filename in word itself) & 41.8 MB to ~8.7 MB
 
 - Try 3 (Yet To implement)(Encode every file to a association, basically will reduce key size of dictionary, can reduce mimum 15% dictionary size usage).
