import argparse
import re
import tensorflow as tf
import os

from .converter import convert
from .quantization import quantize
from .utils import load_quantized_model


def quantize_model(model_path, wq, aq, iq):
    model = load_quantized_model(model_path)
    if iq == -1:
        iq = wq
    model_q = quantize(model, wq, aq, iq)
    # Extract base name
    base_name = os.path.splitext(model_path)[0]
    # Cross-platform path may contain alpha characters, /, \ and :
    path_re = r"([\w/\\:]+)"
    # Quantization suffix has a well-identified structure
    suffix_re = '(_iq\d_wq\d_aq\d)'
    p = re.compile(path_re + suffix_re)
    # Look for an existing quantization suffix in the base name
    m = p.match(base_name)
    if m:
        # Only keep the actual base name (group(2) contains the suffix)
        base_name = m.group(1)
    out_path = f"{base_name}_iq{iq}_wq{wq}_aq{aq}.h5"
    model_q.save(out_path, include_optimizer=False)
    print(f"Model successfully quantized and saved as {out_path}.")


def convert_model(model_path, scale, shift, is_sparse):
    base_name = os.path.splitext(model_path)[0]
    q_model = load_quantized_model(model_path)
    ak_model = convert(q_model,
                       input_scaling=(scale, shift),
                       input_is_sparse=is_sparse)
    out_path = f"{base_name}.fbz"
    ak_model.save(out_path)
    print(f"Model successfully converted and saved as {out_path}.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", default=None, help="The source model")
    sp = parser.add_subparsers(dest="action")
    q_parser = sp.add_parser("quantize", help="Quantize a Keras model")
    q_parser.add_argument("-wq",
                          "--weight_quantization",
                          type=int,
                          default=4,
                          help="The weight quantization")
    q_parser.add_argument("-aq",
                          "--activ_quantization",
                          type=int,
                          default=4,
                          help="The activations quantization")
    q_parser.add_argument("-iq",
                          "--input_weight_quantization",
                          type=int,
                          default=-1,
                          help="The first layer weight quantization (same as" \
                          " weight_quantization if omitted)")
    c_parser = sp.add_parser(
        "convert", help="Convert a quantized Keras model to an akida model")
    c_parser.add_argument("-sc",
                          "--scale",
                          type=int,
                          default=1,
                          help="The scale factor applied on uint8 inputs.")
    c_parser.add_argument("-sh",
                          "--shift",
                          type=int,
                          default=0,
                          help="The shift applied on uint8 inputs.")
    c_parser.add_argument("-sp",
                          "--sparse",
                          action='store_true',
                          default=False,
                          help="Use sparse input.")
    args = parser.parse_args()
    if args.action == "quantize":
        quantize_model(args.model, args.weight_quantization,
                       args.activ_quantization, args.input_weight_quantization)
    if args.action == "convert":
        convert_model(args.model, args.scale, args.shift, args.sparse)
