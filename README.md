# SDModelsAndImagesComparison
Comparison of Stable Diffusion models and images files hashs.
* Used Python: 3.10
* Used libs:Pillow, tqdm.

* Description.
The program should compile reports on how many and which images were generated using certain models. Information about which model generated the image is stored in its EXIF parameter.
The program scans directories:
1. The first one contains the "model" files in the format ".safetensors" and ".ckpt". For example, model1.safetensors, model2.safetensors, model3.ckpt and so on. There may also be other files in the directory that should be ignored. The directory may contain nested directories that also contain model files. The nesting is not limited.
2. The second one contains the "image" files in the ".png" format. For example, image1.png, image2.png and so on. There may also be other files in the directory that should be ignored. The directory may contain nested directories that also contain image files. The nesting is not limited.
