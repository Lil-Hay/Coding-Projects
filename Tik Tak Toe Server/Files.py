
# returns all data from line where user is found or index of line if bool changed
def find_user(nickname, find_index=False):
    index = 0
    try:
        with open("Stats.txt") as f:
            all_Nicks = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError
    except Exception as e:
        print(f'find_user error: {e}')
        return
    
    for i in all_Nicks:
        if i.find(f'Nickname="{nickname}"') != -1:

            match find_index:
                case False:
                    return i
                case True:
                    return index
                
        index += 1
    return False




# returns all the stats user has in file
def read_stats(nickname):
    try:
        Stats_file = find_user(nickname)
    except FileNotFoundError:
        raise FileNotFoundError
    except Exception as e:
        print(f'read_stats error: {e}')
        return
    Stats = list(Stats_file)
    w = ''
    l = ''
    t = ''
    # find wins
    start_index = Stats_file.rfind("W=") + 2
    stop_index = Stats_file.rfind(" L")
    i = start_index
    while i <= stop_index:
        w += Stats[i]
        i += 1

    # find Losses
    start_index = Stats_file.rfind("L=") + 2
    stop_index = Stats_file.rfind(" T")
    i = start_index
    while i <= stop_index:
        l += Stats[i]
        i += 1

    # find ties
    start_index = Stats_file.rfind("T=") + 2
    stop_index = Stats_file.rfind(" (END)")
    i = start_index
    while i <= stop_index:
        t += Stats[i]
        i += 1


    return {
        'W': int(w),
        'L': int(l),
        'T': int(t)
        }




# used in creating new stats or modifying existing stats
def stat_to_modify(stat, Stats=None):
        '''
        pass stat as "W" to add win, "L" to add loss, "T" to add tie
        '''

        if Stats is None:
            Stats = {
                    'W': 0,
                    'L': 0,
                    'T': 0
                    }
            
        match stat:
            case 'W':
                Stats['W'] += 1
            case 'L':
                Stats['L'] += 1
            case 'T':
                Stats['T'] += 1
        return Stats




# handles modifying stats already in file
def modify_existing_stat(nickname, stat):
    '''
    pass stat as "W" to add win, "L" to add loss, "T" to add tie
    '''
    try:
        Stats = read_stats(nickname)
    except Exception as e:
        print(f'modify_existing_stat weird problem: {e}')
        return
    


    try:
        with open("Stats.txt") as f:
            File = f.readlines()
    except FileNotFoundError:
        return FileNotFoundError
    except Exception as e:
        print(f"Copy file: Weird problem: {e}")
        return
    
    
    try:
        index = find_user(nickname, True)
    except FileNotFoundError:
        return FileNotFoundError
    except Exception as e:
        print(f"find index: Weird problem: {e}")
        return
    

    
    Stats = stat_to_modify(stat, Stats)

    File[index] = f'Nickname="{nickname}" W={Stats['W']} L={Stats['L']} T={Stats['T']} (END)\n'
    

    try:
        with open("Stats.txt", 'w') as f:
            f.writelines(File)
    except Exception as e:
        print(f'rewriting file error: {e}')
        return




# can write stats for new user, modify existing user stats, or create new Stats file if one not found
def write_stats(nickname, stat):
    '''
    pass stat as "W" to add win, "L" to add loss, "T" to add tie
    '''
    
    try:
        user = find_user(nickname)

    except FileNotFoundError: # if file not created yet

        try:
            with open("Stats.txt", 'x') as f:
                Stats = stat_to_modify(stat)
                f.write(f'Nickname="{nickname}" W={Stats["W"]} L={Stats["L"]} T={Stats["T"]} (END)\n') # no newline character
                return
            
        except Exception as e: # if program can't create file
            print(f"Won't create file: {e}")
            return
        

    except Exception as e:
        print(f'write_stats problem: {e}')
        return    

    
        
    # if file exist but user doesn't yet
    if user == False:
        Stats = stat_to_modify(stat)
        try:
            with open("Stats.txt", 'a') as f:
                f.write(f'Nickname="{nickname}" W={Stats["W"]} L={Stats["L"]} T={Stats["T"]} (END)') # difference is newline character
        except Exception as e:
            print(f'write_stats, problem creating new user: {e}')
        return
        
    modify_existing_stat(nickname, stat)
        

def find_password(username, all_passwords):

    for i in all_passwords:
        if i.find(f'Username="{username}"') != -1:
            start_index = i.rfind('Password="') + 10
            stop_index = i.rfind('" (end)')
            Line = list(i)
            password = ''
            index = start_index
            while index <= stop_index:
                password += Line[index]
                index += 1
            return password
    
    return False


def Password_Correct(username, password_input):
    valid_password = password(username, password_input)

    if valid_password == True:
        return True 
    elif valid_password == password_input:
        return True
    
    return False

     


# manage passwords
def password(username, password):
    try:
        with open("Passwords.txt") as f:
            all_passwords = f.readlines()

    # Create File if it doesn't exist
    except FileNotFoundError:
        with open("Passwords.txt", 'x') as f:
            f.write(f'Username="{username}" Password="{password}" (end)\n')
            return True
    
    # see if user already has account
    valid_password = find_password(username, all_passwords)
    
    # if user doesn't have account
    if valid_password == False:
        try:
            with open("Passwords.txt", "a") as f:
                f.write(f'Username="{username}" Password="{password}" (end)\n')
                return True
        except Exception as e:
            print(f"Can't add user: {e}")
            return
        
    return password
    
            

        




             


