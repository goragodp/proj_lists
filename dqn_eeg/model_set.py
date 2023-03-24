#@title Custom Model 
#Network define
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Activation, Permute, Dropout
from tensorflow.keras.layers import MaxPooling2D, AveragePooling2D, MaxPooling1D, AveragePooling1D 
from tensorflow.keras.layers import Conv2D, Conv1D 
from tensorflow.keras.layers import SeparableConv2D, DepthwiseConv2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import SpatialDropout2D, SpatialDropout1D
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.layers import Input, Flatten
from tensorflow.keras.constraints import max_norm
from tensorflow.keras import backend as K

def HopefulNet1DCNN(chs = 19, samples = 1000, output_classes = 4):
        
        input1      = Input(shape = (samples, chs), name='input')
        # self.conv1 = tf.keras.layers.Conv1D(filters=32, kernel_size=self.kernel_size_0, padding="same", activation="relu", input_shape=input_shape)
        # self.batch1 = tf.keras.layers.BatchNormalization()
        block1      = Conv1D(32, 20, padding = 'same',input_shape = (samples, chs), name='conv1')(input1)
        block1      = Activation('relu', name='relu1')(block1)
        block1      = BatchNormalization()(block1)
        #layer2
        # self.conv2 = tf.keras.layers.Conv1D(filters=32, kernel_size=self.kernel_size_0, padding="valid", activation="relu")
        # self.batch2 = tf.keras.layers.BatchNormalization()
        # self.spatial_drop2 = tf.keras.layers.SpatialDropout1D(self.drop_rate)
        block2      = Conv1D(32, 20, padding = 'valid', name='conv2')(block1)
        block2      = Activation('relu', name='relu2')(block2)
        block2      = BatchNormalization()(block2)
        block2      = SpatialDropout1D(.5, name = 'spatialdrop1')(block2)
        
        #layer3
        # self.conv3 = tf.keras.layers.Conv1D(filters=32, kernel_size=self.kernel_size_1, padding="valid", activation="relu")
        # self.avg3 = tf.keras.layers.AveragePooling1D(pool_size=self.pool_size)
        block3      = Conv1D(32, 6, padding = 'valid', name='conv3')(block2)
        block3      = Activation('relu', name='relu3')(block3)
        block3      = AveragePooling1D(pool_size = 2, name = 'averagepool1')(block3)
        #layer 4
        # self.conv4 = tf.keras.layers.Conv1D(filters = 32, kernel_size=self.kernel_size_1, padding="valid", activation="relu")
        # self.spatial_drop4 = tf.keras.layers.SpatialDropout1D(self.drop_rate)
        block4      = Conv1D(32, 6, padding = 'valid', name='conv4')(block3)
        block4      = Activation('relu', name='relu4')(block4)
        block4      = SpatialDropout1D(.5, name = 'spatialdrop2')(block4)

        #OUT
        # self.flatten = tf.keras.layers.Flatten() 
        flatten     = Flatten(name='flatten')(block4)
        
        # self.denseout_1  = tf.keras.layers.Dense(296, activation="relu")
        # self.dropout_1 = tf.keras.layers.Dropout(self.drop_rate)
        dense1      = Dense(296, name = 'dense1')(flatten)
        dense1      = Activation('relu', name = 'relu5')(dense1)
        dense1      = Dropout(.5, name = 'drop1')(dense1)
        
        # self.denseout_2  = tf.keras.layers.Dense(148, activation="relu")
        # self.dropout_2 = tf.keras.layers.Dropout(self.drop_rate)
        dense2      = Dense(148, name = 'dense2')(dense1)
        dense2      = Activation('relu', name = 'relu6')(dense2)
        dense2      = Dropout(.5, name = 'drop2')(dense2)
        
        # self.denseout_3 = tf.keras.layers.Dense(74, activation="relu")
        # self.dropout_3 = tf.keras.layers.Dropout(self.drop_rate)
        dense3      = Dense(74, name = 'dense3')(dense2)
        dense3      = Activation('relu', name = 'relu7')(dense3)
        dense3      = Dropout(.5, name = 'drop3')(dense3)
        # self.out = tf.keras.layers.Dense(output_classes, activation='softmax')
        logit       = Dense(output_classes, name = 'logit')(dense3)
        out         = Activation('softmax', name = 'out')(logit)
        
        return Model(inputs=input1, outputs=out)

