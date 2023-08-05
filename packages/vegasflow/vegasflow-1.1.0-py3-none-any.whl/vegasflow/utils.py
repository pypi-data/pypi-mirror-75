"""
    This module contains tensorflow_compiled utilities
"""

import tensorflow as tf
from vegasflow.configflow import DTYPEINT, fzero


@tf.function
def consume_array_into_indices(input_arr, indices, result_size):
    """
    Accumulate the input tensor `input_arr` into an output tensor of
    size `result_size`. The accumulation occurs according to the array
    of `indices`.

    For instance, `input_array` = [a,b,c,d] and vector column `indices` = [[0,1,0,0]].T
    (with `result_size` = 2) will result in a final_result;
        (a+c+d, b)

    Parameters
    ----------
        `input_arr`
            Array of results to be consumed
        `indices`
            Indices of the bins in which to accumulate the input array
        `result_size`
            size of the output array

    Returns
    -------
        `final_result`
            Array of size `result_size`
    """
    all_bins = tf.range(result_size, dtype=DTYPEINT)
    eq = tf.transpose(tf.equal(indices, all_bins))
    res_tmp = tf.where(eq, input_arr, fzero)
    final_result = tf.reduce_sum(res_tmp, axis=1)
    return final_result
