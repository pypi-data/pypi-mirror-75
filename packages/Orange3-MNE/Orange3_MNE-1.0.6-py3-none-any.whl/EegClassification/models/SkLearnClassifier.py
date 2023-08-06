from sklearn import metrics


class SkLearnClassifier:
    def __init__(self, model):
        self.model = model

    def get_model(self):
        return self.model

    def fit(self, x_train, y_train, x_val, y_val):
        """
        Fits the model using training data
        Taken from original source code: https://bitbucket.org/lvareka/cnnforgtn/src/eb1327b165c02b8cb1dce6059df163117086a357/models/sklearnclassifier.py#lines-23

        :param x: x[number of examples x number of channels x samples in each epoch x 1]
        :param y: y[number of examples x number of categories - default 2]
        :param x_val: validation data to evaluate
        :param y_val: validation data to evaluate
        """
        if x_train.ndim == 4:
            x_train = x_train.reshape((x_train.shape[-4], -1))

        if len(y_train.shape) > 1:
            self.model.fit(x_train, y_train[:, 0])
        else:
            self.model.fit(x_train, y_train)

        return self.evaluate(x_val, y_val)

    def evaluate(self, x, y):
        """
        Evaluates the classifier using testing data:
        Taken from original source code: https://bitbucket.org/lvareka/cnnforgtn/src/eb1327b165c02b8cb1dce6059df163117086a357/models/sklearnclassifier.py#lines-35

        :param x: [number of examples x length of each feature vector]
        :param y: [number of examples x number of categories - default 2]
        :return: [(loss) accuracy precision recall]
        """
        predictions = []
        real_outputs = []
        for i in range(x.shape[0]):
            pattern = x[i, :].reshape(1, -1)
            prediction = self.model.predict(pattern)
            predictions.append(prediction[0])

            if len(y.shape) > 1:
                real_outputs.append(y[i, 0])
            else:
                real_outputs.append(y[i])

        acc = metrics.accuracy_score(real_outputs, predictions)
        try:
            auc = metrics.roc_auc_score(real_outputs, predictions)
            prec = metrics.precision_score(real_outputs, predictions)
            recall = metrics.recall_score(real_outputs, predictions)
            return [acc, auc, prec, recall]
        except ValueError as err:
            print(err)

        return [acc]