def SugiyamaNet(Chans = 19, Samples = 1000, output_classes = 4):
    
    input1   = Input(shape = (Chans, Samples, 1),name='input')
    block1       = Conv2D(32, (1, 20), strides = (1,1),input_shape = (Chans, Samples, 1), name='conv1')(input1)
    block1       = Conv2D(32, (3, 1),strides = (1,1),name='conv2')(block1)
    block1       = BatchNormalization(name='bn1')(block1)
    block1       = Activation('relu',name='relu1')(block1)
    block1       = MaxPooling2D((1, 5), strides = (1,2),name='pool1')(block1)
    
    block2      = Conv2D(64, (1, 20),name='conv3')(block1)
    block2      = BatchNormalization(name='bn2')(block2)
    block2      = Activation('relu',name='relu2')(block2)
    block2      = MaxPooling2D((1, 7), strides = (1,2),name='pool2')(block2)
    
    block3      = Conv2D(64, (1,10),strides = (1,1), name='conv4')(block2)
    block3      = BatchNormalization(name='bn3')(block3)
    block3      = Activation('relu',name='relu3')(block3)
    block3      = MaxPooling2D((1, 5), strides = (1,2),name='pool3')(block3)
    
    flatten     = Flatten(name='f1')(block3)
    dp1         = Dropout(0.5,name='drop1')(flatten)
    dense1      = Dense(32,name='ful1')(dp1)
    nrm         = BatchNormalization(name='bn7')(dense1)
    act         = Activation('relu',name='relu7')(nrm)
    
    dp2         = Dropout(0.3, name='drop3')(act)
    dense2      = Dense(output_classes,name='out')(dp2)
    out         = Activation('softmax',name='soft1_out')(dense2)
    
    return Model(inputs=input1, outputs=out)

def TakahashiNet(Chans = 19, Samples = 1000, 
             output_classes = 4):
    
    input1   = Input(shape = (Chans, Samples, 1),name='input')
    block1       = Conv2D(32, (1, 20), padding = 'valid',input_shape = (Chans, Samples, 1), name='conv1')(input1)
    block1       = Conv2D(32, (3, 1), padding = 'valid',name='conv2')(block1)
    block1       = BatchNormalization(name='bn1')(block1)
    block1       = Activation('relu',name='relu1')(block1)
    block1       = MaxPooling2D((1, 5), strides = (1,2),name='pool1')(block1)
    block2      = Conv2D(16, (1, 15),name='conv3')(block1)
    block2      = BatchNormalization(name='bn2')(block2)
    block2      = Activation('relu',name='relu2')(block2)
    block2      = MaxPooling2D((1, 7), strides = (1,2),name='pool2')(block2)
    block3      = Conv2D(64, (1,8),name='conv4')(block2)
    block3      = BatchNormalization(name='bn3')(block3)
    block3      = Activation('relu',name='relu3')(block3)
    block3      = MaxPooling2D((1, 5), strides = (1,2),name='pool3')(block3)
    block4      = Conv2D(128, (1,8),name='conv5')(block3)
    block4      = BatchNormalization(name='bn4')(block4)
    block4      = Activation('relu',name='relu4')(block4)
    block4      = MaxPooling2D((1, 3), strides = (1,1),name='pool4')(block4)
    block5      = Conv2D(128, (1,6),name='conv6')(block4)
    block5      = BatchNormalization(name='bn5')(block5)
    block5      = Activation('relu',name='relu5')(block5)
    block5      = MaxPooling2D((1, 3), strides = (1,1),name='pool5')(block5)
    block6      = Conv2D(256, (1,4),name='conv7')(block5)
    block6      = BatchNormalization(name='bn6')(block6)
    block6      = Activation('relu',name='relu6')(block6)
    block6      = MaxPooling2D((1, 2), strides = (1,1),name='pool6')(block6)
    flatten     = Flatten(name='f1')(block6)
    dense1      = Dropout(0.5,name='drop1')(flatten)
    dense1      = Dense(64,name='ful1')(dense1)
    dense1      = BatchNormalization(name='bn7')(dense1)
    dense1      = Activation('relu',name='relu7')(dense1)
    dense2      = Dropout(0.5,name='drop2')(dense1)
    dense2      = Dense(32,name='ful2')(dense2)
    dense2      = BatchNormalization(name='bn8')(dense2)
    dense2      = Activation('relu',name='relu8')(dense2)
    out         = Dropout(0.3, name='drop3')(dense2)
    out         = Dense(output_classes,name='ful3')(out)
    out         = Activation('softmax',name='soft1_out')(out)

    
    return Model(inputs=input1, outputs=out)

