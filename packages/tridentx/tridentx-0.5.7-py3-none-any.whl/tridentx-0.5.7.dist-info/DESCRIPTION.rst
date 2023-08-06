Multiverse for Deep Learning Developers without Pitfall



Release Note
#. Support AMP (automatic mixed precision) with pytorch 1.6.
#. attach lots of functions in ops on the tensor and use @numpy_compatible to share same syntax within numpy array or tensor.
#. New attribute 'sequence_rank' comes to all conv_blocks familay, if sequence_rank='cna' means the order is  'Convolution-Normalization-Activation'.
#. Adding EvoNorm, SIREN ..

