# Verbose-The-Indexer

Verbose the new way of searching local files. We are trying to implement this using hashing. Because O(1) >= O(*)

 
 Efficiency in storing
 
 Try 1 = 22.5 MB of files indexed to ~54 MB saved data (using filename in each index)
 
 Try 2 = 22.5 MB of files indexed to ~6.4 MB saved data (using filename in word itself) & 41.8 MB to ~8.7 MB
 
 Try 3 (Encode every file to a association, Can use a sort of structe like huffman coding will surely reduces it 1/2 of its size ~3MB, basically will reduce inhand memory).
