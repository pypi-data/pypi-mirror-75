import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold

class Regressor:
    def __init__(self):
      tf.random.set_seed(2020)
      #lists to coefficient values
      self.loss_values = []

##################################### HUPOTHESIS FUNCTION ######################################
    def hypothesis(self, Xdata):
      h = self.k*tf.matmul(Xdata,self.WeightX)/(self.RNI - self.k * self.WeightY) + self.Bias
      return h
###################################### LOSS FUNCTIONS ##########################################

    def get_loss_logcosh(self):
        loss = tf.keras.losses.LogCosh()
        loss = loss(self.y, self.hypothesis(self.X))
        return loss

    def get_loss_Huber(self):
        loss1 = tf.reduce_mean(tf.math.abs(y_true - y_pred))
        if loss1 > self.delta:
          loss = loss1
        else:
          loss = tf.reduce_mean(tf.square(y_pred - y_true))
        return loss

    def get_loss_MeanSquaredError(self):
        loss = tf.keras.losses.MeanSquaredError()
        loss = loss(self.y, self.hypothesis(self.X))
        #print(loss)
        return loss

    def get_loss_MeanAbsoluteError(self):
        loss = tf.keras.losses.MeanAbsoluteError()
        loss = loss(self.y, self.hypothesis(self.X))
        return loss

    def get_loss_MeanAbsolutePercentageError(self):
        loss = tf.keras.losses.MeanAbsolutePercentageError()
        loss = loss(self.y, self.hypothesis(self.X))
        return loss

    def get_loss_Poisson(self):
        loss = tf.keras.losses.Poisson()
        loss = loss(self.y, self.hypothesis(self.X))
        return loss
#######################################################################################

    def t_get_loss_logcosh(self):
        loss = tf.keras.losses.LogCosh()
        loss = loss(self.y_test, self.hypothesis(self.X_test))
        return loss

    def t_get_loss_Huber(self):
        loss1 = tf.reduce_mean(tf.math.abs(self.y_test - self.hypothesis(self.X_test)))
        if loss1 > self.delta:
          loss = loss1
        else:
          loss = tf.reduce_mean(tf.square(self.hypothesis(self.X_test) - self.y_test))
        return loss

    def t_get_loss_MeanSquaredError(self):
        loss = tf.keras.losses.MeanSquaredError()
        loss = loss(self.y_test, self.hypothesis(self.X_test))
        #print(loss)
        return loss

    def t_get_loss_MeanAbsoluteError(self):
        loss = tf.keras.losses.MeanAbsoluteError()
        loss = loss(self.y_test, self.hypothesis(self.X_test))
        return loss

    def t_get_loss_MeanAbsolutePercentageError(self):
        loss = tf.keras.losses.MeanAbsolutePercentageError()
        loss = loss(self.y_test, self.hypothesis(self.X_test))
        return loss

    def t_get_loss_Poisson(self):
        loss = tf.keras.losses.Poisson()
        loss = loss(self.y_test, self.hypothesis(self.X_test))
        return loss

#######################################################################################
    def get_loss_defMSE(y_true,y_pred):
        loss = tf.reduce_mean(tf.math.square(y_true - y_pred))
        #print(loss)
        return loss

########################################## OPTIMIZING FUNCTIONS #########################
    def opt_Adadelta(self, lr):
      opt = tf.keras.optimizers.Adadelta(learning_rate=lr , rho = self.rho, epsilon = self.epsilon)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Adagrad(self, lr):
      opt = tf.keras.optimizers.Adagrad(learning_rate=lr, initial_accumulator_value = self.initial_accumulator_value)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Adam(self, lr):
      opt = tf.keras.optimizers.Adam(learning_rate=lr, beta_1=self.beta_1, beta_2=self.beta_2, epsilon=self.epsilon, amsgrad=self.amsgrad)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Adamax(self, lr):
      opt = tf.keras.optimizers.Adamax(learning_rate=lr, beta_1=self.beta_1, beta_2=self.beta_2, epsilon=self.epsilon)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Ftrl(self, lr):

      opt = tf.keras.optimizers.Ftrl(learning_rate=lr, learning_rate_power=self.learning_rate_power, 
                                      initial_accumulator_value=self.initial_accumulator_value,
                                      l1_regularization_strength=self.l1_regularization_strength, l2_regularization_strength=self.l2_regularization_strength,
                                      l2_shrinkage_regularization_strength=self.l2_shrinkage_regularization_strength)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Nadam(self, lr):
      opt = tf.keras.optimizers.Nadam(learning_rate=lr, beta_1=self.beta_1, beta_2=self.beta_2, epsilon=self.epsilon)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_RMSprop(self, lr):
      opt = tf.keras.optimizers.RMSprop(learning_rate=lr, rho = self.rho, epsilon = self.epsilon, momentum = self.momentum, centered = self.centered)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_SGD(self, lr):
      opt = tf.keras.optimizers.SGD(learning_rate=lr, momentum=self.momentum, nesterov=self.nesterov)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_GD(self,lr):
        with tf.GradientTape() as t:
            wx_grad, b_grad, wy_grad, rni_grad = t.gradient(self.get_loss(), [self.WeightX, self.Bias, self.WeightY, self.RNI] )

        self.WeightX.assign_sub(lr * wx_grad)
        self.Bias.assign_sub(lr * b_grad)
        self.WeightY.assign_sub(lr * wy_grad)
        self.RNI.assign_sub(lr * rni_grad)

