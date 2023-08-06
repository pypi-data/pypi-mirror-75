# HB Datacache

Package to manage temporary files in the cache and streamline codes with downloads and repetitive functions

    import hbdatacache

    #Check if exist temp file
    if (hbdatacache.check_temp_data("example_data", parameters=["teste",])):
        #Loading data from temp
        data = hbdatacache.load_temp_data("example_data", parameters=["teste",])
    else:
        #Generate new data
        data = [1,2,3,4,5,6,7,8,9,10] #Your data generating...
        #Save data
        hbdatacache.save_temp_data(data, "example_data", parameters=["teste",])
