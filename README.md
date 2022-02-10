# Negation detection

* the idea here is to extract the negations from a given text that can alter the snetiment of a text.
* for intance, 
  * “The Supplier may not terminate this Contract for convenience.”
  * “The Supplier may terminate this Contract for convenience”
  * the negation term to be extracted from the first sentence is "may not" which changes the meaning of the sentence.
* The approach for the solution present here is as follows:
  * have a list of negation words like no, not, without, neither, nor
  * extract the above words from the text and also the surrounding texts, so as to form a sentence.
  * obtain the N-grams of the above created sentence
  * apply snetiment analysis on these ngrams to obtain the sentiment score of each
  * The n-gram with the highest negative score will be negation
* once the negation is obtained, it is stored in an output file along with its character offset wtih respect to the text.

## Running the project
```sh
pip install -r requirements.txt
python3 extract_negations.py --input="demo.txt" --output="output.txt"
```