######################################################################################


    def fit(self,train_x=None, train_y=None, test_x=None, test_y=None, CCapacity=None,  optimizer="SGD", loss_function="MSE", delta = 1, rho=0.95, 
            epsilon=1e-07, initial_accumulator_value=0.1, beta_1=0.9, beta_2=0.999, 
            amsgrad=False,
            learning_rate_power=-0.5, 
            l1_regularization_strength=0.0, 
            l2_regularization_strength=0.0,
            l2_shrinkage_regularization_strength=0.0,
            momentum=0.0,
            centered=False,
            nesterov=False):

      '''

      LOSSES:
      --------
      logcosh = get_loss_logcosh
      huber = get_loss_Huber
      MSE = get_loss_MeanSquaredError
      MAE = get_loss_MeanAbsoluteError
      MAPE = get_loss_MeanAbsolutePercentageError
      Poisson = get_loss_Poisson
      sqr_hinge = get_loss_SquaredHinge

      OPTIMIZERS:
      ------------

      Adadelta
      Adagrad
      Adam
      Adamax
      Ftrl
      Nadam
      RMSprop
      SGD
      GD

      '''

      self.Xdata = train_x
      self.ydata = train_y
      self.validation = False
      if test_x is not None and test_y is not None:
          self.validation = True
          self.Xtest = test_x
          self.ytest = test_y





      self.k =  max(train_y)+0.1
      if CCapacity is not None:
        self.k=CCapacity+0.1
      #initializing Weights, Bias and RNI 
      self.WeightX = tf.Variable(tf.random.normal( [self.Xdata.shape[1], 1 ], mean=0.0) )
      self.Bias = tf.Variable(tf.random.normal([1], mean=0.0))
      self.WeightY = tf.Variable(tf.random.normal([1], mean=0.0))
      self.RNI = tf.Variable(tf.random.normal([1], mean=0.0))

      self.delta = delta

      self.rho = rho
      self.epsilon = epsilon
      self.initial_accumulator_value = initial_accumulator_value
      self.beta_1 = beta_1
      self.beta_2 = beta_2
      self.amsgrad = amsgrad
      self.learning_rate_power=learning_rate_power
      self.initial_accumulator_value=initial_accumulator_value
      self.l1_regularization_strength=l1_regularization_strength
      self.l2_regularization_strength=l2_regularization_strength
      self.l2_shrinkage_regularization_strength=l2_shrinkage_regularization_strength
      self.momentum = momentum
      self.centered = centered
      self.nesterov = nesterov



  #-----------------------------------------------------------------
      if loss_function == "logcosh": self.get_loss = self.get_loss_logcosh; self.t_get_loss = self.t_get_loss_logcosh;
      elif loss_function == "huber": self.get_loss = self.get_loss_Huber; self.t_get_loss = self.t_get_loss_Huber;
      elif loss_function == "MSE": self.get_loss = self.get_loss_MeanSquaredError;  self.t_get_loss = self.t_get_loss_MeanSquaredError;
      elif loss_function == "MAE": self.get_loss = self.get_loss_MeanAbsoluteError; self.t_get_loss = self.t_get_loss_MeanAbsoluteError;
      elif loss_function == "MAPE": self.get_loss = self.get_loss_MeanAbsolutePercentageError; self.t_get_loss = self.t_get_loss_MeanAbsolutePercentageError;
      elif loss_function == "Poisson": self.get_loss = self.get_loss_Poisson; self.t_get_loss = self.t_get_loss_Poisson;
      else: print("Incorrect Loss function chosen"); return 0

  #------------------------------------------------------------------
      if optimizer == "Adadelta": self.optimizer=self.opt_Adadelta
      elif optimizer == "Adagrad": self.optimizer=self.opt_Adagrad
      elif optimizer == "Adam": self.optimizer=self.opt_Adam
      elif optimizer == "Adamax": self.optimizer=self.opt_Adamax
      elif optimizer == "Ftrl": self.optimizer=self.opt_Ftrl
      elif optimizer == "Nadam": self.optimizer=self.opt_Nadam
      elif optimizer == "RMSprop": self.optimizer=self.opt_RMSprop
      elif optimizer == "SGD": self.optimizer=self.opt_SGD
      elif optimizer == "GD": self.optimizer=self.opt_GD
      else : print("Incorrect Optimizer chosen"); return 0
  #------------------------------------------------------------------

    def train(self,epochs=2000, lr=0.009, progress_per=100):
        self.epochs = epochs
        self.lr = lr
        self.temp_loss = 99999999
        self.loss_score = 0

        if self.validation == False:
          self.X = tf.convert_to_tensor(self.Xdata, dtype=tf.float32)
          self.y = tf.convert_to_tensor(self.ydata, dtype=tf.float32)
          for epoch_count in range(1, self.epochs+1):
                  self.optimizer(self.lr)
                  train_loss  = self.get_loss().numpy()
                  self.loss_values.append(train_loss)

                 

                  if train_loss<self.temp_loss:
                      self.temp_loss = train_loss
                      self.h_WeightX = self.WeightX
                      self.h_Bias = self.Bias
                      self.h_WeightY = self.WeightY
                      self.h_RNI = self.RNI

                  if progress_per != None and epoch_count % progress_per == 0:
                      print("Epoch: %i, loss: %f "% (epoch_count,train_loss))
          self.loss_score = train_loss

          print("Training Completed")

        else:
            self.val_acc_scores = {
                'train_acc':[],
                'test_acc':[],
                'train_loss':[],
                'test_loss':[],
            }
            fold_count = 0
            self.X = tf.convert_to_tensor(self.Xdata, dtype=tf.float32)
            self.y = tf.convert_to_tensor(self.ydata, dtype=tf.float32)
            
            self.X_test = tf.convert_to_tensor(self.Xtest, dtype=tf.float32)
            self.y_test = tf.convert_to_tensor(self.ytest, dtype=tf.float32)
            
            for epoch_count in range(1, self.epochs+1):
                  self.optimizer(self.lr)
                  train_loss = self.get_loss().numpy()
                  self.loss_values.append(train_loss)

                  if train_loss<self.temp_loss:
                        self.temp_loss = train_loss
                        self.h_WeightX = self.WeightX
                        self.h_Bias = self.Bias
                        self.h_WeightY = self.WeightY
                        self.h_RNI = self.RNI
              

                  test_loss = self.t_get_loss().numpy()


                  self.val_acc_scores['train_loss'].append(train_loss)
                  self.val_acc_scores['test_loss'].append(test_loss)


                  if progress_per != None and epoch_count % progress_per == 0:
                      print("Epoch: %i, train_loss: %f, test_loss: %f "% (epoch_count, train_loss, test_loss))
            print("Training Completed")

    def predict(self,X_data):
        X_data = tf.convert_to_tensor(X_data,  dtype=tf.float32)
        # pred_y = self.k*tf.matmul(X_data,self.WeightX)/(self.RNI - self.k * self.WeightY) + self.Bias
        pred_y = self.k*tf.matmul(X_data,self.WeightX)/(self.RNI - self.k * self.WeightY) + self.Bias

        return pred_y.numpy()

    def get_coefficients(self):
        return  {
                  "WeightX" : self.h_WeightX.numpy(),
                  "Bias":self.h_Bias.numpy(), 
                  "Carrying Capacity":self.k,
                  "Weighty":self.h_WeightY.numpy(), 
                  "RNI":self.h_RNI.numpy()
                 }
        
    def getLossValues(self):
        return self.loss_values

    def get_scores(self, name=None):
        if self.validation is False:
            print("Loss: %f"%self.loss_score)
        else:
          if name == "train":
              return {
                  'max_train_loss' : max(self.val_acc_scores['train_loss']),
                  'min_train_loss' : min(self.val_acc_scores['train_loss'])
              }
          elif name == "test":
              return {
                  'max_test_loss' : max(self.val_acc_scores['test_loss']),
                  'min_test_loss' : min(self.val_acc_scores['test_loss'])
              }
          else:
              return {
                  'max_train_loss' : max(self.val_acc_scores['train_loss']),
                  'min_train_loss' : min(self.val_acc_scores['train_loss']),
                  'max_test_loss' : max(self.val_acc_scores['test_loss']),
                  'min_test_loss' : min(self.val_acc_scores['test_loss'])
              }

