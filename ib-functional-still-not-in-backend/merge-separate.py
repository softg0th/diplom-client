import os


def split_file(file_path):
    # Получаем размер файла
    file_size = os.path.getsize(file_path)
    part_size = file_size // 3

    with open(file_path, "rb") as file:
        for i in range(3):
            start_position = i * part_size
            end_position = start_position + part_size
            if i == 2:
                end_position = file_size
            with open(f"part_{i + 1}.bin", "wb") as output_file:
                file.seek(start_position)
                output_file.write(file.read(end_position - start_position))


def merge_files(part1_path, part2_path, part3_path, output_path):
    with open(output_path, "wb") as output_file:
        for part_path in [part1_path, part2_path, part3_path]:
            with open(part_path, "rb") as part_file:
                output_file.write(part_file.read())


part1_path = "part_1.bin"
part2_path = "part_2.bin"
part3_path = "part_3.bin"
output_path = "merged_file.jpg"

merge_files(part1_path, part2_path, part3_path, output_path)

file_path = "testasks.jpg"

split_file(file_path)
