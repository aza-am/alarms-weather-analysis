The task is binary classification, and the requirements for algorithms are not only the ability to separate classes, but also to process data efficiently and minimize the number of missed dangers.


Key Metrics:


**ROC AUC**

This is the area under the error curve. It shows the overall ability of the model to distinguish between threat and calm.


**Recall** (Security Priority)

This metric answers the question: "What fraction of all real alarms were we able to predict?". For our project, this is the most important indicator. We maximized Recall to minimize the number of "missed" dangers, because the cost of a "False Negative" error is important.


**Accuracy** (Confidence Level)

Shows how often the "Alarm" prediction turns out to be true. High accuracy helps avoid the effect of "alarm fatigue": if the model gives false predictions (False Positives) too often, users will stop trusting it.


**F1 Score (Balance)**

This is the harmonious average between accuracy and completeness. We use this metric to make sure that the pursuit of safety (Recall) has not turned the model into a "panic hunter" who sees danger where there is none.


**Balanced Accuracy**

Unlike regular Accuracy, this metric calculates the arithmetic average between the completeness for both classes (alarm and calm). This is critical: if the model is perfectly guessing "calm" but fails all "alarms", the regular accuracy will still be high (~80-90%), while the balanced accuracy will immediately drop to 0.5 (50%). (Our result of 0.75+ confirms that the model works equally well with both states.)


**MCC (Matthews Correlation Coefficient)**

This is probably the most rigorous and honest metric in machine learning. It takes into account all four cells of the error matrix simultaneously: +1 means perfect prediction, 0 means random guessing, -1 means complete mismatch. (An MCC above 0.4–0.5 in our complex topic is a good result, as it proves the presence of a strong statistical relationship between our 227 features and the real danger.)
