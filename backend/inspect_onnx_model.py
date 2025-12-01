"""
Inspect the 640m.onnx model to understand its structure.
This helps us integrate it correctly without guessing.
"""
import onnx
import onnxruntime as ort
import numpy as np

model_path = "data/models/640m.onnx"

print("=" * 60)
print("ONNX Model Inspection: 640m.onnx")
print("=" * 60)

try:
    model = onnx.load(model_path)
    print("✅ Model loaded successfully")
    
    session = ort.InferenceSession(model_path)
    
    print("\n--- INPUTS ---")
    for i, inp in enumerate(session.get_inputs()):
        print(f"Input {i}:")
        print(f"  Name: {inp.name}")
        print(f"  Shape: {inp.shape}")
        print(f"  Type: {inp.type}")
    
    print("\n--- OUTPUTS ---")
    for i, out in enumerate(session.get_outputs()):
        print(f"Output {i}:")
        print(f"  Name: {out.name}")
        print(f"  Shape: {out.shape}")
        print(f"  Type: {out.type}")
    
    print("\n--- METADATA ---")
    metadata = session.get_modelmeta()
    print(f"Producer: {metadata.producer_name}")
    print(f"Version: {metadata.version}")
    print(f"Description: {metadata.description}")
    
    print("\n--- TEST INFERENCE ---")
    input_shape = session.get_inputs()[0].shape
    test_shape = [1 if isinstance(d, str) else d for d in input_shape]
    print(f"Creating dummy input with shape: {test_shape}")
    
    dummy_input = np.random.randn(*test_shape).astype(np.float32)
    input_name = session.get_inputs()[0].name
    
    outputs = session.run(None, {input_name: dummy_input})
    print(f"✅ Inference successful!")
    print(f"Output shape: {outputs[0].shape}")
    print(f"Output sample: {outputs[0][:5] if len(outputs[0].flatten()) > 5 else outputs[0]}")
    
    print("\n" + "=" * 60)
    print("INTEGRATION RECOMMENDATIONS:")
    print("=" * 60)
    print(f"1. Input preprocessing: Resize images to {test_shape[2:]} (HxW)")
    print(f"2. Input format: {session.get_inputs()[0].type}")
    print(f"3. Normalization: Likely [0, 1] or ImageNet mean/std")
    print(f"4. Output interpretation: Check if it's logits, probabilities, or bounding boxes")
    
except FileNotFoundError:
    print(f"❌ Model file not found: {model_path}")
    print("Make sure the file exists at the specified path.")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