def EEGNet(nb_classes, Chans = 64, Samples = 128, 
             dropoutRate = 0.5, kernLength = 64, F1 = 8, 
             D = 2, F2 = 16, norm_rate = 0.25, dropoutType = 'Dropout'):
    """ Keras Implementation of EEGNet
    http://iopscience.iop.org/article/10.1088/1741-2552/aace8c/meta

    Note that this implements the newest version of EEGNet and NOT the earlier
    version (version v1 and v2 on arxiv). We strongly recommend using this
    architecture as it performs much better and has nicer properties than
    our earlier version. For example:
        
        1. Depthwise Convolutions to learn spatial filters within a 
        temporal convolution. The use of the depth_multiplier option maps 
        exactly to the number of spatial filters learned within a temporal
        filter. This matches the setup of algorithms like FBCSP which learn 
        spatial filters within each filter in a filter-bank. This also limits 
        the number of free parameters to fit when compared to a fully-connected
        convolution. 
        
        2. Separable Convolutions to learn how to optimally combine spatial
        filters across temporal bands. Separable Convolutions are Depthwise
        Convolutions followed by (1x1) Pointwise Convolutions. 
        
    
    While the original paper used Dropout, we found that SpatialDropout2D 
    sometimes produced slightly better results for classification of ERP 
    signals. However, SpatialDropout2D significantly reduced performance 
    on the Oscillatory dataset (SMR, BCI-IV Dataset 2A). We recommend using
    the default Dropout in most cases.
        
    Assumes the input signal is sampled at 128Hz. If you want to use this model
    for any other sampling rate you will need to modify the lengths of temporal
    kernels and average pooling size in blocks 1 and 2 as needed (double the 
    kernel lengths for double the sampling rate, etc). Note that we haven't 
    tested the model performance with this rule so this may not work well. 
    
    The model with default parameters gives the EEGNet-8,2 model as discussed
    in the paper. This model should do pretty well in general, although it is
	advised to do some model searching to get optimal performance on your
	particular dataset.

    We set F2 = F1 * D (number of input filters = number of output filters) for
    the SeparableConv2D layer. We haven't extensively tested other values of this
    parameter (say, F2 < F1 * D for compressed learning, and F2 > F1 * D for
    overcomplete). We believe the main parameters to focus on are F1 and D. 

    Inputs:
        
      nb_classes      : int, number of classes to classify
      Chans, Samples  : number of channels and time points in the EEG data
      dropoutRate     : dropout fraction
      kernLength      : length of temporal convolution in first layer. We found
                        that setting this to be half the sampling rate worked
                        well in practice. For the SMR dataset in particular
                        since the data was high-passed at 4Hz we used a kernel
                        length of 32.     
      F1, F2          : number of temporal filters (F1) and number of pointwise
                        filters (F2) to learn. Default: F1 = 8, F2 = F1 * D. 
      D               : number of spatial filters to learn within each temporal
                        convolution. Default: D = 2
      dropoutType     : Either SpatialDropout2D or Dropout, passed as a string.

    """
    
    if dropoutType == 'SpatialDropout2D':
        dropoutType = SpatialDropout2D
    elif dropoutType == 'Dropout':
        dropoutType = Dropout
    else:
        raise ValueError('dropoutType must be one of SpatialDropout2D '
                         'or Dropout, passed as a string.')
    
    input1   = Input(shape = (Chans, Samples, 1))

    ##################################################################
    block1       = Conv2D(F1, (1, kernLength), padding = 'same',
                                   input_shape = (Chans, Samples, 1),
                                   use_bias = False)(input1)
    block1       = BatchNormalization()(block1)
    block1       = DepthwiseConv2D((Chans, 1), use_bias = False, 
                                   depth_multiplier = D,
                                   depthwise_constraint = max_norm(1.))(block1)
    block1       = BatchNormalization()(block1)
    block1       = Activation('elu')(block1)
    block1       = AveragePooling2D((1, 4))(block1)
    block1       = dropoutType(dropoutRate)(block1)
    
    block2       = SeparableConv2D(F2, (1, 16),
                                   use_bias = False, padding = 'same')(block1)
    block2       = BatchNormalization()(block2)
    block2       = Activation('elu')(block2)
    block2       = AveragePooling2D((1, 8))(block2)
    block2       = dropoutType(dropoutRate)(block2)
        
    flatten      = Flatten(name = 'flatten')(block2)
    
    dense        = Dense(nb_classes, name = 'dense', 
                         kernel_constraint = max_norm(norm_rate))(flatten)
    softmax      = Activation('softmax', name = 'softmax')(dense)
    
    return Model(inputs=input1, outputs=softmax)