import numpy as np
import tensorflow as tf
import pickle
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold

class Classifier:
    """
    TEST EXAMPLE:
    -----------------


    from sklearn.datasets import load_iris
    import numpy as np
    x_train, y_train = load_iris(return_X_y=True)
    x_train = np.array(x_train, dtype=np.float32)
    y_train = np.array(y_train, dtype=np.uint8)

    il = ImpactLearning()
    il.fit(x_train, y_train, k=1, num_classes=3, optimizer="GD", loss_function="CategoricalCrossentropy")
    il.train(epochs = 100, lr=0.001, progress_per=1, kfold=2)
    """
    def __init__(self):
      tf.random.set_seed(2020)
      #lists to coefficient values
      self.loss_values = []

##################################### HUPOTHESIS FUNCTION ########################################
    def hypothesis(self, Xdata):
        h = self.k*tf.matmul(Xdata,self.WeightX)/(self.RNI - self.k * self.WeightY) + self.Bias
        h = tf.nn.softmax(h)
        return h
###################################### LOSS FUNCTIONS ############################################

    def get_loss_BinaryCrossentropy(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.binary_crossentropy(self.y_true_onehot, y_pred))
        return loss

    def get_loss_CategoricalCrossentropy(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.categorical_crossentropy(self.y_true_onehot, y_pred))
        return loss

    def get_loss_CosineSimilarity(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.cosine_similarity(self.y_true_onehot, y_pred))
        return loss

    def get_loss_Hinge(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.hinge(self.y_true_onehot, y_pred))
        return loss

    def get_loss_CategoricalHinge(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.categorical_hinge(self.y_true_onehot, y_pred))
        return loss

    def get_loss_Logosh(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.logcosh(self.y_true_onehot, y_pred))
        return loss

    def get_loss_Poisson(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.poisson(self.y_true_onehot, y_pred))
        return loss

    def get_loss_SquaredHinge(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.squared_hinge(self.y_true_onehot, y_pred))
        return loss

    def get_loss_KLD(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.KLD(self.y_true_onehot, y_pred))
        return loss
