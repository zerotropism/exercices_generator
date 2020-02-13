## Specs:
Aims to generate 4 types of exercise based on video subtitles:
* "conjugation", 
* "fill the blanks",
* "punctuations",
* and "scramble".

### Requirements:
#### at OS level:
+ **sql-lib**: in case you do not have it on your linux-based machine : 
```bash
sudo apt install default-libmysqlclient-dev
```
#### at env level:
##### setup the conda packages:
+ **from anaconda channel**: `conda install -c anaconda numpy pandas nltk openpyxl beautifulsoup4`
+ **from conda-forge channel**: `conda install -c conda-forge spacy`
+ **from menpo channel**: `conda install -c menpo pathlib`
+ **the pattern library from github repo**: `git clone https://github.com/clips/pattern` or `git fetch` then
```bash
git checkout development
pip install mysqlclient
python setup.py install
```

##### setup the packages' features:
+ **spacy**: download datasets in different languages (here, English, German & French)
```bash
python -m spacy download en
python -m spacy download de
python -m spacy download fr
```
+ **nltk**: download nltk sublibraries from python itself
```python
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```

### Examples of subtitles:
You can find some examples of subtitles to use as input in our google drive, here: https://drive.google.com/drive/folders/1ZktjrJ6J4YOUr-EBUd0hzaRnFmZMf1BY

### Command line:
Command line syntax:
```bash
python main.py --generate <exercice_type> --subtitle <subtitle>
```
With:
+ **\<exercice_type\>:** { `conjugaison`; `fillblanks`; `ponctuations`; `scramble`; `all` }
+ **\<subtitle\>:** the path to subtitles file

### Exercices:
#### conjugaison:
This exercice will parse each sentence from the subtitle and will extract all conjugated verbs to build the exercice:
- **Sentence:** "This seemed like the smartest place to pick up a lot of different skills in one summer." 
- **Exercice:** "This ______ like the smartest place to pick up a lot of different skills in one summer."
- **Verb to conjugate in proposal:** "to seem"
- **Answer:** "seemed"

#### fill the blanks:
This exercice will parse each sentence from the the subtitle and will exrtact one word to fill:
- **Sentence:** "This seemed like the smartest place to pick up a lot of different skills in one summer."
- **Exercice:** "This seemed like the smartest place to ____ up a lot of different skills in one summer."
- **Proposal words to fill:** { "pick"; "choice"; "selection" }
- **Answer:** "pick"

#### punctutation:
This exercice will parse the whole subtitle and will extract all pontuations to fill:
- **Text:** "In the new movie The Internship, Vince. Vaughn and Owen Wilson play middle-aged out of work salesman that somehow land Google internships.. That's a sharpie by the way, genius.. That's my fault.. The movie focuses on a fierce competition among the interns to get full-time jobs at Google, but in real life, the challenge is just landing a Google internship.. It was immediately captivating.. New York native and Yale student,. Florian Collins Berger is an intern for the marketing department.. This seemed like the smartest place to pick up a lot of different skills in one summer.. I've never been put in an environment where work and play are so sort of seamlessly integrated and still felt productive.. He is one of the 1,500 interns selected this summer out of a record high pool of more than 40,000 applicants.. At that rate, it's harder to get into the Google internship program than into Harvard or Stanford.. Kyle Ewing heads the internship program.. There's no best way to get into Google, at the end of the day we're looking for students who are smart, who are creative, who are leaders, who are passionate inside and outside of work, who care about their community and who really care about technology.. Applicants must be full-time students, if they make it past the written application phase, they go through a series of phone and face-to-face interviews with questions reportedly ranging from coding to quirky.. In addition to the famous Google perks like free food, campus bikes and gym access, interns also get paid a competitive wage.. The average Google intern makes about 5,800 dollars per month.. If you're a software engineer intern at Google, you're making about. 6,500 dollars per month, even more and that's upwards of. 75,000 dollars per year.. 75,000 dollars per year is much higher than the average U.S. worker.. Interns are expected to complete a project and get hands on experience.. Even in my first few weeks, I'd put out code that everyone was using and it was really cool to call my mom and get to say like "Mom,. Mom look what I'm doing!"     Software engineer Kitt Vanderwater, interned for. Google for two summers, and is now a full-time employee.. As soon as I started my senior year I knew I'd have a job at Google and that was really great peace of mind.. Something most interns are hoping to get when they return for their senior year.. In San Francisco, I'm Kara Tsuboi,. CNET.com for CBS News."
- **Exercice:** "In the new movie The Internship  __  Vince  __  Vaughn and Owen Wilson play middle-aged out of work salesman that somehow land Google internships.. That 's a sharpie by the way  __  genius.. That 's my fault.. The movie focuses on a fierce competition among the interns to get full-time jobs at Google  __  but in real life  __  the challenge is just landing a Google internship.. It was immediately captivating.. New York native and Yale student  __   __  Florian Collins Berger is an intern for the marketing department.. This seemed like the smartest place to pick up a lot of different skills in one summer.. I 've never been put in an environment where work and play are so sort of seamlessly integrated and still felt productive.. He is one of the 1,500 interns selected this summer out of a record high pool of more than 40,000 applicants.. At that rate  __  it 's harder to get into the Google internship program than into Harvard or Stanford.. Kyle Ewing heads the internship program.. There 's no best way to get into Google  __  at the end of the day we 're looking for students who are smart  __  who are creative  __  who are leaders  __  who are passionate inside and outside of work  __  who care about their community and who really care about technology.. Applicants must be full-time students  __  if they make it past the written application phase  __  they go through a series of phone and face-to-face interviews with questions reportedly ranging from coding to quirky.. In addition to the famous Google perks like free food  __  campus bikes and gym access  __  interns also get paid a competitive wage.. The average Google intern makes about 5,800 dollars per month.. If you 're a software engineer intern at Google  __  you 're making about  __  6,500 dollars per month  __  even more and that 's upwards of  __  75,000 dollars per year.. 75,000 dollars per year is much higher than the average U.S. worker.. Interns are expected to complete a project and get hands on experience.. Even in my first few weeks  __  I 'd put out code that everyone was using and it was really cool to call my mom and get to say like `` Mom  __   __  Mom look what I 'm doing ! '' Software engineer Kitt Vanderwater  __  interned for  __  Google for two summers  __  and is now a full-time employee.. As soon as I started my senior year I knew I 'd have a job at Google and that was really great peace of mind.. Something most interns are hoping to get when they return for their senior year.. In San Francisco  __  I 'm Kara Tsuboi  __   __  CNET.com for CBS News  __ "
- **Answer:** ['.', ',', '.', ',', ',', ',', ',', '.', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', '.', ',', '.', ',', ',', '.', ',', '.', ',', ',', ',', '.', '.']

#### scramble (or shuffle):
This exercice will parse each sentence from the subtitle and will shuffle the words:
- **Sentence:** "This seemed like the smartest place to pick up a lot of different skills in one summer."
- **Exercice:** {'up', 'a', 'the', 'place', 'seemed', 'in', 'lot', 'summer.', 'one', 'smartest', 'pick', 'This', 'skills', 'to', 'like', 'different', 'of'}
- **Answer:** "This seemed like the smartest place to pick up a lot of different skills in one summer."

### On-going future features
- open questions
- MCQ
- UCQ