def EEGNet_SSVEP(nb_classes = 12, Chans = 8, Samples = 256, 
             dropoutRate = 0.5, kernLength = 256, F1 = 96, 
             D = 1, F2 = 96, dropoutType = 'Dropout'):
    """ SSVEP Variant of EEGNet, as used in [1]. 

    Inputs:
        
      nb_classes      : int, number of classes to classify
      Chans, Samples  : number of channels and time points in the EEG data
      dropoutRate     : dropout fraction
      kernLength      : length of temporal convolution in first layer
      F1, F2          : number of temporal filters (F1) and number of pointwise
                        filters (F2) to learn. 
      D               : number of spatial filters to learn within each temporal
                        convolution.
      dropoutType     : Either SpatialDropout2D or Dropout, passed as a string.
      
      
    [1]. Waytowich, N. et. al. (2018). Compact Convolutional Neural Networks
    for Classification of Asynchronous Steady-State Visual Evoked Potentials.
    Journal of Neural Engineering vol. 15(6). 
    http://iopscience.iop.org/article/10.1088/1741-2552/aae5d8

    """
    
    if dropoutType == 'SpatialDropout2D':
        dropoutType = SpatialDropout2D
    elif dropoutType == 'Dropout':
        dropoutType = Dropout
    else:
        raise ValueError('dropoutType must be one of SpatialDropout2D '
                         'or Dropout, passed as a string.')
    
    input1   = Input(shape = (Chans, Samples, 1))

    ##################################################################
    block1       = Conv2D(F1, (1, kernLength), padding = 'same',
                                   input_shape = (Chans, Samples, 1),
                                   use_bias = False)(input1)
    block1       = BatchNormalization()(block1)
    block1       = DepthwiseConv2D((Chans, 1), use_bias = False, 
                                   depth_multiplier = D,
                                   depthwise_constraint = max_norm(1.))(block1)
    block1       = BatchNormalization()(block1)
    block1       = Activation('elu')(block1)
    block1       = AveragePooling2D((1, 4))(block1)
    block1       = dropoutType(dropoutRate)(block1)
    
    block2       = SeparableConv2D(F2, (1, 16),
                                   use_bias = False, padding = 'same')(block1)
    block2       = BatchNormalization()(block2)
    block2       = Activation('elu')(block2)
    block2       = AveragePooling2D((1, 8))(block2)
    block2       = dropoutType(dropoutRate)(block2)
        
    flatten      = Flatten(name = 'flatten')(block2)
    
    dense        = Dense(nb_classes, name = 'dense')(flatten)
    softmax      = Activation('softmax', name = 'softmax')(dense)
    
    return Model(inputs=input1, outputs=softmax)

