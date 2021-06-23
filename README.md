# bani_training
 
Desciption: 

This is organised: 

- csv_folder will contains the csv file of the faqs where col 1 contains question and col 2 contains answer to the question. (No header)
- faqStore: after building faq, it will generate .pkl file of the faq which will be stored in this folder. The files in this folder is will be required to load faq to vreate bani bot for training. 
- generatedModel: store models files after training. 
- Covid FAQs_test_question(18).csv: sample question with paraphase wordings


To run main.py:
- without docker: virtual env will be required
- with docker: 
	1. docker build -t bani_training . 
	- without volume: 
		2. docker run -it bani_training
	- with volume: 
		2. docker run -it -v PATH_TO_FOLDER/generatedModel:/automation_training/generatedModel bani_training
