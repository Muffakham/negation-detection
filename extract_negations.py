from flair.models import TextClassifier
from flair.data import Sentence
import re
import string
import argparse


NEGATION_WORDS = ["no", "without", "illegal","nil","not", "n't", "never","notwithstanding", "none", "neither", "nor", "non","subside","retract","reject","denied","deny","retracted","refused","refuse"]
class extractNegations():
  """
  A class module to extract the negations from a given text
  Input - text file containing data (input file name and the file name to store negations)
  output - negations extracted from the input and stored in file along with their character offsets
  Description:
    The idea here is to extract the negations (words in the list mentioned above)
    along with their neighboring 3 words on each side.

    Now that we have a sentence containing negations, we obtain the n-grams of this sentence,
    pass these ngrams to sentiment analysis model and obtain sentiment score.
    The n-gram having the most negative score is selected as negation.
  """
  
  def __init__(self,inputFileName,outputFileName):

    """
    Intialising function
    Intialises the classfier for sentiment analysis, reads the data 
    from the file and removex the new line character from the text.
    """
    self.classifier = TextClassifier.load('en-sentiment')
    with open(inputFileName, 'r') as inputFile:
      self.text = inputFile.read()#reading data
    inputFile.close()
    self.text = self.text.replace("\n", "")#removing new line character
    self.outputFile = open(outputFileName,'w')#opening the output file
    self.wordList = self.text.split()#creating a list of words for the text
    
  def generate_N_grams(self,text,ngram=1):
    """
    this function generates the ngrams of a text
    Input - text, ngram range
    output list of n-grams (unigram,bigram depending upon ngram range)
    """
    words=[word for word in text.split(" ")]  
    temp=zip(*[words[i:] for i in range(0,ngram)])
    ans=[' '.join(ngram) for ngram in temp]
    return ans

  def getNGrams(self,match, negatedWord, ngramArray=[]):
    """
    function to convert text to N-grams with the max value of N as one less than the lenght of text.
    Inputs - match(text), the negated word from the negation list, array to store n-grams
    Outputs - n-gram array (consisting of unigram, bigram, trigram ..... n-1 gram)
    keypoint -  this function only generates the n-gram which contain the negated word extracted
    """
    for i in range(1,len(match.split(" "))-1):
      for j in self.generate_N_grams(match,i):
        if negatedWord in j:
          ngramArray.append(j)
    return ngramArray


  def getNegation(self,match,negatedWord):
    """
    function to run sentiment analysis model on given n-grams
    input - text, the negation word extracted
    output - the actual negation associated with the negation word extracted.
    funcitonality - 
      this function takes in the text(sentence containing negation word and its surrounding words)
      obtains the n-grams of the text
      applies sentiment analysis model on n-grams to obtain their sentiment score
      selects the n-gram with most negative score as the negation
    """
    ngrams = self.getNGrams(match,negatedWord,[]) #obtaing ngrams
    score = []
    for i in ngrams:

      sentence = Sentence(i)
      self.classifier.predict(sentence)#obtaining sentiment scores for every n-gram
      label = str(sentence.labels)
      if 'POSITIVE' not in label:#considering only negrative sentiments
        score.append([float(label.split("(")[1].split(")")[0])*10000,i])#extracting score and storing it
    
    listOfTerms = [x[1] for x in score]
    if score:
      for i,j in score:
        if negatedWord not in listOfTerms:#considering the ngrams which contain the negation wword extracted
          return negatedWord
        else:
          returnVal = max(score, key=lambda x:x[0])[1]#maximum negative score n-grAM 
          if negatedWord not in returnVal:
            return negatedWord
          else:
            return returnVal
    else:
      return negatedWord

  def writeNegationsToFile(self, negationTerm):
    """
    FUNCTION TO extract the start and end indices of negations and store them in a file
    takes in the negation word to be extracted
    writed the negations associated with the term in a file
    """
    indices = (i for i,word in enumerate(self.wordList) if word==negationTerm)#extracting the negation term
    for ind in indices:#location of all the words that have negation term
      neighbors = []
      #otnaining the neiighboring words for the negation term
      if ind-4 < 0:
        pre = self.wordList[:ind]
      else:
        pre = self.wordList[ind-4:ind]
      if ind+4 > len(self.wordList):
        post = self.wordList[ind:]
      else:
        post = self.wordList[ind:ind+4]
      neighbors.append(pre+post)
      sentence = " ".join(neighbors[0] if neighbors else [])#creating a sentence to extract n-grams from 
      negatedTerms = self.getNegation(sentence,negationTerm)
      print(negatedTerms)
      try:
        #extracting the index of obtained negation with respect to the text
        matchForSentenceinText = re.search(sentence, self.text)
        startSent,endSent = matchForSentenceinText.span()
        matchForNegatedTermInSentence = re.search(negatedTerms, sentence)
        negatedTermStart,negatedTermEnd = matchForNegatedTermInSentence.span()
        print((startSent+negatedTermStart, startSent+negatedTermEnd))
        self.outputFile.write("("+str(startSent+negatedTermStart)+","+str(startSent+negatedTermEnd)+") "+negatedTerms+"\n")
      except:
        continue

  def run(self):
    for i in NEGATION_WORDS:
      if i in self.text:
        self.writeNegationsToFile(i)
    self.outputFile.close()


def main(filename, outputFile):
  obj = extractNegations(filename,outputFile)
  obj.run()
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument('--input',
                        type=str,
                        default = "demo.txt",
                        dest="input_file",
                        help='file path to the input data to preprocess.'
                             'Example path: "./demo.txt"')
    parser.add_argument('--output',
                        type=str,
                        default = "output.txt",
                        dest="output_file",
                        help='file path to store data.'
                             'Example path: "./output.txt"')

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    main(input_file,output_file)