#########################################################################################
    def t_get_loss_BinaryCrossentropy(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X_test), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.binary_crossentropy(self.t_y_true_onehot, y_pred))
        return loss

    def t_get_loss_CategoricalCrossentropy(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X_test), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.categorical_crossentropy(self.t_y_true_onehot, y_pred))
        return loss

    def t_get_loss_CosineSimilarity(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X_test), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.cosine_similarity(self.t_y_true_onehot, y_pred))
        return loss

    def t_get_loss_Hinge(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X_test), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.hinge(self.t_y_true_onehot, y_pred))
        return loss

    def t_get_loss_CategoricalHinge(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X_test), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.categorical_hinge(self.t_y_true_onehot, y_pred))
        return loss

    def t_get_loss_Logosh(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X_test), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.logcosh(self.t_y_true_onehot, y_pred))
        return loss

    def t_get_loss_Poisson(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X_test), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.poisson(self.t_y_true_onehot, y_pred))
        return loss

    def t_get_loss_SquaredHinge(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X_test), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.squared_hinge(self.t_y_true_onehot, y_pred))
        return loss

    def t_get_loss_KLD(self):
        y_pred = tf.clip_by_value(self.hypothesis(self.X_test), 1e-9, 1.)
        loss = tf.reduce_mean(tf.keras.losses.KLD(self.t_y_true_onehot, y_pred))
        return loss
