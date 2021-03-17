
class HashTable(object):
    """Hashtable class - The class takes care of creation of hashtable and hash function
    Supported Operations : Insert, Selection, remove, Cleanup, get_keys
    Hash function - Implemented with basic operations and Double hashing collision handling
    The Hash table doubles in size when the threshold load factor reaches 0.5
    """
    hash_resize_flag = False

    def __init__(self, size):
        """ Constructor to initialize the variables size, Hash table - value_array, Total_entries, threshold"""
        self.size = int(size)
        self.value_array = []
        self.total_entries = 0
        if self.size > 0:
            self.value_array = [None] * self.size
        else:
            raise Exception("Please initialize hash table with size > 0")
        self.threshold = 0.5

    def hash1(self, key):
        """ Hash function to sum up the unicode character values of the input key
        using inbuilt function ord() and modulus with size of hashtable """
        hash_sum = sum([ord(c) for c in key])
        hash_sum = hash_sum % self.size
        return hash_sum

    @staticmethod
    def hash2(key):
        """ Second Hash function to subtract and modulo with a  prime number """
        hash_val = 5 - (key % 5)
        return hash_val

    def __str__(self):
        """Function to display the hash table syntax - print(object of class HashTable)"""
        output_lines = []
        for item in self.value_array:
            if item is not None:
                output_lines.append("Key: " + str(item[0]) + " Value: " + str(item[1]))
        return "\n".join(output_lines)

    def resize_hashtable(self):
        """ Resize function to increase the size of the hash table based on the load factor of 0.5 """
        # print('Hash table exceeded load factor - Resize done!!')
        self.hash_resize_flag = True
        new_size = 2 * self.size
        new_value_array = [None] * (self.size * 2)
        temp_size = self.size
        self.size = new_size
        for i in range(temp_size):
            if (self.value_array[i] is not None) and (self.value_array[i] != -1):
                self.add_Entries(self.value_array[i][0], self.value_array[i][1], new_value_array, new_size, True)
        self.value_array = new_value_array

    def __setitem__(self, key, value):
        """ __setitem__ is a inbuilt dunder variable that replaces add operation.
        Here the keys - student id and the value - cgpa passed to this function is added to the Hash table
        using the Double hashing method"""
        self.add_Entries(key, value, self.value_array, self.size)

    def add_Entries(self, key, value, value_array, size, resize_flag=False):
        """ Function implementation of the double hashing collision handling for insert operation
        and resize the hashtable if the threshold exceeds the load factor 0.5"""
        hash_v1 = self.hash1(key)
        if value_array[hash_v1] is None or value_array[hash_v1] == -1:
            value_array[hash_v1] = key, value
            self.total_entries += 1
            return
        else:
            if isinstance(value_array[hash_v1], tuple):
                if value_array[hash_v1][0] == key:
                    value_array[hash_v1] = key, value
                    return
            # find the next slot with double hashing
            added = False
            attempt_count = 1
            while not added:
                new_hash = (hash_v1 + attempt_count * self.hash2(hash_v1)) % size
                # print(value_array[new_hash])
                if value_array[new_hash] is not None and isinstance(value_array[new_hash], tuple):
                    if value_array[new_hash][0] == key:
                        value_array[new_hash] = key, value
                        return
                if value_array[new_hash] is None or value_array[new_hash] == -1:
                    value_array[new_hash] = key, value
                    self.total_entries += 1
                    added = True
                else:
                    attempt_count += 1
        if not resize_flag:
            if self.total_entries / size > self.threshold:
                self.resize_hashtable()

    def remove(self, key):
        """ Function implementation of the double hashing collision handling for delete operation"""
        hash_val = self.hash1(key)
        got_value = self.value_array[hash_val]
        if got_value is None or got_value == -1:
            # print('Student ID not found')
            return None
        retrieved_key, retrieved_value = got_value
        if retrieved_key == key:
            self.value_array[hash_val] = -1
            self.total_entries -= 1
            # print('Student ID removed')
            return
        else:
            # find the next slot with double hashing
            removed = False
            attempt_count = 1
            while not removed:
                new_hash = (hash_val + attempt_count * self.hash2(hash_val)) % self.size
                value_at_hash = self.value_array[new_hash]
                # print('value_at_hash :', value_at_hash)
                if value_at_hash is not None and value_at_hash != -1:
                    retrieved_key, retrieved_value = value_at_hash
                    if retrieved_key == key:
                        # Marking the removed item position by -1
                        self.value_array[new_hash] = -1
                        self.total_entries -= 1
                        removed = True
                        # print('Student ID removed')
                    attempt_count += 1
                else:
                    attempt_count += 1

    def getKeys(self):
        """ Function to retrieve all the keys present inside the Hash table"""
        keys = []
        n = 0
        while n < self.size:
            if self.value_array[n] is not None:
                keys.append(self.value_array[n][0])
            n = n + 1
        return keys

    def __getitem__(self, key):
        """ Function implementation using double hashing for read operation"""
        hash_val1 = self.hash1(key)
        retrieved_value = None
        got_value = self.value_array[hash_val1]
        #         print('got_value', got_value)
        if (got_value is not None) and got_value != -1:
            if got_value[0] == key:
                return got_value[1]
            else:
                # find the next slot with double hashing
                found = False
                attempt_count = 1
                while not found:
                    new_hash = (hash_val1 + attempt_count * self.hash2(hash_val1)) % self.size
                    value_at_hash = self.value_array[new_hash]
                    if value_at_hash is not None:
                        if value_at_hash != -1:
                            retrieved_key, retrieved_value = value_at_hash
                            if retrieved_key == key:
                                found = True
                        attempt_count += 1
                    else:
                        retrieved_value = None
                        break
        if retrieved_value is None:
            pass
        else:
            return retrieved_value

    def cleanup(self):
        """ Function implementation for cleanup of the all the entries in hash table.
        For element wise selective cleanup - Use the delete method"""
        del self.value_array[:]
        return 'Hash table cleanup completed!!!'


