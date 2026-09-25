import os

stat = os.statvfs('/')
block_size = stat[0]
total_blocks = stat[2]
free_blocks = stat[3]

total_flash = (block_size * total_blocks) / (1024 * 1024)
free_flash = (block_size * free_blocks) / (1024 * 1024)

print(f"Total Flash Storage: {total_flash:.2f} MB")
print(f"Free Flash Storage:  {free_flash:.2f} MB")
