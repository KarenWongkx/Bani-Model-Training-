# Bani's Model Training 
 
Desciption: 

This make use of bani package for training of question and answering model. It first extract question and answer from csv files before creating a FAQ class for it. Created FAQ class will generate .pkl file which is saved into the faq_store. .pkl files are loaded before it is used for traning of bot. Output of the model will be saved into the model folder. 

File structure:
- csv_folder will contains the csv file of the faqs where column 1 contains question and column 2 contains answer to the question. (No header)
- Docker Volume:
    1. /faq_store: to hold generated .pkl files
    2. /model: to hold generated model files

Execution: 

1. Create volume for /faq_store and /model via docker desktop or commmand line interface.
2. Build docker image: docker build -t bani_training_script .
3. Run docker image: docker run -v $(pwd):/bani_training -it --mount source=bani_model,target=/model --mount source=bani_faq,target=/faq_store bani_training_script 
