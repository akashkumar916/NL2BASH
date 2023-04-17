# NL2CMD

"A model that can generate Bash commands based on natural language input." <br/>
<b>main.ipynb</b> contains the code for the following:<br><br>
<b>Preprocessing</b>: The code in main.ipynb includes preprocessing steps such as tokenization, lowercasing, removing digits and punctuation, removing stop words, and stemming for both the input and target text. These steps are applied to the training, testing, and validation datasets to clean and prepare the data for model training.

<b>Train, Test, and Validation</b>: The code includes splitting the dataset into train, test, and validation sets with a defined batch size of 4. The training set is used to train the seq-to-seq model, while the test and validation sets are used to evaluate the model's performance during and after training.

<b>Seq-to-Seq Model</b>: The code includes the implementation of a seq-to-seq model, which consists of an encoder and a decoder. The encoder processes the input text and converts it into a fixed-size vector representation, while the decoder generates the output sequence (Bash command) based on the encoded input vector. The model is optimized using an optimizer, and a loss function is used to calculate the difference between the predicted output and the ground truth output (target Bash command).

<b>Grid Search for Hyperparameters</b>: The code includes a grid search over hyperparameters to fine-tune the model's performance. Hyperparameters such as learning rate, batch size, and number of epochs are tuned to optimize the model's accuracy and performance.

<b>Accuracy Metric</b>: The code includes the calculation of two accuracy metrics - Bleu score and a custom score. Bleu score is a standard evaluation metric used in natural language processing tasks, which measures the similarity between the generated Bash commands and the ground truth Bash commands. The custom score is a metric specifically designed for this task, which takes into consideration the correctness and relevance of the generated Bash commands based on the input natural language query.

<b>Dataset</b>: The code uses three datasets - train_data.json, test_data.json, and nl2bash-data.json. These datasets contain examples of natural language queries and their corresponding Bash commands, which are used for training, testing, and evaluating the seq-to-seq model. The datasets are loaded, preprocessed, and split into train, test, and validation sets for model training and evaluation.


Dataset Used:
1. train_data.json<br>
2. test_data.json<br>
3. nl2bash-data.json<br>

Sample data:
<pre>
{
  {
invocation:	'Copy loadable kernel mod…matchig current kernel.',
cmd:	"sudo cp mymodule.ko /lib…ame -r)/kernel/drivers/" }
  {
invocation:	`Display all lines contai…mpile-time config file.`,
cmd:	"cat /boot/config-`uname -r` | grep IP_MROUTE" }
}
</pre>


Presentation link: https://docs.google.com/presentation/d/1kNCmtRllG1YTMObrwn8hrcfUrs3nHUDcsIBkTQuCa2w/edit#slide=id.p<br/>

References : https://arxiv.org/pdf/1802.08979.pdf

Reserach Paper: https://www.overleaf.com/project/6407a0603bfd14ed931794eb
