# This is the main API that users interact with LEAP. Users
# will create an instance of the LEAP class and can either
# set their own user defined functions or use one of the func-
# tions available in LEAP

import LeapApi.codes as codes

class Leap():

    # Constructor that takes in a code representing one of
    # the available algorithms in Leap.
    def __init__(self, algo_code):
        self.algo_code = algo_code
        self.__map_fn = None
        self.__agg_fn = None
        self.__choice_fn = None
        self.__update_fn = None
        self.__stop_fn = None
        self.__data_prep_fn = None
        self.__setup_fn = None
        self.__postprocessing_fn = None

    # Returns an instance of the Leap class that will count
    # the number of selected records.
    def Count(self):
        return Leap(codes.COUNT)

    # Returns an instance of the Leap class that will compute
    # a summation of selected records.
    def Sum(self):
        return Leap(codes.SUM)

    # Returns an instance of the Leap class that will compute
    # the variance of selected records.
    def Variance(self):
        return Leap(codes.VARIANCE)

    # Returns an instance of the Leap class that can fit a
    # federated learning model.
    def FederatedLearning(self):
        return FedLearn(codes.FEDERATED_LEARNING)

    # Sets the map function of the algorithm to be a user
    # defined map function.
    #
    # map_fn: User defined map function.
    def set_map_fn(self, map_fn):
        self.__map_fn = map_fn

    # Sets the aggregation function of the algorithm to be a
    # user defined aggregation function.
    #
    # agg_fn: User defined aggregate function.
    def set_agg_fn(self, agg_fn):
        self.__agg_fn = agg_fn

    # Sets the choice function of the algorithm to be a user
    # defined choice function.
    #
    # choice_fn: User defined choice function.
    def set_choice_fn(self, choice_fn):
        self.__choice_fn = choice_fn

    # Sets the update function of the algorithm to be a user
    # defined update function.
    #
    # update_fn: User defined update function.
    def set_update_fn(self, update_fn):
        self.__update_fn = update_fn

    # Sets the stop function of the algorithm to be a user
    # defined stop function.
    #
    # stop_fn: User defined stop function.
    def set_stop_fn(self, stop_fn):
        self.__stop_fn = stop_fn

    # Sets the data prep function of the algorithm to be a
    # user defined data prep function.
    #
    # data_prep_fn: User defined data prep function.
    def set_data_prep_fn(self, data_prep_fn):
        self.__data_prep_fn = data_prep_fn

    # Sets the setup function of the algorithm to be a user
    # defined setup function.
    #
    # setup_fn: User defined setup function.
    def set_setup_fn(self, setup_fn):
        self.__setup_fn = setup_fn

    # Sets the postprocessing function of the algorithm to be
    # a user defined postprocessing function.
    #
    # postprocessing_fn: User defined postprocessing function.
    def set_postprocessing_fn(self, postprocessing_fn):
        self.__postprocessing_fn = postprocessing_fn


# Federated Learning class that extends the main Leap class.
class FedLearn(Leap):
    def __init__(self, algo_id):
        super().__init__(algo_id)
        self.optimizer = None
        self. model = None
        self. criterion = None

    # Sets the optimizer for federated learning to be the
    # optimizer given as a parameter.
    #
    # optimizer: Optimizer for federated learning
    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    # Sets the model for federated learning to be the model
    # given as a parameter.
    #
    # model: Model for federated learning.
    def set_model(self, model):
        self.model = model

    # Sets the criterion for federated learning to be the
    # criterion given as a parameter.
    #
    # criterion: Criterion for federated learning.
    def set_criterion(self, criterion):
        self.criterion = criterion
