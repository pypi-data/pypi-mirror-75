# 1D, 2D, and 3D Sinusodal Postional Encoding Pytorch

This is an implemenation of 1D, 2D, and 3D sinusodal positional encoding, being able to encode on tensors of the form `(batchsize, x, ch)`, `(batchsize, x, y, ch)`, and `(batchsize, x, y, z, ch)`, where the positional encodings will be added to the `ch` dimension. The [Attention is All You Need](https://arxiv.org/pdf/1706.03762.pdf) allowed for positional encoding in only one dimension, however, this works to extend this to 2 and 3 dimensions.

Check out more on the [github page](https://github.com/tatp22/multidim-positional-encoding).
