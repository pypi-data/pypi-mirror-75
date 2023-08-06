''' Main Module '''
from .__version__ import __version__
from .utils import populate_data_sources

def list_data(available_only = True):
    data_sources = populate_data_sources()
    # print only sources available
    if available_only:
        print("AVAILABLE DATA SOURCES (Version " + __version__ + ") : ")
        print("============")
        for source in data_sources["Available"]:
            print(source)

    # when asked, print all the data sources planned as well
    else:
        print("AVAILABLE DATA SOURCES (Version " + __version__ + ") : ")
        print("============")
        if data_sources["Available"] == []:
            print("None")
        else:
            for source in data_sources["Available"]:
                print(source)

        print("\n")
        print("IN DEVELOPMENT DATA SOURCES (Version " + __version__ + ") : ")
        print("============")
        if data_sources["In Development"] == []:
            print("None")
        else:
            for source in data_sources["In Development"]:
                print(source)

        print("\n")
        print("PLANNED DATA SOURCES (Version " + __version__ + ") : ")
        print("============")
        if data_sources["Planned"] == []:
            print("None")
        else:
            for source in data_sources["Planned"]:
                print(source)


    print("\n")
    print("Done!")