########################################## OPTIMIZING FUNCTIONS #########################
    def opt_Adadelta(self, lr):
      opt = tf.keras.optimizers.Adadelta(learning_rate=lr , rho = self.rho, epsilon = self.epsilon)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Adagrad(self, lr):
      opt = tf.keras.optimizers.Adagrad(learning_rate=lr, initial_accumulator_value = self.initial_accumulator_value)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Adam(self, lr):
      opt = tf.keras.optimizers.Adam(learning_rate=lr, beta_1=self.beta_1, beta_2=self.beta_2, epsilon=self.epsilon, amsgrad=self.amsgrad)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Adamax(self, lr):
      opt = tf.keras.optimizers.Adamax(learning_rate=lr, beta_1=self.beta_1, beta_2=self.beta_2, epsilon=self.epsilon)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Ftrl(self, lr):

      opt = tf.keras.optimizers.Ftrl(learning_rate=lr, learning_rate_power=self.learning_rate_power, 
                                      initial_accumulator_value=self.initial_accumulator_value,
                                      l1_regularization_strength=self.l1_regularization_strength, l2_regularization_strength=self.l2_regularization_strength,
                                      l2_shrinkage_regularization_strength=self.l2_shrinkage_regularization_strength)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_Nadam(self, lr):
      opt = tf.keras.optimizers.Nadam(learning_rate=lr, beta_1=self.beta_1, beta_2=self.beta_2, epsilon=self.epsilon)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_RMSprop(self, lr):
      opt = tf.keras.optimizers.RMSprop(learning_rate=lr, rho = self.rho, epsilon = self.epsilon, momentum = self.momentum, centered = self.centered)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_SGD(self, lr):
      opt = tf.keras.optimizers.SGD(learning_rate=lr, momentum=self.momentum, nesterov=self.nesterov)
      opt.minimize(self.get_loss, [self.WeightX, self.Bias, self.WeightY, self.RNI])

    def opt_GD(self,lr):
        with tf.GradientTape() as t:
            wx_grad, b_grad, wy_grad, rni_grad = t.gradient(self.get_loss(), [self.WeightX, self.Bias, self.WeightY, self.RNI] )

        self.WeightX.assign_sub(lr * wx_grad)
        self.Bias.assign_sub(lr * b_grad)
        self.WeightY.assign_sub(lr * wy_grad)
        self.RNI.assign_sub(lr * rni_grad)

######################################################################################
##################################   Accuracy   ######################################
    def accuracy(self,y_pred, y_true):
        # Predicted class is the index of highest score in prediction vector (i.e. argmax).  
        correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.cast(y_true, tf.int64))
        acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return acc