def permute(inp_str):
    """ Function to create the permutation list of all the possible values
    for the 11 players using recursion and retrieve already processed values
    from the hash table(Memoisation)"""
    out = []
    if len(inp_str) == 1:
        return inp_str
    # print('Hashtab', Hashtab)
    if Hashtab1[''.join(inp_str)]:
        # Memoisation
        return Hashtab1[''.join(inp_str)]
    else:
        for i, let in enumerate(inp_str):
            for perm in permute(inp_str[:i] + inp_str[i + 1:]):
                out += [let + perm]
    Hashtab1[''.join(inp_str)] = out
    return out


def player_constraints():
    """Read the input file inputPS18.txt and get the player position constraints
    and handle if the input records are not given properly"""

    player_list_temp, player_list = [], []
    with open('inputPS18.txt') as f:
        total_lines = f.readlines()
        if len(total_lines) != 0:
            if len(total_lines) == 11:
                for ln in total_lines:
                    # Verify the input record formatting
                    if ln.strip()[0].lower() == 'p' and '/' in ln:
                        if ln.strip().split('/')[0].lower().split('p')[1] != ' ':
                            if ln.strip().split('/')[1] != '' or len(ln.strip().split('/')) != 2:
                                lst = [x.strip() for x in ln.strip().split('/')]
                                player_list_temp.append(lst)
                            else:
                                raise Exception("No Player position provided for the player! Check input file!")
                        else:
                            raise Exception('Incorrect input record format! Processing Stopped')
                    else:
                        raise Exception('Incorrect input record format! Processing Stopped')
                # sort the player list to ascending order if the input player records are jumbled
                player_list_temp.sort(key=lambda x: int(x[0].lower().split('p')[1]))

                # condition to verify if duplicate players are found in the file
                if len({itm[0] for itm in player_list_temp}) != 11:
                    raise Exception('Duplicate player name found in file! Processing stopped')

                for v1 in player_list_temp:
                    v1.pop(0)
                    lst_temp = [x for x in v1 if int(x) > 11]
                    if len(lst_temp) == 0:
                        player_list.append(set(map(Hashtab3.__getitem__, [str(x) for x in v1])))
                    else:
                        raise Exception("Player position greater than 11 is given! Check input file!")
            else:
                raise Exception("11 players not provided. List Generation Stopped!")
        else:
            raise Exception("Error: Input file empty!")
    return player_list


def main():
    try:
        with open('outputPS18.txt', 'w') as out_file:
            # Call the player_constraints function to get the list of player constraints
            player_list = player_constraints()
            # print('player_list', player_list)
            lis2, lis3 = [], []
            if len(player_list) == 11:
                print('Generating all possible permutation of the players...\n')
                lis1 = permute(list('abcdefghijk'))
                # print(f'Total permutations generated without player positions applied is : {len(lis1)}\n')
                # Filter the total player position list with the player constraints and get the final list
                for x1 in lis1:
                    flag = 0
                    for a1 in range(11):
                        if x1[a1] not in player_list[a1]:
                            flag = 1
                    if flag == 0:
                        lis2.append(x1)
                del lis1
                for x_val in lis2:
                    lis3.append(list(map(Hashtab2.__getitem__, list(x_val))))
                del lis2
                # print(lis3)
                out_file.write(f'The total number of allocations possible is: {len(lis3)}.')
                print('The total number of allocations possible is:', len(lis3))
            else:
                raise Exception('Error! Player constraints not given for all 11 players!')
    except Exception as err:
        print(err)
    except FileNotFoundError:
        print("Input File does not exist")


if __name__ == "__main__":
    # Create a hash table to store the memoisation intermediate values for dynamic programming
    Hashtab1, Hashtab2, Hashtab3 = HashTable(100), HashTable(100), HashTable(100)
    for ind, val in enumerate(list('abcdefghijk')):
        Hashtab2[val] = ind + 1
        Hashtab3[str(ind + 1)] = val
    main()