def EEGNet_old(nb_classes, Chans = 64, Samples = 128, regRate = 0.0001,
           dropoutRate = 0.25, kernels = [(2, 32), (8, 4)], strides = (2, 4)):
    """ Keras Implementation of EEGNet_v1 (https://arxiv.org/abs/1611.08024v2)

    This model is the original EEGNet model proposed on arxiv
            https://arxiv.org/abs/1611.08024v2
    
    with a few modifications: we use striding instead of max-pooling as this 
    helped slightly in classification performance while also providing a 
    computational speed-up. 
    
    Note that we no longer recommend the use of this architecture, as the new
    version of EEGNet performs much better overall and has nicer properties.
    
    Inputs:
        
        nb_classes     : total number of final categories
        Chans, Samples : number of EEG channels and samples, respectively
        regRate        : regularization rate for L1 and L2 regularizations
        dropoutRate    : dropout fraction
        kernels        : the 2nd and 3rd layer kernel dimensions (default is 
                         the [2, 32] x [8, 4] configuration)
        strides        : the stride size (note that this replaces the max-pool
                         used in the original paper)
    
    """

    # start the model
    input_main   = Input((Chans, Samples))
    layer1       = Conv2D(16, (Chans, 1), input_shape=(Chans, Samples, 1),
                                 kernel_regularizer = l1_l2(l1=regRate, l2=regRate))(input_main)
    layer1       = BatchNormalization()(layer1)
    layer1       = Activation('elu')(layer1)
    layer1       = Dropout(dropoutRate)(layer1)
    
    permute_dims = 2, 1, 3
    permute1     = Permute(permute_dims)(layer1)
    
    layer2       = Conv2D(4, kernels[0], padding = 'same', 
                            kernel_regularizer=l1_l2(l1=0.0, l2=regRate),
                            strides = strides)(permute1)
    layer2       = BatchNormalization()(layer2)
    layer2       = Activation('elu')(layer2)
    layer2       = Dropout(dropoutRate)(layer2)
    
    layer3       = Conv2D(4, kernels[1], padding = 'same',
                            kernel_regularizer=l1_l2(l1=0.0, l2=regRate),
                            strides = strides)(layer2)
    layer3       = BatchNormalization()(layer3)
    layer3       = Activation('elu')(layer3)
    layer3       = Dropout(dropoutRate)(layer3)
    
    flatten      = Flatten(name = 'flatten')(layer3)
    
    dense        = Dense(nb_classes, name = 'dense')(flatten)
    softmax      = Activation('softmax', name = 'softmax')(dense)
    
    return Model(inputs=input_main, outputs=softmax)

def DeepConvNet(nb_classes, Chans = 64, Samples = 256,
                dropoutRate = 0.5):
    """ Keras implementation of the Deep Convolutional Network as described in
    Schirrmeister et. al. (2017), Human Brain Mapping.
    
    This implementation assumes the input is a 2-second EEG signal sampled at 
    128Hz, as opposed to signals sampled at 250Hz as described in the original
    paper. We also perform temporal convolutions of length (1, 5) as opposed
    to (1, 10) due to this sampling rate difference. 
    
    Note that we use the max_norm constraint on all convolutional layers, as 
    well as the classification layer. We also change the defaults for the
    BatchNormalization layer. We used this based on a personal communication 
    with the original authors.
    
                      ours        original paper
    pool_size        1, 2        1, 3
    strides          1, 2        1, 3
    conv filters     1, 5        1, 10
    
    Note that this implementation has not been verified by the original 
    authors. 
    
    """

    # start the model
    input_main   = Input((Chans, Samples, 1))
    block1       = Conv2D(25, (1, 5), 
                                 input_shape=(Chans, Samples, 1),
                                 kernel_constraint = max_norm(2., axis=(0,1,2)))(input_main)
    block1       = Conv2D(25, (Chans, 1),
                                 kernel_constraint = max_norm(2., axis=(0,1,2)))(block1)
    block1       = BatchNormalization(epsilon=1e-05, momentum=0.9)(block1)
    block1       = Activation('elu')(block1)
    block1       = MaxPooling2D(pool_size=(1, 2), strides=(1, 2))(block1)
    block1       = Dropout(dropoutRate)(block1)
  
    block2       = Conv2D(50, (1, 5),
                                 kernel_constraint = max_norm(2., axis=(0,1,2)))(block1)
    block2       = BatchNormalization(epsilon=1e-05, momentum=0.9)(block2)
    block2       = Activation('elu')(block2)
    block2       = MaxPooling2D(pool_size=(1, 2), strides=(1, 2))(block2)
    block2       = Dropout(dropoutRate)(block2)
    
    block3       = Conv2D(100, (1, 5),
                                 kernel_constraint = max_norm(2., axis=(0,1,2)))(block2)
    block3       = BatchNormalization(epsilon=1e-05, momentum=0.9)(block3)
    block3       = Activation('elu')(block3)
    block3       = MaxPooling2D(pool_size=(1, 2), strides=(1, 2))(block3)
    block3       = Dropout(dropoutRate)(block3)
    
    block4       = Conv2D(200, (1, 5),
                                 kernel_constraint = max_norm(2., axis=(0,1,2)))(block3)
    block4       = BatchNormalization(epsilon=1e-05, momentum=0.9)(block4)
    block4       = Activation('elu')(block4)
    block4       = MaxPooling2D(pool_size=(1, 2), strides=(1, 2))(block4)
    block4       = Dropout(dropoutRate)(block4)
    
    flatten      = Flatten()(block4)
    
    dense        = Dense(nb_classes, kernel_constraint = max_norm(0.5))(flatten)
    softmax      = Activation('softmax')(dense)
    
    return Model(inputs=input_main, outputs=softmax)


