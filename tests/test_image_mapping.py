from src.images.mapping import find_images_for

def test_find_images_for():
    m = {"4BR-TYPE-B-POOL": ["data/WebP/AlBadia_Floorplans_A3_Rev11-7.webp"]}
    images = find_images_for(["4BR-TYPE-B-POOL"], m)
    assert images and "floorplan" in images[0]["relevance"]
