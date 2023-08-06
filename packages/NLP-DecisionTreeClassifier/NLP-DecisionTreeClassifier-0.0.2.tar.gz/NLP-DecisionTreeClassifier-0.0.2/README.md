# NLP-DecisionTreeClassifier
Sci-kit Learn Decision Tree Classifier for identifying word entities in text 

# Installation Instructions!
pip install NLP-DecisionTreeClassifier

To train a model using this Decision Tree Classifier, you need to provide a text file,
that it will be trained on. Example large_text_file.txt

1. Call get_sentences_from_text(file_path)
The file path is the route to the text file
2. Call sentence_processor(file_path, sentence)
This is the same file_path, the sentence parameter is step 1.
3. Call train_model(model_name, file_path_model)
The model name will be the model file's name, saved in the file path.

After training you can get accuracy scores for the model, or predict on unseen data

