import os
import hashlib
from PIL import Image
from tqdm import tqdm


def calculate_sha256(filename):
    hash_sha256 = hashlib.sha256()
    try:
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
    except Exception as e:
        print(f"Error calculating hash for {filename}: {e}")
        return None
    return hash_sha256.hexdigest()[:10]


def get_model_hash_from_image_file(filename):
    try:
        im = Image.open(filename)
        im.load()
        png_EXIF_data = im.info.get('parameters', '')
        index_in_string = png_EXIF_data.find('Model hash: ')
        if index_in_string == -1:
            return None
        return png_EXIF_data[index_in_string + 12: index_in_string + 12 + 10]
    except Exception as e:
        print(f"Error reading EXIF data from {filename}: {e}")
        return None


def scan_directory_for_models(directory):
    model_files = {}
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.safetensors', '.ckpt')):
                all_files.append(os.path.join(root, file))
    for filepath in tqdm(all_files, desc="Scanning Models"):
        hash_value = calculate_sha256(filepath)
        if hash_value:
            relative_path = os.path.relpath(filepath, directory)
            model_files[relative_path] = hash_value

    return model_files


def scan_directory_for_images(directory):
    image_files = {}
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.png'):
                all_files.append(os.path.join(root, file))

    for filepath in tqdm(all_files, desc="Scanning Images"):
        model_hash = get_model_hash_from_image_file(filepath)
        if model_hash:
            relative_path = os.path.relpath(filepath, directory)
            image_files[relative_path] = model_hash

    return image_files


def generate_reports(models, images):
    hash_to_model = {hash_val: name for name, hash_val in models.items()}
    model_to_images = {name: [] for name in models}
    unmatched_images = []
    unmatched_images_hash = []

    for image, hash_val in images.items():
        if hash_val in hash_to_model:
            model_name = hash_to_model[hash_val]
            model_to_images[model_name].append(image)
        else:
            unmatched_images.append(image)
            unmatched_images_hash.append(hash_val)

    sorted_models = sorted(model_to_images.items(), key=lambda x: len(x[1]), reverse=True)

    print("Summary Report:")
    for model, image_list in sorted_models:
        print(f"{model}, {models[model]}, {len(image_list)} images")
    if input("You need detailed report? Input n for exit ") == 'n': exit(0)
    print("\nDetailed Report:")
    for model, image_list in sorted_models:
        print(f"{model}, {models[model]}, {len(image_list)} images")
        for image in image_list:
            print(f"\t{image}")

    if unmatched_images:
        print("\nUnmatched Images:")
        for i in range(len(unmatched_images)):
            print(f"\t{unmatched_images[i]}\tHash: {unmatched_images_hash[i]}")


if __name__ == "__main__":
    models_directory = input("Enter the path to the models directory: ")
    images_directory = input("Enter the path to the images directory: ")
    if not os.path.exists(models_directory):
        print('models directory missing!')
        exit(1)
    if not os.path.exists(images_directory):
        print('images directory missing!')
        exit(1)
    models = scan_directory_for_models(models_directory)
    images = scan_directory_for_images(images_directory)

    generate_reports(models, images)
