from sklearn.model_selection import ShuffleSplit

from EegClassification.structs.TestTrainStruct import TestTrainStruct


class AbstractClassifierRunner:
    def run_model(self, model, test_train_struct: TestTrainStruct, shuffle_split: ShuffleSplit):
        val_results = []
        test_results = []

        for train, validation in shuffle_split.split(test_train_struct.get_x_train()):
            validation_metrics = model.fit(x_train=test_train_struct.get_x_train()[train],
                                           y_train=test_train_struct.get_y_train()[train],
                                           x_val=test_train_struct.get_x_train()[validation],
                                           y_val=test_train_struct.get_y_train()[validation])
            val_results.append(validation_metrics)

            test_metrics = model.evaluate(x=test_train_struct.get_x_test(),
                                          y=test_train_struct.get_y_test())
            test_results.append(test_metrics)

        return [val_results, test_results]
