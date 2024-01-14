def convert_flexikon(flexikon_file,result_file):
    """ 
    Parameters
    ----------
    flexikon_file : str: 'filename.txt'
        Original unformatted flexikon document.
    result_file : str: 'resultfile.txt'
        Output file formatted flexikon as table.

    Returns
    -------
    None.
    
    Function
    -------
    Converts original flexikon to a table.
    https://korpus.dsl.dk/resources/details/flexikon.html
    
    @AUTHOR: Aleksandra Kaszowska, 02/10/2023
    """
    
    import re
    
    with open(flexikon_file, encoding='utf-8') as file_object:
        contents = file_object.read() 
    
    contents = contents[2:]
        
    allCategoriesList = re.split('\n\*\n',contents)
    
    with open(result_file, 'w', encoding='utf-8') as f:
    
        for item in allCategoriesList:
            itemList = re.split('\n',item)
            counter = 2
            while counter <= len(itemList)-1:
                newItem = re.split('\t', itemList[counter])
                newLine = f"{itemList[1]}\t{itemList[0]}\t{newItem[1]}\n"
                f.write(newLine)
                counter += 1
        