######################################################################################


    def fit(self,train_x=None, train_y=None, test_x=None, test_y=None, CCapacity=None,
            num_classes = None,
            optimizer="SGD", loss_function="CategoricalCrossentropy", delta = 1, rho=0.95, 
            epsilon=1e-07, initial_accumulator_value=0.1, beta_1=0.9, beta_2=0.999, 
            amsgrad=False,
            learning_rate_power=-0.5, 
            l1_regularization_strength=0.0, 
            l2_regularization_strength=0.0,
            l2_shrinkage_regularization_strength=0.0,
            momentum=0.0,
            centered=False,
            nesterov=False):

      '''

      LOSSES:
      --------

      BinaryCrossentropy = get_loss_BinaryCrossentropy
      CategoricalCrossentropy = get_loss_CategoricalCrossentropy
      CosineSimilarity = get_loss_CosineSimilarity
      Hinge = get_loss_Hinge
      CategoricalHinge = get_loss_CategoricalHinge
      Logosh = get_loss_Logosh
      Poisson = get_loss_Poisson
      SquaredHinge = get_loss_SquaredHinge
      KLD = get_loss_KLD


      OPTIMIZERS:
      ------------

      Adadelta
      Adagrad
      Adam
      Adamax
      Ftrl
      Nadam
      RMSprop
      SGD
      GD

      '''

     
      self.Xdata = train_x
      self.ydata = train_y
      self.validation = False
      if test_x is not None and test_y is not None:
          self.validation = True
          self.Xtest = test_x
          self.ytest = test_y

      if num_classes is None:
        return "Please Specify the Number of Classes"

      self.y_true_onehot = tf.one_hot(self.ydata, depth=num_classes)

      self.num_classes = num_classes

      self.k =  max(train_y)+0.1
      if CCapacity is not None:
        self.k=CCapacity+0.1
        
      #initializing Weights, Bias and RNI 
      
      self.WeightX = tf.Variable(tf.ones( [self.Xdata.shape[1], self.num_classes ]) )
      self.Bias = tf.Variable(tf.zeros([num_classes]))
      self.WeightY = tf.Variable(tf.ones([]))
      self.RNI = tf.Variable(tf.ones([]))

      #other parameteres
      
      self.delta = delta

      self.rho = rho
      self.epsilon = epsilon
      self.initial_accumulator_value = initial_accumulator_value
      self.beta_1 = beta_1
      self.beta_2 = beta_2
      self.amsgrad = amsgrad
      self.learning_rate_power=learning_rate_power
      self.initial_accumulator_value=initial_accumulator_value
      self.l1_regularization_strength=l1_regularization_strength
      self.l2_regularization_strength=l2_regularization_strength
      self.l2_shrinkage_regularization_strength=l2_shrinkage_regularization_strength
      self.momentum = momentum
      self.centered = centered
      self.nesterov = nesterov
      



  #-----------------------------------------------------------------
      if loss_function == "BinaryCrossentropy": 
        self.get_loss = self.get_loss_BinaryCrossentropy
        self.t_get_loss = self.t_get_loss_BinaryCrossentropy
      elif loss_function == "CategoricalCrossentropy": 
        self.get_loss = self.get_loss_CategoricalCrossentropy
        self.t_get_loss = self.t_get_loss_CategoricalCrossentropy
      elif loss_function == "CosineSimilarity": 
        self.get_loss = self.get_loss_CosineSimilarity
        self.t_get_loss = self.t_get_loss_CosineSimilarity
      elif loss_function == "Hinge": 
        self.get_loss = self.get_loss_Hinge
        self.t_get_loss = self.t_get_loss_Hinge
      elif loss_function == "CategoricalHinge": 
        self.get_loss = self.get_loss_CategoricalHinge
        self.t_get_loss = self.t_get_loss_CategoricalHinge
      elif loss_function == "Logosh": 
        self.get_loss = self.get_loss_Logosh
        self.t_get_loss = self.t_get_loss_Logosh
      elif loss_function == "Poisson": 
        self.get_loss = self.get_loss_Poisson
        self.t_get_loss = self.t_get_loss_Poisson
      elif loss_function == "SquaredHinge": 
        self.get_loss = self.get_loss_SquaredHinge
        self.t_get_loss = self.t_get_loss_SquaredHinge
      elif loss_function == "KLD": 
        self.get_loss = self.get_loss_KLD
        self.t_get_loss = self.t_get_loss_KLD
      else: print("Incorrect Loss function chosen"); return 0

  #------------------------------------------------------------------
      if optimizer == "Adadelta": self.optimizer=self.opt_Adadelta
      elif optimizer == "Adagrad": self.optimizer=self.opt_Adagrad
      elif optimizer == "Adam": self.optimizer=self.opt_Adam
      elif optimizer == "Adamax": self.optimizer=self.opt_Adamax
      elif optimizer == "Ftrl": self.optimizer=self.opt_Ftrl
      elif optimizer == "Nadam": self.optimizer=self.opt_Nadam
      elif optimizer == "RMSprop": self.optimizer=self.opt_RMSprop
      elif optimizer == "SGD": self.optimizer=self.opt_SGD
      elif optimizer == "GD": self.optimizer=self.opt_GD
      else : print("Incorrect Optimizer chosen"); return 0
  #------------------------------------------------------------------
   
    def train(self,epochs=2000, lr=0.009, progress_per=100):
        self.epochs = epochs
        self.lr = lr
        self.temp_acc = 0
        self.ac_score = 0
        if self.validation == False:
          self.X = tf.convert_to_tensor(self.Xdata, dtype=tf.float32)
          self.y = tf.convert_to_tensor(self.ydata, dtype=tf.uint8)
          for epoch_count in range(1, self.epochs+1):
                  self.optimizer(self.lr)
                  self.loss_values.append(self.get_loss().numpy())
                  acc = self.accuracy(self.hypothesis(self.X), self.y)

                  if acc>self.temp_acc:
                      self.temp_acc = acc
                      self.h_WeightX = self.WeightX
                      self.h_Bias = self.Bias
                      self.h_WeightY = self.WeightY
                      self.h_RNI = self.RNI

                  if progress_per != None and epoch_count % progress_per == 0:
                      print("Epoch: %i, loss: %f, train_accuracy: %f "% (epoch_count, self.get_loss().numpy(), acc))
          self.ac_score = acc
          print("Training Completed")

        else:
          self.val_acc_scores = {
              'train_acc':[],
              'test_acc':[],
              'train_loss':[],
              'test_loss':[],
          }
    
          self.X = tf.convert_to_tensor(self.Xdata, dtype=tf.float32)
          self.y = tf.convert_to_tensor(self.ydata, dtype=tf.uint8)
          self.y_true_onehot = tf.one_hot(self.y, depth=self.num_classes)

          self.X_test = tf.convert_to_tensor(self.Xtest, dtype=tf.float32)
          self.y_test = tf.convert_to_tensor(self.ytest, dtype=tf.uint8)
          self.t_y_true_onehot = tf.one_hot(self.y_test, depth=self.num_classes)
          
          
          for epoch_count in range(1, self.epochs+1):
                self.optimizer(self.lr)
                train_loss = self.get_loss().numpy()
                self.loss_values.append(train_loss)

                acc = self.accuracy(self.hypothesis(self.X), self.y)

                if acc>self.temp_acc:
                    self.temp_acc = acc
                    self.h_WeightX = self.WeightX
                    self.h_Bias = self.Bias
                    self.h_WeightY = self.WeightY
                    self.h_RNI = self.RNI
                val_acc = self.accuracy(self.hypothesis(self.X_test), self.y_test)

                test_loss = self.t_get_loss().numpy()

                self.val_acc_scores['train_acc'].append(acc)
                self.val_acc_scores['test_acc'].append(val_acc)

                self.val_acc_scores['train_loss'].append(train_loss)
                self.val_acc_scores['test_loss'].append(test_loss)


                if progress_per != None and epoch_count % progress_per == 0:
                    print("Epoch: %i, train_loss: %f, test_loss: %f, train_accuracy: %f test_accuracy: %f"% (epoch_count, train_loss, test_loss, acc, val_acc))
          print("Training Completed")



    def predict(self,X_data):
        X_data = tf.convert_to_tensor(X_data, dtype=tf.float32)
        h = self.k*tf.matmul(X_data,self.WeightX)/(self.RNI - self.k * self.WeightY) + self.Bias
        h = tf.nn.softmax(h)
        return tf.argmax(h, 1).numpy()

    def get_coefficients(self):
        return  {
                  "WeightX" : self.h_WeightX.numpy(),
                  "Bias":self.h_Bias.numpy(), 
                  "Carrying Capacity":self.k,
                  "Weighty":self.h_WeightY.numpy(), 
                  "RNI":self.h_RNI.numpy()
                 }
        
    def getLossValues(self):
        return self.loss_values

    def get_scores(self, name=None):
        if self.validation is False:
            print("Accuracy: %f"%self.ac_score)
        else:
          if name == "train":
              return {
                  'max_train_accuracy' : max(self.val_acc_scores['train_acc']).numpy(),
                  'min_train_accuracy' : min(self.val_acc_scores['train_acc']).numpy(),
                  'max_train_loss' : max(self.val_acc_scores['train_loss']),
                  'min_train_loss' : min(self.val_acc_scores['train_loss'])
              }
          elif name == "test":
              return {
                  'max_test_accuracy' : max(self.val_acc_scores['test_acc']).numpy(),
                  'min_test_accuracy' : min(self.val_acc_scores['test_acc']).numpy(),
                  'max_test_loss' : max(self.val_acc_scores['test_loss']),
                  'min_test_loss' : min(self.val_acc_scores['test_loss'])
              }
          else:
              return {
                  'max_train_accuracy' : max(self.val_acc_scores['train_acc']).numpy(),
                  'min_train_accuracy' : min(self.val_acc_scores['train_acc']).numpy(),
                  'max_train_loss' : max(self.val_acc_scores['train_loss']),
                  'min_train_loss' : min(self.val_acc_scores['train_loss']),
                  'max_test_accuracy' : max(self.val_acc_scores['test_acc']).numpy(),
                  'min_test_accuracy' : min(self.val_acc_scores['test_acc']).numpy(),
                  'max_test_loss' : max(self.val_acc_scores['test_loss']),
                  'min_test_loss' : min(self.val_acc_scores['test_loss'])
              }