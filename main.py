import os
import sys
import pandas as pd
from datetime import datetime
from typing import List, Tuple, Dict

from Bani.Bani import Bani
from Bani.core.FAQ import FAQ
from Bani.core.generation import GenerateManager
from Bani.core.defaults import defaultGenerateManager

from Bani.generation.rajat_work.qgen.generator.symsub import SymSubGenerator
from Bani.generation.rajat_work.qgen.generator.fpm.fpm import FPMGenerator
from Bani.generation.rajat_work.qgen.encoder.dummy import dummyEN
from Bani.generation.rajat_work.qgen.generator.eda import EDAGenerator
from Bani.generation.sentAug.sentAug import AUG


class automation_training:
    def __init__(self):
        self.FAQSTORE_PATH = "./faqStore"
        self.CSV_PATH = "./csv_folder/"
        self.MODEL_PATH = "./generatedModel"

        self.faq_list = []  # to capture and store the name of FAQ
        self.generatorManager = self.generator_manager()

    def start_training(self):
        try:
            for file_name in os.listdir(self.CSV_PATH):
                if file_name.endswith(".csv"):
                    faq_name = file_name.partition('.')[0]
                    file_path = self.CSV_PATH+file_name
                    self.create_faq_from_csv(file_path, faq_name)
                    self.faq_list.append(faq_name)
                    
            loaded_faq_list = self.load_faq()
            bot = self.train_model(loaded_faq_list)
            self.test_trained_model(bot)

        except Exception as e:
            print("Exception: %s" % e)

    def generator_manager(self):
        names = ["SymSub", "FPM", "EDA", "nlpAug"]
        quantity = [3, 3, 3, 2]

        generatorManager = GenerateManager(
            producers=[
                SymSubGenerator(dummyEN("lite")),
                FPMGenerator(),
                EDAGenerator(),
                AUG(),
            ],
            names=names,
            nums=quantity,
        )
        return generatorManager

    def create_faq_from_csv(self, file_path, faq_name):
        df = pd.read_csv(file_path, header=None)
        questions = df.iloc[:, 0]
        answers = df.iloc[:, 1]

        faq_name = FAQ(
            name=faq_name, questions=questions, answers=answers)
        faq_name.buildFAQ(self.generatorManager)
        faq_name.save(self.FAQSTORE_PATH)  # save as .pkl
        print(f"{faq_name} created")

    def load_faq(self):
        loaded_faq_list = []  # contains a list of loaded FAQs
        for i in self.faq_list:
            faq_name = FAQ(name=i)
            faq_name.load(self.FAQSTORE_PATH)
            loaded_faq_list.append(faq_name)
            print("FAQ %s loaded! " % i)
        print(f"All FAQs loaded - {self.faq_list}")
        return loaded_faq_list

    def train_model(self, loaded_faq_list):
        # Create bot using the list of faq - loaded faqs
        bot = Bani(FAQs=loaded_faq_list, modelPath=None)
        print("--- Training Bot --- ")
        start_time = datetime.now()
        # Type of training: "batchHardTriplet", "contrastiveLoss", "tripletLoss", "softmaxLayerLoss"
        bot.train(self.MODEL_PATH, epochs=5, batchSize=64,
                  lossName="batchHardTriplet")
        bot.saveModel(self.MODEL_PATH)
        end_time = datetime.now()
        time_taken = end_time - start_time
        print(f"Bot training completed, model saved, time taken {time_taken}")

        with open(self.MODEL_PATH +"/model_info.txt", "w") as f:   
            f.write(f"Model Updated at {end_time}, Training Time ({time_taken}) with {self.faq_list}") 

        return bot

    def test_trained_model(self, bot):
        # read file from csv - append it as original and reframed questions - use bot.test
        print("--- Testing Model ---")
        df = pd.read_csv("CovidFAQs_test_questions(18).csv")
        testData = []

        for i in range(len(df)):
            original = df.loc[i, "Original"]
            re = df.loc[i, "Reframed"]
            testData.append([original, re])

        for e in range(len(self.faq_list)):
            acc = bot.test(e, testData)
            print(f"Accuracy using Bani's test method for faq {e}: {acc}")

        print("------")
        qn = "What is the prevailing permissible group size for social activities?"
        ans = bot.findClosest(qn)

        for i in range(len(self.faq_list)):
            print(f"FAQ {ans[i].faqId}, {ans[i].faqName},\
                max score: {ans[i].maxScore}, score {ans[i].score}, answer: {ans[i].answer}")

if __name__ == "__main__":
    main = automation_training()
    main.start_training()
    
