# NL2CMD

"A model that can generate CMD (Command Prompt) commands based on natural language input." <br/>
<b>main.ipynb</b> contains the code for the following:
1. Preprocessing using: 
Using  tokenization, lowercasing, removing digits and punctuation, removing stop words, and stemming to the input and target text
2. Train , test, validation with BATCH_SIZE = 4
3. Seq to seq Model - Encoder, decoder, optimizer, and loss function
4. Grid search over hyperparameters
5. Accuracy metric: Blue score and our custom score


Dataset Used:
1. train_data.json
2. test_data.json
3.nl2bash-data.json

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