# need these for ShallowConvNet
def square(x):
    return K.square(x)

def log(x):
    return K.log(K.clip(x, min_value = 1e-7, max_value = 10000))   


def ShallowConvNet(nb_classes, Chans = 64, Samples = 128, dropoutRate = 0.5):
    """ Keras implementation of the Shallow Convolutional Network as described
    in Schirrmeister et. al. (2017), Human Brain Mapping.
    
    Assumes the input is a 2-second EEG signal sampled at 128Hz. Note that in 
    the original paper, they do temporal convolutions of length 25 for EEG
    data sampled at 250Hz. We instead use length 13 since the sampling rate is 
    roughly half of the 250Hz which the paper used. The pool_size and stride
    in later layers is also approximately half of what is used in the paper.
    
    Note that we use the max_norm constraint on all convolutional layers, as 
    well as the classification layer. We also change the defaults for the
    BatchNormalization layer. We used this based on a personal communication 
    with the original authors.
    
                     ours        original paper
    pool_size        1, 35       1, 75
    strides          1, 7        1, 15
    conv filters     1, 13       1, 25    
    
    Note that this implementation has not been verified by the original 
    authors. We do note that this implementation reproduces the results in the
    original paper with minor deviations. 
    """

    # start the model
    input_main   = Input((Chans, Samples, 1))
    block1       = Conv2D(40, (1, 13), 
                                 input_shape=(Chans, Samples, 1),
                                 kernel_constraint = max_norm(2., axis=(0,1,2)))(input_main)
    block1       = Conv2D(40, (Chans, 1), use_bias=False, 
                          kernel_constraint = max_norm(2., axis=(0,1,2)))(block1)
    block1       = BatchNormalization(epsilon=1e-05, momentum=0.9)(block1)
    block1       = Activation(square)(block1)
    block1       = AveragePooling2D(pool_size=(1, 35), strides=(1, 7))(block1)
    block1       = Activation(log)(block1)
    block1       = Dropout(dropoutRate)(block1)
    flatten      = Flatten()(block1)
    dense        = Dense(nb_classes, kernel_constraint = max_norm(0.5))(flatten)
    softmax      = Activation('softmax')(dense)
    
    return Model(inputs=input_main, outputs=softmax)

def test():
    model = tf.keras.models.Sequential()

    input_shape = (1000,19,1)
    model.add(Conv2D(32, kernel_size=(10, 1), strides=(1, 1), input_shape=input_shape))
    model.add(Conv2D(32, kernel_size=(1, 19), strides=(1, 1)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=(5, 1), strides=(2, 1)))
    model.add(Conv2D(64, kernel_size=(10, 1), strides=(1, 1)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=(5, 1), strides=(2, 1)))
    model.add(Conv2D(64, kernel_size=(10, 1), strides=(1, 1)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=(5, 1), strides=(2, 1)))

    model.add(Flatten())

    Dropout(0.5)
    model.add(Dense(32))
    model.add(BatchNormalization())
    model.add(Activation('relu'))

    Dropout(0.3)
    model.add(Dense(4, activation='softmax'))

    # model.compile(loss='categorical_crossentropy',
    #             optimizer=optimizers.Adam(learning_rate=0.001), metrics=['accuracy'])
    model.summary()
if __name__ == "__main__":
    import numpy as np

    # model = Custom1DCNN()
    # model.model().summary()
    
    # model = HopefulNet1DCNN(chs = 19, samples = 1000, output_classes = 3)
    
    # model.summary()

    model = SugiyamaNet(Chans = 19, Samples = 1000, 
             output_classes = 4)

    # model = EEGNet(4, Chans = 19, Samples = 1000, 
    #                                     dropoutRate = 0.5, kernLength = 512, F1 = 64, 
    #                                     D = 8, F2 = 128, norm_rate = 0.25, dropoutType = 'Dropout')
    model.summary()
    # test()

    # model.summary()
    # print(len(model.layers))
    # dummy = np.arange(38000).reshape(2,19,1000,1)
    # out = model(dummy)
    # print(out.shape)

    # tf.keras.backend.clear_session()

