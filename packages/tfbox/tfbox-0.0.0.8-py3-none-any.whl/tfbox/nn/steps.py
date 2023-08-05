from pprint import pprint
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tfbox.utils.helpers import StrideManager
from . import blocks
from . import load
#
# Steps Network:
#
class Steps(tf.keras.Model):
    #
    # CONSTANTS
    #
    DEFAULT_KEY='steps'
    DEFAULTS=load.config(cfig='steps',key_path=DEFAULT_KEY)
    GAP='gap'
    SEGMENT='segment'



    #
    # STATIC
    #
    @staticmethod
    def from_config(
            key_path=DEFAULT_KEY,
            cfig='steps',
            is_file_path=False,
            **kwargs):
        config=load.config(
            cfig=cfig,
            key_path=key_path,
            is_file_path=is_file_path,
            **kwargs)
        print('STEPS:')
        pprint(config)
        return Steps(**config)



    #
    # PUBLIC
    #
    def __init__(self,
            filters_list=DEFAULTS['filters_list'],
            strides_list=DEFAULTS.get('strides_list',1),
            kernel_size_list=DEFAULTS.get('kernel_size_list',3),
            depth_list=DEFAULTS.get('depth_list',1),
            dilation_rate_list=DEFAULTS.get('dilation_rate_list',1),
            squeeze_excitation_list=DEFAULTS.get('squeeze_excitation_list',False),
            residual_list=DEFAULTS.get('residual_list',False),
            nb_classes=DEFAULTS.get('nb_classes',None),
            classifier_type=DEFAULTS.get('classifier_type',SEGMENT),
            classifier_act=DEFAULTS.get('classifier_act',True),
            classifier_act_config=DEFAULTS.get('classifier_act_config',{}),
            classifier_kernel_size_list=DEFAULTS.get('classifier_kernel_size_list'),
            classifier_filters_list=DEFAULTS.get('classifier_filters_list'),
            **step_kwargs):
        super(Steps, self).__init__()
        self.nb_steps=len(filters_list)
        self.steps=self._steps(
            filters_list,
            self._as_list(strides_list),
            self._as_list(kernel_size_list),
            self._as_list(depth_list),
            self._as_list(dilation_rate_list),
            self._as_list(squeeze_excitation_list),
            self._as_list(residual_list),
            step_kwargs)
        if classifier_type==Steps.GAP:
            # todo: global-avg-pooling+dense+classifier
            pass
        elif classifier_type==Steps.SEGMENT:
            self.classifier=blocks.SegmentClassifier(
                nb_classes=nb_classes,
                filters_list=classifier_filters_list,
                kernel_size_list=classifier_kernel_size_list,
                output_act=classifier_act,
                output_act_config=classifier_act_config)
        else:
            self.classifier=False


    def __call__(self,x,training=False,**kwargs):
        for l in self.steps:
            x=l(x)
        if self.classifier:
            return self.classifier(x)
        else:
            return x


    #
    # INTERNAL
    #
    def _steps(self,
            filters_list,
            strides_list,
            kernel_size_list,
            depth_list,
            dilation_rate_list,
            squeeze_excitation_list,
            residual_list,
            step_config):
        _layers=[]
        for f,s,k,depth,d,se,res in zip(
                filters_list,
                strides_list,
                kernel_size_list,
                depth_list,
                dilation_rate_list,
                squeeze_excitation_list,
                residual_list):
            blk=blocks.CBADStack(
                filters=f,
                output_stride=s,
                kernel_size=k,
                depth=depth,
                dilation_rate=d,
                squeeze_excitation=se,
                residual=res,
                **step_config)
            _layers.append(blk)
        return _layers


    def _as_list(self,value):
        if isinstance(value,int):
            value=[value]*self.nb_steps
        return value





