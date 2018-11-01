# -*- coding: UTF-8 -*-
import sys

def is_half_width_form(ustring):

	for uchar in ustring:
		inside_code = ord(uchar)
		if inside_code == 0x0020:
			continue
		else:
			if not (0x0021 <= inside_code and inside_code <= 0x7e):
				return False
	return True

def find_maximum_length(name_str):
	if is_half_width_form(name_str):
		max_char_len = 10
	else:
		max_char_len = 6
	return max_char_len

def check():
	if len(sys.argv) != 4:
		print("need 3 argv. 1:save_file path 2: save slot number 3: the player's name you want")
		sys.exit()
	name_str = sys.argv[3]
	if len(name_str) == 0  or len(name_str) > find_maximum_length(name_str):
		print("the length of the player's name is illgeal")
		print("the maximum length for full-width forms is 6 and for half forms is 10")	
		sys.exit()

	
check()

# assign argv

ns_path = sys.argv[1]
save_slot = int(sys.argv[2])
name_str = sys.argv[3]
ns_file = open(ns_path, 'rb')

# set offset

beginning_offset = 36
_1st_data_offset = 16 + beginning_offset
_2nd_data_offset = _1st_data_offset + 4
_3rd_data_offset = _2nd_data_offset + 4
guild_name_offset = 815549

#set save slot offset

if save_slot == 1:
	user_offset = _1st_data_offset
elif save_slot == 2:
	user_offset = _2nd_data_offset
else:
	user_offset = _3rd_data_offset

# read_save_data

data = ns_file.read()
data = bytearray(data)

name_offset = data[user_offset:user_offset+3][::-1].hex()
name_position = int(name_offset,16) + beginning_offset
name_position1 = name_position + 146301

print('user_offset,name_offset,name_position,name_position1 are ',user_offset,name_offset,name_position,name_position1)
print()


name_len = len(name_str.encode('utf-8'))
pad_len = 32 - name_len
pad_byte = b'\x00'
name_hex =  name_str.encode('utf-8') + pad_byte * pad_len

print('name was used:',data[name_position1:name_position1+32].decode())
print('______________________________________')
# print(name_str.encode('utf-8'))
# print(name_hex)
print('name is changed to:',name_hex.decode())
print('______________________________________')

# set new name to position 0 and 1

data[name_position1:name_position1+32] = name_hex
data[name_position:name_position+32] = name_hex



guild_name_position = name_position + 815549
guild_name_hex = name_str.encode('utf-16le')

# print(name_str.encode('utf-16le'))
# print(name_str.encode('utf-16le').hex())


name_len = len(guild_name_hex)

pad_len = 24 - name_len

print('name was used on guild card:',data[guild_name_position:guild_name_position+24].decode('utf-16le'))
data[guild_name_position:guild_name_position+24] = guild_name_hex + pad_byte * pad_len

# print(data[guild_name_position:guild_name_position+24])
# print(data[guild_name_position:guild_name_position+24].hex())

print('name on guild card is changed to:',data[guild_name_position:guild_name_position+24].decode('utf-16le'))

with open(ns_path+'_new','wb') as f:
	f.write(data)

print('\nDone! new save data is '+ns_path+'_new')
print('\nplz use Checkpoint and rename and replace the system save file')

