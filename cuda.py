import torch
print(torch.cuda.is_available())  # Should return True if the GPU is available
print(torch.cuda.current_device())  # Get the current GPU device
print(torch.cuda.get_device_name(torch.cuda.current_device()))  # Get GPU name
