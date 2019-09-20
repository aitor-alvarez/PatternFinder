# PatternFinder
An algorithmic framework for retrieving musical patterns from Renaissance music. 


## Installation

git clone https://github.com/aitor-mir/PatternFinder.git 

pip install -r requirements.txt

## Instructions

The following code finds and extracts patterns from a music midi file.

The following command python get_patterns.py 'obras/Ave_Maris_Stella-1-Kyrie.midi' runs the program, taking as input the path where the midi file is located.

The code outputs in the folder "output" 6 files: 'closed.txt', 'maximal.txt', 'minimal.txt' and their respective pattern file. These files represent intervallic patterns in sequences. Intervals are codified for each song by using Music21 chromatic step values, and encode interval direction with Boolean values (1 for ascending and 0 for descending).
