# Building Question Answer Agent – Bani Bot (1)

**Bani's Model Training**</br>

## Description

Creating the question answer agent begins with the training of dataset on a pretrained model using the package, Bani: https://github.com/captanlevi/Bani. Training is ran using training script and loading of Bani bot is ran as another process.

## Installation/ Set up:

- Ensure docker is available on your machine. </br>
- Create 2 docker volume (this can be done via docker app or using command line). </br>
  - 1 volume: Store faq store files (.pkl) after building of FAQ classes. </br>
  - 1 volume: Store generated model files, after bot training has been completed. </br>
- Placed FAQs files in the csv_folder. </br>

## Steps:

- Access to the project directory. </br>
- Build docker image: docker build -t bani_training_script .</br>
- Run docker image with created volume: </br>

```bash
docker run -v $(pwd):/bani_training -it --mount source=model_vol_name,target=/model --mount source=faq_vol_name,target=/faq_store bani_training_script
```

## To note:

**FAQ file:**</br>

- Each FAQ file contains question and answer for 1 topic. </br>
- The first column is the question, second column is the answer. Question and answer data begins on the first line (no header).</br>
- File should be available in a CSV format. </br>

**Volume:**</br>

- Subsequent training of FAQ classes with the same file name will overwrite the FAQ files in the faq_store volume. </br>
- If subsequent training does not support a topic that was trained previously, do remove the files in the volume, in case there may be issue with loading of bot for answering. </br>
