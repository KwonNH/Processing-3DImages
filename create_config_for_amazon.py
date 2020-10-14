from glob import glob



def create_config():
    path = "{\"source-ref\": \"s3://test-3dlabeling-support-set3/"

    file_list = glob("./valid_images/set3/" + "*")

    result = ""

    for file in file_list:
        file_name = file.split("/")[-1]
        result += path + file_name + "\"}" + "\n"

    file = open("./menifest.menifest", "w")
    file.write(result)
    file.close()


if __name__ == "__main__":
    create_config()

